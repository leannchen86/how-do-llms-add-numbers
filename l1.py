from manim import *
import numpy as np

class L1RegularizationAnimation(Scene):
    def construct(self):
        # Title
        title = Text("L1 Regularization: Sparsity Through Zeroing", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # Create axes
        axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[0, 2, 0.5],
            x_length=6,
            y_length=3,
            axis_config={"color": BLUE},
            tips=False,
        )
        
        # Labels
        x_label = axes.get_x_axis_label("w", edge=DOWN, direction=DOWN)
        y_label = axes.get_y_axis_label("L1(w) = |w|", edge=LEFT, direction=LEFT)
        
        # Position axes
        axes_group = VGroup(axes, x_label, y_label)
        axes_group.shift(UP * 0.5)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Create L1 loss function (V-shape)
        def l1_func(x):
            return abs(x)
        
        l1_graph = axes.plot(l1_func, color=RED, x_range=[-2, 2], stroke_width=4)
        self.play(Create(l1_graph))
        
        # Show gradient descent with moving dot
        self.show_gradient_descent_animation(axes, l1_func)
        
        self.wait(2)
        
        # Show multiple starting points
        self.show_multiple_trajectories(axes, l1_func)
        
        self.wait(3)

    def show_gradient_descent_animation(self, axes, l1_func):
        """Show gradient descent with a moving dot and real-time updates"""
        
        # Parameters
        learning_rate = 0.15
        initial_weight = 1.5
        
        # Create weight tracker
        weight_tracker = ValueTracker(initial_weight)
        
        # Moving dot on the curve
        moving_dot = always_redraw(lambda: Dot(
            axes.coords_to_point(weight_tracker.get_value(), l1_func(weight_tracker.get_value())),
            color=GREEN,
            radius=0.1
        ))
        
        self.play(FadeIn(moving_dot))
        
        # Show step-by-step gradient descent
        current_weight = initial_weight
        step_count = 0
        
        while abs(current_weight) > 0.02 and step_count < 8:
            step_count += 1
            
            # Calculate gradient (sign of weight)
            if current_weight > 0:
                gradient = 1
            elif current_weight < 0:
                gradient = -1
            else:
                break
            
            # Calculate next weight
            next_weight = current_weight - learning_rate * gradient
            
            # If we would overshoot zero, clamp to zero
            if current_weight > 0 and next_weight < 0:
                next_weight = 0
            elif current_weight < 0 and next_weight > 0:
                next_weight = 0
            
            # Animate the step
            self.play(
                weight_tracker.animate.set_value(next_weight),
                run_time=0.8,
                rate_func=smooth
            )
            
            current_weight = next_weight
            self.wait(0.3)
            
            # If we hit zero, highlight it
            if abs(next_weight) < 0.01:
                zero_highlight = Circle(radius=0.2, color=YELLOW).move_to(moving_dot.get_center())
                zero_text = Text("Zeroed!", font_size=20, color=YELLOW)
                zero_text.next_to(zero_highlight, DOWN, buff=0.2)
                
                self.play(Create(zero_highlight), Write(zero_text))
                self.wait(1)
                self.play(FadeOut(zero_highlight), FadeOut(zero_text))
                break
        
        # Clean up
        self.play(FadeOut(moving_dot))

    def show_multiple_trajectories(self, axes, l1_func):
        """Show multiple starting points converging to zero"""
        
        starting_points = [-1.8, -0.8, 0.6, 1.4]
        colors = [PINK, PURPLE, TEAL, ORANGE]
        learning_rate = 0.12
        
        # Create multiple dots
        dots = []
        trackers = []
        paths = []
        
        for i, start_w in enumerate(starting_points):
            tracker = ValueTracker(start_w)
            trackers.append(tracker)
            
            dot = always_redraw(lambda t=tracker, c=colors[i]: Dot(
                axes.coords_to_point(t.get_value(), l1_func(t.get_value())),
                color=c,
                radius=0.08
            ))
            dots.append(dot)
            
            # Create path trace
            path = VMobject(color=colors[i], stroke_width=2, stroke_opacity=0.7)
            paths.append(path)
        
        # Show all dots
        self.play(*[FadeIn(dot) for dot in dots])
        
        # Animate all trajectories simultaneously
        for step in range(15):
            animations = []
            
            for i, (tracker, path) in enumerate(zip(trackers, paths)):
                current_w = tracker.get_value()
                
                if abs(current_w) > 0.01:
                    # Calculate gradient step
                    gradient = 1 if current_w > 0 else -1
                    next_w = current_w - learning_rate * gradient
                    
                    # Clamp to zero if overshooting
                    if current_w > 0 and next_w < 0:
                        next_w = 0
                    elif current_w < 0 and next_w > 0:
                        next_w = 0
                    
                    # Add point to path
                    current_point = axes.coords_to_point(current_w, l1_func(current_w))
                    next_point = axes.coords_to_point(next_w, l1_func(next_w))
                    
                    if len(path.points) == 0:
                        path.start_new_path(current_point)
                    path.add_line_to(next_point)
                    
                    animations.append(tracker.animate.set_value(next_w))
            
            if animations:
                self.play(*animations, run_time=0.4)
                
                # Show paths after a few steps
                if step == 3:
                    self.play(*[Create(path) for path in paths], run_time=0.5)
        
        # Final highlight at zero
        zero_point = axes.coords_to_point(0, 0)
        zero_circle = Circle(radius=0.3, color=YELLOW, stroke_width=3)
        zero_circle.move_to(zero_point)
        
        conclusion = Text("All weights converge to zero", font_size=24, color=YELLOW)
        conclusion.to_edge(DOWN, buff=1)
        
        self.play(Create(zero_circle), Write(conclusion))
        self.wait(2)
        
        # Clean up
        self.play(
            *[FadeOut(dot) for dot in dots],
            *[FadeOut(path) for path in paths],
            FadeOut(zero_circle),
            FadeOut(conclusion)
        )


# To render this animation, save as a .py file and run:
# manim -pql filename.py L1RegularizationAnimation