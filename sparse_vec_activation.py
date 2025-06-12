from manim import *

class ReLUL1VectorDemo(Scene):
    def construct(self):
        # Raw and ReLU versions (8 values each)
        raw_values = ["0.8", "-0.3", "0.2", "-0.05", "0.7", "-0.1"]
        relu_values = ["0.8", "0.0", "0.0", "0.0", "0.7", "0.0"]

        def vector_tex(values, color_neg=RED):
            # Build elements for Tex
            elements = ["\\big["]
            for i, v in enumerate(values):
                elements.append(v)
                if i < len(values) - 1:
                    elements.append(", \quad")
            elements.append("\\big]")
            vec = Tex(*elements, font_size=44)
            # Color negatives
            if color_neg:
                for i, v in enumerate(values):
                    if "-" in v:
                        vec[1 + 2*i].set_color(color_neg)
            return vec

        # Title
        title = Tex(r"\text{Sparse Feature Activation Vector}", font_size=40)
        
        # Vertical positions for vectors
        FIRST_VEC_Y = 1.2
        SECOND_VEC_Y = -0.5
        
        # Create (but don't yet animate) both vectors
        raw_vec = vector_tex(raw_values, color_neg=RED).move_to([0, FIRST_VEC_Y, 0])
        relu_vec = vector_tex(relu_values, False).move_to([0, SECOND_VEC_Y, 0])

        # Position title relative to relu_vec
        title.next_to(relu_vec, UP, buff=0.8)
        self.play(FadeIn(title))

        # (Later: animate raw_vec first, then the ReLU arrow, labels, and relu_vec.)
        self.play(FadeIn(relu_vec))
        self.wait(0.5)

        # Highlight consecutive zeroes in relu_vec with a rounded rectangle
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
            # Surround all mobjects in the group
            rect = SurroundingRectangle(VGroup(*mobjects), color=RED, stroke_width=2, buff=0.08, corner_radius=0.1)
            highlight_rects.append(rect)
        self.play(*[Create(rect) for rect in highlight_rects])
        self.wait(0.5)
        # Animate set_stroke effect on the rectangles
        self.play(*[rect.animate.set_stroke(width=5, color=RED) for rect in highlight_rects], run_time=0.8)
        # End the set_stroke effect by returning to original stroke
        self.play(*[rect.animate.set_stroke(width=2, color=RED) for rect in highlight_rects], run_time=0.5)
        self.wait(0.5)


