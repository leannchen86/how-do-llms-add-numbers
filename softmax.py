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
        # Title
        title = Tex(r"\text{Softmax Function}", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Clean up
        self.play(FadeOut(title))
        
        # Test input values (including negatives)
        input_values = [2.0, -1.0, 0.5, -0.3]
        
        # Calculate softmax using proper function
        softmax_values = self.softmax(input_values)
        
        # Create before/after visualization with shared baseline
        self.create_bar_comparison(input_values, softmax_values)
        
        # Show formula
        self.show_softmax_formula()
        
        self.wait(2)

    def create_bar_comparison(self, input_values, softmax_values):
        """Create side-by-side bar chart with shared baseline"""
        
        # Labels for sections
        before_softmax = Tex(r"\text{Before Softmax}", font_size=28, color=RED)
        before_softmax.move_to(LEFT * 4.5 + UP * 3)
        
        after_softmax = Tex(r"\text{After Softmax}", font_size=28, color=BLUE)
        after_softmax.move_to(RIGHT * 2.5 + UP * 3)
        
        self.play(Write(before_softmax), Write(after_softmax))
        
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
            # All bars align to baseline - positive go up, negative go down
            if val >= 0:
                bar.move_to(x_pos + UP*(baseline_y + height/2))
                value_label = Tex(f"{val}", font_size=24)
                value_label.next_to(bar, UP, buff=0.1)
            else:
                bar.move_to(x_pos + UP*(baseline_y - height/2))
                value_label = Tex(f"{val}", font_size=24)
                value_label.next_to(bar, DOWN, buff=0.1)
            
            before_bars.add(bar, value_label)
        
        # After bars - all start from baseline
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
            run_time=2.5,
            rate_func=smooth
        )
        self.play(Write(baseline_txt), run_time=1)
        
        # Everything happens at once
        self.play(
            FadeOut(flashlight_group),
            FadeOut(baseline_txt),
            Create(before_bars),
            Create(after_bars),
            run_time=0.8
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

    def show_softmax_formula(self):
        """Show the mathematical formula for softmax"""
        formula = MathTex(
            r"\text{softmax}(x_i) = \frac{e^{x_i}}{\sum_{j=1}^{n} e^{x_j}}",
            font_size=48
        )
        formula.move_to(ORIGIN)
        
        self.play(Write(formula))
        self.wait(3)
        
        # Add explanation
        explanation = Tex(
            r"\text{Converts any real numbers into probabilities that sum to 1}",
            font_size=24,
            color=GRAY
        )
        explanation.next_to(formula, DOWN, buff=1)
        
        self.play(Write(explanation))
        self.wait(2)