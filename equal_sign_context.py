from manim import *

class EqualSignContext(Scene):
    def construct(self):
        # ─────────────────────────────────────────────────────────────────
        # 1) Build each equation so that the "=" is its own submobject
        # ─────────────────────────────────────────────────────────────────
        eq1 = Tex(
            "'",         # [0] opening quote
            "26 + 55 ",  # [1] the digits/operators plus a trailing space
            "=",         # [2] the equals-sign
            "'",         # [3] closing quote
            font_size=50
        )
        eq2 = Tex(
            "'",
            "150 - 100 ",  # notice the space after “100” so "=" won’t jam against it
            "=",
            "'",
            font_size=50
        )

        # Position eq1 above center and eq2 below center
        eq1.shift(UP * 1)
        eq2.shift(DOWN * 1)

        # ─────────────────────────────────────────────────────────────────
        # 2) Animate writing the two equations
        # ─────────────────────────────────────────────────────────────────
        self.play(Write(eq1))
        self.play(Write(eq2))
        self.wait(0.5)

        # ─────────────────────────────────────────────────────────────────
        # 3) Circle the "=" submobject (index 2 in each Tex)
        # ─────────────────────────────────────────────────────────────────
        circ1 = Circle(radius=0.25) \
            .move_to(eq1[2].get_center()) \
            .set_stroke(color=[PINK, RED], width=5) \
            .set_fill(opacity=0)
        circ2 = Circle(radius=0.25) \
            .move_to(eq2[2].get_center()) \
            .set_stroke(color=[PINK, RED], width=5) \
            .set_fill(opacity=0)

        self.play(Create(circ1), Create(circ2))
        self.wait(0.5)

        # ─────────────────────────────────────────────────────────────────
        # 4) Add the explanatory text to the right
        # ─────────────────────────────────────────────────────────────────
        explanation = Tex(
            "Same ‘=’, but different contextual meanings",
            font_size=32
        )
        explanation.next_to(VGroup(eq1, eq2), UP, buff=0.5)

        self.play(Write(explanation))
        self.wait(2)
