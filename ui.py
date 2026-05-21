"""
User Interface Module

Provides a GUI for the Animated Billboard Designer using Tkinter.
Users can:
- Draw shapes with Bezier curves
- Set control points
- Preview animations
- Play/pause animations
- Save and load shapes
"""

import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import config
import bezier
from shape import Shape, ShapeCollection
from animation import Animation
import easing


class DesignerUI:
    """Main UI window for the Billboard Designer."""
    
    def __init__(self, root):
        """Initialize UI."""
        self.root = root
        self.root.title("Animated Billboard Designer")
        self.root.geometry(f"{config.CANVAS_WIDTH + 250}x{config.CANVAS_HEIGHT + 100}")
        
        self.shape_collection = ShapeCollection()
        self.animation = None
        self.current_shape = None
        self.selected_point = None
        self.drawing_points = []
        
        # State
        self.is_editing = False
        self.animation_playing = False
        self.animation_frame = 0
        
        self._setup_ui()
        self._setup_canvas()
        self._start_animation_loop()
    
    def _setup_ui(self):
        """Setup the UI layout."""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left sidebar for controls
        self.sidebar = ttk.Frame(main_frame, width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        
        # Canvas area
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Canvas
        self.canvas = tk.Canvas(
            canvas_frame,
            width=config.CANVAS_WIDTH,
            height=config.CANVAS_HEIGHT,
            bg=tk.Color(config.CANVAS_BG_COLOR[0], config.CANVAS_BG_COLOR[1], config.CANVAS_BG_COLOR[2]) 
               if hasattr(tk, 'Color') else '#FFFFFF',
            cursor="crosshair"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<Motion>", self._on_canvas_motion)
        self.canvas.bind("<Button-3>", self._on_canvas_right_click)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(canvas_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Sidebar controls
        self._setup_sidebar_controls()
    
    def _setup_sidebar_controls(self):
        """Setup sidebar control panel."""
        # Title
        title = ttk.Label(self.sidebar, text="Billboard Designer", font=("Arial", 14, "bold"))
        title.pack(pady=10, padx=5)
        
        # Shape Management Section
        ttk.Separator(self.sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(self.sidebar, text="Shapes", font=("Arial", 11, "bold")).pack(anchor=tk.W, padx=5)
        
        btn_new_shape = ttk.Button(self.sidebar, text="New Shape", command=self._new_shape)
        btn_new_shape.pack(fill=tk.X, padx=5, pady=2)
        
        btn_finalize_shape = ttk.Button(self.sidebar, text="Finish Shape", command=self._finalize_shape)
        btn_finalize_shape.pack(fill=tk.X, padx=5, pady=2)
        
        # Shapes list
        ttk.Label(self.sidebar, text="Shapes List:", font=("Arial", 10)).pack(anchor=tk.W, padx=5, pady=(10, 5))
        
        self.shapes_listbox = tk.Listbox(self.sidebar, height=6)
        self.shapes_listbox.pack(fill=tk.BOTH, padx=5, pady=2)
        self.shapes_listbox.bind("<<ListboxSelect>>", self._on_shape_select)
        
        btn_delete_shape = ttk.Button(self.sidebar, text="Delete Selected", command=self._delete_shape)
        btn_delete_shape.pack(fill=tk.X, padx=5, pady=2)
        
        # Drawing section
        ttk.Separator(self.sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(self.sidebar, text="Drawing", font=("Arial", 11, "bold")).pack(anchor=tk.W, padx=5)
        
        self.target_points_var = tk.IntVar(value=config.DEFAULT_CONTROL_POINTS_TARGET)
        ttk.Label(self.sidebar, text="Target Control Points:").pack(anchor=tk.W, padx=5)
        
        points_spinbox = ttk.Spinbox(
            self.sidebar,
            from_=config.MIN_CONTROL_POINTS,
            to=config.MAX_CONTROL_POINTS,
            textvariable=self.target_points_var
        )
        points_spinbox.pack(fill=tk.X, padx=5, pady=2)
        
        self.points_status_var = tk.StringVar(value="Points: 0/12")
        points_status = ttk.Label(self.sidebar, textvariable=self.points_status_var, foreground="blue")
        points_status.pack(anchor=tk.W, padx=5, pady=5)
        
        btn_clear_drawing = ttk.Button(self.sidebar, text="Clear Drawing", command=self._clear_drawing)
        btn_clear_drawing.pack(fill=tk.X, padx=5, pady=2)
        
        # Animation section
        ttk.Separator(self.sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(self.sidebar, text="Animation", font=("Arial", 11, "bold")).pack(anchor=tk.W, padx=5)
        
        btn_generate_animation = ttk.Button(self.sidebar, text="Generate Animation", command=self._generate_animation)
        btn_generate_animation.pack(fill=tk.X, padx=5, pady=2)
        
        # Animation controls
        btn_play = ttk.Button(self.sidebar, text="Play", command=self._play_animation)
        btn_play.pack(fill=tk.X, padx=5, pady=2)
        
        btn_pause = ttk.Button(self.sidebar, text="Pause", command=self._pause_animation)
        btn_pause.pack(fill=tk.X, padx=5, pady=2)
        
        btn_reset = ttk.Button(self.sidebar, text="Reset", command=self._reset_animation)
        btn_reset.pack(fill=tk.X, padx=5, pady=2)
        
        # Easing selection
        ttk.Label(self.sidebar, text="Easing Function:", font=("Arial", 10)).pack(anchor=tk.W, padx=5, pady=(10, 2))
        
        self.easing_var = tk.StringVar(value=config.DEFAULT_EASING)
        easing_combo = ttk.Combobox(
            self.sidebar,
            textvariable=self.easing_var,
            values=list(easing.EASING_FUNCTIONS.keys()),
            state="readonly"
        )
        easing_combo.pack(fill=tk.X, padx=5, pady=2)
        
        # File operations
        ttk.Separator(self.sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(self.sidebar, text="File", font=("Arial", 11, "bold")).pack(anchor=tk.W, padx=5)
        
        btn_save = ttk.Button(self.sidebar, text="Save Project", command=self._save_project)
        btn_save.pack(fill=tk.X, padx=5, pady=2)
        
        btn_load = ttk.Button(self.sidebar, text="Load Project", command=self._load_project)
        btn_load.pack(fill=tk.X, padx=5, pady=2)
    
    def _setup_canvas(self):
        """Setup canvas for drawing."""
        pass
    
    def _on_canvas_click(self, event):
        """Handle canvas click for adding control points."""
        if self.current_shape is None:
            messagebox.showwarning("No Shape", "Create a new shape first")
            return
        
        point = (event.x, event.y)
        self.drawing_points.append(point)
        self._update_status(f"Points: {len(self.drawing_points)}/{self.target_points_var.get()}")
        self._redraw_canvas()
    
    def _on_canvas_motion(self, event):
        """Handle canvas mouse movement."""
        pass
    
    def _on_canvas_right_click(self, event):
        """Handle right click to finish curve."""
        if len(self.drawing_points) < config.MIN_CONTROL_POINTS:
            messagebox.showwarning("Not Enough Points", f"Need at least {config.MIN_CONTROL_POINTS} points")
            return
        
        try:
            self.current_shape.add_curve(self.drawing_points)
            self.drawing_points = []
            self._redraw_canvas()
            self._update_status(f"Curve added. Total control points: {self.current_shape.get_total_control_points()}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _on_shape_select(self, event):
        """Handle shape selection from listbox."""
        selection = self.shapes_listbox.curselection()
        if selection:
            index = selection[0]
            self._redraw_canvas()
    
    def _new_shape(self):
        """Create a new shape."""
        self.current_shape = Shape(f"Shape {len(self.shape_collection.shapes) + 1}")
        self.drawing_points = []
        self._update_status("New shape created. Click to add control points, right-click to finish curve")
        self._redraw_canvas()
    
    def _finalize_shape(self):
        """Finalize the current shape."""
        if self.current_shape is None:
            messagebox.showwarning("No Shape", "Create a shape first")
            return
        
        if self.current_shape.get_total_control_points() == 0:
            messagebox.showwarning("Empty Shape", "Add at least one curve to the shape")
            return
        
        try:
            self.shape_collection.add_shape(self.current_shape)
            self.shapes_listbox.insert(tk.END, self.current_shape.name)
            self._update_status(f"Shape finalized: {self.current_shape.name}")
            self.current_shape = None
            self.drawing_points = []
            self._redraw_canvas()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def _delete_shape(self):
        """Delete selected shape."""
        selection = self.shapes_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Select a shape to delete")
            return
        
        index = selection[0]
        self.shape_collection.remove_shape(index)
        self.shapes_listbox.delete(index)
        self._update_status("Shape deleted")
        self._redraw_canvas()
    
    def _clear_drawing(self):
        """Clear current drawing."""
        self.drawing_points = []
        self.current_shape = None
        self._redraw_canvas()
        self._update_status("Cleared")
    
    def _generate_animation(self):
        """Generate animation from shapes."""
        if not self.shape_collection.can_generate_animation():
            messagebox.showwarning("Not Enough Shapes", "Need at least 2 shapes")
            return
        
        try:
            self.animation = Animation(
                self.shape_collection.get_shapes(),
                fps=config.ANIMATION_FPS,
                duration_per_transition=config.ANIMATION_DURATION,
                easing_name=self.easing_var.get()
            )
            info = self.animation.get_animation_info()
            messagebox.showinfo(
                "Animation Generated",
                f"Total frames: {info['total_frames']}\n"
                f"Duration: {info['total_duration']:.1f}s\n"
                f"FPS: {info['fps']}"
            )
            self._update_status("Animation generated and ready for playback")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _play_animation(self):
        """Play animation."""
        if self.animation is None:
            messagebox.showwarning("No Animation", "Generate animation first")
            return
        
        self.animation_playing = True
        self._update_status("Animation playing...")
    
    def _pause_animation(self):
        """Pause animation."""
        self.animation_playing = False
        self._update_status("Animation paused")
    
    def _reset_animation(self):
        """Reset animation to start."""
        if self.animation:
            self.animation.reset()
            self.animation_frame = 0
            self.animation_playing = False
            self._redraw_canvas()
            self._update_status("Animation reset")
    
    def _save_project(self):
        """Save project to file."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".shapes",
            filetypes=[("Shape files", "*.shapes"), ("All files", "*.*")]
        )
        if filepath:
            try:
                self.shape_collection.save_to_file(filepath)
                messagebox.showinfo("Success", "Project saved successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def _load_project(self):
        """Load project from file."""
        filepath = filedialog.askopenfilename(
            filetypes=[("Shape files", "*.shapes"), ("All files", "*.*")]
        )
        if filepath:
            try:
                self.shape_collection = ShapeCollection.load_from_file(filepath)
                self.shapes_listbox.delete(0, tk.END)
                for shape in self.shape_collection.get_shapes():
                    self.shapes_listbox.insert(tk.END, shape.name)
                messagebox.showinfo("Success", "Project loaded successfully")
                self._redraw_canvas()
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def _redraw_canvas(self):
        """Redraw the canvas."""
        self.canvas.delete("all")
        
        # Draw grid
        for x in range(0, config.CANVAS_WIDTH, 50):
            self.canvas.create_line(x, 0, x, config.CANVAS_HEIGHT, fill="#EEE")
        for y in range(0, config.CANVAS_HEIGHT, 50):
            self.canvas.create_line(0, y, config.CANVAS_WIDTH, y, fill="#EEE")
        
        # Draw current drawing points
        for i, point in enumerate(self.drawing_points):
            self.canvas.create_oval(
                point[0] - config.POINT_RADIUS,
                point[1] - config.POINT_RADIUS,
                point[0] + config.POINT_RADIUS,
                point[1] + config.POINT_RADIUS,
                fill='#FF6666',
                outline='#FF0000'
            )
            self.canvas.create_text(point[0] + 10, point[1], text=str(i), fill='black')
        
        # Draw shapes from collection
        for shape in self.shape_collection.get_shapes():
            for curve in shape.get_curves():
                if len(curve.control_points) > 1:
                    curve_points = bezier.render_bezier_curve(curve.control_points, 100)
                    for i in range(len(curve_points) - 1):
                        self.canvas.create_line(
                            curve_points[i][0], curve_points[i][1],
                            curve_points[i+1][0], curve_points[i+1][1],
                            fill='#0064C8', width=2
                        )
                
                # Draw control points
                for cp in curve.control_points:
                    self.canvas.create_oval(
                        cp[0] - config.CONTROL_POINT_COLOR[0]//255*5,
                        cp[1] - config.CONTROL_POINT_COLOR[1]//255*5,
                        cp[0] + config.CONTROL_POINT_COLOR[0]//255*5,
                        cp[1] + config.CONTROL_POINT_COLOR[1]//255*5,
                        fill='#6464FF',
                        outline='#0000FF'
                    )
        
        # Draw animation frame
        if self.animation and self.animation_frame < self.animation.total_frames:
            points = self.animation.get_frame(self.animation_frame)
            if points:
                # Render as connected curves
                curve_points = bezier.render_bezier_curve(points, 200)
                for i in range(len(curve_points) - 1):
                    self.canvas.create_line(
                        curve_points[i][0], curve_points[i][1],
                        curve_points[i+1][0], curve_points[i+1][1],
                        fill='#00CC00', width=3
                    )
    
    def _update_status(self, message):
        """Update status bar."""
        self.status_var.set(message)
    
    def _start_animation_loop(self):
        """Start animation loop."""
        if self.animation_playing and self.animation:
            self.animation_frame = (self.animation_frame + 1) % self.animation.total_frames
            self._redraw_canvas()
        
        self.root.after(1000 // config.ANIMATION_FPS, self._start_animation_loop)


def main():
    """Main entry point for UI."""
    root = tk.Tk()
    app = DesignerUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
