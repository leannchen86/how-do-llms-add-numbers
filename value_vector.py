from manim import *

class AttentionWeightsAnimation(Scene):
    def construct(self):
        # Title
        title = Tex(
            r"\text{Attention Weights Applied to Value Vectors}", 
            font_size=36
        )
        title.to_edge(UP, buff=1)
        
        # Mathematical expression with highlighted weights
        expression = MathTex(
            "0.21", r" \cdot V_{26} + ", "0.22", r" \cdot V_{+} + ", "0.29", r" \cdot V_{55} + ", "0.29", r" \cdot V_{=}"
        )
        expression.move_to(ORIGIN)
        
        # Highlight the weights with light yellow
        expression.set_color_by_tex("0.21", YELLOW_C)
        expression.set_color_by_tex("0.22", YELLOW_C)
        expression.set_color_by_tex("0.29", YELLOW_C)
        expression.set_color_by_tex("0.29", YELLOW_C)
        
        # Animation sequence
        self.play(Write(title))
        self.wait(1)
        self.play(Write(expression))
        self.wait(3)
        self.play(FadeOut(Group(*self.mobjects)))
