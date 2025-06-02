from manim import *
import numpy as np

class LLMTokenizationAndEmbedding(ThreeDScene):
    def construct(self):
        # Enhanced color scheme
        self.token_colors = [BLUE_C, BLUE_C, BLUE_C, BLUE_C]  # Different colors for each token
        
        # Scene 2: Tokenization Process
        token_elements, token_ids = self.tokenization()
        
        # Scene 3: Embedding Vectors
        embedding_group, individual_embeddings, arrows = self.embedding_vectors(token_elements, token_ids)
        
        # Scene 4: Latent Space Visualization
        self.latent_space(individual_embeddings, arrows, token_elements)
        
    def tokenization(self):
        # Smoother title animation
        explanation = Text("Tokenization", font_size=42, color=WHITE)
        explanation.to_edge(UP, buff=1)
        
        self.play(Write(explanation), run_time=1.5)
        self.wait(0.8)
        
        # Original text with better positioning
        original_text = Text("'26 + 55 ='", font_size=44, color=GRAY_A)
        original_text.move_to(UP * 1.5)
        self.play(FadeOut(explanation))
        
        # Add subtle glow effect
        original_glow = original_text.copy().set_stroke(WHITE, width=3, opacity=0.3)
        
        self.play(
            FadeIn(original_glow),
            Write(original_text),
            run_time=2.8
        )
        self.wait(1.2)
        
        # Enhanced tokenization with better spacing
        tokens = [
            Text("'26'", font_size=45, color=self.token_colors[0]),
            Text("'+'", font_size=45, color=self.token_colors[1]),
            Text("'55'", font_size=45, color=self.token_colors[2]),
            Text("'='", font_size=45, color=self.token_colors[3])
        ]
        
        # Better positioning with dynamic spacing
        token_positions = [LEFT * 3, LEFT * 1, RIGHT * 1, RIGHT * 3]
        for token, pos in zip(tokens, token_positions):
            token.move_to(pos + DOWN * 0.5)
        
        token_group = VGroup(*tokens)
        
        # More dramatic split animation
        self.play(
            FadeOut(original_glow),
            original_text.animate.set_opacity(0.3),
            run_time=0.8
        )
        
        # Animate tokens appearing one by one with bounce effect
        for i, token in enumerate(tokens):
            self.play(
                FadeIn(token, scale=1.3),
                run_time=0.6
            )
            self.play(
                token.animate.scale(1/1.3),
                run_time=0.4
            )
        
        # Enhanced token IDs with glowing effect
        token_ids = [
            Text("ID: 253", font_size=18, color=YELLOW_C),
            Text("ID: 16", font_size=18, color=YELLOW_C),
            Text("ID: 361", font_size=18, color=YELLOW_C),
            Text("ID: 54", font_size=18, color=YELLOW_C)
        ]
        
        # Position IDs with better spacing
        for token_id, token in zip(token_ids, tokens):
            token_id.next_to(token, DOWN, buff=0.8)
            # Add subtle glow to IDs
            token_id.set_stroke(YELLOW, width=1, opacity=0.5)
        
        # Dramatic ID reveal
        self.play(
            LaggedStart(*[FadeIn(token_id, scale=0.8) for token_id in token_ids],
                       lag_ratio=0.2),
            run_time=2
        )
        
        self.wait(1.5)
        
        # Group all elements
        token_elements = VGroup(*tokens)
        
        # Smoother cleanup transition - fade out labels and IDs here
        self.play(
            FadeOut(original_text),
            FadeOut(VGroup(*token_ids)),      # Fade out IDs
            token_elements.animate.arrange(RIGHT, buff=1.5).to_edge(UP, buff=2),
            run_time=2
        )
        
        return token_elements, token_ids
        
    def embedding_vectors(self, token_elements, token_ids):
        # Enhanced title
        explanation = Text("Embedding Vectors", font_size=42, color=WHITE)
        explanation.to_edge(UP, buff=0.5)
        
        self.play(Write(explanation), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(explanation), run_time=1)
        
        # Better vector visualization with more spacing
        embeddings = []
        
        for i in range(4):
            # Create more visually appealing vector representation
            vector_values = [round(np.random.uniform(-1, 1), 2) for _ in range(4)]
            
            # Create vector as a column matrix style
            vector_elements = VGroup()
            
            # Create the vector components first
            vector_components = VGroup()
            for j, val in enumerate(vector_values):
                val_text = Text(f"{val:.2f}", font_size=16, color=GRAY_A)
                if j == 0:
                    val_text.move_to(ORIGIN)
                else:
                    val_text.next_to(vector_components[-1], DOWN, buff=0.2)
                vector_components.add(val_text)

            # Add ellipsis
            ellipsis = Text("⋮", font_size=20, color=GRAY_B)
            ellipsis.next_to(vector_components[-1], DOWN, buff=0.2)
            vector_components.add(ellipsis)

            # Add final component
            final_val = Text(f"{round(np.random.uniform(-1, 1), 2):.2f}", font_size=16, color=GRAY_A)
            final_val.next_to(ellipsis, DOWN, buff=0.2)
            vector_components.add(final_val)

            # Add brackets on top and bottom (no rotation)
            open_bracket = Text("[", font_size=32, color=WHITE).rotate(-PI/2)
            close_bracket = Text("]", font_size=32, color=WHITE).rotate(-PI/2)

            # Position brackets above and below the vector components
            open_bracket.next_to(vector_components, UP, buff=0.1)
            close_bracket.next_to(vector_components, DOWN, buff=0.1)

            # Add all elements to vector_elements
            vector_elements.add(open_bracket)
            vector_elements.add(vector_components)
            vector_elements.add(close_bracket)
            
            # Position vectors with increased spacing
            x_pos = (i - 1.5) * 2.1  # Increased from 0.8 to 1.2 for more space
            vector_elements.move_to(RIGHT * x_pos + DOWN * 1.2)
            
            vector_group = VGroup(vector_elements)
            embeddings.append(vector_group)
        
        # Create dimension label and brace (only once, on the left)
        dim_label = Text("768-dim", font_size=38, color=GRAY_C, slant=ITALIC)
        brace = Text("{", font_size=150, color=GRAY_C)
        
        # Position the brace and label to the left of all embeddings
        all_embeddings_group = VGroup(*embeddings)
        brace.next_to(all_embeddings_group, LEFT, buff=0.3)
        dim_label.next_to(brace, LEFT, buff=0.2)
        
        # Smoother vector appearance
        for i, embedding in enumerate(embeddings):
            self.play(
                FadeIn(embedding, shift=DOWN*0.3),
                run_time=0.8
            )
        
        # Add the dimension label and brace after all embeddings are shown
        self.play(
            FadeIn(brace),
            FadeIn(dim_label),
            run_time=1
        )
        
        # Enhanced arrows with animation
        arrows = []
        for i in range(4):
            start_pos = token_elements[i].get_center() + DOWN * 0.3
            end_pos = embeddings[i].get_top() + UP * 0.2
            
            arrow = Arrow(
                start_pos, end_pos,
                buff=0.2,
                stroke_width=6.5,
                color=self.token_colors[i],
                max_tip_length_to_length_ratio=0.12
            )
            arrows.append(arrow)
        
        # Animated arrow appearance
        self.play(
            LaggedStart(*[GrowArrow(arrow) for arrow in arrows],
                       lag_ratio=0.2),
            run_time=2
        )
        
        self.wait(2)

        self.play(
            FadeOut(brace),
            FadeOut(dim_label)
        )
        
        # Return embedding group and individual embeddings for transformation
        embedding_group = VGroup(*embeddings, brace, dim_label)
        return embedding_group, embeddings, arrows
        
    def latent_space(self, individual_embeddings, arrows, token_elements):
        # Enhanced title
        explanation = Text("Tokens in high-dimensional space", font_size=42, color=WHITE)
        explanation.to_edge(UP, buff=1)
        
        # Enhanced 3D axes - create off-screen to the right
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
        
        # Position axes off-screen to the right
        axes.shift(RIGHT * 20)
              
        # Add axes off-screen to the right and slide them in while moving vectors left
        self.add(axes)
        self.play(
            # Slide vectors to the left
            VGroup(*individual_embeddings).animate.shift(LEFT * 4).scale(0.8),
            token_elements.animate.shift(LEFT * 4).scale(0.8),
            # Bring axes in from the right to CENTER of screen
            VGroup(*arrows).animate.shift(LEFT * 4).scale(0.8),
            axes.animate.shift(LEFT * 20).scale(0.8),  # Changed to LEFT * 20 to center the axes
            run_time=2.5
        )
        
        # Enhanced token positioning with clustering - positions relative to axes center
        token_vectors = [
            (axes.c2p(2.2, 1.5, 2.8), "'26'", self.token_colors[0]),
            (axes.c2p(-2.8, -1.8, 0.5), "'+'", self.token_colors[1]),
            (axes.c2p(2.5, 1.2, 3.1), "'55'", self.token_colors[2]),
            (axes.c2p(-2.5, -2.1, 0.8), "'='", self.token_colors[3])
        ]
        
        dots = []
        labels = []
        
        # Create target dots and labels
        for i, (pos, text_content, color) in enumerate(token_vectors):
            # Create enhanced dot with glow
            dot = Dot3D(radius = 0.09, color=color)
            dot.move_to(pos)
            dots.append(dot)
            
            # Create enhanced label
            label = Text(text_content, font_size=20, color=color, weight=BOLD)
            label.scale(0.6)
            label.move_to(pos + OUT * 0.3 + UP * 0.3)
            self.add_fixed_orientation_mobjects(label)
            labels.append(label)
        
        # Transform individual embeddings to dots while still in 2D view
        transform_animations = []
        for i in range(4):
            transform_animations.append(Transform(individual_embeddings[i], dots[i]))

        self.play(Write(explanation), run_time=1.5)
        self.play(FadeOut(explanation), run_time=1)

        # Transform vectors to dots and fade in labels
        self.play(
            *transform_animations,
            FadeOut(*arrows),
            FadeOut(*token_elements),
            *[FadeIn(label) for label in labels],
            run_time=2.5
        )
        
        # NOW move camera to proper 3D view for the final scene
        self.move_camera(
            phi=70 * DEGREES,
            theta=-45 * DEGREES,
            zoom=0.8,
            run_time=2
        )
        
        self.wait(1)
        
        # Define additional tokens with their positions and colors
        additional_tokens = [
            # Numbers cluster (near our number tokens)
            (axes.c2p(1.8, 2.1, 2.3), "'7'", BLUE_A),
            (axes.c2p(2.7, 0.9, 3.5), "'100'", BLUE_A),
            (axes.c2p(1.5, 1.8, 2.1), "'42'", BLUE_A),
            
            # Mathematical operators cluster (near + and =)
            (axes.c2p(-2.2, -1.5, 1.1), "'-'", GREEN_C),
            (axes.c2p(-3.1, -2.4, 0.2), "'*'", GREEN_C),
            (axes.c2p(-2.0, -2.8, 0.9), "'/'", GREEN_C),
            
            # Common words (distributed in other areas)
            (axes.c2p(-1.2, 3.2, -2.1), "'the'", PURPLE_C),
            (axes.c2p(0.5, -3.1, -1.8), "'and'", PURPLE_C),
            (axes.c2p(3.2, -0.8, -2.5), "'is'", PURPLE_C),
            (axes.c2p(-3.5, 1.2, -1.2), "'of'", PURPLE_C),
            
            # Punctuation scattered
            (axes.c2p(0.8, 2.8, -3.2), "'.'", ORANGE),
            (axes.c2p(-0.5, -2.2, -2.8), "','", ORANGE),
            (axes.c2p(2.1, -2.5, -1.5), "'?'", ORANGE),
        ]
        
        # Create dots and labels for additional tokens
        additional_dots = []
        additional_labels = []
        
        for pos, text_content, color in additional_tokens:
            # Create smaller, more subtle dots for additional tokens
            dot = Dot3D(radius=0.09, color=color)
            dot.move_to(pos)
            dot.set_opacity(0.7)
            additional_dots.append(dot)
            
            # Create labels
            label = Text(text_content, font_size=20, color=color)
            label.scale(0.5)
            label.move_to(pos + OUT * 0.2 + UP * 0.2)
            self.add_fixed_orientation_mobjects(label)
            additional_labels.append(label)
        
        # Animate additional tokens appearing in waves
        # Numbers first
        self.play(
            *[FadeIn(additional_dots[i], scale=0.5) for i in range(3)],
            *[FadeIn(additional_labels[i], scale=0.5) for i in range(3)],
            run_time=1.5
        )
        self.wait(0.5)
        
        # Then operators
        self.play(
            *[FadeIn(additional_dots[i], scale=0.5) for i in range(3, 6)],
            *[FadeIn(additional_labels[i], scale=0.5) for i in range(3, 6)],
            run_time=1.5
        )
        self.wait(0.5)
        
        # Then common words
        self.play(
            *[FadeIn(additional_dots[i], scale=0.5) for i in range(6, 10)],
            *[FadeIn(additional_labels[i], scale=0.5) for i in range(6, 10)],
            run_time=1.5
        )
        self.wait(0.5)
        
        # Finally punctuation
        self.play(
            *[FadeIn(additional_dots[i], scale=0.5) for i in range(10, 13)],
            *[FadeIn(additional_labels[i], scale=0.5) for i in range(10, 13)],
            run_time=1.5
        )
        
        self.wait(2)
        
        self.move_camera(
            theta=-135 * DEGREES,
            run_time=3
        )