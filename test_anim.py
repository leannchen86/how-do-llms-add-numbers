from manim import *
import numpy as np

class Intro(Scene):
    def construct(self):
        title = Text("First things first—LLMs don’t see numbers or words the way we do.").scale(0.8)
        subtitle = Text(
            "They see tokens. Then each token → an embedding vector."
        ).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(title), FadeIn(subtitle))
        self.wait(2)

class Tokenization(Scene):
    def construct(self):
        expr = MathTex("26\\,+\\,55")
        self.play(Write(expr))
        self.wait(1)
        tokens = VGroup(
            MathTex("26"), MathTex("+"), MathTex("55")
        ).arrange(RIGHT, buff=1)
        self.play(
            TransformMatchingTex(expr, tokens),
            *[FadeIn(tok) for tok in tokens]
        )
        self.wait(1)

class ShowMapping(Scene):
    def construct(self):
        tokens = VGroup(
            MathTex("26"), MathTex("+"), MathTex("55")
        ).arrange(RIGHT, buff=1)

        boxes = VGroup(*[
            SurroundingRectangle(tok, buff=0.2, color=BLUE)
            for tok in tokens
        ])
        self.play(FadeIn(tokens), Create(boxes))
        self.wait(0.5)

        # embedding placeholders as simple dots
        embs = VGroup(*[
            Dot(radius=0.1, color=GREY)
            for _ in tokens
        ]).arrange(RIGHT, buff=1).shift(DOWN * 2)

        arrows = VGroup(*[
            Arrow(start=tok.get_bottom(), end=emb.get_top())
            for tok, emb in zip(tokens, embs)
        ])

        self.play(
            *[FadeIn(emb) for emb in embs],
            *[GrowArrow(ar) for ar in arrows]
        )
        self.wait(1)

class EmbeddingSpace(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-1,1,1], y_range=[-1,1,1],
            x_length=4, y_length=3
        ).to_edge(UP)
        label = Text(
            "Embedding space\n(1024-D → 2D proj.)"
        ).next_to(axes, RIGHT)
        arrow = Vector([0.8, 0.5, 0]).shift(axes.c2p(0,0))
        arrow_label = MathTex(r"\vec{e}_{26}").next_to(arrow.get_end(), UR)

        self.play(Create(axes), Write(label))
        self.wait(0.5)
        self.play(GrowArrow(arrow), Write(arrow_label))
        self.wait(1)

class LatentCloud(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-1,1,1], y_range=[-1,1,1],
            x_length=4, y_length=3
        ).to_edge(UP)
        cloud = VGroup(*[
            Dot(
                axes.c2p(
                    np.random.uniform(-1,1), np.random.uniform(-1,1)
                ),
                radius=0.03, color=GREY
            )
            for _ in range(100)
        ])
        highlighted = VGroup(
            Dot(axes.c2p(0.8,0.5), color=YELLOW, radius=0.08),
            Dot(axes.c2p(-0.4,0.2), color=GREEN, radius=0.08),
            Dot(axes.c2p(0.1,-0.7), color=RED, radius=0.08),
        )
        caption = Text(
            "Every token → its embedding\nin the same high-dimensional space."
        ).to_edge(DOWN)

        self.play(*[FadeIn(pt) for pt in cloud])
        self.wait(0.5)
        self.play(*[
            TransformFromCopy(pt, h) for pt, h in zip(cloud[:3], highlighted)
        ])
        self.play(Write(caption))
        self.wait(2)
