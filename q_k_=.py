from manim import *
import numpy as np

class ExtendedAttentionCalculation(Scene):
    def construct(self):
        # Start with the matrices already displayed (recreate the final state from previous scene)
        self.setup_initial_matrices()
        self.wait(1)
        
        # Focus on the Q_= row calculations
        self.animate_q_equals_calculations()
        self.wait(2)

    def setup_initial_matrices(self):
        """Recreate the final state from the previous animation using Matrix function"""
        
        # Create Q matrix
        self.create_q_matrix()
        
        # Create K^T matrix
        self.create_kt_matrix()
        
        # Create attention scores matrix
        self.create_attention_matrix()
        
        # Add multiplication symbol
        mult_symbol = Text("×", font_size=48, color=WHITE)
        mult_symbol.move_to(LEFT * 0.1 + UP * 0.15)  # Original position
        
        # Display everything at once since this continues from previous scene
        self.add(
            self.q_matrix_group,
            self.kt_matrix_group,
            self.attention_matrix_group,
            mult_symbol
        )

    def create_q_matrix(self):
        """Create the Q matrix using Matrix function"""
        # Q matrix values
        q_values = [
            ["0.2", "0.8", "0.1"],  # Q_26
            ["0.9", "0.1", "0.3"],  # Q_+
            ["0.4", "0.6", "0.9"],  # Q_55
            ["0.1", "0.3", "0.7"]   # Q_=
        ]
        
        # Create matrix with tighter spacing
        self.q_matrix = Matrix(q_values, 
                              element_to_mobject=lambda x: Text(x, font_size=16, color=BLUE),
                              h_buff=0.8,  # Horizontal spacing between elements
                              v_buff=0.6)  # Vertical spacing between elements
        self.q_matrix.move_to(LEFT * 4 + DOWN * 0.3)  # Original position
        
        # Add matrix label
        q_label = MathTex("Q", font_size=32, color=BLUE)
        q_label.next_to(self.q_matrix, LEFT, buff=0.5)
        
        # Add row labels
        token_labels = ["26", "+", "55", "="]
        self.q_row_labels = VGroup()
        
        for i, label in enumerate(token_labels):
            row_label = MathTex(f"Q_{{{label}}}", font_size=20, color=BLUE)
            # Position labels to the left of each row
            row_center = self.q_matrix.get_rows()[i].get_center()
            row_label.move_to([q_label.get_left()[0] - 1.0, row_center[1], 0])
            self.q_row_labels.add(row_label)
        
        self.q_matrix_group = VGroup(self.q_matrix, q_label, self.q_row_labels)

    def create_kt_matrix(self):
        """Create the K^T matrix using Matrix function"""
        # K^T matrix values (transposed)
        kt_values = [
            ["0.3", "0.8", "0.1", "0.5"],  # Row 1
            ["0.7", "0.2", "0.9", "0.3"],  # Row 2
            ["0.2", "0.4", "0.6", "0.8"]   # Row 3
        ]
        
        # Create matrix with tighter spacing
        self.kt_matrix = Matrix(kt_values,
                               element_to_mobject=lambda x: Text(x, font_size=16, color=RED),
                               h_buff=0.6,  # Horizontal spacing between elements
                               v_buff=0.4)  # Vertical spacing between elements
        self.kt_matrix.move_to(RIGHT * 0.2 + UP * 1.2)  # Original position area
        
        # Add matrix label
        kt_label = MathTex("K^T", font_size=32, color=RED)
        kt_label.next_to(self.kt_matrix, UP, buff=0.4)
        
        # Add column labels
        token_labels = ["26", "+", "55", "="]
        self.kt_col_labels = VGroup()
        
        for i, label in enumerate(token_labels):
            col_label = MathTex(f"K^T_{{{label}}}", font_size=20, color=RED)
            # Position labels below each column
            col_center = self.kt_matrix.get_columns()[i].get_center()
            col_label.move_to([col_center[0], self.kt_matrix.get_bottom()[1] - 0.4, 0])
            self.kt_col_labels.add(col_label)
        
        self.kt_matrix_group = VGroup(self.kt_matrix, kt_label, self.kt_col_labels)

    def create_attention_matrix(self):
        """Create the attention scores matrix"""
        # Initial attention matrix (we'll update the last row during animation)
        attention_entries = [
            ["0.83", "0.32", "0.71", "0.42"],  # Q_26 results
            ["0.36", "0.85", "0.45", "0.69"],  # Q_+ results  
            ["0.66", "0.58", "0.87", "0.92"],  # Q_55 results
            ["?", "?", "?", "?"]               # Q_= results (to be calculated)
        ]
        
        self.attention_matrix = Matrix(attention_entries,
                                     element_to_mobject=lambda x: Text(x, font_size=12, color=WHITE if x != "?" else YELLOW),
                                     h_buff=0.5,  # Tighter horizontal spacing
                                     v_buff=0.4)  # Tighter vertical spacing
        
        # Position like original code (center area)
        self.attention_matrix.move_to(RIGHT * 2.5 + DOWN * 0.3)
        
        # Add label
        result_label = Text("Attention Scores", font_size=18, color=ORANGE)
        result_label.next_to(self.attention_matrix, UP, buff=0.3)
        
        self.attention_matrix_group = VGroup(self.attention_matrix, result_label)

    def animate_q_equals_calculations(self):
        """Animate the Q_= row calculations with each K^T column"""
        
        # Add title for this section
        calculation_title = Text("Computing Q_= attention with all tokens", font_size=24, color=YELLOW)
        calculation_title.to_edge(UP)
        self.play(Write(calculation_title))
        self.wait(1)
        
        # Q_= values for calculations
        q_equals_values = [0.1, 0.3, 0.7]
        
        # K^T column values (each column represents one token's key)
        kt_columns = [
            [0.3, 0.7, 0.2],  # K_26
            [0.8, 0.2, 0.4],  # K_+
            [0.1, 0.9, 0.6],  # K_55
            [0.5, 0.3, 0.8]   # K_=
        ]
        
        token_names = ["26", "+", "55", "="]
        
        # Calculate each dot product one by one
        for i, (kt_column, token_name) in enumerate(zip(kt_columns, token_names)):
            self.animate_single_calculation(i, q_equals_values, kt_column, token_name)
            self.wait(1.5)
        
        # Clean up
        self.play(FadeOut(calculation_title))
        
        # Final summary
        summary = Text("Q_= now knows how much to attend to each token!", 
                      font_size=20, color=GREEN)
        summary.to_edge(DOWN)
        self.play(Write(summary))
        self.wait(2)
        self.play(FadeOut(summary))

    def animate_single_calculation(self, column_index, q_values, k_values, token_name):
        """Animate a single dot product calculation with background highlighting"""
        
        # Create background highlights for Q_= row (row 3)
        q_row_highlight = self.create_row_background_highlight(self.q_matrix, 3, YELLOW, 0.3)
        
        # Create background highlights for K^T column
        kt_col_highlight = self.create_column_background_highlight(self.kt_matrix, column_index, YELLOW, 0.3)
        
        # Show highlights
        self.play(
            FadeIn(q_row_highlight),
            FadeIn(kt_col_highlight)
        )
        
        # Create calculation display
        calc_text = self.create_calculation_display(q_values, k_values, token_name)
        self.play(Write(calc_text))
        
        # Animate the step-by-step calculation
        step_calcs = self.create_step_calculations(q_values, k_values)
        self.play(Write(step_calcs))
        
        # Calculate final result
        dot_product = sum(q * k for q, k in zip(q_values, k_values))
        result_text = Text(f"= {dot_product:.2f}", font_size=20, color=GREEN)
        result_text.next_to(step_calcs, RIGHT, buff=0.3)
        self.play(Write(result_text))
        
        # Update the attention matrix
        self.update_attention_matrix_cell(3, column_index, f"{dot_product:.2f}")
        
        # Clean up calculation display and highlights
        self.play(
            FadeOut(calc_text),
            FadeOut(step_calcs), 
            FadeOut(result_text),
            FadeOut(q_row_highlight),
            FadeOut(kt_col_highlight)
        )

    def create_row_background_highlight(self, matrix, row_index, color, opacity):
        """Create a background highlight for a specific row"""
        row = matrix.get_rows()[row_index]
        
        # Create a rectangle that covers the entire row
        highlight_rect = Rectangle(
            width=row.get_width() + 0.3,
            height=row.get_height() + 0.1,
            fill_color=color,
            fill_opacity=opacity,
            stroke_width=0
        )
        highlight_rect.move_to(row.get_center())
        
        return highlight_rect

    def create_column_background_highlight(self, matrix, col_index, color, opacity):
        """Create a background highlight for a specific column"""
        column = matrix.get_columns()[col_index]
        
        # Create a rectangle that covers the entire column
        highlight_rect = Rectangle(
            width=column.get_width() + 0.1,
            height=column.get_height() + 0.3,
            fill_color=color,
            fill_opacity=opacity,
            stroke_width=0
        )
        highlight_rect.move_to(column.get_center())
        
        return highlight_rect

    def create_calculation_display(self, q_values, k_values, token_name):
        """Create the calculation equation display"""
        q_str = f"[{q_values[0]}, {q_values[1]}, {q_values[2]}]"
        k_str = f"[{k_values[0]}, {k_values[1]}, {k_values[2]}]"
        
        calc_text = Text(f"Q_= · K^T_{token_name} = {q_str} · {k_str}", 
                        font_size=16, color=WHITE)
        calc_text.move_to(DOWN * 2.8)
        return calc_text

    def create_step_calculations(self, q_values, k_values):
        """Create step-by-step multiplication display"""
        steps = []
        for i, (q, k) in enumerate(zip(q_values, k_values)):
            steps.append(f"({q}×{k})")
        
        step_text = Text(f"= {' + '.join(steps)}", font_size=16, color=BLUE)
        step_text.move_to(DOWN * 3.2)
        return step_text

    def update_attention_matrix_cell(self, row, col, new_value):
        """Update a specific cell in the attention matrix with background highlight"""
        # Get the current matrix entries
        entries = self.attention_matrix.get_entries()
        target_entry = entries[row * 4 + col]  # 4 columns per row
        
        # Create new text with the calculated value
        new_text = Text(new_value, font_size=12, color=GREEN)
        new_text.move_to(target_entry.get_center())
        
        # Create background highlight for the cell
        cell_highlight = Rectangle(
            width=target_entry.get_width() + 0.2,
            height=target_entry.get_height() + 0.1,
            fill_color=GREEN,
            fill_opacity=0.3,
            stroke_width=0
        )
        cell_highlight.move_to(target_entry.get_center())
        
        # Animate the replacement with background highlight
        self.play(
            FadeIn(cell_highlight),
            run_time=0.5
        )
        self.play(
            Transform(target_entry, new_text),
            run_time=0.8
        )
        self.play(
            FadeOut(cell_highlight),
            run_time=0.5
        )