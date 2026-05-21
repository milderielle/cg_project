# Installation & Quick Start Guide

## System Requirements

- **Python**: 3.7 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: 512MB minimum
- **Disk Space**: 10MB for project folder

## Installation Steps

### 1. Verify Python Installation

Check that Python is installed and accessible:

```bash
python --version
```

You should see version 3.7 or higher.

### 2. No Dependencies to Install!

This project uses only Python's standard library. No external packages required.

Verify that tkinter is installed (it comes with most Python installations):

```bash
python -m tkinter
```

A simple window should appear. Close it and continue.

### 3. Navigate to Project Directory

```bash
cd path\to\CGpj
```

Or if using your workspace:

```bash
cd c:\Users\milderielle\Desktop\CGpj
```

## Running the Application

### Option 1: Interactive GUI (Recommended for Users)

Launch the graphical interface:

```bash
python main.py
```

**What you'll see**:
- Canvas area for drawing shapes
- Control panel on the left with buttons and settings
- Status bar showing operation feedback

### Option 2: Run Demo Script

See programmatic usage examples:

```bash
python demo.py
```

**Output includes**:
- Shape creation examples
- Animation generation
- Easing function comparison
- File operations demo

### Option 3: Run Unit Tests

Verify all components work correctly:

```bash
python test.py
```

**Expected output**: `Ran 28 tests in 0.006s - OK` ✓

## Quick Start Workflow

### Creating Your First Animation

1. **Start the application**:
   ```bash
   python main.py
   ```

2. **Create first shape**:
   - Click "New Shape" button
   - Click on canvas to add control points (red dots)
   - Right-click to finish the curve (blue line)
   - Click "Finish Shape" to save it

3. **Create second shape**:
   - Click "New Shape" again
   - Add control points (must be same number as first shape)
   - Right-click to finish curve
   - Click "Finish Shape"

4. **Generate animation**:
   - Click "Generate Animation"
   - Select easing function from dropdown (try "ease-in-out")
   - Click "Play" to watch the animation

5. **Save your work**:
   - Click "Save Project"
   - Choose a filename
   - Click Save

## Usage Guide

### Drawing Shapes

**Input Method**:
- **Left Click**: Add a control point (red dot appears)
- **Right Click**: Finish the current curve (blue line drawn)
- **Remove Points**: Click "Clear Drawing" to restart

**Workflow**:
1. Create new shape → Add points → Right-click to finish curve
2. Add more curves to the same shape if desired
3. Click "Finish Shape" when done

**Important**: All shapes must have the same total number of control points!

### Managing Shapes

- **New Shape**: Start drawing a new shape
- **Finish Shape**: Save current shape to collection
- **Shapes List**: View all created shapes
- **Delete Selected**: Remove selected shape from collection

### Animation Controls

- **Generate Animation**: Create animation from all shapes
- **Play**: Start playback
- **Pause**: Stop playback
- **Reset**: Go back to frame 0
- **Easing Function**: Choose motion style

**Easing Options**:
- `ease-in-out` - Smooth default (recommended)
- `linear` - Constant speed
- `ease-in-sine` - Smooth acceleration
- `ease-out-sine` - Smooth deceleration
- Others for different effects

### File Operations

- **Save Project**: Export all shapes to .shapes file
- **Load Project**: Import shapes from saved file

**File Format**: JSON-based `.shapes` files

## Configuration

Edit `config.py` to customize:

```python
# Canvas dimensions
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

# Animation settings
ANIMATION_FPS = 30
ANIMATION_DURATION = 2.0

# Default control points target
DEFAULT_CONTROL_POINTS_TARGET = 12
```

## Troubleshooting

### Issue: "tkinter is not installed"

**Solution**: Install tkinter for your Python version

**Windows**:
- Reinstall Python with "tcl/tk and IDLE" checkbox selected

**macOS**:
```bash
brew install python-tk
```

**Linux** (Ubuntu/Debian):
```bash
sudo apt-get install python3-tk
```

### Issue: "Shapes must have same number of control points"

**Solution**: 
- Make sure each shape has identical number of points
- Use the status indicator showing "Points: X/Y"
- X = current points, Y = target points

### Issue: Animation looks jumpy

**Solution**:
- Try different easing function (ease-in-out-sine is smooth)
- Increase FPS in config.py
- Check that shapes have enough control points (8+)

### Issue: "Can't add second shape"

**Solution**:
- First shape should have N control points
- Second shape must also have exactly N control points
- Use "Clear Drawing" if needed and start over

## Keyboard Shortcuts

Currently, the application uses mouse and button clicks. Keyboard shortcuts can be added in future versions.

## Command Line Usage

For advanced users, modules can be imported:

```python
from shape import Shape, ShapeCollection
from animation import Animation

# Create shapes
s1 = Shape("Circle")
s1.add_curve([(0,0), (10,10), (20,0)])

s2 = Shape("Triangle")  
s2.add_curve([(0,0), (10,10), (20,0)])

# Create collection
collection = ShapeCollection()
collection.add_shape(s1)
collection.add_shape(s2)

# Generate animation
animation = Animation(
    collection.get_shapes(),
    fps=30,
    duration_per_transition=2.0,
    easing_name='ease-in-out'
)

# Get frame
frame_points = animation.get_frame(0)
```

## File Structure After Setup

```
CGpj/
├── main.py              ← Run this for GUI
├── demo.py              ← Run this for demo
├── test.py              ← Run this for tests
├── config.py            ← Modify for settings
├── bezier.py            
├── shape.py             
├── animation.py         
├── easing.py            
├── ui.py                
├── README.md            
├── STRUCTURE.md         
├── INSTALL.md           ← This file
└── requirements.txt
```

## Next Steps

After installation:

1. **Run the demo**: `python demo.py`
2. **Start the app**: `python main.py`
3. **Create shapes**: Follow the Quick Start Workflow
4. **Read documentation**: Check README.md for detailed info
5. **Explore code**: Look at shape.py and animation.py to understand structure

## Getting Help

- **README.md**: Feature overview and concepts
- **STRUCTURE.md**: Architecture and design details
- **demo.py**: Usage examples
- **test.py**: Feature testing
- Code comments: Each module is well-documented

## Common Tasks

### Export animation frames

In the future, save animation frames:
```python
# Placeholder for export functionality
animation_export = AnimationExporter()
animation_export.export_to_json(animation, "output.json")
```

### Use custom easing function

```python
import easing
custom_easing = easing.get_easing_function('ease-in-sine')
eased_value = custom_easing(0.5)
```

### Access animation information

```python
info = animation.get_animation_info()
print(f"Total frames: {info['total_frames']}")
print(f"Duration: {info['total_duration']}s")
```

## Uninstallation

Simply delete the project folder:

```bash
rm -rf CGpj  # Linux/macOS
rmdir /s CGpj  # Windows
```

Since we use only Python standard library, there are no other files to clean up.

## Support

For issues or questions:
1. Check this guide's Troubleshooting section
2. Review README.md for concepts
3. Run demo.py to see working examples
4. Examine test.py for feature validation

Enjoy creating shape morphing animations! 🎨
