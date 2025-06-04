from manim import *
import numpy as np

class EmbeddingContextEvolution(Scene):
    def construct(self):
        # Use a slightly wider spacing between tokens/embeddings
        self.token_spacing = 3.5
        
        # Show the main embedding evolution sequence
        self.embedding_evolution()

    def create_embedding_vector(self, values, color=WHITE, scale_factor=1.0):
        """
        Create a vertical list of a few numeric components, plus an ellipsis and final value.
        """
        vector_components = VGroup()
        for j, val in enumerate(values[:3]):
            text = Tex(f"{val:.2f}", font_size=26 * scale_factor, color=WHITE)
            if j == 0:
                text.move_to(ORIGIN)
            else:
                text.next_to(vector_components[-1], DOWN, buff=0.15 * scale_factor)
            vector_components.add(text)

        ellipsis = Tex(r"\vdots", font_size=28 * scale_factor, color=WHITE)
        ellipsis.next_to(vector_components[-1], DOWN, buff=0.15 * scale_factor)
        vector_components.add(ellipsis)

        final_val = Tex(f"{values[-1]:.2f}", font_size=26 * scale_factor, color=WHITE)
        final_val.next_to(ellipsis, DOWN, buff=0.15 * scale_factor)
        vector_components.add(final_val)

        # Brackets around the column
        open_bracket = Tex("[", font_size=38 * scale_factor, color=color).rotate(-PI / 2)
        close_bracket = Tex("]", font_size=38 * scale_factor, color=color).rotate(-PI / 2)
        open_bracket.next_to(vector_components, UP, buff=0.1 * scale_factor)
        close_bracket.next_to(vector_components, DOWN, buff=0.1 * scale_factor)

        return VGroup(open_bracket, vector_components, close_bracket)

    def embedding_evolution(self):
        # 1. Tokens (spaced horizontally) – only "26" and "="
        tokens = VGroup(*[
            Tex(rf"\text{{'{tok}'}}", font_size=50, color=BLUE_C)
            for tok in ['26', '=']
        ])
        for i, token in enumerate(tokens):
            x = (i - 0.5) * self.token_spacing  # positions at -0.5 and +0.5 times spacing
            token.move_to(np.array([x, 2.5, 0]))
        # Animate tokens in
        for token in tokens:
            self.play(FadeIn(token, scale=1.1), run_time=0.4)
        self.wait(0.8)

        # 2. Original (generic) embeddings under each token
        original_vals = [
            [0.23, -0.45, 0.12, 0.78, -0.34],  # "26"
            [-0.65, 0.34, -0.18, 0.52, 0.73]   # "="
        ]
        original_embeddings = VGroup()
        for i, vals in enumerate(original_vals):
            emb = self.create_embedding_vector(vals, WHITE, scale_factor=0.8)
            emb.move_to(tokens[i].get_center() + DOWN * 1.2)
            original_embeddings.add(emb)

        # 3. Original (generic) meanings under each embedding
        original_meanings = VGroup(*[
            Tex(text, font_size=28, color=GREEN_C)
            for text in [
                r"\text{number}",     # for "26"
                r"\text{operator}",   # for "="
            ]
        ])
        for i, meaning in enumerate(original_meanings):
            meaning.next_to(original_embeddings[i], DOWN, buff=1.0)

        meaning_arrows = VGroup()
        for i in range(2):
            ma = Arrow(
                original_embeddings[i].get_bottom() + DOWN * 0.05,
                original_meanings[i].get_top() + UP * 0.05,
                stroke_width=3, color=GREEN_C, max_tip_length_to_length_ratio=0.2
            )
            meaning_arrows.add(ma)

        # 4. Show the original embedding and meaning for "26" first
        self.play(FadeIn(original_embeddings[0], shift=DOWN * 0.2), run_time=0.6)
        self.play(FadeIn(original_meanings[0], shift=UP * 0.2), GrowArrow(meaning_arrows[0]), run_time=0.5)
        self.wait(0.5)

        # 5. Then show the original embedding and meaning for "="
        self.play(FadeIn(original_embeddings[1], shift=DOWN * 0.2), run_time=0.6)
        self.play(FadeIn(original_meanings[1], shift=UP * 0.2), GrowArrow(meaning_arrows[1]), run_time=0.5)
        self.wait(1)

        # 6. Prepare new (contextualized) embeddings and meanings
        new_vals = [
            [0.18, -0.62, 0.35, 0.91, -0.47],  # "26" → "first operand in addition"
            [-0.71, 0.48, -0.32, 0.65, 0.94]   # "=" → "conclusion of 26 + 55"
        ]
        new_embeddings = VGroup()
        for i, vals in enumerate(new_vals):
            ne = self.create_embedding_vector(vals, WHITE, scale_factor=0.8)
            ne.move_to(tokens[i].get_center() + DOWN * 1.2)
            new_embeddings.add(ne)

        new_meanings = VGroup(*[
            Tex(text, font_size=28, color=ORANGE)
            for text in [
                r"\text{first operand in addition}",        # for "26"
                r"\text{conclusion of 26 + 55}",            # for "="
            ]
        ])
        for i, nm in enumerate(new_meanings):
            nm.next_to(new_embeddings[i], DOWN, buff=1.0)

        # 7. Transform for "26": transform embedding + create green arrow + "update" simultaneously; keep yellow arrow visible
        new_arrow_0 = Arrow(
            new_embeddings[0].get_bottom() + DOWN * 0.05,
            new_meanings[0].get_top() + UP * 0.05,
            stroke_width=3, color=ORANGE, max_tip_length_to_length_ratio=0.2
        )
        update_label_0 = Text("update", font_size=24, color=ORANGE)
        update_label_0.next_to(new_arrow_0.get_center(), RIGHT, buff=0.2)
        self.play(
            Transform(original_embeddings[0], new_embeddings[0]),
            Create(new_arrow_0),
            Write(update_label_0),
            run_time=2
        )
        self.wait(0.2)
        # After arrow+update appear, transform meaning and fade out "update"
        self.play(
            Transform(original_meanings[0], new_meanings[0]),
            FadeOut(update_label_0),
            run_time=0.8
        )
        self.wait(0.4)

        # 8. Transform for "=": transform embedding + create green arrow + "update" simultaneously; keep yellow arrow visible
        new_arrow_1 = Arrow(
            new_embeddings[1].get_bottom() + DOWN * 0.05,
            new_meanings[1].get_top() + UP * 0.05,
            stroke_width=3, color=ORANGE, max_tip_length_to_length_ratio=0.2
        )
        update_label_1 = Text("update", font_size=24, color=ORANGE)
        update_label_1.next_to(new_arrow_1.get_center(), RIGHT, buff=0.2)
        self.play(
            Transform(original_embeddings[1], new_embeddings[1]),
            Create(new_arrow_1),
            Write(update_label_1),
            run_time=2
        )
        self.wait(0.2)
        self.play(
            Transform(original_meanings[1], new_meanings[1]),
            FadeOut(update_label_1),
            run_time=0.8
        )
        self.wait(0.4)
