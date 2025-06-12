from manim import *

class ReLUL1VectorDemo(Scene):
    def construct(self):
        # Raw and ReLU versions
        raw_values = ["0.8", "-0.3", "-0.2", "-0.05", "0.7", "-0.1"]
        relu_values = ["0.8", "0.0", "0.0", "0.0", "0.7", "0.0"]

        def vector_tex(values, color_neg=RED, spacing=", \\quad"):
            # Build elements for Tex
            elements = ["\\big["]
            for i, v in enumerate(values):
                elements.append(v)
                if i < len(values) - 1:
                    elements.append(spacing)
            elements.append("\\big]")
            vec = Tex(*elements, font_size=44)
            # Color negatives
            if color_neg:
                for i, v in enumerate(values):
                    if "-" in v:
                        vec[1 + 2*i].set_color(color_neg)
            return vec

        # Create vectors
        raw_vec  = vector_tex(raw_values, color_neg=RED, spacing=", \\,")
        relu_vec = vector_tex(relu_values, color_neg=False, spacing=", \\;")

        # Title
        title = Tex(r"Sparse~Feature~Activation~Vector~Transformation", font_size=40)
        # Position title just above the raw vector
        title.next_to(raw_vec, UP, buff=2.5)

        # Positions
        FIRST_VEC_Y = 1.2
        SECOND_VEC_Y = -0.5

        # 1) Show raw vector
        raw_vec.move_to([0, FIRST_VEC_Y, 0])
        # Add 'original' label to the left of the raw vector
        original_label = Tex(r"original", font_size=32)
        original_label.next_to(raw_vec, LEFT, buff=0.7)
        self.play(FadeIn(title))
        self.play(FadeIn(raw_vec), FadeIn(original_label))
        self.wait(0.8)

        # 2) ReLU: arrow, text, and transformed vector
        relu_vec.move_to([0, SECOND_VEC_Y, 0])
        # Add 'updated' label to the left of the relu vector
        updated_label = Tex(r"updated", font_size=32)
        updated_label.next_to(relu_vec, LEFT, buff=0.7)
        arrow1 = Arrow(
            start=[0, FIRST_VEC_Y - 0.4, 0],
            end=[0, SECOND_VEC_Y + 0.4, 0],
            buff=0,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.2,
            color=WHITE
        ).scale(0.9)

        # ReLU label and description (single line)
        relu_label = Tex(r"ReLU()~zeroes~out~negative~values", font_size=30, color=WHITE)
        relu_label.next_to(arrow1, RIGHT, buff=0.4)

        # Animate ReLU step
        self.play(
            FadeIn(arrow1),
            FadeIn(relu_label),
            FadeIn(relu_vec, shift=DOWN * 0.2),
            FadeIn(updated_label)
        )
        self.wait(0.8)

        # Highlight consecutive zeroes in relu_vec with a rounded rectangle (copied from sparse_vec_activation.py)
        zero_groups = []
        current_group = []
        for idx, v in enumerate(relu_values):
            if v == "0.0":
                current_group.append(idx)
            else:
                if current_group:
                    zero_groups.append(current_group)
                    current_group = []
        if current_group:
            zero_groups.append(current_group)

        highlight_rects = []
        for group in zero_groups:
            mobjects = [relu_vec[1 + 2*i] for i in group]
            rect = SurroundingRectangle(VGroup(*mobjects), color=RED, stroke_width=2, buff=0.08, corner_radius=0.1)
            highlight_rects.append(rect)
        self.play(*[Create(rect) for rect in highlight_rects])
        self.wait(0.5)
        self.play(*[rect.animate.set_stroke(width=5, color=RED) for rect in highlight_rects], run_time=0.8)
        self.play(*[rect.animate.set_stroke(width=2, color=RED) for rect in highlight_rects], run_time=0.5)
        self.wait(0.5)

        # End
        self.wait()
