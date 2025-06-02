from manim import *
import numpy as np

class SoftmaxVisualization(Scene):
    def construct(self):
        # Title
        title = Text("Softmax Function", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Input values
        input_values = [-2, 0, 3, 1]
        
        # Calculate softmax
        exp_values = [np.exp(x) for x in input_values]
        sum_exp = sum(exp_values)
        softmax_values = [exp_val / sum_exp for exp_val in exp_values]
        
        # Create softmax curve
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 1, 0.2],
            x_length=8,
            y_length=4,
            axis_config={"color": WHITE},
            x_axis_config={"numbers_to_include": np.arange(-4, 5, 1)},
            y_axis_config={"numbers_to_include": np.arange(0, 1.1, 0.2)},
        )
        
        axes_labels = axes.get_axis_labels(x_label="Input", y_label="Output")
        
        self.play(Create(axes), Write(axes_labels))
        
        # Softmax curve for 2-component case
        def softmax_single(x, other_val=0):
            exp_x = np.exp(x)
            exp_other = np.exp(other_val)
            return exp_x / (exp_x + exp_other)
        
        softmax_curve = axes.plot(
            lambda x: softmax_single(x, 0),
            color=BLUE,
            x_range=[-4, 4],
        )
        
        self.play(Create(softmax_curve))
        self.wait(1)
        
        # Clear for comparison
        self.play(FadeOut(axes), FadeOut(axes_labels), FadeOut(softmax_curve), FadeOut(title))
        
        # Before vs After comparison
        before_softmax = Text("Before Softmax", font_size=28, color=RED)
        before_softmax.to_edge(LEFT, buff=2).shift(UP*1.8)
        
        after_softmax = Text("After Softmax", font_size=28, color=BLUE)
        after_softmax.to_edge(RIGHT, buff=2).shift(UP*1.8)
        
        self.play(Write(before_softmax))
        self.play(Write(after_softmax))
        
        # Define common baseline
        baseline_y = -0.5
        baseline_txt = Text("baseline", font_size=25, color=WHITE)
        
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
                value_label = Text(f"{val}", font_size=24, weight=BOLD)
                value_label.next_to(bar, UP, buff=0.1)
            else:
                bar.move_to(x_pos + UP*(baseline_y - height/2))
                value_label = Text(f"{val}", font_size=24, weight=BOLD)
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
            
            prob_label = Text(f"{val:.3f}", font_size=20, weight=BOLD, color=WHITE)
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
        sum_text_part = Text("the bars (probability) = 1.00", font_size=24, color=BLUE, weight=BOLD)
        
        # Position them together
        sum_display = VGroup(sum_symbol, sum_text_part)
        sum_display.arrange(RIGHT, buff=0.3)
        
        # Position under the after bars, relative to the new baseline
        sum_display.move_to(RIGHT*3.7 + UP*(baseline_y - 1.0))
        
        self.play(Write(sum_display))
        
        self.wait(2)