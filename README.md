# Animated Billboard Designer

## Overview

A Python-based tool for creating shape morphing animations suitable for digital billboards and motion graphics. This application uses Bezier curves to create smooth transitions between shapes.

## Features

- **Interactive Shape Drawing**: Draw shapes using multiple Bezier curves connected into closed shapes
- **Shape Morphing**: Automatically interpolate between shapes to create smooth animations
- **Easing Functions**: Multiple easing options for natural-looking motion
- **Real-time Preview**: View animations as they play
- **Project Management**: Save and load shape collections
- **User-Friendly Interface**: Designed for non-programmers

## Project Structure

```
CGpj/
├── main.py              # Entry point
├── config.py            # Configuration settings
├── bezier.py            # Bezier curve mathematics
├── shape.py             # Shape and control point management
├── animation.py         # Animation generation and playback
├── easing.py            # Easing functions for smooth motion
├── ui.py                # User interface (Tkinter)
└── README.md            # This file
```

## Requirements

- Python 3.7+
- tkinter (usually included with Python)

## Installation

1. Navigate to the project directory:
```bash
cd CGpj
```

2. No external dependencies required (uses only Python standard library)

## Usage

### Running the Application

```bash
python main.py
```

### Creating Shapes

1. Click "New Shape" to start drawing a new shape
2. Click on the canvas to add control points (red dots)
3. Right-click to finish the current curve (blue line)
4. Repeat to add more curves to the same shape
5. Click "Finish Shape" to complete the shape

**Important**: All shapes must have the same total number of control points for animation to work.

### Animating Shapes

1. Create at least 2 shapes
2. Click "Generate Animation"
3. Select easing function from dropdown (default: ease-in-out)
4. Click "Play" to start the animation
5. Use "Pause" and "Reset" to control playback

### Saving/Loading Projects

- Click "Save Project" to save all shapes to a file
- Click "Load Project" to load previously saved shapes

## Core Concepts

### Bezier Curves
- Smooth curves defined by control points
- Evaluated using De Casteljau's algorithm
- Connected into closed shapes

### Shape Morphing
- Interpolates control points between two shapes
- All shapes must have identical number of control points
- Points are indexed consistently across shapes

### Animation Pipeline
1. Select source and target shapes
2. Interpolate control points for each frame
3. Apply easing function for smooth motion
4. Render interpolated shape

### Easing Functions
Available easing options:
- `linear` - Uniform speed
- `ease-in` - Accelerating motion
- `ease-out` - Decelerating motion
- `ease-in-out` - Smooth acceleration and deceleration (recommended)
- `ease-in-cubic`, `ease-out-cubic`, `ease-in-out-cubic`
- `ease-in-sine`, `ease-out-sine`, `ease-in-out-sine`
- `ease-in-expo`, `ease-out-expo`, `ease-in-out-expo`
- `ease-in-circ`, `ease-out-circ`, `ease-in-out-circ`

## Configuration

Edit `config.py` to customize:

- **Canvas Size**: `CANVAS_WIDTH`, `CANVAS_HEIGHT`
- **Control Points**: `DEFAULT_CONTROL_POINTS_TARGET`
- **Animation**: `ANIMATION_FPS`, `ANIMATION_DURATION`
- **Colors**: Point colors, curve colors, etc.
- **Easing**: `DEFAULT_EASING` function

## Technical Details

### File Formats

**Shape Files** (`.shapes`):
- JSON format containing shape collection
- Stores all control points and curve structure
- Contains metadata about control point count

Example structure:
```json
{
  "target_control_points": 12,
  "shapes": [
    {
      "name": "Shape 1",
      "curves": [...],
      "control_points": [...]
    }
  ]
}
```

### Mathematics

**De Casteljau's Algorithm** for Bezier evaluation:
```
B(t) = Σ bi,n(t) * Pi
where bi,n(t) are basis functions and Pi are control points
```

**Linear Interpolation**:
```
P(t) = (1-t) * P1 + t * P2, where t ∈ [0,1]
```

## Troubleshooting

### "Shape has wrong number of control points"
- All shapes must have identical number of control points
- Check that each shape was drawn with the same complexity

### Animation looks jumpy
- Try different easing functions (ease-in-out-sine is usually smooth)
- Increase FPS in config.py for smoother motion

### Cannot add more curves to shape
- Right-click first to finish the current curve
- Then add new control points for the next curve

## Future Enhancements

Potential features for future versions:

1. **Rendering Export**
   - Export animations as MP4 videos
   - Export frame sequences as PNG/JPG
   - SVG export for vector graphics

2. **Advanced Features**
   - Point ordering optimization to reduce twisting
   - Automatic control point matching between shapes
   - Bezier path manipulation tools
   - Keyframe editor with timeline

3. **UI Improvements**
   - Undo/Redo functionality
   - Layer management
   - Grid snapping
   - Zoom and pan canvas

4. **Performance**
   - GPU acceleration for large animations
   - Real-time curve preview during drawing

## Author

Computer Graphics Project - Bezier Curve Animation System

## License

Educational Use

## References

- De Casteljau's Algorithm: Fundamental for Bezier curve evaluation
- Easing Functions: Based on standard animation easing conventions
- Shape Morphing: Interpolation of corresponding control points technique
