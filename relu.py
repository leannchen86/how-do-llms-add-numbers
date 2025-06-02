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
        title = MathTex(r"\text{ReLU Activation Function: } f(x) = \max(0, x)", font_size=35)
        title.to_edge(UP)
        
        # Create a mathematical expression for ReLU
        relu_formula = MathTex(
            r"f(x) = \begin{cases} x & \text{if } x > 0 \\ 0 & \text{if } x \leq 0 \end{cases}"
        )
        relu_formula.next_to(title, DOWN)
        
        # Create a dot that will move along the graph
        moving_dot = Dot(color=YELLOW)
        
        # Create labels for x and f(x) values
        x_value_label = DecimalNumber(8, num_decimal_places=2, font_size=30)
        fx_value_label = DecimalNumber(8, num_decimal_places=2, font_size=30)
        
        # Set up a coordinate for tracking the values
        x_tracker = ValueTracker(8)  # Start from positive x = 8
        
        # Position the value labels
        x_tex = MathTex("x = ", font_size=30).next_to(x_value_label, LEFT*0.5)
        fx_tex = MathTex(r"f(x) = ", font_size=30).next_to(fx_value_label, LEFT*0.5)
        
        x_group = VGroup(x_tex, x_value_label).to_corner(UR)
        fx_group = VGroup(fx_tex, fx_value_label).next_to(x_group, DOWN)
        
        # Update functions for the moving dot and labels
        def update_dot(dot):
            x = x_tracker.get_value()
            y = max(0, x)
            dot.move_to(axes.c2p(x, y))
            return dot
        
        def update_x_label(label):
            label.set_value(x_tracker.get_value())
            return label
        
        def update_fx_label(label):
            label.set_value(max(0, x_tracker.get_value()))
            return label
        
        # Add updaters
        moving_dot.add_updater(update_dot)
        x_value_label.add_updater(update_x_label)
        fx_value_label.add_updater(update_fx_label)

        # Animate the scene
        self.play(Write(title))
        self.play(Write(relu_formula))
        
        # Group title and formula, then move and scale them
        title_formula_group = VGroup(title, relu_formula)
        self.play(
            title_formula_group.animate.to_edge(LEFT).scale(0.6),
            run_time=1.5
        )
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(relu_graph))
        
        # Add the moving dot and labels
        self.play(FadeIn(moving_dot), Write(x_group), Write(fx_group))
        
        # Move the dot from positive to negative to show the behavior
        self.play(x_tracker.animate.set_value(-8), run_time=3)
        self.wait(1)
        
        # Clean up the moving elements
        moving_dot.clear_updaters()
        x_value_label.clear_updaters()
        fx_value_label.clear_updaters()
        
        self.play(FadeOut(moving_dot), FadeOut(x_group), FadeOut(fx_group))
        
        # Highlight the flat part (negative inputs)
        negative_part = axes.plot(
            lambda x: 0,
            x_range=[-10, 0],
            color=RED,
            stroke_width=8
        )
        
        self.play(Create(negative_part))
        
        # Add text highlighting ReLU's property for negative inputs
        highlight_text = Tex(r"\text{ReLU outputs 0 for all negative inputs}",
                           font_size=30, color=RED)
        highlight_text.next_to(axes, DOWN, buff=0.15)
        
        self.play(Write(highlight_text))
        self.wait(2)
        
        self.play(
            FadeOut(highlight_text),
        )
        
        self.wait(2)


# To render this animation, run:
# manim -pql relu_animation.py ReLUAnimation
# This will render in low quality for faster preview

# For high quality:
# manim -pqh relu_animation.py ReLUAnimation