"""Offline bench tool for three calibrated UVC cameras."""

import argparse
import json
import sys
import time
from contextlib import ExitStack
from pathlib import Path

import cv2
import numpy as np

from board import CALIBRATION, consensus


LANDMARKS = ("outer double rim at 20 center", "outer double rim at 6 center",
             "outer double rim at 3 center", "outer double rim at 11 center", "bull center")


def open_cameras(devices, resources):
    captures = []
    for device in devices:
        camera = cv2.VideoCapture(device, cv2.CAP_V4L2)
        resources.callback(camera.release)
        if not camera.isOpened():
            raise RuntimeError(f"Cannot open {device}")
        camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        camera.set(cv2.CAP_PROP_FPS, 15)
        captures.append(camera)
    return captures


def frames(cameras):
    for camera in cameras:
        if not camera.grab():
            raise RuntimeError("Camera grab failed")
    images = []
    for camera in cameras:
        ok, image = camera.retrieve()
        if not ok:
            raise RuntimeError("Camera read failed")
        images.append(image)
    return images


def calibrate(cameras, devices):
    for _ in range(15):
        images = frames(cameras)
    result = []
    for device, image in zip(devices, images):
        points = []
        window = str(device)
        cv2.namedWindow(window)

        def click(event, x, y, _flags, _parameter):
            if event == cv2.EVENT_LBUTTONDOWN and len(points) < len(LANDMARKS):
                points.append((x, y))

        cv2.setMouseCallback(window, click)
        while len(points) < len(LANDMARKS):
            preview = image.copy()
            for point in points:
                cv2.circle(preview, point, 4, (0, 220, 255), -1)
            cv2.putText(preview, "Click " + LANDMARKS[len(points)], (8, 24),
                        cv2.FONT_HERSHEY_SIMPLEX, .55, (0, 255, 255), 2)
            cv2.imshow(window, preview)
            if cv2.waitKey(30) == 27:
                raise RuntimeError("Calibration cancelled")
        cv2.destroyWindow(window)
        source = np.asarray(points, dtype=np.float32)
        target = np.asarray(CALIBRATION, dtype=np.float32)
        matrix = cv2.getPerspectiveTransform(source[:4], target[:4])
        estimated = cv2.perspectiveTransform(source.reshape(-1, 1, 2), matrix).reshape(-1, 2)
        if (not np.isfinite(matrix).all() or abs(np.linalg.det(matrix)) < 1e-10
                or np.linalg.norm(estimated[4] - target[4]) > 8):
            raise RuntimeError(f"Landmarks do not agree on {device}; recheck lens distortion and placement")
        result.append({"device": device, "size": list(image.shape[:2]), "matrix": matrix.tolist()})
    return result


def gray(image):
    return cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (5, 5), 0)


def endpoints(reference, current, matrix):
    _, mask = cv2.threshold(cv2.absdiff(reference, current), 28, 255, cv2.THRESH_BINARY)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not contours:
        return []
    contour = max(contours, key=cv2.contourArea)
    if not 35 <= cv2.contourArea(contour) <= mask.size * .04:
        return []
    points = contour.reshape(-1, 2).astype(np.float32)
    vx, vy, x0, y0 = cv2.fitLine(points, cv2.DIST_L2, 0, .01, .01).ravel()
    direction = np.asarray((vx, vy))
    origin = np.asarray((x0, y0))
    projections = (points - origin) @ direction
    if projections.max() - projections.min() < 15:
        return []
    ends = origin + np.asarray([projections.min(), projections.max()])[:, None] * direction
    positions = cv2.perspectiveTransform(ends.reshape(-1, 1, 2), matrix).reshape(-1, 2)
    return [tuple(pos) for pos in positions if np.isfinite(pos).all() and np.linalg.norm(pos) <= 180]


def detect(cameras, config):
    previous = None
    stable = 0
    baseline = None
    dirty = False
    empty = None
    matrices = [np.asarray(item["matrix"], dtype=np.float64) for item in config]
    print("Start with an empty, illuminated board. Ctrl-C stops detection.", file=sys.stderr)
    while True:
        current = [gray(image) for image in frames(cameras)]
        if any(list(image.shape) != item["size"] for image, item in zip(current, config)):
            raise RuntimeError("Camera resolution changed; calibrate again")
        if previous is not None:
            moving = any(np.count_nonzero(cv2.absdiff(a, b) > 22) > a.size * .0008
                         for a, b in zip(previous, current))
            stable = 0 if moving else stable + 1
            dirty |= moving
        previous = current
        if stable < 5:
            continue
        if baseline is None:
            baseline = empty = current
            dirty = False
        elif dirty:
            dirty = False
            if all(np.count_nonzero(cv2.absdiff(a, b) > 28) < 35 for a, b in zip(empty, current)):
                baseline = current
                continue
            hit = consensus([endpoints(a, b, matrix) for a, b, matrix in zip(baseline, current, matrices)])
            if hit:
                print(json.dumps({"type": "candidate", "time_ns": time.time_ns(), **hit}), flush=True)
                baseline = current
            else:
                print("No clear camera consensus; use manual entry.", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("calibrate", "detect"))
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--devices", nargs=3, metavar=("CAM1", "CAM2", "CAM3"))
    args = parser.parse_args()
    if args.command == "calibrate":
        if not args.devices or len(set(args.devices)) != 3:
            parser.error("calibration requires three distinct camera device paths")
        with ExitStack() as resources:
            resources.callback(cv2.destroyAllWindows)
            config = calibrate(open_cameras(args.devices, resources), args.devices)
        args.config.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    else:
        config = json.loads(args.config.read_text(encoding="utf-8"))
        devices = [item["device"] for item in config]
        if len(devices) != 3 or len(set(devices)) != 3:
            parser.error("calibration must describe three distinct cameras")
        with ExitStack() as resources:
            detect(open_cameras(devices, resources), config)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except (RuntimeError, OSError, ValueError) as error:
        sys.exit(str(error))
