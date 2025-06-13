from manim import *
import numpy as np

class ExtendedAttentionCalculation(Scene):
    def construct(self):
        # 1) Recreate Q, K^T, and attention‐matrix in their final positions
        self.setup_initial_matrices()
        self.wait(1)
        
        # 2) Animate the Q_= row calculations, with the title in the upper‐left
        self.animate_q_equals_calculations()
        self.wait(2)

    def setup_initial_matrices(self):
        """Recreate the final state from the previous animation with the desired positioning."""
        
        # Create Q (left side)
        self.create_q_matrix()
        
        # Create K^T (shifted farther right and higher)
        self.create_kt_matrix()
        
        # Create the 4×4 attention matrix (under K^T, same height as Q), with larger numbers + no label
        self.create_attention_matrix()
        
        # Place a "×" symbol exactly halfway between Q and K^T
        mult_symbol = MathTex(r"\times", font_size=48, color=WHITE)
        q_right = self.q_matrix.get_right()[0]
        kt_left = self.kt_matrix.get_left()[0]
        mult_x = (q_right + kt_left) / 2
        mult_y = (self.q_matrix.get_center()[1] + self.kt_matrix.get_center()[1]) / 2
        mult_symbol.move_to([mult_x, mult_y, 0])
        
        # Add everything at once
        self.add(
            self.q_matrix_group,
            self.kt_matrix_group,
            self.attention_matrix_group,
            mult_symbol
        )

    def create_q_matrix(self):
        """Build the Q‐matrix on the left, with its bracket and row labels."""
        # Q‐values (4 rows × 3 columns)
        q_values = [
            ["0.2", "0.8", "0.1"],   # q_{26}
            ["0.9", "0.1", "0.3"],   # q_{+}
            ["0.4", "0.6", "0.9"],   # q_{55}
            ["0.1", "0.3", "0.7"]    # q_{=}
        ]
        
        # "start_pos" replicates the original: LEFT * 3.2 + DOWN * 0.3
        start_pos = LEFT * 3.2 + DOWN * 0.3
        
        # 1) Place each number (font_size=32) in a 4×3 grid
        q_matrix_numbers = VGroup()
        all_positions = []
        for i, row_vals in enumerate(q_values):
            for j, val in enumerate(row_vals):
                num_tex = Tex(val, font_size=32, color=BLUE)
                pos = start_pos + DOWN * i * 0.8 + RIGHT * j * 0.7
                num_tex.move_to(pos)
                q_matrix_numbers.add(num_tex)
                all_positions.append(pos)
        
        # 2) Compute bracket extents from extremes of all_positions
        q_left   = min(p[0] for p in all_positions) - 0.5
        q_right  = max(p[0] for p in all_positions) + 0.5
        q_top    = max(p[1] for p in all_positions) + 0.4
        q_bottom = min(p[1] for p in all_positions) - 0.4
        
        bracket_width = 0.3
        stroke_width  = 4
        overlap       = 0.02
        
        # Left bracket
        q_left_vertical = Line(
            start=[q_left,      q_top + overlap,    0],
            end  =[q_left,      q_bottom - overlap, 0],
            stroke_width=stroke_width,
            color=BLUE
        )
        q_left_top    = Line(
            start=[q_left - overlap, q_top,    0],
            end  =[q_left + bracket_width, q_top,    0],
            stroke_width=stroke_width,
            color=BLUE
        )
        q_left_bottom = Line(
            start=[q_left - overlap, q_bottom, 0],
            end  =[q_left + bracket_width, q_bottom, 0],
            stroke_width=stroke_width,
            color=BLUE
        )
        
        # Right bracket
        q_right_vertical = Line(
            start=[q_right,     q_top + overlap,    0],
            end  =[q_right,     q_bottom - overlap, 0],
            stroke_width=stroke_width,
            color=BLUE
        )
        q_right_top    = Line(
            start=[q_right - bracket_width, q_top,    0],
            end  =[q_right + overlap,       q_top,    0],
            stroke_width=stroke_width,
            color=BLUE
        )
        q_right_bottom = Line(
            start=[q_right - bracket_width, q_bottom, 0],
            end  =[q_right + overlap,       q_bottom, 0],
            stroke_width=stroke_width,
            color=BLUE
        )
        
        q_matrix_brackets = VGroup(
            q_left_vertical, q_left_top, q_left_bottom,
            q_right_vertical, q_right_top, q_right_bottom
        )
        
        # Combine numbers + brackets into self.q_matrix
        self.q_matrix = VGroup(q_matrix_numbers, q_matrix_brackets)
        
        # 3) Add "Q" label centered above the bracket
        q_label = MathTex("Q", font_size=32, color=BLUE)
        q_label.move_to([ (q_left + q_right) / 2, q_top + 0.4, 0 ])
        
        # 4) Add row labels ("q_{26}", "q_{+}", "q_{55}", "q_{=}")
        token_labels = ['26', '+', '55', '=']
        self.q_row_labels = VGroup()
        for i, lbl in enumerate(token_labels):
            row_label = MathTex(f"q_{{{lbl}}}", font_size=20, color=BLUE)
            # Vertical center of each row = start_pos[1] + i*(−0.8)
            row_center_y = start_pos[1] + DOWN[1] * i * 0.8
            row_label.move_to([ q_left - 0.8, row_center_y, 0 ])
            self.q_row_labels.add(row_label)
        
        # Combine everything into q_matrix_group
        self.q_matrix_group = VGroup(self.q_matrix, q_label, self.q_row_labels)

    def create_kt_matrix(self):
        """Build a 3×4 K^T‐matrix, higher on screen and shifted right, plus bracket and labels."""
        # K values (transposed form: each sublist is one key)
        k_values = [
            [0.3, 0.7, 0.2],  # k_{26}
            [0.8, 0.2, 0.4],  # k_{+}
            [0.1, 0.9, 0.6],  # k_{55}
            [0.5, 0.3, 0.8]   # k_{=}
        ]
        
        # Shift K^T up higher (UP * 2.5) and right (RIGHT * 1.5)
        start_pos = RIGHT * 1.5 + UP * 2.5
        
        # 1) Place each number (font_size=32) in a 3×4 grid
        kt_matrix_numbers = VGroup()
        all_kt_positions = []
        for row in range(3):
            for col in range(4):
                val = k_values[col][row]  # note the transposed indexing
                num_tex = Tex(f"{val:.1f}", font_size=32, color=RED)
                pos = start_pos + RIGHT * col * 0.9 + DOWN * row * 0.5
                num_tex.move_to(pos)
                kt_matrix_numbers.add(num_tex)
                all_kt_positions.append(pos)
        
        # 2) Compute bracket extents
        kt_left   = min(p[0] for p in all_kt_positions) - 0.5
        kt_right  = max(p[0] for p in all_kt_positions) + 0.5
        kt_top    = max(p[1] for p in all_kt_positions) + 0.35
        kt_bottom = min(p[1] for p in all_kt_positions) - 0.35
        
        bracket_width = 0.3
        stroke_width  = 4
        overlap       = 0.02
        
        # Left bracket
        kt_left_vertical = Line(
            start=[kt_left,      kt_top + overlap,    0],
            end  =[kt_left,      kt_bottom - overlap, 0],
            stroke_width=stroke_width,
            color=RED
        )
        kt_left_top    = Line(
            start=[kt_left - overlap, kt_top,    0],
            end  =[kt_left + bracket_width, kt_top,    0],
            stroke_width=stroke_width,
            color=RED
        )
        kt_left_bottom = Line(
            start=[kt_left - overlap, kt_bottom, 0],
            end  =[kt_left + bracket_width, kt_bottom, 0],
            stroke_width=stroke_width,
            color=RED
        )
        
        # Right bracket
        kt_right_vertical = Line(
            start=[kt_right,     kt_top + overlap,    0],
            end  =[kt_right,     kt_bottom - overlap, 0],
            stroke_width=stroke_width,
            color=RED
        )
        kt_right_top    = Line(
            start=[kt_right - bracket_width, kt_top,    0],
            end  =[kt_right + overlap,       kt_top,    0],
            stroke_width=stroke_width,
            color=RED
        )
        kt_right_bottom = Line(
            start=[kt_right - bracket_width, kt_bottom, 0],
            end  =[kt_right + overlap,       kt_bottom, 0],
            stroke_width=stroke_width,
            color=RED
        )
        
        kt_matrix_brackets = VGroup(
            kt_left_vertical, kt_left_top, kt_left_bottom,
            kt_right_vertical, kt_right_top, kt_right_bottom
        )
        
        # Combine numbers + brackets into self.kt_matrix
        self.kt_matrix = VGroup(kt_matrix_numbers, kt_matrix_brackets)
        
        # 3) Add "K^T" label above
        kt_label = MathTex(r"K^\top", font_size=32, color=RED)
        kt_label.move_to([ (kt_left + kt_right) / 2, kt_top + 0.4, 0 ])
        
        # 4) Add column labels below each column: k^T_{26}, k^T_{+}, k^T_{55}, k^T_{=}
        token_labels = ['26', '+', '55', '=']
        self.kt_col_labels = VGroup()
        for i, lbl in enumerate(token_labels):
            col_label = MathTex(rf"(k_{{{lbl}}})^\top", font_size=20, color=RED)
            col_center_x = start_pos[0] + RIGHT[0] * i * 0.9
            col_label.move_to([ col_center_x, kt_bottom - 0.5, 0 ])
            self.kt_col_labels.add(col_label)
        
        # Combine into kt_matrix_group
        self.kt_matrix_group = VGroup(self.kt_matrix, kt_label, self.kt_col_labels)

    def create_attention_matrix(self):
        """Build a 4×4 attention‐scores matrix that sits under K^\top (no 'Attention Scores' text)."""
        # Use Q's top/bottom for vertical extent, and K^\top's left/right for horizontal
        q_top    = self.q_matrix.get_top()[1]
        q_bottom = self.q_matrix.get_bottom()[1]
        kt_left  = self.kt_matrix.get_left()[0]
        kt_right = self.kt_matrix.get_right()[0]
        
        att_left   = kt_left
        att_right  = kt_right
        att_top    = q_top
        att_bottom = q_bottom
        
        # Hard‐coded attention entries; last row "?" placeholders
        attention_entries = [
            ["0.83", "0.32", "0.71", "0.42"],  # q_{26} row
            ["0.36", "0.85", "0.45", "0.69"],  # q_{+} row
            ["0.66", "0.58", "0.87", "0.92"],  # q_{55} row
            ["?",    "?",    "?",    "?"]     # q_{=} row
        ]
        
        # 1) Place each entry with font_size=32 (same as other matrices) and align with K^\top columns
        att_matrix_numbers = VGroup()
        self.attention_entries = []  # store references for updating
        
        # Use the same positioning as K^\top matrix for horizontal alignment
        kt_start_x = 1.5  # from K^\top's start_pos = RIGHT * 1.5 + UP * 2.5
        kt_col_spacing = 0.9  # from K^\top's RIGHT * col * 0.9
        
        # Use Q matrix's row positions for vertical alignment
        q_start_pos = LEFT * 3.2 + DOWN * 0.3  # from Q matrix creation
        q_row_spacing = 0.8  # from Q's DOWN * i * 0.8
        
        for i, row in enumerate(attention_entries):
            row_entries = []
            for j, val in enumerate(row):
                # Same font_size=32 as other matrices; "?" entries remain YELLOW
                color = WHITE if val != "?" else YELLOW
                entry = Tex(val, font_size=32, color=color)
                # Align horizontally with K^\top columns and vertically with Q rows
                x = kt_start_x + j * kt_col_spacing
                y = q_start_pos[1] + DOWN[1] * i * q_row_spacing
                entry.move_to([x, y, 0])
                att_matrix_numbers.add(entry)
                row_entries.append(entry)
            self.attention_entries.append(row_entries)
        
        # 2) Draw a bracket around that entire 4×4 block
        bracket_width = 0.3
        stroke_width  = 4
        overlap       = 0.02
        
        # Left bracket of attention
        att_left_vertical = Line(
            start=[att_left,      att_top + overlap,    0],
            end  =[att_left,      att_bottom - overlap, 0],
            stroke_width=stroke_width,
            color=WHITE
        )
        att_left_top    = Line(
            start=[att_left - overlap, att_top,    0],
            end  =[att_left + bracket_width, att_top,    0],
            stroke_width=stroke_width,
            color=WHITE
        )
        att_left_bottom = Line(
            start=[att_left - overlap, att_bottom, 0],
            end  =[att_left + bracket_width, att_bottom, 0],
            stroke_width=stroke_width,
            color=WHITE
        )
        
        # Right bracket of attention
        att_right_vertical = Line(
            start=[att_right,     att_top + overlap,    0],
            end  =[att_right,     att_bottom - overlap, 0],
            stroke_width=stroke_width,
            color=WHITE
        )
        att_right_top    = Line(
            start=[att_right - bracket_width, att_top,    0],
            end  =[att_right + overlap,       att_top,    0],
            stroke_width=stroke_width,
            color=WHITE
        )
        att_right_bottom = Line(
            start=[att_right - bracket_width, att_bottom, 0],
            end  =[att_right + overlap,       att_bottom, 0],
            stroke_width=stroke_width,
            color=WHITE
        )
        
        att_matrix_brackets = VGroup(
            att_left_vertical, att_left_top, att_left_bottom,
            att_right_vertical, att_right_top, att_right_bottom
        )
        
        # Combine numbers + brackets into self.attention_matrix
        self.attention_matrix = VGroup(att_matrix_numbers, att_matrix_brackets)
        
        # We do NOT add any "Attention Scores" text here, per your request.
        self.attention_matrix_group = VGroup(self.attention_matrix)

    def animate_q_equals_calculations(self):
        """
        Animate computing Q_{=} ⋅ K^T_{*} for each column. 
        Place the title in the upper‐left corner instead of top‐center.
        """
        
        # Hard‐coded Q_{=} row vector and each K^T column
        q_equals_values = [0.1, 0.3, 0.7]
        kt_columns = [
            [0.3, 0.7, 0.2],   # k_{26}
            [0.8, 0.2, 0.4],   # k_{+}
            [0.1, 0.9, 0.6],   # k_{55}
            [0.5, 0.3, 0.8]    # k_{=}
        ]
        token_names = ['26', '+', '55', '=']
        
        for i, (kt_col_vals, token_name) in enumerate(zip(kt_columns, token_names)):
            self.animate_single_calculation(i, q_equals_values, kt_col_vals, token_name)
            self.wait(1.5)

    def animate_single_calculation(self, column_index, q_values, k_values, token_name):
        """
        1) Highlight Q_{=} row
        2) Highlight K^T's column "column_index"
        3) Write out "Q_{=} · K^T_{token_name} = […], […]"
        4) Write out step‐by‐step "(q×k) + (…) + (…)"
        —with the blue "=" aligned under the white subscript "=" of calc_tex.
        5) Compute dot product and update that cell in the 4×4 (no green text)
        6) Fade out everything
        """
        # 1) Highlight the Q_{=} row (row_index=3)
        q_row_hl = self.create_row_background_highlight(
            matrix=self.q_matrix,
            row_index=3,
            color=YELLOW,
            opacity=0.3
        )
        
        # 2) Highlight the K^T column (column_index)
        kt_col_hl = self.create_column_background_highlight(
            matrix=self.kt_matrix,
            col_index=column_index,
            color=YELLOW,
            opacity=0.3
        )
        
        self.play(FadeIn(q_row_hl), FadeIn(kt_col_hl))
        
        # 3) Show "Q_{=} · K^T_{token_name} = [0.1, 0.3, 0.7] · [k0, k1, k2]"
        calc_tex = self.create_calculation_display(q_values, k_values, token_name)
        self.play(Write(calc_tex))
        
        # 4) Show "= (0.1×k0) + (0.3×k1) + (0.7×k2)"
        step_tex = self.create_step_calculations(q_values, k_values, calc_tex)
        
        # ── NEW BLOCK: Align step_tex's "=" under the white "=" in calc_tex ──
        #  a) Find the subscript "=" from calc_tex (usually the first "=" in the MathTex)
        all_eqs_in_calc = calc_tex.get_part_by_tex("=")
        subscript_eq = all_eqs_in_calc[0]   # That is the "=" inside Q_{=}
        
        #  b) Find the "=" inside step_tex (there is exactly one of them)
        step_eq = step_tex.get_part_by_tex("=")[0]
        
        #  c) Force their left edges to coincide
        step_eq.align_to(subscript_eq, LEFT)
        # ────────────────────────────────────────────────────────────────
        
        self.play(Write(step_tex))
        
        # 5) Compute final float, and update the attention‐matrix cell (no green text)
        dot_product = sum(q * k for q, k in zip(q_values, k_values))
        self.update_attention_matrix_cell(3, column_index, f"{dot_product:.2f}")
        
        # 6) Fade out overlays (just calc_tex, step_tex, and the highlights)
        self.play(
            FadeOut(calc_tex),
            FadeOut(step_tex),
            FadeOut(q_row_hl),
            FadeOut(kt_col_hl)
        )


    def create_row_background_highlight(self, matrix: VGroup, row_index: int, color, opacity):
        """
        Return a rectangle behind row "row_index" (0‐based) of a 4×3 Q‐matrix,
        so that that row is highlighted in color with the given opacity.
        """
        numbers = matrix[0]  # matrix[0] is the VGroup holding all Tex numbers in Q
        row_start = row_index * 3
        row_numbers = [numbers[row_start + i] for i in range(3)]
        
        left   = min(n.get_left()[0] for n in row_numbers) - 0.2
        right  = max(n.get_right()[0] for n in row_numbers) + 0.2
        top    = max(n.get_top()[1] for n in row_numbers) + 0.15
        bottom = min(n.get_bottom()[1] for n in row_numbers) - 0.15
        
        rect = Rectangle(
            width=right - left,
            height=top - bottom,
            fill_color=color,
            fill_opacity=opacity,
            stroke_width=0
        )
        rect.move_to([ (left + right)/2, (top + bottom)/2, 0 ])
        return rect

    def create_column_background_highlight(self, matrix: VGroup, col_index: int, color, opacity):
        """
        Return a rectangle behind column "col_index" (0‐based) of a 3×4 K^T‐matrix,
        so that that entire column is highlighted.
        """
        numbers = matrix[0]  # matrix[0] is the VGroup holding Tex numbers in K^T
        # Each row has 4 numbers; pick index "row*4 + col_index" for row=0,1,2
        col_numbers = [numbers[r * 4 + col_index] for r in range(3)]
        
        left   = min(n.get_left()[0] for n in col_numbers) - 0.15
        right  = max(n.get_right()[0] for n in col_numbers) + 0.15
        top    = max(n.get_top()[1] for n in col_numbers) + 0.2
        bottom = min(n.get_bottom()[1] for n in col_numbers) - 0.2
        
        rect = Rectangle(
            width=right - left,
            height=top - bottom,
            fill_color=color,
            fill_opacity=opacity,
            stroke_width=0
        )
        rect.move_to([ (left + right)/2, (top + bottom)/2, 0 ])
        return rect

    def create_calculation_display(self, q_values, k_values, token_name):
        """
        Return a MathTex showing "q_{=} · (k_{token_name})^\top = [q0,q1,q2] · [k0,k1,k2]"
        positioned closer to the top‐center rather than the far left.
        """
        q_str = f"[{q_values[0]}, {q_values[1]}, {q_values[2]}]"
        k_str = f"[{k_values[0]}, {k_values[1]}, {k_values[2]}]"
        calc_tex = MathTex(
            rf"q_{{=}} \cdot (k_{{{token_name}}})^\top = {q_str} \cdot {k_str}",
            font_size=28,  # increased from 16 → 28
            color=WHITE
        )
        # **Shift it rightward to around x = -3**, y near the top
        calc_tex.move_to([-3, 1.8, 0])
        return calc_tex

    def create_step_calculations(self, q_values, k_values, calc_tex):
        # use \times instead of the × symbol
        steps = [f"({q}\\times {k})" for q, k in zip(q_values, k_values)]
        step_tex = MathTex(
            f"= {' + '.join(steps)}",
            font_size=28,
            color=BLUE
        )
        step_tex.next_to(calc_tex, DOWN, aligned_edge=LEFT, buff=0.2)
        return step_tex


    def update_attention_matrix_cell(self, row, col, new_value: str):
        """
        Replace the Tex in self.attention_entries[row][col] (previously "?")
        with a new MathTex(new_value) in green, performing a Transform.
        """
        entry = self.attention_entries[row][col]
        new_tex = MathTex(new_value, font_size=32, color=GREEN)
        new_tex.move_to(entry)
        self.play(Transform(entry, new_tex))
