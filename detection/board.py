"""Dartboard geometry in millimeters, with positive Y pointing down."""

from itertools import combinations, product
from math import atan2, dist, hypot, pi
from statistics import median


ORDER = (20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5)
CALIBRATION = ((0, -170), (170, 0), (0, 170), (-170, 0), (0, 0))


def segment(x, y):
    radius = hypot(x, y)
    if radius <= 6.35:
        return 25, 2
    if radius <= 15.9:
        return 25, 1
    if radius > 170:
        return 0, 0
    step = pi / 10
    sector = int((atan2(x, -y) + step / 2) // step) % len(ORDER)
    multiplier = 2 if radius >= 162 else 3 if 99 <= radius <= 107 else 1
    return ORDER[sector], multiplier


def consensus(candidates, tolerance=10):
    """Fuse endpoints from distinct cameras, rejecting ambiguous clusters."""
    clusters = []
    for count in (3, 2):
        for views in combinations(candidates, count):
            for points in product(*views):
                if any(dist(a, b) > tolerance for a, b in combinations(points, 2)):
                    continue
                center = tuple(median(coords) for coords in zip(*points))
                clusters.append(center)
        if clusters:
            labels = {segment(*center) for center in clusters}
            if len(labels) != 1:
                return None
            n, m = labels.pop()
            return {"n": n, "m": m, "views": count}
    return None
