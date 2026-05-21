"""
Demo Script - Animated Billboard Designer

This script demonstrates how to use the core components programmatically.
It creates sample shapes and generates animations without using the GUI.
"""

from shape import Shape, ShapeCollection
from animation import Animation
import json


def demo_basic_shapes():
    """Demo 1: Create basic shapes."""
    print("\n" + "="*60)
    print("DEMO 1: Creating Basic Shapes")
    print("="*60 + "\n")
    
    # Create a circle-like shape
    circle = Shape("Circle")
    circle_cp = [
        (100, 50),    # top
        (150, 50),    # top-right
        (200, 100),   # right
        (200, 150),   # bottom-right
        (150, 200),   # bottom
        (100, 200),   # bottom-left
        (50, 150),    # left
        (50, 100)     # top-left
    ]
    circle.add_curve(circle_cp)
    
    print(f"Created shape: {circle.name}")
    print(f"  Total control points: {circle.get_total_control_points()}")
    print(f"  Number of curves: {len(circle.get_curves())}")
    print(f"  Control points: {circle.get_control_points()[:3]}... (showing first 3)")
    
    # Create a diamond-like shape with same number of control points
    diamond = Shape("Diamond")
    diamond_cp = [
        (125, 30),    # top point
        (180, 75),    # upper right
        (200, 125),   # right
        (180, 175),   # lower right
        (125, 220),   # bottom
        (70, 175),    # lower left
        (50, 125),    # left
        (70, 75)      # upper left
    ]
    diamond.add_curve(diamond_cp)
    
    print(f"\nCreated shape: {diamond.name}")
    print(f"  Total control points: {diamond.get_total_control_points()}")
    print(f"  Number of curves: {len(diamond.get_curves())}")
    
    return circle, diamond


def demo_shape_collection(shapes):
    """Demo 2: Manage shape collection."""
    print("\n" + "="*60)
    print("DEMO 2: Managing Shape Collection")
    print("="*60 + "\n")
    
    collection = ShapeCollection()
    
    for shape in shapes:
        collection.add_shape(shape)
        print(f"Added {shape.name} to collection")
    
    print(f"\nCollection Status:")
    print(f"  Total shapes: {collection.get_shape_count()}")
    print(f"  Target control points: {collection.target_control_points}")
    print(f"  Can generate animation: {collection.can_generate_animation()}")
    
    return collection


def demo_shape_interpolation():
    """Demo 3: Shape interpolation."""
    print("\n" + "="*60)
    print("DEMO 3: Shape Interpolation (Morphing)")
    print("="*60 + "\n")
    
    # Simple circle
    shape1 = Shape("Circle")
    circle_cp = [(100, 50), (150, 50), (200, 100), (200, 150), 
                 (150, 200), (100, 200), (50, 150), (50, 100)]
    shape1.add_curve(circle_cp)
    
    # Slightly modified circle
    shape2 = Shape("Circle_Squashed")
    squashed_cp = [(100, 60), (150, 40), (210, 100), (210, 150), 
                   (150, 190), (100, 210), (40, 150), (40, 100)]
    shape2.add_curve(squashed_cp)
    
    print("Interpolation at different time values:")
    print("t=0.0 (Shape 1):")
    for i, cp in enumerate(shape1.get_control_points()[:3]):
        print(f"  Point {i}: {cp}")
    
    print("\nt=0.5 (Midpoint):")
    import bezier
    mid_points = bezier.interpolate_control_points(
        shape1.get_control_points(), 
        shape2.get_control_points(), 
        0.5
    )
    for i, cp in enumerate(mid_points[:3]):
        print(f"  Point {i}: ({cp[0]:.1f}, {cp[1]:.1f})")
    
    print("\nt=1.0 (Shape 2):")
    for i, cp in enumerate(shape2.get_control_points()[:3]):
        print(f"  Point {i}: {cp}")


def demo_animation_generation(shapes):
    """Demo 4: Generate and analyze animation."""
    print("\n" + "="*60)
    print("DEMO 4: Animation Generation & Analysis")
    print("="*60 + "\n")
    
    collection = ShapeCollection()
    for shape in shapes:
        collection.add_shape(shape)
    
    # Create animation
    animation = Animation(
        collection.get_shapes(),
        fps=30,
        duration_per_transition=2.0,
        easing_name='ease-in-out'
    )
    
    info = animation.get_animation_info()
    print("Animation Information:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # Show frame info at key points
    print("\n\nFrame Information at Key Points:")
    for frame_num in [0, 15, 30, 45, 60]:
        if frame_num < animation.total_frames:
            frame_info = animation.get_frame_info(frame_num)
            print(f"\n  Frame {frame_info['frame']}:")
            print(f"    Transition: {frame_info['from_shape']} → {frame_info['to_shape']}")
            print(f"    Progress: {frame_info['transition_progress']}")
    
    return animation


def demo_easing_functions():
    """Demo 5: Compare different easing functions."""
    print("\n" + "="*60)
    print("DEMO 5: Easing Functions Comparison")
    print("="*60 + "\n")
    
    import easing
    
    easing_names = ['linear', 'ease-in', 'ease-out', 'ease-in-out', 
                    'ease-in-sine', 'ease-out-sine', 'ease-in-out-sine']
    
    t_values = [0.0, 0.25, 0.5, 0.75, 1.0]
    
    print("Easing Function Values at Different Time Points:\n")
    print(f"{'Easing':<20}", end='')
    for t in t_values:
        print(f"  t={t:.2f}", end='')
    print()
    print("-" * 60)
    
    for easing_name in easing_names:
        print(f"{easing_name:<20}", end='')
        for t in t_values:
            result = easing.apply_easing(t, easing_name)
            print(f"  {result:.3f}", end='')
        print()


def demo_file_operations():
    """Demo 6: Save and load shapes."""
    print("\n" + "="*60)
    print("DEMO 6: File Operations (Save/Load)")
    print("="*60 + "\n")
    
    # Create shapes
    circle, star = demo_basic_shapes()
    collection = ShapeCollection()
    collection.add_shape(circle)
    collection.add_shape(star)
    
    # Save to file
    filepath = "demo_project.shapes"
    collection.save_to_file(filepath)
    print(f"✓ Saved collection to {filepath}")
    
    # Load from file
    loaded_collection = ShapeCollection.load_from_file(filepath)
    print(f"✓ Loaded collection from {filepath}")
    print(f"  Loaded {loaded_collection.get_shape_count()} shapes")
    for shape in loaded_collection.get_shapes():
        print(f"    - {shape.name}: {shape.get_total_control_points()} control points")


def main():
    """Run all demos."""
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Animated Billboard Designer - Demo Script                ║")
    print("║  Computer Graphics: Bezier Curve Shape Morphing           ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    # Run demos
    circle, star = demo_basic_shapes()
    shapes = [circle, star]
    
    collection = demo_shape_collection(shapes)
    demo_shape_interpolation()
    animation = demo_animation_generation(shapes)
    demo_easing_functions()
    demo_file_operations()
    
    print("\n" + "="*60)
    print("DEMO COMPLETE")
    print("="*60)
    print("\nTo use the interactive GUI, run:")
    print("  python main.py")
    print("\nTo run tests, run:")
    print("  python test.py")
    print()


if __name__ == '__main__':
    main()
