from manim import *

class SoftmaxEquation(Scene):
    def construct(self):
        # Create softmax formula text
        softmax_text = MathTex(
            r"\text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)",
            font_size=60,
            color=WHITE
        )
        
        # Position the equation in the center
        softmax_text.move_to(ORIGIN)
        
        # Display the equation
        self.play(Write(softmax_text))
        self.wait(1)
        
        # Create a red square to highlight √dk
        # First, we need to get the position of the √dk part
        # The √dk corresponds to the last part of the equation
        sqrt_dk_part = softmax_text[-1]  # Get the last part which contains √dk
        
        # Create a red rectangle around √dk
        highlight_rect = SurroundingRectangle(
            sqrt_dk_part,
            color=RED,
            stroke_width=3,
            buff=0.1,
            corner_radius=0.1
        )
        
        # Animate the highlight appearing
        self.play(Create(highlight_rect))
        self.wait(2)
        
        # Optional: Make the highlight pulse
        self.play(
            highlight_rect.animate.set_stroke(width=5),
            rate_func=there_and_back,
            run_time=0.8
        )
        
        self.wait(2)

# Alternative version with more precise highlighting
class SoftmaxEquationPrecise(Scene):
    def construct(self):
        # Create the softmax equation broken into parts for precise control
        softmax_parts = MathTex(
            r"\text{softmax}",
            r"\left(",
            r"\frac{QK^T}{\sqrt{d_k}}",
            r"\right)",
            font_size=60,
            color=WHITE
        )
        
        # Further break down the fraction part
        fraction_parts = MathTex(
            r"\frac{QK^T}{\sqrt{d_k}}",
            font_size=60,
            color=WHITE
        )
        
        # More precise breakdown
        equation_parts = MathTex(
            r"\text{softmax}\left(\frac{QK^T}{",
            r"\sqrt{d_k}",
            r"}\right)",
            font_size=60,
            color=WHITE
        )
        
        # Position the equation in the center
        equation_parts.move_to(ORIGIN)
        
        # Display the equation
        self.play(Write(equation_parts))
        self.wait(1)
        
        # Get the √dk part (index 1 in our breakdown)
        sqrt_dk_part = equation_parts[1]
        
        # Create a red rectangle with rounded corners around √dk
        highlight_rect = SurroundingRectangle(
            sqrt_dk_part,
            color=RED,
            stroke_width=2,
            buff=0.1,
            corner_radius=0.1
        )
        
        # Animate the highlight appearing
        self.play(Create(highlight_rect))
        self.wait(1)
        
        # Make it pulse
        self.play(
            highlight_rect.animate.set_stroke(width=5),
            rate_func=there_and_back,
            run_time=1
        )
        
        self.wait(2)