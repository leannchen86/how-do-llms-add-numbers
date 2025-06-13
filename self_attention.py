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

        # Step 4: Add attention matrix
        self.add_attention_matrix()
        self.wait(3)

    # ------------------------------------------------------------------
    # Positional-encoding explanation
    # ------------------------------------------------------------------
    def show_positional_encoding(self):
        """Show token-specific positional encoding examples"""
        pe_title = Tex(r"\text{Positional Encoding}", font_size=28, color=YELLOW)
        pe_title.move_to(UP * 2.0)
        self.play(Write(pe_title))
        self.wait(1)

        transformations = VGroup(
            MathTex(r"\text{‘26’} \rightarrow \mathbf{e}_{26} + \mathbf{p}_1 = \mathbf{x}_1", font_size=26),
            MathTex(r"\text{‘+’} \rightarrow \mathbf{e}_{+} + \mathbf{p}_2 = \mathbf{x}_2", font_size=26),
            MathTex(r"\text{‘55’} \rightarrow \mathbf{e}_{55} + \mathbf{p}_3 = \mathbf{x}_3", font_size=26),
            MathTex(r"\text{‘=’} \rightarrow \mathbf{e}_{=} + \mathbf{p}_4 = \mathbf{x}_4", font_size=26)
        )
        transformations.arrange(DOWN, buff=0.6).move_to(ORIGIN)

        self.play(Write(transformations), run_time=1)
        self.wait(0.4)

        self.play(Transform(self.tokens, self.x_symbols), run_time=1.2)
        self.wait(0.5)
        self.play(FadeOut(pe_title), FadeOut(transformations))
        self.wait(0.5)

    # ------------------------------------------------------------------
    # Tokenisation (now ending with x_i labels)
    # ------------------------------------------------------------------
    def animate_tokenization(self):
        token_text = Tex(r"\text{Tokens:}", font_size=32).move_to(UP * 2.5 + LEFT * 5)
        self.play(Write(token_text))

        # Original literal tokens
        self.tokens = VGroup(
            Tex(r"‘26’", font_size=28),
            Tex(r"‘+’", font_size=28),
            Tex(r"‘55’", font_size=28),
            Tex(r"‘=’", font_size=28)
        ).arrange(RIGHT, buff=1.5).next_to(token_text, RIGHT, buff=1)
        self.play(Write(self.tokens))

        # Transform literal tokens into positional-encoded vector symbols x_i
        x_symbols = VGroup(
            MathTex(r"\mathbf{x}_1", font_size=28),
            MathTex(r"\mathbf{x}_2", font_size=28),
            MathTex(r"\mathbf{x}_3", font_size=28),
            MathTex(r"\mathbf{x}_4", font_size=28)
        )
        for orig, new in zip(self.tokens, x_symbols):
            new.move_to(orig.get_center())

        # Store x_symbols on self so that animate_qkv_transformation can access it
        self.x_symbols = x_symbols

        self.show_positional_encoding()
        self.arrow_groups = VGroup()
        self.qkv_groups = VGroup()
        self.token_text = token_text

    # ------------------------------------------------------------------
    # Q-K-V projection (using token-specific labels) with wider arrow spacing
    # and W_ labels at arrow midpoints
    # ------------------------------------------------------------------
    def animate_qkv_transformation(self):
        token_labels = ['26', '+', '55', '=']

        for i, symbol in enumerate(self.x_symbols):
            # Wider arrow spacing: use 0.6 instead of 0.4
            arrow_q = Arrow(
                symbol.get_bottom() + LEFT * 0.6,
                symbol.get_bottom() + LEFT * 0.6 + DOWN * 1.2,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.2,
                color=BLUE,
            )
            arrow_k = Arrow(
                symbol.get_bottom(),
                symbol.get_bottom() + DOWN * 1.2,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.2,
                color=RED,
            )
            arrow_v = Arrow(
                symbol.get_bottom() + RIGHT * 0.6,
                symbol.get_bottom() + RIGHT * 0.6 + DOWN * 1.2,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.2,
                color=GREEN,
            )

            token_arrows = VGroup(arrow_q, arrow_k, arrow_v)
            self.arrow_groups.add(token_arrows)

            # Create W labels at the midpoint of each arrow
            wq_label = MathTex(r"W_Q", font_size=24, color=BLUE)
            wq_label.move_to(arrow_q.get_center())
            wk_label = MathTex(r"W_K", font_size=24, color=RED)
            wk_label.move_to(arrow_k.get_center())
            wv_label = MathTex(r"W_V", font_size=24, color=GREEN)
            wv_label.move_to(arrow_v.get_center())

            # Play arrows growing and W_* labels appearing at the midpoints
            self.play(
                Create(token_arrows),
                Write(wq_label),
                Write(wk_label),
                Write(wv_label),
                run_time=0.8
            )

            # Position Q, K, V at the end of their respective arrows
            q_pos = arrow_q.get_end() + DOWN * 0.3
            k_pos = arrow_k.get_end() + DOWN * 0.3
            v_pos = arrow_v.get_end() + DOWN * 0.3

            # Define resulting Q_label, K_label, V_label symbols using token_labels
            label = token_labels[i]
            q_vec = MathTex(f"q_{{{label}}}", font_size=24, color=BLUE).move_to(q_pos)
            k_vec = MathTex(f"k_{{{label}}}", font_size=24, color=RED).move_to(k_pos)
            v_vec = MathTex(f"v_{{{label}}}", font_size=24, color=GREEN).move_to(v_pos)

            # Store final Q/K/V symbols for later fade/transform
            token_qkv = VGroup(q_vec, k_vec, v_vec)
            self.qkv_groups.add(token_qkv)

            # Transform W_* labels into corresponding Q, K, V labels, while fading the original x_i symbol
            self.play(
                symbol.animate.set_opacity(0.3),
                ReplacementTransform(wq_label, q_vec),
                ReplacementTransform(wk_label, k_vec),
                ReplacementTransform(wv_label, v_vec),
                run_time=0.7
            )

    # ------------------------------------------------------------------
    # Attention-formula highlight
    # ------------------------------------------------------------------
    def show_attention_formula_and_highlight(self):
        formula_text = MathTex(r"\mathrm{Attention}(Q,\,K,\,V) = \mathrm{Softmax}\Bigl(\tfrac{Q K^\top}{\sqrt{d_k}}\Bigr) V", font_size=36)
        formula_text.move_to(ORIGIN)
        highlighted_qkt = MathTex(r"Q K^\top", font_size=36, color=YELLOW)
        highlighted_qkt.move_to(formula_text.get_center() + DOWN * 0.8)

        self.play(Write(formula_text))
        self.wait(1.5)
        self.play(Write(highlighted_qkt))
        self.wait(1)
        self.play(highlighted_qkt.animate.scale(1.8), run_time=2)
        self.wait(2)

        explanation = Tex(r"We'll focus on computing $Q K^\top$ first", font_size=24)
        explanation.next_to(formula_text, DOWN, buff=1)
        self.play(Write(explanation))
        self.wait(1.5)

        self.play(FadeOut(formula_text), FadeOut(highlighted_qkt), FadeOut(explanation))

    # ------------------------------------------------------------------
    # Individual vectors → matrices (Q and K^T)
    # ------------------------------------------------------------------
    def animate_individual_to_matrix_transformation(self):
        self.play(FadeOut(self.token_text), FadeOut(self.arrow_groups), FadeOut(self.x_symbols),
                  FadeOut(self.tokens), FadeOut(self.qkv_groups))
        self.show_individual_q_vectors()
        self.wait(2)
        self.show_individual_kt_vectors()
        self.wait(2)
        self.transform_vectors_to_matrices()
        self.wait(2)

    def show_individual_q_vectors(self):
        """Show individual Q vectors as horizontal row vectors positioned where Q matrix will be"""
        token_labels = ['26', '+', '55', '=']

        # Create individual Q vectors with 3D toy values (as row vectors)
        self.q_vectors = VGroup()
        q_values = [
            [0.2, 0.8, 0.1],  # q_26
            [0.9, 0.1, 0.3],  # q_+
            [0.4, 0.6, 0.9],  # q_55
            [0.1, 0.3, 0.7]   # q_=
        ]

        # Position down and to the left where the Q matrix will be
        start_pos = LEFT * 3.2 + DOWN * 0.3

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
            label_text = MathTex(f"q_{{{label}}}", font_size=20, color=BLUE)
            label_text.next_to(vector_matrix, LEFT, buff=0.3)

            vector_group = VGroup(vector_matrix, label_text)
            self.q_vectors.add(vector_group)

        # Add Q vectors title
        q_title = Tex(r"\text{Individual Query Vectors:}", font_size=22, color=BLUE)
        q_title.next_to(self.q_vectors, UP, buff=0.5)

        self.play(Write(q_title), Create(self.q_vectors))
        self.q_title = q_title

    def show_individual_kt_vectors(self):
        """Show individual K vectors as column vectors positioned where K^T matrix will be"""
        token_labels = ['26', '+', '55', '=']

        # Create individual K vectors (which will become columns in K^T)
        self.kt_vectors = VGroup()
        k_values = [
            [0.3, 0.7, 0.2],  # k_26
            [0.8, 0.2, 0.4],  # k_+
            [0.1, 0.9, 0.6],  # k_55
            [0.5, 0.3, 0.8]   # k_=
        ]

        # Position up and to the left where the K^T matrix will be
        start_pos = LEFT * 1.0 + UP * 1.9

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
            brackets.scale([0.5, 1.0, 1])  # Scale: [x_scale, y_scale, z_scale]

            # Position each column vector horizontally side by side (like matrix columns)
            vector_matrix.move_to(start_pos + RIGHT * i * 0.9)

            # Add subscript label below
            label_text = MathTex(r"(k_{" + label + r"})^\top", font_size=20, color=RED)
            label_text.next_to(vector_matrix, DOWN, buff=0.2)

            vector_group = VGroup(vector_matrix, label_text)
            self.kt_vectors.add(vector_group)

        # Add K vectors title
        kt_title = Tex(r"\text{Individual Key Vectors:}", font_size=22, color=RED)
        kt_title.next_to(self.kt_vectors, UP, buff=0.3)

        self.play(Write(kt_title), Create(self.kt_vectors))
        self.kt_title = kt_title

    def transform_vectors_to_matrices(self):
        """Cross fade individual vectors into matrix form - numbers stay in same positions"""
        self.play(
            FadeOut(self.q_title),
            FadeOut(self.kt_title),
        )

        # Extract exact coordinates from existing Q vectors
        q_number_positions = []  # Will store positions of each number
        q_label_positions = []   # Will store positions of each label

        for q_vector_group in self.q_vectors:
            vector_matrix = q_vector_group[0]  # The Matrix object
            label = q_vector_group[1]          # The label (Q_26, etc.)

            # Get positions of individual numbers in this vector
            entries = vector_matrix.get_entries()
            row_positions = [entry.get_center() for entry in entries]
            q_number_positions.append(row_positions)

            # Get position of the label
            q_label_positions.append(label.get_center())

        # Extract exact coordinates from existing K^T vectors
        kt_number_positions = []  # Will store positions of each number
        kt_label_positions = []   # Will store positions of each label

        for kt_vector_group in self.kt_vectors:
            vector_matrix = kt_vector_group[0]  # The Matrix object
            label = kt_vector_group[1]          # The label (K^T_26, etc.)

            # Get positions of individual numbers in this vector
            entries = vector_matrix.get_entries()
            col_positions = [entry.get_center() for entry in entries]
            kt_number_positions.append(col_positions)

            # Get position of the label
            kt_label_positions.append(label.get_center())

        # Get the same values used in individual vectors
        q_values = [
            [0.2, 0.8, 0.1],  # q_26
            [0.9, 0.1, 0.3],  # q_+
            [0.4, 0.6, 0.9],  # q_55
            [0.1, 0.3, 0.7]   # q_=
        ]

        k_values = [
            [0.3, 0.7, 0.2],  # k_26
            [0.8, 0.2, 0.4],  # k_+
            [0.1, 0.9, 0.6],  # k_55
            [0.5, 0.3, 0.8]   # k_=
        ]

        # Create Q matrix numbers at exact existing positions
        q_matrix_numbers = VGroup()
        for i, row_values in enumerate(q_values):
            for j, val in enumerate(row_values):
                number = Tex(f"{val:.1f}", font_size=32, color=BLUE)
                number.move_to(q_number_positions[i][j])  # Exact position from existing vector
                q_matrix_numbers.add(number)

        # Create Q matrix brackets to encompass all numbers
        q_all_positions = [pos for row in q_number_positions for pos in row]
        q_left = min(pos[0] for pos in q_all_positions) - 0.5  # Increased padding
        q_right = max(pos[0] for pos in q_all_positions) + 0.5
        q_top = max(pos[1] for pos in q_all_positions) + 0.4
        q_bottom = min(pos[1] for pos in q_all_positions) - 0.4

        brace_width = 0.3
        stroke_width = 4
        overlap = 0.02

        # Left Q bracket
        q_left_vertical = Line(
            start=[q_left, q_top + overlap, 0],
            end=[q_left, q_bottom - overlap, 0],
            stroke_width=stroke_width,
            color=BLUE
        )
        q_left_top = Line(
            start=[q_left - overlap, q_top, 0],
            end=[q_left + brace_width, q_top, 0],
            stroke_width=stroke_width,
            color=BLUE
        )
        q_left_bottom = Line(
            start=[q_left - overlap, q_bottom, 0],
            end=[q_left + brace_width, q_bottom, 0],
            stroke_width=stroke_width,
            color=BLUE
        )

        # Right Q bracket
        q_right_vertical = Line(
            start=[q_right, q_top + overlap, 0],
            end=[q_right, q_bottom - overlap, 0],
            stroke_width=stroke_width,
            color=BLUE
        )
        q_right_top = Line(
            start=[q_right - brace_width, q_top, 0],
            end=[q_right + overlap, q_top, 0],
            stroke_width=stroke_width,
            color=BLUE
        )
        q_right_bottom = Line(
            start=[q_right - brace_width, q_bottom, 0],
            end=[q_right + overlap, q_bottom, 0],
            stroke_width=stroke_width,
            color=BLUE
        )

        q_matrix_brackets = VGroup(
            q_left_vertical, q_left_top, q_left_bottom,
            q_right_vertical, q_right_top, q_right_bottom
        )

        # Create Q row labels at exact existing positions
        token_labels = ['26', '+', '55', '=']
        q_row_labels = VGroup()
        for i, label in enumerate(token_labels):
            row_label = MathTex(f"q_{{{label}}}", font_size=20, color=BLUE)
            row_label.move_to(q_label_positions[i])  # Exact position from existing label
            q_row_labels.add(row_label)

        # Create K^T matrix numbers at exact existing positions
        kt_matrix_numbers = VGroup()
        for row in range(3):  # 3 rows in K^T
            for col in range(4):  # 4 columns in K^T
                val = k_values[col][row]  # Transposed indexing
                number = Tex(f"{val:.1f}", font_size=32, color=RED)
                number.move_to(kt_number_positions[col][row])  # Exact position
                kt_matrix_numbers.add(number)

        # Create K^T matrix brackets to encompass all numbers
        kt_all_positions = [pos for col in kt_number_positions for pos in col]
        kt_left = min(pos[0] for pos in kt_all_positions) - 0.5
        kt_right = max(pos[0] for pos in kt_all_positions) + 0.5
        kt_top = max(pos[1] for pos in kt_all_positions) + 0.35
        kt_bottom = min(pos[1] for pos in kt_all_positions) - 0.35

        # Left K^T bracket
        kt_left_vertical = Line(
            start=[kt_left, kt_top + overlap, 0],
            end=[kt_left, kt_bottom - overlap, 0],
            stroke_width=stroke_width,
            color=RED
        )
        kt_left_top = Line(
            start=[kt_left - overlap, kt_top, 0],
            end=[kt_left + brace_width, kt_top, 0],
            stroke_width=stroke_width,
            color=RED
        )
        kt_left_bottom = Line(
            start=[kt_left - overlap, kt_bottom, 0],
            end=[kt_left + brace_width, kt_bottom, 0],
            stroke_width=stroke_width,
            color=RED
        )

        # Right K^T bracket
        kt_right_vertical = Line(
            start=[kt_right, kt_top + overlap, 0],
            end=[kt_right, kt_bottom - overlap, 0],
            stroke_width=stroke_width,
            color=RED
        )
        kt_right_top = Line(
            start=[kt_right - brace_width, kt_top, 0],
            end=[kt_right + overlap, kt_top, 0],
            stroke_width=stroke_width,
            color=RED
        )
        kt_right_bottom = Line(
            start=[kt_right - brace_width, kt_bottom, 0],
            end=[kt_right + overlap, kt_bottom, 0],
            stroke_width=stroke_width,
            color=RED
        )

        kt_matrix_brackets = VGroup(
            kt_left_vertical, kt_left_top, kt_left_bottom,
            kt_right_vertical, kt_right_top, kt_right_bottom
        )

        # Create K^T column labels at exact existing positions
        kt_col_labels = VGroup()
        for i, label in enumerate(token_labels):
            col_label = MathTex(r"(k_{" + label + r"})^\top", font_size=20, color=RED)
            col_label.move_to(kt_label_positions[i])  # Exact position
            kt_col_labels.add(col_label)

        # Add matrix labels
        q_matrix_label = MathTex(r"Q", font_size=32, color=BLUE)
        q_matrix_label.move_to([(q_right + q_left) / 2, q_top + 0.4, 0])

        kt_matrix_label = MathTex(r"K^\top", font_size=32, color=RED)
        kt_matrix_label.move_to([(kt_right + kt_left) / 2, kt_top + 0.4, 0])

        # Group matrix components
        q_matrix_complete = VGroup(q_matrix_numbers, q_matrix_brackets, q_row_labels)
        kt_matrix_complete = VGroup(kt_matrix_numbers, kt_matrix_brackets, kt_col_labels)

        # Cross fade: individual vectors out, complete matrices in
        self.play(
            FadeOut(self.q_vectors),
            FadeOut(self.kt_vectors),
            FadeIn(q_matrix_complete),
            FadeIn(kt_matrix_complete),
            Write(q_matrix_label),
            Write(kt_matrix_label),
        )

        # Store references for next steps
        self.q_matrix = q_matrix_complete
        self.kt_matrix = kt_matrix_complete
        self.q_matrix_label = q_matrix_label
        self.kt_matrix_label = kt_matrix_label

    def add_attention_matrix(self):
        """Add attention matrix positioned vertically aligned with Q and horizontally aligned with K^T"""
        # Get the bounds of existing matrices
        q_left = self.q_matrix.get_left()[0]
        q_right = self.q_matrix.get_right()[0]
        q_top = self.q_matrix.get_top()[1]
        q_bottom = self.q_matrix.get_bottom()[1]

        kt_left = self.kt_matrix.get_left()[0]
        kt_right = self.kt_matrix.get_right()[0]
        kt_top = self.kt_matrix.get_top()[1]
        kt_bottom = self.kt_matrix.get_bottom()[1]

        # Position attention matrix:
        att_left = kt_left
        att_right = kt_right
        att_top = q_top
        att_bottom = q_bottom

        bracket_width = 0.3
        stroke_width = 4
        overlap = 0.02

        # Left attention bracket
        att_left_vertical = Line(
            start=[att_left, att_top + overlap, 0],
            end=[att_left, att_bottom - overlap, 0],
            stroke_width=stroke_width,
            color=WHITE
        )
        att_left_top = Line(
            start=[att_left - overlap, att_top, 0],
            end=[att_left + bracket_width, att_top, 0],
            stroke_width=stroke_width,
            color=WHITE
        )
        att_left_bottom = Line(
            start=[att_left - overlap, att_bottom, 0],
            end=[att_left + bracket_width, att_bottom, 0],
            stroke_width=stroke_width,
            color=WHITE
        )

        # Right attention bracket
        att_right_vertical = Line(
            start=[att_right, att_top + overlap, 0],
            end=[att_right, att_bottom - overlap, 0],
            stroke_width=stroke_width,
            color=WHITE
        )
        att_right_top = Line(
            start=[att_right - bracket_width, att_top, 0],
            end=[att_right + overlap, att_top, 0],
            stroke_width=stroke_width,
            color=WHITE
        )
        att_right_bottom = Line(
            start=[att_right - bracket_width, att_bottom, 0],
            end=[att_right + overlap, att_bottom, 0],
            stroke_width=stroke_width,
            color=WHITE
        )

        att_matrix_brackets = VGroup(
            att_left_vertical, att_left_top, att_left_bottom,
            att_right_vertical, att_right_top, att_right_bottom
        )

        # Create the "Attention Matrix" label in the center
        att_label = Tex(r"\text{Attention Scores}", font_size=30, color=WHITE)
        att_label.move_to([(att_left + att_right) / 2, (att_top + att_bottom) / 2, 0])

        attention_matrix = VGroup(att_matrix_brackets, att_label)

        # Animate the attention matrix appearing
        self.play(Create(att_matrix_brackets), Write(att_label), run_time=2)

        self.attention_matrix = attention_matrix