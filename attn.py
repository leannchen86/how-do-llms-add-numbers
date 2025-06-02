from manim import *
import numpy as np

class SelfAttentionAnimation(Scene):
    def construct(self):
        # Title
        title = Tex(r"\text{Self-Attention Mechanism}", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        
        # Step 1: Tokens
        self.animate_tokenization()
        self.wait(2)
        
        # Step 2: Transform to Q, K, V vectors with descriptive labels
        self.animate_qkv_transformation()
        self.wait(2)
        
        # NEW STEP: Show attention formula and highlight Q·K^T
        self.show_attention_formula_and_highlight()
        self.wait(3)
        
        # Step 3: Show individual vectors, then transform to matrices
        self.animate_individual_to_matrix_transformation()
        self.wait(3)

    def show_attention_formula_and_highlight(self):
        """Fallback approach using Tex/MathTex objects to avoid Pango issues"""
        
        # Create the formula using MathTex for proper math rendering
        formula_text = MathTex(
            r"\mathrm{Attention}(Q,\,K,\,V) \;=\; \mathrm{Softmax}\!\Bigl(\tfrac{Q \cdot K^T}{\sqrt{d_k}}\Bigr)\,V",
            font_size=36
        )
        formula_text.move_to(ORIGIN)
        
        # Create highlighted Q·K^T with MathTex
        highlighted_qkt = MathTex(r"Q \cdot K^T", font_size=36, color=YELLOW)
        # Position it approximately where it appears in the formula, moved lower
        highlighted_qkt.move_to(formula_text.get_center() + LEFT * 0.5 + DOWN * 0.8)
        
        # Show the complete formula first
        self.play(Write(formula_text))
        self.wait(1.5)
        
        # Add the highlighted version on top
        self.play(Write(highlighted_qkt))
        self.wait(1)
        
        # Scale up the highlighted part
        self.play(
            highlighted_qkt.animate.scale(1.8),
            run_time=2
        )
        self.wait(2)
        
        # Add explanatory text using Tex
        explanation = Tex(r"We'll focus on computing $Q \cdot K^T$ first", font_size=24, color=WHITE)
        explanation.next_to(formula_text, DOWN, buff=1)
        self.play(Write(explanation))
        self.wait(1.5)
        
        # Fade out everything
        self.play(
            FadeOut(formula_text),
            FadeOut(highlighted_qkt),
            FadeOut(explanation),
        )

    def animate_tokenization(self):
        """Animate the tokenization step exactly as written"""
        # Create tokens exactly as in notes, using Tex for consistency
        token_text = Tex(r"\text{Tokens:}", font_size=32).move_to(UP * 2.5 + LEFT * 5)
        self.play(Write(token_text))
        
        # The exact tokens from the notes with proper quotes
        self.tokens = VGroup(
            Tex(r'"26"', font_size=28),
            Tex(r'"+"', font_size=28),
            Tex(r'"55"', font_size=28),
            Tex(r'"="', font_size=28)
        ).arrange(RIGHT, buff=1.5).next_to(token_text, RIGHT, buff=1)
        
        self.play(Write(self.tokens))
        
        # Initialize groups that will be used later
        self.arrow_groups = VGroup()
        self.qkv_groups = VGroup()  # Initialize qkv_groups
        
        self.token_text = token_text

    def animate_qkv_transformation(self):
        """Use ReplacementTransform with descriptive token-specific labels"""
        # Create Q, K, V representations for each token with descriptive subscripts
        token_labels = ["26", "+", "55", "="]
        
        # Process each token individually
        for i, (token, label) in enumerate(zip(self.tokens, token_labels)):
            # Create 3 arrows for this token - one for Q, one for K, one for V
            arrow_q = Arrow(
                start=token.get_bottom() + LEFT * 0.4, 
                end=token.get_bottom() + LEFT * 0.4 + DOWN * 1.2, 
                stroke_width=3, max_tip_length_to_length_ratio=0.2, color=BLUE
            )
            arrow_k = Arrow(
                start=token.get_bottom(), 
                end=token.get_bottom() + DOWN * 1.2, 
                stroke_width=3, max_tip_length_to_length_ratio=0.2, color=RED
            )
            arrow_v = Arrow(
                start=token.get_bottom() + RIGHT * 0.4, 
                end=token.get_bottom() + RIGHT * 0.4 + DOWN * 1.2, 
                stroke_width=3, max_tip_length_to_length_ratio=0.2, color=GREEN
            )
            
            token_arrows = VGroup(arrow_q, arrow_k, arrow_v)
            self.arrow_groups.add(token_arrows)
            
            # Show the arrows
            self.play(Create(token_arrows), run_time=0.5)
            
            # Position Q, K, V at the end of their respective arrows
            q_pos = arrow_q.get_end() + DOWN * 0.3
            k_pos = arrow_k.get_end() + DOWN * 0.3
            v_pos = arrow_v.get_end() + DOWN * 0.3
            
            # Create Q, K, V vectors with proper mathematical subscripts
            q_vec = MathTex(f"Q_{{{label}}}", font_size=24, color=BLUE).move_to(q_pos)
            k_vec = MathTex(f"K_{{{label}}}", font_size=24, color=RED).move_to(k_pos)
            v_vec = MathTex(f"V_{{{label}}}", font_size=24, color=GREEN).move_to(v_pos)
            
            token_qkv = VGroup(q_vec, k_vec, v_vec)
            self.qkv_groups.add(token_qkv)
            
            # Create copy of this token for transformation effect
            token_copy = token.copy()
            
            # Transform this token to QKV and fade the original
            self.play(
                token.animate.set_opacity(0.3),
                ReplacementTransform(token_copy, token_qkv),
                run_time=0.7
            )

    def animate_individual_to_matrix_transformation(self):
        """Show individual Q and K^T vectors, then transform to matrices"""
        # Clear previous content except title
        self.play(
            FadeOut(self.token_text),
            FadeOut(self.arrow_groups),
            FadeOut(self.tokens),
            FadeOut(self.qkv_groups)
        )
        
        # Step 1: Show individual Q vectors (positioned down)
        self.show_individual_q_vectors()
        self.wait(2)
        
        # Step 2: Show individual K^T vectors (positioned up)
        self.show_individual_kt_vectors()
        self.wait(2)
        
        # Step 3: Transform individual vectors to matrices
        self.transform_vectors_to_matrices()
        self.wait(2)
        
        # Step 4: Show the multiplication process
        self.animate_matrix_multiplication()

    def show_individual_q_vectors(self):
        """Show individual Q vectors as horizontal row vectors positioned where Q matrix will be"""
        token_labels = ["26", "+", "55", "="]
        
        # Create individual Q vectors with 3D toy values (as row vectors)
        self.q_vectors = VGroup()
        q_values = [
            [0.2, 0.8, 0.1],  # Q_26
            [0.9, 0.1, 0.3],  # Q_+
            [0.4, 0.6, 0.9],  # Q_55
            [0.1, 0.3, 0.7]   # Q_=
        ]
        
        # Position down and to the left where the Q matrix will be
        start_pos = LEFT * 4 + DOWN * 0.3
        
        for i, (label, values) in enumerate(zip(token_labels, q_values)):
            # Create horizontal row vector with brackets, using Tex for numbers
            vector_entries = [f"{val:.1f}" for val in values]
            vector_matrix = Matrix(
                [vector_entries], 
                element_to_mobject=lambda x: Tex(x, font_size=32),
                h_buff=0.7
            )
            vector_matrix.set_color(BLUE)
            
            # Position each row vector vertically stacked (like matrix rows)
            vector_matrix.move_to(start_pos + DOWN * i * 0.8)
            
            # Add subscript label to the left
            label_text = MathTex(f"Q_{{{label}}}", font_size=20, color=BLUE)
            label_text.next_to(vector_matrix, LEFT, buff=0.3)
            
            vector_group = VGroup(vector_matrix, label_text)
            self.q_vectors.add(vector_group)
        
        # Add Q vectors title
        q_title = Tex(r"\text{Individual Q Vectors:}", font_size=24, color=BLUE)
        q_title.next_to(self.q_vectors, UP, buff=0.5)
        
        self.play(Write(q_title), Create(self.q_vectors))
        self.q_title = q_title

    def show_individual_kt_vectors(self):
        """Show individual K vectors as column vectors positioned where K^T matrix will be"""
        token_labels = ["26", "+", "55", "="]
        
        # Create individual K vectors (which will become columns in K^T)
        self.kt_vectors = VGroup()
        k_values = [
            [0.3, 0.7, 0.2],  # K_26
            [0.8, 0.2, 0.4],  # K_+
            [0.1, 0.9, 0.6],  # K_55
            [0.5, 0.3, 0.8]   # K_=
        ]
        
        # Position up and to the right where the K^T matrix will be
        start_pos = RIGHT * 0.2 + UP * 1.9
        
        for i, (label, values) in enumerate(zip(token_labels, k_values)):
            # Create vertical column vector with brackets, using Tex for numbers
            vector_entries = [f"{val:.1f}" for val in values]
            vector_matrix = Matrix(
                [[entry] for entry in vector_entries], 
                element_to_mobject=lambda x: Tex(x, font_size=32)
            )
            vector_matrix.set_color(RED)
            
            # Scale down just the brackets to keep them smaller
            brackets = vector_matrix.get_brackets()
            brackets.scale([0.5, 1.0, 1])  # Scale: [x_scale, y_scale, z_scale] - narrower but taller
            
            # Position each column vector horizontally side by side (like matrix columns)
            vector_matrix.move_to(start_pos + RIGHT * i * 1.2)
            
            # Add subscript label below
            label_text = MathTex(r"K^T_{" + label + r"}", font_size=20, color=RED)
            label_text.next_to(vector_matrix, DOWN, buff=0.2)
            
            vector_group = VGroup(vector_matrix, label_text)
            self.kt_vectors.add(vector_group)
        
        # Add K vectors title
        kt_title = Tex(r"\text{Individual K Vectors:}", font_size=24, color=RED)
        kt_title.next_to(self.kt_vectors, UP, buff=0.3)
        
        self.play(Write(kt_title), Create(self.kt_vectors))
        self.kt_title = kt_title

    def transform_vectors_to_matrices(self):
        """Transform individual vectors into matrix form - brackets merge, labels stay"""
        
        # Only fade out the titles (keep individual labels like Q_26, K_26)
        self.play(
            FadeOut(self.q_title),
            FadeOut(self.kt_title),
        )
        
        # For Q matrix: get bounding box of ALL Q vector content INCLUDING labels
        q_left = self.q_vectors.get_left()[0] - 0.3  # Include extra padding for labels
        q_right = self.q_vectors.get_right()[0] + 0.2
        q_top = self.q_vectors.get_top()[1] + 0.1
        q_bottom = self.q_vectors.get_bottom()[1] - 0.1
        q_center_y = (q_top + q_bottom) / 2
        
        # Create Q matrix brackets that properly encompass all Q vectors INCLUDING labels
        q_bracket_left = MathTex(r"[", font_size=250, color=BLUE)
        q_bracket_right = MathTex(r"]", font_size=250, color=BLUE)
        q_bracket_left.move_to([q_left, q_center_y, 0])
        q_bracket_right.move_to([q_right, q_center_y, 0])
        q_matrix_brackets = VGroup(q_bracket_left, q_bracket_right)
        
        # For K^T matrix: get bounding box of all K^T vectors INCLUDING labels
        kt_left = self.kt_vectors.get_left()[0] - 0.2
        kt_right = self.kt_vectors.get_right()[0] + 0.2
        kt_top = self.kt_vectors.get_top()[1] + 0.1
        kt_bottom = self.kt_vectors.get_bottom()[1] - 0.3  # Include extra padding for labels below
        kt_center_y = (kt_top + kt_bottom) / 2
        
        # Create K^T matrix brackets that properly encompass all K^T vectors
        kt_bracket_left = MathTex(r"[", font_size=150, color=RED)
        kt_bracket_right = MathTex(r"]", font_size=150, color=RED)
        kt_bracket_left.move_to([kt_left, kt_center_y, 0])
        kt_bracket_right.move_to([kt_right, kt_center_y, 0])
        kt_matrix_brackets = VGroup(kt_bracket_left, kt_bracket_right)
        
        # Collect all individual brackets for transformation
        individual_brackets_q = VGroup()
        individual_brackets_k = VGroup()
        
        for q_vector_group in self.q_vectors:
            individual_brackets_q.add(q_vector_group[0].get_brackets())
            
        for k_vector_group in self.kt_vectors:
            individual_brackets_k.add(k_vector_group[0].get_brackets())
        
        # Add matrix labels - position Q label further left to avoid overlap
        q_matrix_label = MathTex(r"Q", font_size=32, color=BLUE)
        q_matrix_label.move_to([q_left - 0.8, q_center_y, 0])  # Moved further left
        
        kt_matrix_label = MathTex(r"K^T", font_size=32, color=RED)
        kt_matrix_label.move_to([(kt_right + kt_left) / 2, kt_top + 0.4, 0])
        
        # Transform: individual brackets merge into large brackets
        self.play(
            # Transform small brackets into large brackets
            Transform(individual_brackets_q, q_matrix_brackets),
            Transform(individual_brackets_k, kt_matrix_brackets),
            # Add matrix labels
            Write(q_matrix_label),
            Write(kt_matrix_label),
        )
        
        # Store references for next steps
        self.q_matrix_brackets = q_matrix_brackets
        self.kt_matrix_brackets = kt_matrix_brackets
        self.q_matrix_label = q_matrix_label
        self.kt_matrix_label = kt_matrix_label

    def animate_matrix_multiplication(self):
        """Show the Q·K^T multiplication process with proper positioning"""
        # Add multiplication symbol positioned between Q and K^T matrices
        mult_symbol = MathTex(r"\times", font_size=48, color=WHITE)
        mult_symbol.move_to(LEFT * 0.1 + UP * 0.15)  # Between the matrices
        self.play(Write(mult_symbol))
        
        # Create attention matrix result positioned in the middle
        attention_matrix = self.create_attention_matrix_result()
        
        # Show a few key computations with curved arrows
        self.show_key_computations()

    def create_attention_matrix_result(self):
        """Create the resulting attention matrix positioned in the center"""
        # Calculate actual results from our toy values (Q·K^T)
        attention_entries = [
            ["0.83", "0.32", "0.71", "0.42"],  # Q_26 · [K^T columns]
            ["0.36", "0.85", "0.45", "0.69"],  # Q_+ · [K^T columns]
            ["0.66", "0.58", "0.87", "0.92"],  # Q_55 · [K^T columns]
            ["0.44", "0.34", "0.69", "0.65"]   # Q_= · [K^T columns]
        ]
        
        attention_matrix = Matrix(
            attention_entries,
            element_to_mobject=lambda x: Tex(x, font_size=32, color=WHITE)
        )
        q_vertical_center = self.q_vectors.get_center()[1]  # Y coordinate of Q matrix center
        kt_horizontal_center = self.kt_vectors.get_center()[0]  # X coordinate of K^T matrix center
        attention_matrix.move_to([kt_horizontal_center, q_vertical_center, 0])
        
        # Add labels using Tex
        result_label = Tex(r"\text{Attention Scores}", font_size=18, color=ORANGE)
        result_label.next_to(attention_matrix, UP, buff=0.3)
        
        self.play(
            Create(attention_matrix),
            Write(result_label),
        )
        
        return attention_matrix

    def show_key_computations(self):
        """Show a few key dot product computations"""
        # Show how Q_26 · K^T_26 produces the first attention score
        comp_text = MathTex(
            r"Q_{26} \cdot K^T_{26} \;=\; [0.2,\,0.8,\,0.1] \cdot [0.3,\,0.7,\,0.2] \;=\; 0.83",
            font_size=16, color=YELLOW
        )
        comp_text.move_to(DOWN * 3.5)  # Below everything
        
        self.play(Write(comp_text))
        self.wait(2)
        
        # Highlight the concept with Tex
        final_note = Tex(r"Each cell shows how much one token 'attends' to another", font_size=16, color=GREEN)
        final_note.move_to(DOWN * 4.2)
        self.play(Write(final_note))
        self.wait(1.5)
