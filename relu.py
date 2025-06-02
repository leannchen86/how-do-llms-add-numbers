from manim import *

class ReLUAnimation(Scene):
    def construct(self):
        # Create the coordinate system
        axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[-1, 10, 1],
            axis_config={"color": GREY},
            x_length=10,
            y_length=6,
        )
        
        # Add labels
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("f(x)")
        
        # Create the ReLU function
        relu_graph = axes.plot(
            lambda x: max(0, x),
            x_range=[-10, 10],
            color=BLUE,
        )
        
        # Title
        title = Text("ReLU Activation Function: f(x) = max(0, x)", font_size=32)
        title.to_edge(UP)
        
        # Create a mathematical expression for ReLU
        relu_formula = MathTex(
            r"f(x) = \begin{cases} x & \text{if } x > 0 \\ 0 & \text{if } x \leq 0 \end{cases}"
        )
        relu_formula.next_to(title, DOWN)
        
        # Create a dot that will move along the graph
        moving_dot = Dot(color=YELLOW)
        
        # Create labels for x and f(x) values
        x_value_label = DecimalNumber(8, num_decimal_places=2)
        fx_value_label = DecimalNumber(8, num_decimal_places=2)
        
        # Set up a coordinate for tracking the values
        x_tracker = ValueTracker(8)  # Start from positive x = 8
        
        # Position the value labels
        x_tex = MathTex("x =").next_to(x_value_label, LEFT)
        fx_tex = MathTex(r"f(x) =").next_to(fx_value_label, LEFT)
        
        x_group = VGroup(x_tex, x_value_label).to_corner(UR)
        fx_group = VGroup(fx_tex, fx_value_label).next_to(x_group, DOWN)
        
        # Update functions for the moving dot and labels
        def update_dot(dot):
            x = x_tracker.get_value()
            y = max(0, x)
            dot.move_to(axes.c2p(x, y))
            return dot
        
        def update_x_value(decimal):
            decimal.set_value(x_tracker.get_value())
            return decimal
        
        def update_fx_value(decimal):
            decimal.set_value(max(0, x_tracker.get_value()))
            return decimal
        
        # Create a vertical line from x-axis to the point on the graph
        def get_vertical_line():
            x = x_tracker.get_value()
            y = max(0, x)
            start = axes.c2p(x, 0)
            end = axes.c2p(x, y)
            return DashedLine(start, end, color=RED)
        
        v_line = always_redraw(get_vertical_line)
        
        # Add updaters
        moving_dot.add_updater(update_dot)
        x_value_label.add_updater(update_x_value)
        fx_value_label.add_updater(update_fx_value)
        
        # Add all elements to the scene
        self.play(
            Write(title),
            Write(relu_formula),
            Create(axes),
            Write(x_label),
            Write(y_label),
            Create(relu_graph),
        )
        self.play(
            FadeIn(moving_dot),
            FadeIn(x_group),
            FadeIn(fx_group),
            Create(v_line),
        )
        
        # Animate the dot moving from right to left (positive to negative x)
        self.play(
            x_tracker.animate.set_value(-8),
            run_time=10,
            rate_func=linear,
        )
        
        # Highlight the important property of ReLU
        highlight_text = Text("ReLU outputs 0 for all negative inputs", 
                              font_size=28, color=YELLOW)
        highlight_text.next_to(relu_formula, DOWN, buff=1)
        
        self.play(FadeIn(highlight_text))
        
        # Add final text highlighting ReLU's importance
        importance_text = [
            Text("Key Properties of ReLU:", font_size=24),
            Text("• Simple computation", font_size=20),
            Text("• Non-linear but with linear behavior for positive inputs", font_size=20),
            Text("• Helps mitigate vanishing gradient problem", font_size=20),
            Text("• Promotes sparsity in the network", font_size=20),
        ]
        
        importance_group = VGroup(*importance_text).arrange(DOWN, aligned_edge=LEFT)
        importance_group.to_edge(DOWN, buff=0.5)
        
        self.play(
            FadeOut(highlight_text),
            FadeIn(importance_group),
        )
        
        self.wait(2)


# To render this animation, run:
# manim -pql relu_animation.py ReLUAnimation
# This will render in low quality for faster preview

# For high quality:
# manim -pqh relu_animation.py ReLUAnimation