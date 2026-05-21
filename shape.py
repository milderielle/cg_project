"""
Shape Module

Manages shape data including control points, curves, and shape properties.
Each shape stores both:
- Curve structure (list of curves with their control points)
- Flat list of control points (for interpolation)
"""

from typing import List, Tuple, Dict, Any
import json
import copy

class Curve:
    """Represents a single Bezier curve segment."""
    
    def __init__(self, control_points: List[Tuple[float, float]]):
        """
        Initialize a curve with control points.
        
        Args:
            control_points: List of (x, y) tuples
        """
        self.control_points = control_points
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize curve to dictionary."""
        return {
            'control_points': self.control_points
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Curve':
        """Deserialize curve from dictionary."""
        return Curve(data['control_points'])


class Shape:
    """
    Represents a complete shape made of connected Bezier curves.
    
    Constraints:
    - All shapes must have the same total number of control points
    - Each shape forms a closed loop
    - Control points are stored in consistent order
    """
    
    def __init__(self, name: str = "Unnamed Shape"):
        """
        Initialize an empty shape.
        
        Args:
            name: Name of the shape
        """
        self.name = name
        self.curves: List[Curve] = []
        self.control_points: List[Tuple[float, float]] = []
    
    def add_curve(self, control_points: List[Tuple[float, float]]) -> None:
        """
        Add a curve to the shape.
        
        Args:
            control_points: List of control points for the new curve
        """
        if len(control_points) == 0:
            raise ValueError("Curve must have at least one control point")
        
        curve = Curve(control_points)
        self.curves.append(curve)
        self._update_flat_control_points()
    
    def _update_flat_control_points(self) -> None:
        """Rebuild the flat list of control points from curves."""
        self.control_points = []
        
        for curve_idx, curve in enumerate(self.curves):
            for point_idx, point in enumerate(curve.control_points):
                # For first curve, add all points
                # For subsequent curves, skip the first point (it's shared with previous curve's end)
                if curve_idx == 0 or point_idx > 0:
                    self.control_points.append(point)
    
    def set_control_points(self, points: List[Tuple[float, float]]) -> None:
        """
        Set all control points directly (for interpolation).
        This distributes the flat control point list back to the curves.
        
        Args:
            points: List of (x, y) control points
        """
        if len(points) != len(self.control_points):
            raise ValueError(
                f"Expected {len(self.control_points)} control points, got {len(points)}"
            )
        
        self.control_points = points
        # Reconstruct curves from flat points (keeping same structure)
        self._distribute_control_points_to_curves()
    
    def _distribute_control_points_to_curves(self) -> None:
        """Distribute flat control points back to curve structure."""
        # This is a simplified distribution - would need customization per use case
        pass
    
    def get_total_control_points(self) -> int:
        """Get total number of control points in this shape."""
        return len(self.control_points)
    
    def get_curves(self) -> List[Curve]:
        """Get all curves in the shape."""
        return self.curves
    
    def get_control_points(self) -> List[Tuple[float, float]]:
        """Get the flat list of all control points."""
        return copy.deepcopy(self.control_points)
    
    def clone(self) -> 'Shape':
        """Create a deep copy of this shape."""
        cloned = Shape(f"{self.name} (copy)")
        cloned.curves = [Curve(copy.deepcopy(curve.control_points)) for curve in self.curves]
        cloned.control_points = copy.deepcopy(self.control_points)
        return cloned
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize shape to dictionary."""
        return {
            'name': self.name,
            'curves': [curve.to_dict() for curve in self.curves],
            'control_points': self.control_points
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Shape':
        """Deserialize shape from dictionary."""
        shape = Shape(data['name'])
        shape.curves = [Curve.from_dict(curve_data) for curve_data in data['curves']]
        shape.control_points = data['control_points']
        return shape
    
    def save_to_file(self, filepath: str) -> None:
        """Save shape to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @staticmethod
    def load_from_file(filepath: str) -> 'Shape':
        """Load shape from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return Shape.from_dict(data)


class ShapeCollection:
    """Manages a collection of shapes."""
    
    def __init__(self):
        """Initialize empty collection."""
        self.shapes: List[Shape] = []
        self.target_control_points: int = 0
    
    def add_shape(self, shape: Shape) -> None:
        """
        Add a shape to the collection.
        
        Args:
            shape: Shape object to add
        
        Raises:
            ValueError: If shape has wrong number of control points
        """
        if len(self.shapes) == 0:
            # First shape - set the target
            self.target_control_points = shape.get_total_control_points()
        else:
            # Verify consistency
            if shape.get_total_control_points() != self.target_control_points:
                raise ValueError(
                    f"Shape has {shape.get_total_control_points()} control points, "
                    f"but expected {self.target_control_points}"
                )
        
        self.shapes.append(shape)
    
    def remove_shape(self, index: int) -> None:
        """Remove shape at given index."""
        if 0 <= index < len(self.shapes):
            self.shapes.pop(index)
    
    def get_shape(self, index: int) -> Shape:
        """Get shape at given index."""
        if 0 <= index < len(self.shapes):
            return self.shapes[index]
        raise IndexError(f"Shape index out of range: {index}")
    
    def get_shapes(self) -> List[Shape]:
        """Get all shapes."""
        return self.shapes
    
    def get_shape_count(self) -> int:
        """Get number of shapes."""
        return len(self.shapes)
    
    def can_generate_animation(self) -> bool:
        """Check if we have enough shapes to generate animation."""
        return len(self.shapes) >= 2
    
    def save_to_file(self, filepath: str) -> None:
        """Save collection to JSON file."""
        data = {
            'target_control_points': self.target_control_points,
            'shapes': [shape.to_dict() for shape in self.shapes]
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    @staticmethod
    def load_from_file(filepath: str) -> 'ShapeCollection':
        """Load collection from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        collection = ShapeCollection()
        collection.target_control_points = data['target_control_points']
        collection.shapes = [Shape.from_dict(shape_data) for shape_data in data['shapes']]
        return collection
