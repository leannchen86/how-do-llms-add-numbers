from manim import *

class LLMScene(Scene):
    def construct(self):
        # 1) Everything in LaTeX
        title = Tex(r"\text{How do LLMs calculate...}", font_size=80)
        
        # 2) Equations also in Tex (math mode is invoked automatically) - moved to origin area
        eq1 = Tex(r"26 + 55 = ?", font_size=70)
        eq2 = Tex(r"36 + 59 = ?", font_size=70).next_to(eq1, DOWN, buff=0.5)
        
        # 3) Position equations at origin and title above them
        eq1.move_to(ORIGIN)
        title.next_to(eq1, UP, buff=0.8)
        
        # 4) Animate
        self.play(Write(title), run_time=2)
        self.play(FadeIn(eq1, eq2), run_time=2)
        self.wait(1)
