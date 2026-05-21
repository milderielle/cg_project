"""
Easing Functions Module

Implements various easing functions for smooth animations.
These functions transform linear interpolation into natural-looking motion.
"""

import math
from typing import Callable

def linear(t: float) -> float:
    """Linear easing - no acceleration or deceleration."""
    return t


def ease_in(t: float) -> float:
    """Ease-in (accelerating) - quadratic."""
    return t * t


def ease_out(t: float) -> float:
    """Ease-out (decelerating) - quadratic."""
    return 1 - (1 - t) ** 2


def ease_in_out(t: float) -> float:
    """Ease-in-out (cubic) - starts slow, accelerates, then decelerates."""
    if t < 0.5:
        return 2 * t * t
    else:
        return 1 - pow(-2 * t + 2, 2) / 2


def ease_in_cubic(t: float) -> float:
    """Cubic ease-in."""
    return t ** 3


def ease_out_cubic(t: float) -> float:
    """Cubic ease-out."""
    return 1 - pow(1 - t, 3)


def ease_in_out_cubic(t: float) -> float:
    """Cubic ease-in-out."""
    if t < 0.5:
        return 4 * t ** 3
    else:
        return 1 - pow(-2 * t + 2, 3) / 2


def ease_in_sine(t: float) -> float:
    """Sine ease-in."""
    return 1 - math.cos((t * math.pi) / 2)


def ease_out_sine(t: float) -> float:
    """Sine ease-out."""
    return math.sin((t * math.pi) / 2)


def ease_in_out_sine(t: float) -> float:
    """Sine ease-in-out."""
    return -(math.cos(math.pi * t) - 1) / 2


def ease_in_expo(t: float) -> float:
    """Exponential ease-in."""
    return 0 if t == 0 else pow(2, 10 * t - 10)


def ease_out_expo(t: float) -> float:
    """Exponential ease-out."""
    return 1 if t == 1 else 1 - pow(2, -10 * t)


def ease_in_out_expo(t: float) -> float:
    """Exponential ease-in-out."""
    if t == 0:
        return 0
    elif t == 1:
        return 1
    elif t < 0.5:
        return pow(2, 20 * t - 10) / 2
    else:
        return (2 - pow(2, -20 * t + 10)) / 2


def ease_in_circ(t: float) -> float:
    """Circular ease-in."""
    return 1 - math.sqrt(1 - pow(t, 2))


def ease_out_circ(t: float) -> float:
    """Circular ease-out."""
    return math.sqrt(1 - pow(t - 1, 2))


def ease_in_out_circ(t: float) -> float:
    """Circular ease-in-out."""
    if t < 0.5:
        return (1 - math.sqrt(1 - pow(2 * t, 2))) / 2
    else:
        return (math.sqrt(1 - pow(-2 * t + 2, 2)) + 1) / 2


# Dictionary of available easing functions
EASING_FUNCTIONS = {
    'linear': linear,
    'ease-in': ease_in,
    'ease-out': ease_out,
    'ease-in-out': ease_in_out,
    'ease-in-cubic': ease_in_cubic,
    'ease-out-cubic': ease_out_cubic,
    'ease-in-out-cubic': ease_in_out_cubic,
    'ease-in-sine': ease_in_sine,
    'ease-out-sine': ease_out_sine,
    'ease-in-out-sine': ease_in_out_sine,
    'ease-in-expo': ease_in_expo,
    'ease-out-expo': ease_out_expo,
    'ease-in-out-expo': ease_in_out_expo,
    'ease-in-circ': ease_in_circ,
    'ease-out-circ': ease_out_circ,
    'ease-in-out-circ': ease_in_out_circ,
}


def get_easing_function(name: str) -> Callable[[float], float]:
    """
    Get an easing function by name.
    
    Args:
        name: Name of the easing function
    
    Returns:
        The easing function
    
    Raises:
        ValueError: If easing function not found
    """
    if name not in EASING_FUNCTIONS:
        raise ValueError(f"Unknown easing function: {name}")
    return EASING_FUNCTIONS[name]


def apply_easing(t: float, easing_name: str) -> float:
    """
    Apply an easing function to a parameter.
    
    Args:
        t: Parameter in range [0, 1]
        easing_name: Name of the easing function
    
    Returns:
        Eased parameter value
    """
    # Clamp t to [0, 1]
    t = max(0, min(1, t))
    easing_fn = get_easing_function(easing_name)
    return easing_fn(t)
