"""
Bezier Curve Math and Rendering Module

Implements mathematical operations for Bezier curves including:
- De Casteljau's algorithm for curve evaluation
- Bezier curve rendering
- Control point interpolation
"""

import math
from typing import List, Tuple

def evaluate_bezier(t: float, control_points: List[Tuple[float, float]]) -> Tuple[float, float]:
    """
    Evaluate a Bezier curve at parameter t using De Casteljau's algorithm.
    
    Args:
        t: Parameter in range [0, 1]
        control_points: List of (x, y) tuples representing control points
    
    Returns:
        (x, y) coordinate on the Bezier curve at parameter t
    """
    if len(control_points) == 0:
        return (0, 0)
    if len(control_points) == 1:
        return control_points[0]
    
    # De Casteljau's algorithm
    points = [list(p) for p in control_points]
    
    for i in range(1, len(control_points)):
        for j in range(len(control_points) - i):
            x = (1 - t) * points[j][0] + t * points[j + 1][0]
            y = (1 - t) * points[j][1] + t * points[j + 1][1]
            points[j] = [x, y]
    
    return (points[0][0], points[0][1])


def render_bezier_curve(control_points: List[Tuple[float, float]], 
                       resolution: int = 100) -> List[Tuple[float, float]]:
    """
    Render a Bezier curve as a series of line segments.
    
    Args:
        control_points: List of control points
        resolution: Number of segments to generate
    
    Returns:
        List of (x, y) coordinates along the curve
    """
    curve_points = []
    for i in range(resolution + 1):
        t = i / resolution
        point = evaluate_bezier(t, control_points)
        curve_points.append(point)
    return curve_points


def interpolate_control_point(p1: Tuple[float, float], 
                             p2: Tuple[float, float], 
                             t: float) -> Tuple[float, float]:
    """
    Linearly interpolate between two control points.
    
    Args:
        p1: First point (x, y)
        p2: Second point (x, y)
        t: Interpolation parameter in range [0, 1]
    
    Returns:
        Interpolated point (x, y)
    """
    x = (1 - t) * p1[0] + t * p2[0]
    y = (1 - t) * p1[1] + t * p2[1]
    return (x, y)


def interpolate_control_points(points1: List[Tuple[float, float]], 
                              points2: List[Tuple[float, float]], 
                              t: float) -> List[Tuple[float, float]]:
    """
    Interpolate all control points between two shapes.
    
    Args:
        points1: Control points of first shape
        points2: Control points of second shape
        t: Interpolation parameter in range [0, 1]
    
    Returns:
        Interpolated control points
    """
    if len(points1) != len(points2):
        raise ValueError("Both shapes must have the same number of control points")
    
    interpolated = []
    for p1, p2 in zip(points1, points2):
        p = interpolate_control_point(p1, p2, t)
        interpolated.append(p)
    
    return interpolated


def distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Calculate Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def point_near_point(p1: Tuple[float, float], p2: Tuple[float, float], 
                     threshold: float = 10) -> bool:
    """Check if two points are close to each other."""
    return distance(p1, p2) <= threshold
