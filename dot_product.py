from manim import *

class DotProductExpandedEllipsis(Scene):
    def construct(self):
        # 1. Show "Q · K^T"
        eq1 = MathTex(r"Q \cdot K^T", font_size=72)
        eq1.move_to(ORIGIN)
        self.play(Write(eq1), run_time=1.0)
        self.wait(0.5)

        # 2. Expand to "Q · K^T = Q₁·K₁ + Q₂·K₂ + Q₃·K₃ + … + Q_{d_k}·K_{d_k}"
        eq2 = MathTex(
            r"Q \cdot K^T",
            r"=",
            r"Q_1 \cdot K_1",
            r"+",
            r"Q_2 \cdot K_2",
            r"+",
            r"Q_3 \cdot K_3",
            r"+",
            r"\dots",
            r"+",
            r"Q_{d_k} \cdot K_{d_k}",
            font_size=48
        )
        eq2.move_to(ORIGIN)

        # Transform "Q · K^T" into the expanded form with ellipsis
        self.play(TransformMatchingTex(eq1, eq2), run_time=2.5)
        self.wait(1.0)
