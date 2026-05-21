# Animated Billboard Designer

A Python-based tool for creating shape morphing animations suitable for digital billboards using Bezier curves.

## Author

Ariyaporn Sudsatientanone 65070501060

## Features

- **Interactive Shape Drawing**: Draw shapes using multiple Bezier curves
- **Shape Morphing**: Automatically interpolate between shapes to create smooth animations
- **Easing Functions**: Multiple easing options for natural-looking motion
- **Real-time Preview**: View animations as they play
- **Project Management**: Save and load shape collections

## Requirements

- Python 3.7+
- tkinter (usually included with Python)

## Installation

Navigate to the project directory and run:

```bash
python main.py
```

No external dependencies required (uses only Python standard library).

## Usage

1. Click "New Shape" to start drawing a new shape
2. Click on the canvas to add control points (red dots)
3. Right-click to finish the current curve
4. Repeat to add more curves to the same shape
5. Click "Finish Shape" to complete the shape

**Important**: All shapes must have the same total number of control points for animation to work.

To create an animation:

1. Create at least 2 shapes
2. Click "Generate Animation"
3. Select an easing function (default: ease-in-out)
4. Click "Play" to start the animation

## License

Educational Use
