from manim import *
import numpy as np

class SoftmaxVisualization(Scene):
    def softmax(self, x):
        """
        Compute softmax values for array x.
        Uses numerical stability trick: subtract max value before exponentiating.
        """
        x = np.array(x)
        # Subtract max for numerical stability
        x_shifted = x - np.max(x)
        exp_x = np.exp(x_shifted)
        return exp_x / np.sum(exp_x)
    
    def construct(self):
        # Show softmax formula in left upper corner
        formula = MathTex(
            r"\text{softmax}(x_i) = \frac{e^{x_i}}{\sum_{j=1}^{n} e^{x_j}}",
            font_size=32
        )
        formula.to_corner(UL)
        self.play(Write(formula))
        
        # Show softmax curve visualization
        self.show_softmax_curve(formula)
        
        # Test input values (including negatives)
        input_values = [2.0, -1.0, 0.5, -0.3]
        
        # Calculate softmax using proper function
        softmax_values = self.softmax(input_values)
        
        # Create before/after visualization with shared baseline
        self.create_bar_comparison(input_values, softmax_values)
        
        self.wait(2)

    def create_bar_comparison(self, input_values, softmax_values):
        """Create side-by-side bar chart with shared baseline"""
        
        # Labels for sections
        before_softmax = Tex(r"\text{Before Softmax}", font_size=28, color=RED)
        before_softmax.move_to(LEFT * 4.0 + UP * 3)
        
        after_softmax = Tex(r"\text{After Softmax}", font_size=28, color=BLUE)
        after_softmax.move_to(RIGHT * 2.5 + UP * 3)
        
        # Define common baseline
        baseline_y = -0.5
        baseline_txt = Tex(r"\text{baseline}", font_size=25, color=WHITE)
        
        # Create a long flashlight baseline that sweeps across the entire scene
        full_baseline = Line(
            LEFT*7, RIGHT*7, 
            color=WHITE, 
            stroke_width=3
        ).move_to(UP*baseline_y)
        
        # Add subtle glow effect
        baseline_glow = Line(
            LEFT*7, RIGHT*7, 
            color=WHITE, 
            stroke_width=6,
            stroke_opacity=0.3
        ).move_to(UP*baseline_y)
        
        # Create the flashlight group
        flashlight_group = VGroup(baseline_glow, full_baseline)
        
        # Start the baseline off-screen to the left
        flashlight_group.shift(LEFT*14)
        
        # Before bars
        before_bars = VGroup()
        for i, val in enumerate(input_values):
            height = abs(val) * 0.6 + 0.3
            color = GREEN if val >= 0 else RED
            bar = Rectangle(width=0.8, height=height, fill_color=color, fill_opacity=0.8)
            
            x_pos = LEFT*4 + RIGHT*i*1.2
            # All bars align to baseline — positive go up, negative go down
            if val >= 0:
                bar.move_to(x_pos + UP*(baseline_y + height/2))
                value_label = Tex(f"{val}", font_size=24)
                value_label.next_to(bar, UP, buff=0.1)
            else:
                bar.move_to(x_pos + UP*(baseline_y - height/2))
                value_label = Tex(f"{val}", font_size=24)
                value_label.next_to(bar, DOWN, buff=0.1)
            
            before_bars.add(bar, value_label)
        
        # After bars — all start from baseline
        after_bars = VGroup()
        for i, val in enumerate(softmax_values):
            height = val * 2.0  # Height scaling for probabilities
            bar = Rectangle(width=0.8, height=height, fill_color=BLUE, fill_opacity=0.8)
            
            x_pos = RIGHT*2.5 + RIGHT*i*1.2
            # All probability bars start from baseline and go up
            bar.move_to(x_pos + UP*(baseline_y + height/2))
            
            prob_label = Tex(f"{val:.3f}", font_size=20, color=WHITE)
            prob_label.next_to(bar, UP, buff=0.1)
            
            after_bars.add(bar, prob_label)

        # Show the flashlight sweeping across from left to right
        self.play(Create(flashlight_group))
        self.play(
            flashlight_group.animate.shift(RIGHT*14),
            run_time=0.8,
            rate_func=smooth
        )
        self.play(Write(baseline_txt), run_time=0.2)
        self.play(Write(before_softmax), Write(after_softmax))
        # Everything happens at once
        self.play(
            FadeOut(flashlight_group),
            FadeOut(baseline_txt),
            Create(before_bars),
            Create(after_bars),
            run_time=1.5
        )
        self.wait(1)
        
        # Sum verification with flipped sum symbol
        total_sum = sum(softmax_values)
        
        # Create the sum symbol (∑) and flip it horizontally
        sum_symbol = MathTex(r"\sum", font_size=36, color=BLUE)
        sum_symbol.flip(RIGHT)  # Flip horizontally
        
        # Create the text part
        sum_text_part = Tex(r"\text{the bars (probability) = 1.00}", font_size=24, color=BLUE)
        
        # Position them together
        sum_display = VGroup(sum_symbol, sum_text_part)
        sum_display.arrange(RIGHT, buff=0.3)
        
        # Position under the after bars, relative to the new baseline
        sum_display.move_to(RIGHT*3.7 + UP*(baseline_y - 1.0))
        
        self.play(Write(sum_display))
        
        self.wait(2)
        
        # Clean up
        self.play(
            FadeOut(before_softmax),
            FadeOut(after_softmax),
            FadeOut(before_bars),
            FadeOut(after_bars),
            FadeOut(sum_display)
        )

    def show_softmax_curve(self, formula):
        """Show how softmax probabilities change as one input varies"""
        # Create axes — slightly smaller and shifted down
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 1, 0.2],
            axis_config={"color": GREY},
            x_length=8,
            y_length=5,
        )
        # Shift entire axes downward by 0.5 units
        axes.shift(DOWN * 0.5)
        
        # Add labels, reducing the font size of the y-axis
        x_label = axes.get_x_axis_label("x_1")
        y_label = axes.get_y_axis_label("P(x_1)")
        
        # Fixed values for other inputs
        x2_fixed = 0.5
        x3_fixed = -0.2
        
        # Create softmax curve for the main input only
        def softmax_prob_x1(x1):
            """Calculate P(x1) when x1 varies, x2=0.5, x3=-0.2"""
            logits = [x1, x2_fixed, x3_fixed]
            probs = self.softmax(logits)
            return probs[0]  # Probability of x1
        
        # Plot only the main curve
        curve_x1 = axes.plot(softmax_prob_x1, x_range=[-4, 4], color=BLUE, stroke_width=4)
        
        # Title for the graph with P(x) prefix
        graph_title = MathTex(r"\text{Softmax Output } P(x_1)", font_size=32)
        graph_title.next_to(axes, UP, buff=0.8)
        
        # Animate the visualization
        self.play(Write(graph_title))
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(curve_x1), run_time=2)
        
        # Add moving dot to show specific values
        x_tracker = ValueTracker(-4)  # Start from the left
        moving_dot = always_redraw(lambda: Dot(
            axes.c2p(x_tracker.get_value(), softmax_prob_x1(x_tracker.get_value())),
            color=YELLOW,
            radius=0.12
        ))
        
        # Value display using DecimalNumber to avoid LaTeX issues
        x_value_display = DecimalNumber(-4, num_decimal_places=1, font_size=24)
        p_value_display = DecimalNumber(0, num_decimal_places=3, font_size=24)
        
        x_label_text = MathTex(r"x_1 = ", font_size=20)
        p_label_text = MathTex(r"P(x_1) = ", font_size=20)
        
        x_display_group = VGroup(x_label_text, x_value_display).arrange(RIGHT, buff=0.08)
        p_display_group = VGroup(p_label_text, p_value_display).arrange(RIGHT, buff=0.08)
        
        value_display = VGroup(x_display_group, p_display_group).arrange(DOWN, buff=0.08)
        
        # Update function for the displays
        def update_displays():
            x_val = x_tracker.get_value()
            p_val = softmax_prob_x1(x_val)
            x_value_display.set_value(x_val)
            p_value_display.set_value(p_val)
            
            # Position the display above the dot with some offset
            dot_pos = axes.c2p(x_val, p_val)
            value_display.move_to(dot_pos + UP * 1.2)
        
        value_display.add_updater(lambda m: update_displays())
        
        self.play(FadeIn(moving_dot), Write(value_display))
        
        # Move the dot from left to right once, slower to see the values change
        self.play(x_tracker.animate.set_value(4), run_time=5, rate_func=smooth)
        
        self.wait(2)
        
        # Clean up the graph
        self.play(
            FadeOut(graph_title),
            FadeOut(axes),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(curve_x1),
            FadeOut(moving_dot),
            FadeOut(value_display),
            FadeOut(formula)
        )
