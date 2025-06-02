from manim import *
import numpy as np

class LLMTokenizationAndEmbedding(ThreeDScene):
    def construct(self):
        # Enhanced color scheme
        self.token_colors = [BLUE_C, BLUE_C, BLUE_C, BLUE_C]
        
        # Scene 2: Tokenization Process
        token_elements, token_ids = self.tokenization()
        
        # Scene 3: Embedding Vectors
        embedding_group, individual_embeddings, arrows = self.embedding_vectors(token_elements, token_ids)
        
        # Scene 4: Latent Space Visualization
        self.latent_space(individual_embeddings, arrows, token_elements)
        
        
    def tokenization(self):
        explanation = Tex(r"\text{Tokenization}", font_size=42, color=WHITE)
        explanation.to_edge(UP, buff=1)
        self.play(Write(explanation), run_time=1.5)
        self.wait(0.8)
        
        original_text = Tex(r"\text{'26 + 55 ='}", font_size=44, color=GRAY_A)
        original_text.move_to(UP * 1.5)
        self.play(FadeOut(explanation))
        
        original_glow = original_text.copy().set_stroke(WHITE, width=3, opacity=0.3)
        self.play(
            FadeIn(original_glow),
            Write(original_text),
            run_time=2.8
        )
        self.wait(1.2)
        
        tokens = [
            Tex(r"\text{'26'}", font_size=45, color=self.token_colors[0]),
            Tex(r"\text{'+'}", font_size=45, color=self.token_colors[1]),
            Tex(r"\text{'55'}", font_size=45, color=self.token_colors[2]),
            Tex(r"\text{'='}", font_size=45, color=self.token_colors[3])
        ]
        token_positions = [LEFT * 3, LEFT * 1, RIGHT * 1, RIGHT * 3]
        for token, pos in zip(tokens, token_positions):
            token.move_to(pos + DOWN * 0.5)
        token_group = VGroup(*tokens)
        
        self.play(
            FadeOut(original_glow),
            original_text.animate.set_opacity(0.3),
            run_time=0.8
        )
        
        for token in tokens:
            self.play(FadeIn(token, scale=1.3), run_time=0.6)
            self.play(token.animate.scale(1 / 1.3), run_time=0.4)
        
        token_ids = [
            Tex(r"\text{ID: 253}", font_size=18, color=YELLOW_C),
            Tex(r"\text{ID: 16}", font_size=18, color=YELLOW_C),
            Tex(r"\text{ID: 361}", font_size=18, color=YELLOW_C),
            Tex(r"\text{ID: 54}", font_size=18, color=YELLOW_C)
        ]
        for token_id, token in zip(token_ids, tokens):
            token_id.next_to(token, DOWN, buff=0.8)
            token_id.set_stroke(YELLOW, width=1, opacity=0.5)
        
        self.play(
            LaggedStart(*[FadeIn(tid, scale=0.8) for tid in token_ids], lag_ratio=0.2),
            run_time=2
        )
        self.wait(1.5)
        
        token_elements = VGroup(*tokens)
        self.play(
            FadeOut(original_text),
            FadeOut(VGroup(*token_ids)),
            token_elements.animate.arrange(RIGHT, buff=1.5).to_edge(UP, buff=2),
            run_time=2
        )
        
        return token_elements, token_ids
    
    
    def embedding_vectors(self, token_elements, token_ids):
        explanation = Tex(r"\text{Embedding Vectors}", font_size=42, color=WHITE)
        explanation.to_edge(UP, buff=0.5)
        self.play(Write(explanation), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(explanation), run_time=1)
        
        embeddings = []
        for i in range(4):
            values = [round(np.random.uniform(-1, 1), 2) for _ in range(4)]
            vector_components = VGroup()
            for j, val in enumerate(values):
                text = Tex(f"{val:.2f}", font_size=16, color=GRAY_A)
                if j == 0:
                    text.move_to(ORIGIN)
                else:
                    text.next_to(vector_components[-1], DOWN, buff=0.2)
                vector_components.add(text)
            ellipsis = Tex(r"\vdots", font_size=20, color=GRAY_B)
            ellipsis.next_to(vector_components[-1], DOWN, buff=0.2)
            vector_components.add(ellipsis)
            final_val = Tex(f"{round(np.random.uniform(-1, 1), 2):.2f}", font_size=16, color=GRAY_A)
            final_val.next_to(ellipsis, DOWN, buff=0.2)
            vector_components.add(final_val)
            
            open_bracket = Tex("[", font_size=32, color=WHITE).rotate(-PI / 2)
            close_bracket = Tex("]", font_size=32, color=WHITE).rotate(-PI / 2)
            open_bracket.next_to(vector_components, UP, buff=0.1)
            close_bracket.next_to(vector_components, DOWN, buff=0.1)
            
            vector_elements = VGroup(open_bracket, vector_components, close_bracket)
            x_pos = (i - 1.5) * 2.1
            vector_elements.move_to(RIGHT * x_pos + DOWN * 1.2)
            embeddings.append(VGroup(vector_elements))
        
        arrows = []
        for i in range(4):
            start = token_elements[i].get_center() + DOWN * 0.3
            end = embeddings[i].get_top() + UP * 0.2
            arrow = Arrow(
                start, end,
                buff=0.2,
                stroke_width=6.5,
                color=self.token_colors[i],
                max_tip_length_to_length_ratio=0.12
            )
            arrows.append(arrow)
        
        dim_label = Tex(r"\text{768-dim}", font_size=38, color=GRAY_C)
        brace = Tex(r"\{", font_size=150, color=GRAY_C)
        all_embeddings = VGroup(*embeddings)
        brace.next_to(all_embeddings, LEFT, buff=0.3)
        dim_label.next_to(brace, LEFT, buff=0.2)
        
        for embed, arrow in zip(embeddings, arrows):
            self.play(FadeIn(embed, shift=DOWN * 0.3), GrowArrow(arrow), run_time=0.8)
        self.wait(2)
        
        self.play(FadeIn(brace), FadeIn(dim_label), run_time=1)
        self.play(FadeOut(brace), FadeOut(dim_label))
        
        embedding_group = VGroup(*embeddings, brace, dim_label)
        return embedding_group, embeddings, arrows
    
    
    def latent_space(self, individual_embeddings, arrows, token_elements):
        # Repositioned explanation to avoid overlap
        explanation = Tex(
            r"\text{Embeddings in high-dimensional space}", 
            font_size=25, 
            color=WHITE
        )
        explanation.to_edge(UL, buff=1.95)
        
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            z_length=8,
            axis_config={
                "color": GRAY_B,
                "stroke_width": 2,
                "include_tip": True,
                "tip_length": 0.2
            }
        )
        axes.shift(RIGHT * 20)
        
        self.add(axes)
        self.play(
            VGroup(*individual_embeddings).animate.shift(LEFT * 4).scale(0.8),
            token_elements.animate.shift(LEFT * 4).scale(0.8),
            VGroup(*arrows).animate.shift(LEFT * 4).scale(0.8),
            axes.animate.shift(LEFT * 20).scale(0.8),
            run_time=2.5
        )
        
        dots = []
        labels = []
        token_vectors = [
            (axes.c2p(2.2, 1.5, 2.8), r"\text{'26'}", self.token_colors[0]),
            (axes.c2p(-2.8, -1.8, 0.5), r"\text{'+'}", self.token_colors[1]),
            (axes.c2p(2.5, 1.2, 3.1), r"\text{'55'}", self.token_colors[2]),
            (axes.c2p(-2.5, -2.1, 0.8), r"\text{'='}", self.token_colors[3])
        ]
        for pos, txt, color in token_vectors:
            dot = Dot3D(radius=0.09, color=color).move_to(pos)
            dots.append(dot)
            label = Tex(txt, font_size=20, color=color).scale(0.6).move_to(pos + OUT * 0.3 + UP * 0.3)
            self.add_fixed_orientation_mobjects(label)
            labels.append(label)
        
        transform_animations = [
            Transform(individual_embeddings[i], dots[i]) for i in range(4)
        ]
        self.play(
            *transform_animations,
            FadeOut(*arrows),
            FadeOut(*token_elements),
            *[FadeIn(lab) for lab in labels],
            run_time=2.5
        )
        
        # Display explanation after transforms, in top-right corner
        self.play(Write(explanation), run_time=1.5)
        self.play(FadeOut(explanation), run_time=1)
        
        # Move camera for 3D perspective
        self.move_camera(phi=70 * DEGREES, theta=-45 * DEGREES, zoom=0.8, run_time=2)
        self.wait(1)
        
        # Additional tokens (all light up simultaneously)
        additional_tokens = [
            (axes.c2p(1.8, 2.1, 2.3), r"\text{'7'}", BLUE_A),
            (axes.c2p(2.7, 0.9, 3.5), r"\text{'100'}", BLUE_A),
            (axes.c2p(1.5, 1.8, 2.1), r"\text{'42'}", BLUE_A),
            (axes.c2p(-2.2, -1.5, 1.1), r"\text{'-'}", GREEN_C),
            (axes.c2p(-3.1, -2.4, 0.2), r"\text{'*'}", GREEN_C),
            (axes.c2p(-2.0, -2.8, 0.9), r"\text{'/'}", GREEN_C),
            (axes.c2p(-1.2, 3.2, -2.1), r"\text{'the'}", PURPLE_C),
            (axes.c2p(0.5, -3.1, -1.8), r"\text{'and'}", PURPLE_C),
            (axes.c2p(3.2, -0.8, -2.5), r"\text{'is'}", PURPLE_C),
            (axes.c2p(-3.5, 1.2, -1.2), r"\text{'of'}", PURPLE_C),
            (axes.c2p(0.8, 2.8, -3.2), r"\text{'.'}", ORANGE),
            (axes.c2p(-0.5, -2.2, -2.8), r"\text{','}", ORANGE),
            (axes.c2p(2.1, -2.5, -1.5), r"\text{'?'}", ORANGE),
        ]
        
        additional_dots = []
        additional_labels = []
        for pos, txt, color in additional_tokens:
            dot = Dot3D(radius=0.09, color=color).move_to(pos).set_opacity(0.7)
            additional_dots.append(dot)
            label = Tex(txt, font_size=20, color=color).scale(0.5).move_to(pos + OUT * 0.2 + UP * 0.2)
            self.add_fixed_orientation_mobjects(label)
            additional_labels.append(label)
        
        # Fade in all additional dots and labels at once
        self.play(
            *[FadeIn(dot, scale=0.5) for dot in additional_dots],
            *[FadeIn(label, scale=0.5) for label in additional_labels],
            run_time=1.5
        )
        
        # Final camera adjustment
        self.move_camera(phi=60 * DEGREES, theta=-30 * DEGREES, zoom=0.7, run_time=3)
        self.wait(3)
