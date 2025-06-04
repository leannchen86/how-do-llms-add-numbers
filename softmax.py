from manim import *
import numpy as np

class SoftmaxVisualization(Scene):
    def softmax(self, x):
        """
        Compute softmax values for array x.
        Uses numerical stability trick: subtract max value before exponentiating.
        """
        x = np.array(x)
        x_shifted = x - np.max(x)
        exp_x = np.exp(x_shifted)
        return exp_x / np.sum(exp_x)
    
    def construct(self):
        # Show softmax formula in upper-left corner
        formula = MathTex(
            r"\text{softmax}(x_i) = \frac{e^{x_i}}{\sum_{j=1}^{n} e^{x_j}}",
            font_size=32
        )
        formula.to_corner(UL)
        self.play(Write(formula))
        
        # Draw the “full‐scale” softmax curve with a labelled 1.0 tick
        self.show_softmax_curve(formula)
        
        # Example inputs (including negatives)
        input_values = [2.0, -1.0, 0.5, -0.3]
        softmax_values = self.softmax(input_values)
        
        # Show before/after bar comparison
        self.create_bar_comparison(input_values, softmax_values)
        
        self.wait(2)

    def create_bar_comparison(self, input_values, softmax_values):
        """Create side-by-side bar chart with a shared baseline."""
        
        before_softmax = Tex(r"\text{Before Softmax}", font_size=28, color=RED)
        before_softmax.move_to(LEFT * 4 + UP * 3)
        
        after_softmax = Tex(r"\text{After Softmax}", font_size=28, color=BLUE)
        after_softmax.move_to(RIGHT * 2.5 + UP * 3)
        
        baseline_y = -0.5
        baseline_txt = Tex(r"\text{baseline}", font_size=25, color=WHITE)
        
        # A long baseline (with subtle glow) that sweeps across
        full_baseline = Line(LEFT * 7, RIGHT * 7, color=WHITE, stroke_width=3).move_to(UP * baseline_y)
        baseline_glow = Line(LEFT * 7, RIGHT * 7, color=WHITE, stroke_width=6, stroke_opacity=0.3).move_to(UP * baseline_y)
        flashlight_group = VGroup(baseline_glow, full_baseline)
        flashlight_group.shift(LEFT * 14)  # start off-screen
        
        # "Before" bars
        before_bars = VGroup()
        for i, val in enumerate(input_values):
            height = abs(val) * 0.6 + 0.3
            color = GREEN if val >= 0 else RED
            bar = Rectangle(width=0.8, height=height, fill_color=color, fill_opacity=0.8)
            x_pos = LEFT * 4 + RIGHT * i * 1.2
            if val >= 0:
                bar.move_to(x_pos + UP * (baseline_y + height / 2))
                label = Tex(f"{val}", font_size=24).next_to(bar, UP, buff=0.1)
            else:
                bar.move_to(x_pos + UP * (baseline_y - height / 2))
                label = Tex(f"{val}", font_size=24).next_to(bar, DOWN, buff=0.1)
            before_bars.add(bar, label)
        
        # "After" bars (softmax probabilities)
        after_bars = VGroup()
        for i, val in enumerate(softmax_values):
            height = val * 2.0  # scale up for visibility
            bar = Rectangle(width=0.8, height=height, fill_color=BLUE, fill_opacity=0.8)
            x_pos = RIGHT * 2.5 + RIGHT * i * 1.2
            bar.move_to(x_pos + UP * (baseline_y + height / 2))
            label = Tex(f"{val:.3f}", font_size=20, color=WHITE).next_to(bar, UP, buff=0.1)
            after_bars.add(bar, label)

        # Animate the sweeping baseline, then show bars
        self.play(Create(flashlight_group))
        self.play(
            flashlight_group.animate.shift(RIGHT * 14),
            run_time=0.8,
            rate_func=smooth
        )
        self.play(Write(baseline_txt), run_time=0.2)
        self.play(Write(before_softmax), Write(after_softmax))
        self.play(
            FadeOut(flashlight_group),
            FadeOut(baseline_txt),
            Create(before_bars),
            Create(after_bars),
            run_time=1.5
        )
        self.wait(1)
        
        # Verify sum ≈ 1.00 with a flipped summation symbol
        sum_symbol = MathTex(r"\sum", font_size=36, color=BLUE).flip(RIGHT)
        sum_text = Tex(r"\text{the bars (probability) = 1.00}", font_size=24, color=BLUE)
        sum_display = VGroup(sum_symbol, sum_text).arrange(RIGHT, buff=0.3)
        sum_display.move_to(RIGHT * 3.7 + UP * (baseline_y - 1.0))
        self.play(Write(sum_display))
        self.wait(2)
        
        self.play(
            FadeOut(before_softmax),
            FadeOut(after_softmax),
            FadeOut(before_bars),
            FadeOut(after_bars),
            FadeOut(sum_display)
        )

    def show_softmax_curve(self, formula):
        """Visualize how softmax probabilities for x₁ change as x₁ varies."""
        # Create axes from x = –4 to 4 (step 1), y = 0 to 1.0 (step 0.2).
        # Make y_length tall enough (5) so the raw curve never “jumps out.”
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 1.2, 0.2],
            x_length=6,
            y_length=4,
            axis_config={"color": GREY},
            x_axis_config={"numbers_to_include": list(range(-4, 5))},
            y_axis_config={"numbers_to_include": [0, 0.2, 0.4, 0.6, 0.8, 1.0]},
        ).shift(DOWN * 0.5)  # shift down slightly to center under the formula

        # Axis labels
        x_label = axes.get_x_axis_label("x_1")
        y_label = axes.get_y_axis_label("P(x_1)")

        # Other logits are fixed at 0.5 and -0.2
        x2_fixed = 0.5
        x3_fixed = -0.2

        def softmax_prob_x1(x1):
            logits = [x1, x2_fixed, x3_fixed]
            probs = self.softmax(logits)
            return min(probs[0], 1.0)

        # Plot the raw curve without scaling
        raw_curve = axes.plot(softmax_prob_x1, x_range=[-4, 4], color=BLUE, stroke_width=4)

        graph_title = MathTex(r"\text{Softmax Output } P(x_1)", font_size=32)
        graph_title.next_to(axes, UP, buff=0.8)

        # Animate the axes, tick-label, guide line, label, and the unscaled curve
        self.play(Write(graph_title))
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(raw_curve), run_time=2)

        # Add a moving dot tracking the unscaled curve
        x_tracker = ValueTracker(-4)
        moving_dot = always_redraw(lambda: Dot(
            axes.c2p(x_tracker.get_value(), softmax_prob_x1(x_tracker.get_value())),
            color=YELLOW,
            radius=0.12
        ))

        # Display “x₁ = …” and “P(x₁) = …” (true values)
        x_value_display = DecimalNumber(-4, num_decimal_places=1, font_size=24)
        p_value_display = DecimalNumber(0, num_decimal_places=3, font_size=24)

        x_label_text = MathTex(r"x_1 = ", font_size=20)
        p_label_text = MathTex(r"P(x_1) = ", font_size=20)

        x_display_group = VGroup(x_label_text, x_value_display).arrange(RIGHT, buff=0.08)
        p_display_group = VGroup(p_label_text, p_value_display).arrange(RIGHT, buff=0.08)
        value_display = VGroup(x_display_group, p_display_group).arrange(DOWN, buff=0.08)

        def update_displays():
            x_val = x_tracker.get_value()
            raw_p = softmax_prob_x1(x_val)
            x_value_display.set_value(x_val)
            p_value_display.set_value(raw_p)
            dot_pos = axes.c2p(x_val, raw_p)
            value_display.move_to(dot_pos + UP * 1.2)

        value_display.add_updater(lambda m: update_displays())

        self.play(FadeIn(moving_dot), Write(value_display))
        self.play(x_tracker.animate.set_value(4), run_time=5, rate_func=smooth)
        self.wait(2)

        # Fade everything out
        self.play(
            FadeOut(graph_title),
            FadeOut(axes),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(raw_curve),
            FadeOut(moving_dot),
            FadeOut(value_display),
            FadeOut(formula)
        )
