"""
Animated Billboard Designer - Main Entry Point

This application provides a tool for creating shape morphing animations
that can be used in digital signage. Users can:

1. Create shapes by drawing Bezier curves
2. Ensure all shapes have consistent control points
3. Generate smooth animations between shapes
4. Preview and customize animations with easing functions
5. Save and load projects

Usage:
    python main.py
"""

import sys
import tkinter as tk
from ui import main as ui_main


def main():
    """Main entry point."""
    print("=" * 60)
    print("  Animated Billboard Designer")
    print("  Computer Graphics: Bezier Curve Shape Morphing")
    print("=" * 60)
    print()
    print("Starting UI...")
    
    try:
        ui_main()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
