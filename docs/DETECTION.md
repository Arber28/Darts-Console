# Camera detection

The bench tool reads three OpenCV V4L2 feeds and emits local candidate segments as newline-delimited JSON. Manual entry remains the kiosk scoring path while the detector is validated. The camera tool runs separately and can be stopped without interrupting a match.

## Reuse investigated

- [OpenDartboard](https://github.com/OpenDartboard/OpenDartboard) is a three-camera project with a headless scorer and WebSocket output. Its camera platform and deployment need a compatibility trial on the Lenovo with USB UVC cameras.
- [ThrowVision](https://github.com/kashiwagiren/ThrowVision) documents a CPU-based OpenCV approach and multi-camera fusion. Compare results against it once reference throws can be captured. Review upstream licensing before importing code.
- This bench tool uses [OpenCV perspective transforms](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html) and nominal [WDF board geometry](https://site.dartswdf.com/wp-content/uploads/2020/05/2018-02-28_WDF_Playing_and_Tournament_Rules_rev20.pdf). Actual wire shape, thickness and lens distortion can affect calls near boundaries.

## Bench procedure

1. Install `python3-opencv`, `python3-numpy` and `v4l-utils` from Debian while package access is available.
2. Rigidly mount three UVC cameras around the board. Power the LED lighting separately. Use `v4l2-ctl --list-devices` and test all three streams simultaneously. Prefer distinct and stable `/dev/v4l/by-path/*-video-index0` paths, especially for identical cameras without serial numbers.
3. Use a graphical maintenance session with a pointer for calibration. Select the outside double wire at the centers of 20, 6, 3 and 11, then the bull center, in that order for each camera. Recalibrate when a camera moves or the capture resolution changes.

   ```sh
   python3 detection/camera.py calibrate --devices /dev/video0 /dev/video2 /dev/video4 --config calibration.json
   python3 detection/camera.py detect --config calibration.json
   ```

4. Start detection with a stable, empty, illuminated board. Record expected and actual segments for known singles, doubles, triples, bulls, misses, wire hits, obstructed darts and board clearings. Keep calibration files local to the machine.

The prototype compares the stable frame against a baseline and projects both ends of the largest candidate difference onto the board plane. It emits a segment only when two or more cameras agree and competing clusters agree on the same segment. The thresholds, board-clear behavior, camera timing, distorted views and actual tip accuracy need bench validation before live scoring. A future adapter should deliver deduplicated candidates with turn identity and keep manual correction available.
