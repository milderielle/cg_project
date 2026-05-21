"""
Animation Module

Handles animation generation and playback between shapes.
Includes interpolation, easing, and frame generation.
"""

from typing import List, Tuple, Optional
import bezier
import easing
from shape import Shape, ShapeCollection


class Animation:
    """
    Manages animation between multiple shapes.
    
    Animation cycle: Shape1 -> Shape2 -> Shape3 -> ... -> Shape1
    Each transition uses interpolation and easing for smooth motion.
    """
    
    def __init__(self, shapes: List[Shape], 
                 fps: int = 30, 
                 duration_per_transition: float = 2.0,
                 easing_name: str = 'ease-in-out'):
        """
        Initialize animation.
        
        Args:
            shapes: List of shapes to animate through
            fps: Frames per second
            duration_per_transition: Duration of each shape-to-shape transition in seconds
            easing_name: Name of easing function to use
        """
        if len(shapes) < 2:
            raise ValueError("Need at least 2 shapes for animation")
        
        # Verify all shapes have same number of control points
        num_points = shapes[0].get_total_control_points()
        for i, shape in enumerate(shapes[1:], 1):
            if shape.get_total_control_points() != num_points:
                raise ValueError(
                    f"Shape {i} has {shape.get_total_control_points()} control points, "
                    f"but shape 0 has {num_points}"
                )
        
        self.shapes = shapes
        self.fps = fps
        self.duration_per_transition = duration_per_transition
        self.easing_name = easing_name
        
        # Calculate frames per transition
        self.frames_per_transition = int(fps * duration_per_transition)
        
        # Total frames for complete cycle
        self.total_frames = self.frames_per_transition * len(shapes)
        
        self.is_playing = False
        self.current_frame = 0
    
    def get_frame(self, frame_number: int) -> List[Tuple[float, float]]:
        """
        Get interpolated control points for a specific frame.
        
        Args:
            frame_number: Frame number (0 to total_frames-1)
        
        Returns:
            List of interpolated control points
        """
        # Wrap frame number for looping
        frame_number = frame_number % self.total_frames
        
        # Which transition (shape pair) are we in?
        transition_index = frame_number // self.frames_per_transition
        frame_in_transition = frame_number % self.frames_per_transition
        
        # Handle wrapping for seamless loop
        shape1_index = transition_index % len(self.shapes)
        shape2_index = (transition_index + 1) % len(self.shapes)
        
        shape1 = self.shapes[shape1_index]
        shape2 = self.shapes[shape2_index]
        
        # Normalized time parameter [0, 1]
        t_normalized = frame_in_transition / self.frames_per_transition
        
        # Apply easing
        t_eased = easing.apply_easing(t_normalized, self.easing_name)
        
        # Interpolate control points
        points1 = shape1.get_control_points()
        points2 = shape2.get_control_points()
        
        interpolated = bezier.interpolate_control_points(points1, points2, t_eased)
        return interpolated
    
    def get_all_frames(self) -> List[List[Tuple[float, float]]]:
        """
        Get control points for all frames in animation.
        
        Returns:
            List of frames, each containing list of control points
        """
        frames = []
        for frame_num in range(self.total_frames):
            frame = self.get_frame(frame_num)
            frames.append(frame)
        return frames
    
    def get_frame_info(self, frame_number: int) -> dict:
        """Get debugging info about a specific frame."""
        frame_number = frame_number % self.total_frames
        transition_index = frame_number // self.frames_per_transition
        frame_in_transition = frame_number % self.frames_per_transition
        
        shape1_index = transition_index % len(self.shapes)
        shape2_index = (transition_index + 1) % len(self.shapes)
        
        t_normalized = frame_in_transition / self.frames_per_transition
        
        return {
            'frame': frame_number,
            'total_frames': self.total_frames,
            'transition_index': transition_index,
            'from_shape': self.shapes[shape1_index].name,
            'to_shape': self.shapes[shape2_index].name,
            'transition_progress': f"{t_normalized*100:.1f}%",
            'fps': self.fps,
            'duration': self.duration_per_transition
        }
    
    def play(self) -> None:
        """Start animation playback."""
        self.is_playing = True
        self.current_frame = 0
    
    def pause(self) -> None:
        """Pause animation."""
        self.is_playing = False
    
    def step(self) -> None:
        """Advance to next frame."""
        if self.is_playing:
            self.current_frame = (self.current_frame + 1) % self.total_frames
    
    def get_current_frame_points(self) -> List[Tuple[float, float]]:
        """Get control points for current frame."""
        return self.get_frame(self.current_frame)
    
    def set_frame(self, frame_number: int) -> None:
        """Jump to specific frame."""
        self.current_frame = frame_number % self.total_frames
    
    def reset(self) -> None:
        """Reset animation to start."""
        self.current_frame = 0
        self.is_playing = False
    
    def get_animation_info(self) -> dict:
        """Get animation information."""
        return {
            'num_shapes': len(self.shapes),
            'total_frames': self.total_frames,
            'fps': self.fps,
            'duration_per_transition': self.duration_per_transition,
            'total_duration': (self.duration_per_transition * len(self.shapes)),
            'easing_function': self.easing_name,
            'control_points_per_frame': self.shapes[0].get_total_control_points()
        }


class AnimationExporter:
    """Export animations to various formats."""
    
    @staticmethod
    def export_to_sequence(animation: Animation, 
                          output_dir: str,
                          format: str = 'png') -> None:
        """
        Export animation as frame sequence.
        
        Args:
            animation: Animation object
            output_dir: Directory to save frames
            format: Image format (png, jpg, etc.)
        """
        # This would require rendering library
        # Placeholder for future implementation
        pass
    
    @staticmethod
    def export_to_json(animation: Animation, 
                      filepath: str) -> None:
        """
        Export animation data to JSON file.
        
        Args:
            animation: Animation object
            filepath: Output file path
        """
        import json
        
        data = {
            'animation_info': animation.get_animation_info(),
            'shapes': [shape.to_dict() for shape in animation.shapes],
            'total_frames': animation.total_frames
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
