from manim import *
import numpy as np

class CLTAnimation(Scene):
    def construct(self):
        # Title
        title = Tex(r"\text{Cross-Layer Transcoder (CLT)}", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Create the main architecture
        self.setup_architecture()
        self.animate_data_flow()
        self.demonstrate_sparsity()
        self.show_interpretability()
        
    def setup_architecture(self):
        # Create three main components
        self.encoder_box = Rectangle(width=2.5, height=1.5, color=GREEN)
        self.sparse_box = Rectangle(width=2.5, height=1.5, color=ORANGE)
        self.decoder_box = Rectangle(width=2.5, height=1.5, color=BLUE)
        
        # Position them
        self.encoder_box.shift(LEFT * 4)
        self.sparse_box.shift(ORIGIN)
        self.decoder_box.shift(RIGHT * 4)
        
        # Labels
        encoder_label = Tex(r"\text{Encoder}\\\text{(dense)}", font_size=20, color=WHITE)
        sparse_label = Tex(r"\text{Sparse}\\\text{Activation}", font_size=20, color=WHITE)
        decoder_label = Tex(r"\text{Decoder}\\\text{(dense)}", font_size=20, color=WHITE)
        
        encoder_label.move_to(self.encoder_box.get_center())
        sparse_label.move_to(self.sparse_box.get_center())
        decoder_label.move_to(self.decoder_box.get_center())
        
        # Weight matrices labels
        w_e_label = MathTex("W_e", font_size=24, color=GREEN).next_to(self.encoder_box, DOWN)
        w_d_label = MathTex("W_d", font_size=24, color=BLUE).next_to(self.decoder_box, DOWN)
        
        # Dimension labels
        input_dim = Tex(r"\text{768-D}\\\text{embeddings}", font_size=14, color=GRAY).next_to(self.encoder_box, LEFT)
        sparse_dim = Tex(r"\text{16,384 features}\\\text{(\textasciitilde5 active)}", font_size=14, color=GRAY).next_to(self.sparse_box, DOWN, buff=0.5)
        output_dim = Tex(r"\text{768-D}\\\text{embeddings}", font_size=14, color=GRAY).next_to(self.decoder_box, RIGHT)
        
        # ReLU + L1 loss label
        loss_label = Tex(r"\text{ReLU + L1 loss}", font_size=14, color=RED).next_to(self.sparse_box, UP)
        
        # Arrows
        arrow1 = Arrow(self.encoder_box.get_right(), self.sparse_box.get_left(), color=WHITE)
        arrow2 = Arrow(self.sparse_box.get_right(), self.decoder_box.get_left(), color=WHITE)
        
        # Animate the setup
        self.play(
            Create(self.encoder_box),
            Create(self.sparse_box),
            Create(self.decoder_box),
            Write(encoder_label),
            Write(sparse_label),
            Write(decoder_label)
        )
        
        self.play(
            Write(w_e_label),
            Write(w_d_label),
            Write(input_dim),
            Write(sparse_dim),
            Write(output_dim),
            Write(loss_label)
        )
        
        self.play(Create(arrow1), Create(arrow2))
        self.wait(1)
        
        # Store references
        self.components = VGroup(
            self.encoder_box, self.sparse_box, self.decoder_box,
            encoder_label, sparse_label, decoder_label,
            w_e_label, w_d_label, input_dim, sparse_dim, output_dim,
            loss_label, arrow1, arrow2
        )
        
    def animate_data_flow(self):
        # Create input dense vector (768-D embeddings with actual values)
        input_values = VGroup()
        sample_values = [0.23, -0.15, 0.87, -0.42, 0.61, -0.33, 0.19, 0.74]
        for i, val in enumerate(sample_values):
            val_text = Tex(f"{val:.2f}", font_size=10, color=YELLOW)
            val_text.shift(LEFT * 6 + UP * (i-3.5) * 0.3)
            input_values.add(val_text)
        
        input_bracket = Tex("[", font_size=40, color=YELLOW).next_to(input_values, LEFT)
        input_bracket2 = Tex("]", font_size=40, color=YELLOW).next_to(input_values, RIGHT)
        input_ellipsis = MathTex(r"\ldots", font_size=12, color=YELLOW).next_to(input_values, DOWN)
        
        input_vector = VGroup(input_values, input_bracket, input_bracket2, input_ellipsis)
        
        # Show input flowing through encoder
        self.play(Create(input_vector))
        self.wait(0.5)
        
        self.play(input_vector.animate.shift(RIGHT * 1.5), run_time=1.5)
        
        # Transform to sparse feature activations (fundamentally different - not a vector)
        sparse_features = VGroup()
        # Show feature indices and their activation values
        active_features = [(1247, 0.82), (5832, 0.67), (12156, 0.91), (3891, 0.45), (8445, 0.73)]
        
        for i, (feature_id, activation) in enumerate(active_features):
            feature_text = Tex(rf"F{feature_id}: {activation:.2f}", font_size=9, color=ORANGE)
            feature_text.shift(UP * (i-2) * 0.4)
            sparse_features.add(feature_text)
        
        # Add inactive features representation
        inactive_text = Tex(r"\text{15,979 features: 0.00}", font_size=8, color=GRAY, fill_opacity=0.5)
        inactive_text.shift(DOWN * 1.5)
        
        sparse_group = VGroup(sparse_features, inactive_text)
        
        self.play(
            Transform(input_vector, sparse_group), 
            run_time=2
        )
        self.wait(1)
        
        # Flow through decoder - back to dense 768-D embeddings
        output_values = VGroup()
        output_sample = [0.21, -0.18, 0.89, -0.39, 0.58, -0.31, 0.22, 0.71]
        for i, val in enumerate(output_sample):
            val_text = Tex(f"{val:.2f}", font_size=10, color=BLUE)
            val_text.shift(RIGHT * 6 + UP * (i-3.5) * 0.3)
            output_values.add(val_text)
        
        output_bracket = Tex("[", font_size=40, color=BLUE).next_to(output_values, LEFT)
        output_bracket2 = Tex("]", font_size=40, color=BLUE).next_to(output_values, RIGHT)
        output_ellipsis = MathTex(r"\ldots", font_size=12, color=BLUE).next_to(output_values, DOWN)
        
        output_vector = VGroup(output_values, output_bracket, output_bracket2, output_ellipsis)
        
        self.play(input_vector.animate.shift(RIGHT * 4), run_time=1.5)
        self.play(
            Transform(input_vector, output_vector),
            run_time=1.5
        )
        self.wait(1)
        
        # Clean up data flow visualization
        self.play(FadeOut(input_vector))
        
    def demonstrate_sparsity(self):
        # Move components up to make room
        self.play(self.components.animate.shift(UP * 1.5))
        
        # Create comparison
        comparison_title = MathTex(r"\text{Dense Embeddings} \rightarrow \text{Sparse Features} \rightarrow \text{Dense Embeddings}", font_size=20, color=WHITE)
        comparison_title.shift(DOWN * 1.8)
        
        # Traditional MLP: dense in, dense out
        mlp_label = Tex(r"\text{Traditional MLP}", font_size=14, color=RED)
        mlp_label.shift(LEFT * 3 + DOWN * 2.8)
        
        # Show dense vector with many non-zero values
        mlp_vector = VGroup()
        mlp_values = [0.23, -0.15, 0.87, -0.42, 0.61, -0.33]
        for i, val in enumerate(mlp_values):
            val_text = Tex(f"{val:.1f}", font_size=8, color=RED)
            val_text.shift(LEFT * 3 + DOWN * 3.4 + RIGHT * (i-2.5) * 0.3)
            mlp_vector.add(val_text)
        
        # CLT: sparse feature activations
        clt_label = Tex(r"\text{CLT Features}", font_size=14, color=GREEN)
        clt_label.shift(RIGHT * 3 + DOWN * 2.8)
        
        # Show sparse activations with feature IDs
        clt_features = VGroup()
        sparse_features = [("F1247", 0.8), ("F5832", 0.0), ("F12156", 0.9), ("F3891", 0.0), ("F8445", 0.7), ("F9021", 0.0)]
        for i, (feature_id, val) in enumerate(sparse_features):
            color = ORANGE if val > 0 else GRAY
            opacity = 1.0 if val > 0 else 0.3
            val_text = Tex(f"{val:.1f}", font_size=8, color=color, fill_opacity=opacity)
            val_text.shift(RIGHT * 3 + DOWN * 3.4 + RIGHT * (i-2.5) * 0.3)
            clt_features.add(val_text)
        
        self.play(Write(comparison_title))
        self.play(
            Write(mlp_label),
            Write(clt_label),
            Create(mlp_vector),
            Create(clt_features)
        )
        self.wait(2)
        
        # Clean up
        self.play(
            FadeOut(comparison_title),
            FadeOut(mlp_label),
            FadeOut(clt_label),
            FadeOut(mlp_vector),
            FadeOut(clt_features)
        )
        
    def show_interpretability(self):
        # Show specific feature detection
        feature_title = Tex(r"\text{Interpretable Features}", font_size=22, color=PURPLE)
        feature_title.shift(DOWN * 2)
        
        # Examples of what sparse features detect
        examples = VGroup(
            Tex(r"\text{F1247: Math expressions}", font_size=12, color=YELLOW),
            Tex(r"\text{F5832: City names}", font_size=12, color=YELLOW),
            Tex(r"\text{F12156: Animals}", font_size=12, color=YELLOW),
            Tex(r"\text{F3891: Emotions}", font_size=12, color=YELLOW),
            Tex(r"\text{F8445: Code syntax}", font_size=12, color=YELLOW)
        )
        
        examples.arrange(DOWN, buff=0.2)
        examples.shift(DOWN * 3.2)
        
        self.play(Write(feature_title))
        self.play(Write(examples), run_time=2)
        self.wait(2)
        
        # Final cleanup
        self.play(
            FadeOut(feature_title),
            FadeOut(examples),
            self.components.animate.shift(DOWN * 1.5)
        )
        
        # End with the architecture
        self.wait(2)

# Alternative simpler version focusing on the core concept
class SimpleCLTDemo(Scene):
    def construct(self):
        # Title
        title = Tex(r"\text{Cross-Layer Transcoder Architecture}", font_size=36)
        title.to_edge(UP)
        
        # Create the flow diagram
        # Input
        input_rect = Rectangle(width=1.5, height=3, color=BLUE, fill_opacity=0.3)
        input_label = Tex(r"\text{Input}\\\text{768-D}", font_size=16).move_to(input_rect)
        input_group = VGroup(input_rect, input_label).shift(LEFT * 5)
        
        # Encoder
        encoder_rect = Rectangle(width=2, height=2, color=GREEN, fill_opacity=0.3)
        encoder_label = MathTex(r"\text{Encoder}\\W_e", font_size=16).move_to(encoder_rect)
        encoder_group = VGroup(encoder_rect, encoder_label).shift(LEFT * 2)
        
        # Sparse layer
        sparse_rect = Rectangle(width=2, height=1.5, color=ORANGE, fill_opacity=0.3)
        sparse_label = MathTex(r"\text{Sparse}\\k\text{-D}", font_size=16).move_to(sparse_rect)
        relu_label = Tex(r"\text{ReLU + L1}", font_size=12, color=RED).next_to(sparse_rect, UP)
        sparse_group = VGroup(sparse_rect, sparse_label).shift(ORIGIN)
        
        # Decoder
        decoder_rect = Rectangle(width=2, height=2, color=BLUE, fill_opacity=0.3)
        decoder_label = MathTex(r"\text{Decoder}\\W_d", font_size=16).move_to(decoder_rect)
        decoder_group = VGroup(decoder_rect, decoder_label).shift(RIGHT * 2)
        
        # Output
        output_rect = Rectangle(width=1.5, height=3, color=BLUE, fill_opacity=0.3)
        output_label = Tex(r"\text{Output}\\\text{768-D}", font_size=16).move_to(output_rect)
        output_group = VGroup(output_rect, output_label).shift(RIGHT * 5)
        
        # Arrows
        arrows = VGroup(
            Arrow(input_group.get_right(), encoder_group.get_left()),
            Arrow(encoder_group.get_right(), sparse_group.get_left()),
            Arrow(sparse_group.get_right(), decoder_group.get_left()),
            Arrow(decoder_group.get_right(), output_group.get_left())
        )
        
        # Animation sequence
        self.play(Write(title))
        self.wait(1)
        
        self.play(Create(input_group))
        self.play(Create(arrows[0]), Create(encoder_group))
        self.play(Create(arrows[1]), Create(sparse_group), Write(relu_label))
        self.play(Create(arrows[2]), Create(decoder_group))
        self.play(Create(arrows[3]), Create(output_group))
        
        self.wait(2)
        
        # Show the key insight
        insight = Tex(r"\text{Key: Sparse features are more interpretable}", 
                      font_size=20, color=YELLOW)
        insight.shift(DOWN * 3)
        
        self.play(Write(insight))
        self.wait(3)