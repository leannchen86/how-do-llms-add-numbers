from manim import *
import numpy as np

class TransformerArchitecture(Scene):
    def construct(self):
        # Title
        title = Text("Transformer Architecture", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # Create the main transformer block
        self.create_transformer_block()
        self.wait(1)
        
        # Animate attention mechanism
        self.animate_attention()
        self.wait(1)
        
        # Animate MLP block
        self.animate_mlp()
        self.wait(1)
        
        # Show data flow
        self.animate_data_flow()
        self.wait(2)

    def create_transformer_block(self):
        # Input embeddings
        self.input_box = Rectangle(width=3, height=0.8, color=GREEN, fill_opacity=0.3)
        input_text = Text("Input Embeddings\n+ Positional Encoding", font_size=14)
        input_group = VGroup(self.input_box, input_text)
        input_group.move_to(DOWN * 3)
        
        # Multi-Head Attention
        self.attention_box = Rectangle(width=4, height=1.2, color=BLUE, fill_opacity=0.3)
        attention_text = Text("Multi-Head\nSelf-Attention", font_size=16, color=WHITE)
        self.attention_group = VGroup(self.attention_box, attention_text)
        self.attention_group.move_to(DOWN * 1.5)
        
        # Add & Norm 1
        self.norm1_box = Rectangle(width=2.5, height=0.6, color=YELLOW, fill_opacity=0.3)
        norm1_text = Text("Add & Norm", font_size=12)
        norm1_group = VGroup(self.norm1_box, norm1_text)
        norm1_group.move_to(DOWN * 0.5)
        
        # Feed Forward (MLP)
        self.mlp_box = Rectangle(width=4, height=1.2, color=RED, fill_opacity=0.3)
        mlp_text = Text("Feed Forward\n(MLP)", font_size=16, color=WHITE)
        self.mlp_group = VGroup(self.mlp_box, mlp_text)
        self.mlp_group.move_to(UP * 0.5)
        
        # Add & Norm 2
        self.norm2_box = Rectangle(width=2.5, height=0.6, color=YELLOW, fill_opacity=0.3)
        norm2_text = Text("Add & Norm", font_size=12)
        norm2_group = VGroup(self.norm2_box, norm2_text)
        norm2_group.move_to(UP * 1.5)
        
        # Output
        self.output_box = Rectangle(width=3, height=0.8, color=PURPLE, fill_opacity=0.3)
        output_text = Text("Output", font_size=14)
        output_group = VGroup(self.output_box, output_text)
        output_group.move_to(UP * 2.5)
        
        # Arrows connecting components
        arrow1 = Arrow(input_group.get_top(), self.attention_group.get_bottom(), buff=0.1)
        arrow2 = Arrow(self.attention_group.get_top(), norm1_group.get_bottom(), buff=0.1)
        arrow3 = Arrow(norm1_group.get_top(), self.mlp_group.get_bottom(), buff=0.1)
        arrow4 = Arrow(self.mlp_group.get_top(), norm2_group.get_bottom(), buff=0.1)
        arrow5 = Arrow(norm2_group.get_top(), output_group.get_bottom(), buff=0.1)
        
        # Residual connections
        residual1 = CurvedArrow(
            input_group.get_right() + RIGHT * 0.5,
            norm1_group.get_right() + RIGHT * 0.5,
            color=ORANGE, angle=-PI/4
        )
        residual2 = CurvedArrow(
            norm1_group.get_right() + RIGHT * 0.5,
            norm2_group.get_right() + RIGHT * 0.5,
            color=ORANGE, angle=-PI/4
        )
        
        # Store all components
        self.transformer_components = VGroup(
            input_group, self.attention_group, norm1_group,
            self.mlp_group, norm2_group, output_group,
            arrow1, arrow2, arrow3, arrow4, arrow5,
            residual1, residual2
        )
        
        # Animate creation
        self.play(
            *[FadeIn(comp) for comp in [input_group, arrow1]],
            run_time=0.5
        )
        self.play(
            *[FadeIn(comp) for comp in [self.attention_group, arrow2]],
            run_time=0.5
        )
        self.play(
            *[FadeIn(comp) for comp in [norm1_group, arrow3, residual1]],
            run_time=0.5
        )
        self.play(
            *[FadeIn(comp) for comp in [self.mlp_group, arrow4]],
            run_time=0.5
        )
        self.play(
            *[FadeIn(comp) for comp in [norm2_group, arrow5, residual2]],
            run_time=0.5
        )
        self.play(FadeIn(output_group), run_time=0.5)

    def animate_attention(self):
        # Highlight attention block
        highlight = Rectangle(width=4.5, height=1.7, color=YELLOW, stroke_width=3)
        highlight.move_to(self.attention_group.get_center())
        
        self.play(Create(highlight))
        
        # Create detailed attention mechanism
        attention_detail = self.create_attention_detail()
        attention_detail.scale(0.7).next_to(self.attention_group, RIGHT, buff=1)
        
        self.play(FadeIn(attention_detail))
        self.wait(2)
        
        # Animate query, key, value computation
        self.animate_qkv_computation(attention_detail)
        self.wait(1)
        
        self.play(FadeOut(attention_detail), FadeOut(highlight))

    def create_attention_detail(self):
        # Input representation
        input_tokens = VGroup()
        for i in range(3):
            token = Circle(radius=0.2, color=GREEN, fill_opacity=0.7)
            token.shift(UP * 2 + RIGHT * (i - 1) * 0.8)
            input_tokens.add(token)
        
        # Q, K, V matrices
        q_matrix = Rectangle(width=0.6, height=1.5, color=BLUE, fill_opacity=0.5)
        q_matrix.shift(LEFT * 1.5 + UP * 0.5)
        q_label = Text("Q", font_size=12).next_to(q_matrix, DOWN)
        
        k_matrix = Rectangle(width=0.6, height=1.5, color=RED, fill_opacity=0.5)
        k_matrix.shift(UP * 0.5)
        k_label = Text("K", font_size=12).next_to(k_matrix, DOWN)
        
        v_matrix = Rectangle(width=0.6, height=1.5, color=PURPLE, fill_opacity=0.5)
        v_matrix.shift(RIGHT * 1.5 + UP * 0.5)
        v_label = Text("V", font_size=12).next_to(v_matrix, DOWN)
        
        # Attention scores
        attention_matrix = Rectangle(width=1.2, height=1.2, color=ORANGE, fill_opacity=0.5)
        attention_matrix.shift(DOWN * 1)
        attention_label = Text("Attention\nScores", font_size=10).next_to(attention_matrix, DOWN)
        
        # Output
        output_tokens = VGroup()
        for i in range(3):
            token = Circle(radius=0.2, color=YELLOW, fill_opacity=0.7)
            token.shift(DOWN * 2.5 + RIGHT * (i - 1) * 0.8)
            output_tokens.add(token)
        
        return VGroup(
            input_tokens, q_matrix, q_label, k_matrix, k_label,
            v_matrix, v_label, attention_matrix, attention_label, output_tokens
        )

    def animate_qkv_computation(self, attention_detail):
        # Get components
        input_tokens = attention_detail[0]
        q_matrix = attention_detail[1]
        k_matrix = attention_detail[3]
        v_matrix = attention_detail[5]
        attention_matrix = attention_detail[7]
        output_tokens = attention_detail[9]
        
        # Animate Q, K, V computation
        for token in input_tokens:
            for matrix in [q_matrix, k_matrix, v_matrix]:
                arrow = Arrow(token.get_center(), matrix.get_center(), buff=0.1, color=WHITE)
                self.play(Create(arrow), run_time=0.3)
                self.play(FadeOut(arrow), run_time=0.1)
        
        # Animate attention computation (Q @ K^T)
        qk_arrow = Arrow(q_matrix.get_bottom(), attention_matrix.get_left(), color=BLUE)
        kq_arrow = Arrow(k_matrix.get_bottom(), attention_matrix.get_top(), color=RED)
        self.play(Create(qk_arrow), Create(kq_arrow))
        self.wait(0.5)
        self.play(FadeOut(qk_arrow), FadeOut(kq_arrow))
        
        # Animate final output (Attention @ V)
        for i, output_token in enumerate(output_tokens):
            av_arrow = Arrow(attention_matrix.get_bottom(), output_token.get_center(), color=ORANGE)
            v_arrow = Arrow(v_matrix.get_bottom(), output_token.get_center(), color=PURPLE)
            self.play(Create(av_arrow), Create(v_arrow), run_time=0.3)
            self.play(FadeOut(av_arrow), FadeOut(v_arrow), run_time=0.1)

    def animate_mlp(self):
        # Highlight MLP block
        highlight = Rectangle(width=4.5, height=1.7, color=YELLOW, stroke_width=3)
        highlight.move_to(self.mlp_group.get_center())
        
        self.play(Create(highlight))
        
        # Create detailed MLP
        mlp_detail = self.create_mlp_detail()
        mlp_detail.scale(0.8).next_to(self.mlp_group, LEFT, buff=1)
        
        self.play(FadeIn(mlp_detail))
        self.wait(1)
        
        # Animate MLP computation
        self.animate_mlp_computation(mlp_detail)
        self.wait(1)
        
        self.play(FadeOut(mlp_detail), FadeOut(highlight))

    def create_mlp_detail(self):
        # Input layer
        input_layer = VGroup()
        for i in range(4):
            neuron = Circle(radius=0.15, color=GREEN, fill_opacity=0.7)
            neuron.shift(LEFT * 2 + UP * (1.5 - i * 1))
            input_layer.add(neuron)
        
        # Hidden layer (expanded)
        hidden_layer = VGroup()
        for i in range(6):
            neuron = Circle(radius=0.15, color=BLUE, fill_opacity=0.7)
            neuron.shift(UP * (2.5 - i * 1))
            hidden_layer.add(neuron)
        
        # Output layer
        output_layer = VGroup()
        for i in range(4):
            neuron = Circle(radius=0.15, color=RED, fill_opacity=0.7)
            neuron.shift(RIGHT * 2 + UP * (1.5 - i * 1))
            output_layer.add(neuron)
        
        # Connections
        connections = VGroup()
        for input_neuron in input_layer:
            for hidden_neuron in hidden_layer:
                line = Line(input_neuron.get_center(), hidden_neuron.get_center(), 
                          stroke_width=1, color=GRAY)
                connections.add(line)
        
        for hidden_neuron in hidden_layer:
            for output_neuron in output_layer:
                line = Line(hidden_neuron.get_center(), output_neuron.get_center(),
                          stroke_width=1, color=GRAY)
                connections.add(line)
        
        # Labels
        input_label = Text("Input", font_size=10).next_to(input_layer, DOWN)
        hidden_label = Text("Hidden\n(ReLU)", font_size=10).next_to(hidden_layer, DOWN)
        output_label = Text("Output", font_size=10).next_to(output_layer, DOWN)
        
        return VGroup(connections, input_layer, hidden_layer, output_layer,
                     input_label, hidden_label, output_label)

    def animate_mlp_computation(self, mlp_detail):
        input_layer = mlp_detail[1]
        hidden_layer = mlp_detail[2]
        output_layer = mlp_detail[3]
        
        # Animate forward pass
        # Input to hidden
        for input_neuron in input_layer:
            self.play(input_neuron.animate.set_color(YELLOW), run_time=0.2)
        
        for hidden_neuron in hidden_layer:
            self.play(hidden_neuron.animate.set_color(YELLOW), run_time=0.1)
        
        # Hidden to output
        for output_neuron in output_layer:
            self.play(output_neuron.animate.set_color(YELLOW), run_time=0.1)
        
        # Reset colors
        self.play(
            *[neuron.animate.set_color(GREEN) for neuron in input_layer],
            *[neuron.animate.set_color(BLUE) for neuron in hidden_layer],
            *[neuron.animate.set_color(RED) for neuron in output_layer],
            run_time=0.5
        )

    def animate_data_flow(self):
        # Create data flow particles
        particles = VGroup()
        for i in range(5):
            particle = Dot(radius=0.05, color=YELLOW)
            particle.move_to(self.transformer_components[0].get_top() + LEFT * (i - 2) * 0.3)
            particles.add(particle)
        
        self.play(FadeIn(particles))
        
        # Animate particles flowing through the transformer
        path_points = [
            self.transformer_components[0].get_top(),  # Input
            self.attention_group.get_center(),         # Attention
            self.transformer_components[2].get_center(),  # Norm1
            self.mlp_group.get_center(),              # MLP
            self.transformer_components[4].get_center(),  # Norm2
            self.transformer_components[5].get_center()   # Output
        ]
        
        for i in range(len(path_points) - 1):
            self.play(
                *[particle.animate.move_to(path_points[i + 1] + LEFT * (j - 2) * 0.1) 
                  for j, particle in enumerate(particles)],
                run_time=0.8
            )
            self.wait(0.3)
        
        self.play(FadeOut(particles))
        
        # Add final explanation
        explanation = Text(
            "Transformer Block: Attention → Add&Norm → MLP → Add&Norm",
            font_size=20, color=WHITE
        ).to_edge(DOWN)
        
        self.play(Write(explanation))
        self.wait(2)
        self.play(FadeOut(explanation))

# Additional scene for detailed attention visualization
class AttentionMechanism(Scene):
    def construct(self):
        title = Text("Multi-Head Self-Attention", font_size=32, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create attention heads
        self.create_attention_heads()
        self.wait(1)
        
        # Show attention patterns
        self.show_attention_patterns()
        self.wait(2)

    def create_attention_heads(self):
        # Input sequence
        input_text = Text("Input: 'The cat sat on the mat'", font_size=16)
        input_text.to_edge(LEFT + UP * 2)
        self.play(Write(input_text))
        
        # Multiple attention heads
        heads = VGroup()
        colors = [RED, BLUE, GREEN, ORANGE]
        
        for i, color in enumerate(colors):
            head = Rectangle(width=1.5, height=2, color=color, fill_opacity=0.3)
            head.shift(DOWN * 1 + RIGHT * (i - 1.5) * 2)
            head_label = Text(f"Head {i+1}", font_size=12).next_to(head, UP)
            heads.add(VGroup(head, head_label))
        
        self.play(*[FadeIn(head) for head in heads])
        self.heads = heads

    def show_attention_patterns(self):
        # Show different attention patterns for each head
        tokens = ["The", "cat", "sat", "on", "the", "mat"]
        
        for i, head_group in enumerate(self.heads):
            head = head_group[0]
            
            # Create attention pattern visualization
            pattern = self.create_attention_pattern(tokens, i)
            pattern.scale(0.5).next_to(head, DOWN)
            
            self.play(FadeIn(pattern))
            self.wait(0.5)
        
        self.wait(1)

    def create_attention_pattern(self, tokens, head_idx):
        # Different patterns for different heads
        patterns = [
            # Head 1: Focus on subject-verb relationships
            [[0.8, 0.1, 0.1, 0.0, 0.0, 0.0],  # The
             [0.2, 0.6, 0.2, 0.0, 0.0, 0.0],  # cat
             [0.1, 0.7, 0.2, 0.0, 0.0, 0.0],  # sat
             [0.0, 0.1, 0.1, 0.5, 0.2, 0.1],  # on
             [0.0, 0.0, 0.0, 0.2, 0.6, 0.2],  # the
             [0.0, 0.0, 0.0, 0.1, 0.3, 0.6]], # mat
            # Head 2: Focus on determiners
            [[0.5, 0.0, 0.0, 0.0, 0.5, 0.0],
             [0.0, 0.8, 0.0, 0.0, 0.0, 0.2],
             [0.0, 0.0, 0.9, 0.1, 0.0, 0.0],
             [0.0, 0.0, 0.0, 0.8, 0.2, 0.0],
             [0.4, 0.0, 0.0, 0.0, 0.6, 0.0],
             [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]],
            # Add more patterns...
        ]
        
        if head_idx < len(patterns):
            attention_matrix = patterns[head_idx]
        else:
            # Default pattern
            attention_matrix = np.random.rand(6, 6)
            attention_matrix = attention_matrix / attention_matrix.sum(axis=1, keepdims=True)
        
        # Create visual representation
        grid = VGroup()
        for i in range(6):
            for j in range(6):
                intensity = attention_matrix[i][j]
                cell = Rectangle(width=0.3, height=0.3, 
                               fill_opacity=intensity, 
                               fill_color=YELLOW,
                               stroke_width=1)
                cell.shift(RIGHT * j * 0.3 + DOWN * i * 0.3)
                grid.add(cell)
        
        return grid

if __name__ == "__main__":
    # To render: manim -pql transformer_animation.py TransformerArchitecture
    pass