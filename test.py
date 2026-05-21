"""
Test Module for Animated Billboard Designer

Unit tests for core functionality including:
- Bezier curve evaluation
- Shape management
- Animation generation
- Easing functions
"""

import unittest
import math
import bezier
import easing
from shape import Shape, ShapeCollection, Curve
from animation import Animation


class TestBezierCurve(unittest.TestCase):
    """Test Bezier curve functionality."""
    
    def test_evaluate_bezier_linear(self):
        """Test Bezier evaluation with 2 control points (linear)."""
        points = [(0, 0), (10, 10)]
        result = bezier.evaluate_bezier(0.5, points)
        self.assertAlmostEqual(result[0], 5, places=5)
        self.assertAlmostEqual(result[1], 5, places=5)
    
    def test_evaluate_bezier_quadratic(self):
        """Test Bezier evaluation with 3 control points."""
        points = [(0, 0), (5, 10), (10, 0)]
        result = bezier.evaluate_bezier(0.5, points)
        # At t=0.5, should be at the middle-top of the curve
        self.assertAlmostEqual(result[0], 5, places=5)
        self.assertGreater(result[1], 0)
    
    def test_evaluate_bezier_endpoints(self):
        """Test that Bezier passes through endpoints."""
        points = [(0, 0), (5, 10), (10, 0)]
        start = bezier.evaluate_bezier(0, points)
        end = bezier.evaluate_bezier(1, points)
        
        self.assertAlmostEqual(start[0], points[0][0], places=5)
        self.assertAlmostEqual(start[1], points[0][1], places=5)
        self.assertAlmostEqual(end[0], points[-1][0], places=5)
        self.assertAlmostEqual(end[1], points[-1][1], places=5)
    
    def test_render_bezier_curve(self):
        """Test Bezier curve rendering."""
        points = [(0, 0), (5, 10), (10, 0)]
        curve_points = bezier.render_bezier_curve(points, 10)
        
        self.assertEqual(len(curve_points), 11)  # 0 to 1 inclusive
        self.assertEqual(curve_points[0], points[0])
        self.assertEqual(curve_points[-1], points[-1])
    
    def test_interpolate_control_point(self):
        """Test linear interpolation."""
        p1 = (0, 0)
        p2 = (10, 10)
        result = bezier.interpolate_control_point(p1, p2, 0.5)
        
        self.assertAlmostEqual(result[0], 5, places=5)
        self.assertAlmostEqual(result[1], 5, places=5)
    
    def test_distance_calculation(self):
        """Test distance between points."""
        p1 = (0, 0)
        p2 = (3, 4)
        dist = bezier.distance(p1, p2)
        
        self.assertAlmostEqual(dist, 5, places=5)
    
    def test_point_near_point(self):
        """Test point proximity check."""
        p1 = (0, 0)
        p2 = (5, 5)
        p3 = (0.1, 0.1)
        
        self.assertFalse(bezier.point_near_point(p1, p2, threshold=5))
        self.assertTrue(bezier.point_near_point(p1, p3, threshold=1))


class TestShape(unittest.TestCase):
    """Test shape management."""
    
    def setUp(self):
        """Setup test shapes."""
        self.shape = Shape("Test Shape")
    
    def test_shape_creation(self):
        """Test shape creation."""
        self.assertEqual(self.shape.name, "Test Shape")
        self.assertEqual(len(self.shape.curves), 0)
        self.assertEqual(self.shape.get_total_control_points(), 0)
    
    def test_add_curve_to_shape(self):
        """Test adding curves to shape."""
        curve_points = [(0, 0), (5, 10), (10, 0)]
        self.shape.add_curve(curve_points)
        
        self.assertEqual(len(self.shape.curves), 1)
        self.assertEqual(self.shape.get_total_control_points(), 3)
    
    def test_add_multiple_curves(self):
        """Test adding multiple curves."""
        curve1 = [(0, 0), (5, 10), (10, 0)]
        curve2 = [(10, 0), (15, 10), (20, 0)]
        
        self.shape.add_curve(curve1)
        self.shape.add_curve(curve2)
        
        self.assertEqual(len(self.shape.curves), 2)
    
    def test_shape_clone(self):
        """Test shape cloning."""
        curve_points = [(0, 0), (5, 10), (10, 0)]
        self.shape.add_curve(curve_points)
        
        cloned = self.shape.clone()
        self.assertEqual(cloned.get_total_control_points(), self.shape.get_total_control_points())
        self.assertIsNot(cloned, self.shape)
    
    def test_shape_serialization(self):
        """Test shape serialization and deserialization."""
        curve_points = [(0, 0), (5, 10), (10, 0)]
        self.shape.add_curve(curve_points)
        
        data = self.shape.to_dict()
        restored = Shape.from_dict(data)
        
        self.assertEqual(restored.name, self.shape.name)
        self.assertEqual(restored.get_total_control_points(), self.shape.get_total_control_points())


class TestShapeCollection(unittest.TestCase):
    """Test shape collection management."""
    
    def setUp(self):
        """Setup test collection."""
        self.collection = ShapeCollection()
    
    def test_empty_collection(self):
        """Test empty collection."""
        self.assertEqual(self.collection.get_shape_count(), 0)
        self.assertFalse(self.collection.can_generate_animation())
    
    def test_add_shape_to_collection(self):
        """Test adding shapes."""
        shape = Shape("Test")
        shape.add_curve([(0, 0), (5, 10), (10, 0)])
        
        self.collection.add_shape(shape)
        self.assertEqual(self.collection.get_shape_count(), 1)
    
    def test_shape_control_point_consistency(self):
        """Test that collection enforces control point consistency."""
        shape1 = Shape("Shape1")
        shape1.add_curve([(0, 0), (5, 10), (10, 0)])
        self.collection.add_shape(shape1)
        
        shape2 = Shape("Shape2")
        shape2.add_curve([(0, 0), (5, 5)])  # Different number of points
        
        with self.assertRaises(ValueError):
            self.collection.add_shape(shape2)


class TestEasingFunctions(unittest.TestCase):
    """Test easing functions."""
    
    def test_linear_easing(self):
        """Test linear easing."""
        self.assertEqual(easing.linear(0), 0)
        self.assertEqual(easing.linear(0.5), 0.5)
        self.assertEqual(easing.linear(1), 1)
    
    def test_ease_in_out(self):
        """Test ease-in-out."""
        result_0 = easing.ease_in_out(0)
        result_half = easing.ease_in_out(0.5)
        result_1 = easing.ease_in_out(1)
        
        self.assertAlmostEqual(result_0, 0, places=5)
        self.assertAlmostEqual(result_1, 1, places=5)
    
    def test_easing_function_retrieval(self):
        """Test getting easing functions by name."""
        func = easing.get_easing_function('linear')
        self.assertEqual(func(0.5), 0.5)
        
        with self.assertRaises(ValueError):
            easing.get_easing_function('unknown_easing')
    
    def test_apply_easing(self):
        """Test applying easing function."""
        result = easing.apply_easing(0.5, 'linear')
        self.assertAlmostEqual(result, 0.5, places=5)
    
    def test_easing_clamping(self):
        """Test that easing clamps values to [0, 1]."""
        result_over = easing.apply_easing(1.5, 'linear')
        result_under = easing.apply_easing(-0.5, 'linear')
        
        self.assertEqual(result_over, 1)
        self.assertEqual(result_under, 0)


class TestAnimation(unittest.TestCase):
    """Test animation generation."""
    
    def setUp(self):
        """Setup test shapes for animation."""
        self.shape1 = Shape("Circle")
        self.shape1.add_curve([(50, 50), (100, 100), (100, 50)])
        
        self.shape2 = Shape("Triangle")
        self.shape2.add_curve([(75, 75), (125, 125), (125, 75)])
    
    def test_animation_creation(self):
        """Test animation creation."""
        anim = Animation([self.shape1, self.shape2], fps=30, duration_per_transition=1.0)
        
        self.assertEqual(anim.fps, 30)
        self.assertEqual(anim.frames_per_transition, 30)
    
    def test_animation_requires_two_shapes(self):
        """Test that animation requires at least 2 shapes."""
        with self.assertRaises(ValueError):
            Animation([self.shape1], fps=30)
    
    def test_animation_control_point_consistency(self):
        """Test that animation checks control point consistency."""
        shape_bad = Shape("Bad")
        shape_bad.add_curve([(0, 0), (10, 10)])
        
        with self.assertRaises(ValueError):
            Animation([self.shape1, shape_bad])
    
    def test_animation_frame_generation(self):
        """Test getting animation frames."""
        anim = Animation([self.shape1, self.shape2], fps=30, duration_per_transition=1.0)
        
        frame_0 = anim.get_frame(0)
        frame_mid = anim.get_frame(15)
        frame_end = anim.get_frame(30)
        
        self.assertEqual(len(frame_0), 3)
        self.assertEqual(len(frame_mid), 3)
    
    def test_animation_looping(self):
        """Test that animation loops correctly."""
        anim = Animation([self.shape1, self.shape2], fps=30, duration_per_transition=1.0)
        
        # After total frames, should wrap
        frame = anim.get_frame(anim.total_frames + 5)
        frame_direct = anim.get_frame(5)
        
        for p1, p2 in zip(frame, frame_direct):
            self.assertAlmostEqual(p1[0], p2[0], places=3)
            self.assertAlmostEqual(p1[1], p2[1], places=3)
    
    def test_animation_info(self):
        """Test animation info retrieval."""
        anim = Animation([self.shape1, self.shape2], fps=30, duration_per_transition=2.0)
        info = anim.get_animation_info()
        
        self.assertEqual(info['num_shapes'], 2)
        self.assertEqual(info['fps'], 30)
        self.assertEqual(info['duration_per_transition'], 2.0)


class TestInterpolation(unittest.TestCase):
    """Test shape interpolation."""
    
    def test_control_point_interpolation(self):
        """Test control point interpolation."""
        points1 = [(0, 0), (10, 10), (20, 0)]
        points2 = [(0, 0), (10, 20), (20, 0)]
        
        result = bezier.interpolate_control_points(points1, points2, 0.5)
        
        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(result[1][1], 15, places=5)
    
    def test_interpolation_sequence(self):
        """Test interpolation sequence from start to end."""
        points1 = [(0, 0), (10, 10), (20, 0)]
        points2 = [(0, 0), (10, 20), (20, 0)]
        
        result_start = bezier.interpolate_control_points(points1, points2, 0)
        result_end = bezier.interpolate_control_points(points1, points2, 1)
        
        # At t=0, should match shape1
        for i, (p1, r) in enumerate(zip(points1, result_start)):
            self.assertAlmostEqual(p1[0], r[0], places=5, msg=f"Point {i} x")
            self.assertAlmostEqual(p1[1], r[1], places=5, msg=f"Point {i} y")
        
        # At t=1, should match shape2
        for i, (p2, r) in enumerate(zip(points2, result_end)):
            self.assertAlmostEqual(p2[0], r[0], places=5, msg=f"Point {i} x")
            self.assertAlmostEqual(p2[1], r[1], places=5, msg=f"Point {i} y")


def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == '__main__':
    run_tests()
