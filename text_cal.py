from manim import *
import numpy as np

class SoftmaxTransformation(Scene):
    def construct(self):
        # Create the original attention matrix more centered
        attention_matrix = self.create_attention_matrix()
        attention_matrix.move_to(LEFT * 4.0)  # Position left matrix 4.0 units left of origin
        
        # Add "Before Softmax" text above the attention matrix
        before_text = MathTex(r"\text{Before Softmax}", font_size=42, color=WHITE)
        before_text.next_to(attention_matrix, UP, buff=0.5)
        
        # Add the attention matrix to the scene
        self.play(FadeIn(attention_matrix), FadeIn(before_text))
        self.wait(1)
        
        # Create shorter arrow
        arrow = Arrow(
            start=LEFT * 1.0,
            end=RIGHT * 1.0,
            color=WHITE,
            stroke_width=4
        ).scale(1.8)
        arrow.move_to(ORIGIN)
        
        # Create softmax formula text
        softmax_text = MathTex(
            r"\text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)",
            font_size=36,  # Slightly smaller
            color=WHITE
        )
        softmax_text.next_to(arrow, UP, buff=0.3)
        
        # Animate arrow and formula
        self.play(
            Create(arrow),
            FadeIn(softmax_text)
        )
        self.wait(1)
        
        # Calculate softmax values
        attention_values = [
            [0.83, 0.32, 0.71, 0.42],
            [0.36, 0.85, 0.45, 0.69],
            [0.66, 0.58, 0.87, 0.92],
            [0.38, 0.42, 0.70, 0.70]
        ]
        
        # Apply softmax to each row
        softmax_values = []
        for row in attention_values:
            exp_row = [np.exp(val) for val in row]
            sum_exp = sum(exp_row)
            softmax_row = [exp_val / sum_exp for exp_val in exp_row]
            softmax_values.append(softmax_row)
        
        # Create softmaxed matrix more centered
        softmax_matrix = self.create_softmax_matrix(softmax_values)
        softmax_matrix.move_to(RIGHT * 4.0)  # Position right matrix 4.0 units right of origin
        
        # Add "After Softmax" text above the softmax matrix
        after_text = MathTex(r"\text{After Softmax}", font_size=42, color=WHITE)
        after_text.next_to(softmax_matrix, UP, buff=0.5)
        
        # Animate the creation of the softmax matrix
        self.play(FadeIn(softmax_matrix), FadeIn(after_text), run_time=2)
        self.wait(1)
        
        # Optional: Highlight the transformation by showing one row calculation
        self.animate_row_transformation(attention_matrix, softmax_matrix, row_index=3)
        self.wait(2)

    def create_attention_matrix(self):
        """Create the original attention matrix with white brackets and values."""
        # Hard-coded attention values from the image
        attention_values = [
            ["0.83", "0.32", "0.71", "0.42"],
            ["0.36", "0.85", "0.45", "0.69"],
            ["0.66", "0.58", "0.87", "0.92"],
            ["0.38", "0.42", "0.70", "0.70"]
        ]
        
        # Create matrix numbers
        matrix_numbers = VGroup()
        positions = []
        
        for i, row in enumerate(attention_values):
            for j, val in enumerate(row):
                entry = Tex(val, font_size=36, color=WHITE)
                pos = RIGHT * j * 0.9 + DOWN * i * 0.8
                entry.move_to(pos)
                matrix_numbers.add(entry)
                positions.append(pos)
        
        # Calculate bracket dimensions
        mat_left   = min(p[0] for p in positions) - 0.5
        mat_right  = max(p[0] for p in positions) + 0.5
        mat_top    = max(p[1] for p in positions) + 0.4
        mat_bottom = min(p[1] for p in positions) - 0.4
        
        # Create brackets
        brackets = self.create_brackets(mat_left, mat_right, mat_top, mat_bottom, WHITE)
        
        return VGroup(matrix_numbers, brackets)

    def create_softmax_matrix(self, values):
        """Create the softmax matrix with white brackets and values (2 decimal places)."""
        # Create matrix numbers
        matrix_numbers = VGroup()
        positions = []
        
        for i, row in enumerate(values):
            for j, val in enumerate(row):
                # Show 2 decimal places for softmax values
                entry = Tex(f"{val:.2f}", font_size=36, color=WHITE)  # Changed to WHITE and .2f
                pos = RIGHT * j * 0.9 + DOWN * i * 0.8
                entry.move_to(pos)
                matrix_numbers.add(entry)
                positions.append(pos)
        
        # Calculate bracket dimensions
        mat_left   = min(p[0] for p in positions) - 0.5
        mat_right  = max(p[0] for p in positions) + 0.5
        mat_top    = max(p[1] for p in positions) + 0.4
        mat_bottom = min(p[1] for p in positions) - 0.4
        
        # Create brackets
        brackets = self.create_brackets(mat_left, mat_right, mat_top, mat_bottom, WHITE)  # Changed to WHITE
        
        return VGroup(matrix_numbers, brackets)

    def create_brackets(self, left, right, top, bottom, color):
        """Create matrix brackets with the specified dimensions and color."""
        bracket_width = 0.3
        stroke_width = 4
        overlap = 0.02
        
        # Left bracket
        left_vertical = Line(
            start=[left, top + overlap, 0],
            end=[left, bottom - overlap, 0],
            stroke_width=stroke_width,
            color=color
        )
        left_top = Line(
            start=[left - overlap, top, 0],
            end=[left + bracket_width, top, 0],
            stroke_width=stroke_width,
            color=color
        )
        left_bottom = Line(
            start=[left - overlap, bottom, 0],
            end=[left + bracket_width, bottom, 0],
            stroke_width=stroke_width,
            color=color
        )
        
        # Right bracket
        right_vertical = Line(
            start=[right, top + overlap, 0],
            end=[right, bottom - overlap, 0],
            stroke_width=stroke_width,
            color=color
        )
        right_top = Line(
            start=[right - bracket_width, top, 0],
            end=[right + overlap, top, 0],
            stroke_width=stroke_width,
            color=color
        )
        right_bottom = Line(
            start=[right - bracket_width, bottom, 0],
            end=[right + overlap, bottom, 0],
            stroke_width=stroke_width,
            color=color
        )
        
        return VGroup(
            left_vertical, left_top, left_bottom,
            right_vertical, right_top, right_bottom
        )

    def animate_row_transformation(self, original_matrix, softmax_matrix, row_index):
        """Animate the transformation of a specific row to show the softmax calculation."""
        # Create highlight rectangles for the specified row
        original_highlight = self.create_row_highlight(original_matrix, row_index, YELLOW)
        softmax_highlight = self.create_row_highlight(softmax_matrix, row_index, YELLOW)
        
        # Fade in highlights
        self.play(
            FadeIn(original_highlight),
            FadeIn(softmax_highlight)
        )
        
        self.wait(1)
        
        # Fade out highlights and calculation
        self.play(
            FadeOut(original_highlight),
            FadeOut(softmax_highlight)
        )

    def create_row_highlight(self, matrix, row_index, color):
        """Create a highlight rectangle for a specific row in the matrix."""
        numbers = matrix[0]  # The VGroup containing all numbers
        
        # Get the numbers in the specified row (4 numbers per row)
        row_start = row_index * 4
        row_numbers = [numbers[row_start + i] for i in range(4)]
        
        # Calculate highlight dimensions
        left   = min(n.get_left()[0] for n in row_numbers) - 0.2
        right  = max(n.get_right()[0] for n in row_numbers) + 0.2
        top    = max(n.get_top()[1] for n in row_numbers) + 0.15
        bottom = min(n.get_bottom()[1] for n in row_numbers) - 0.15
        
        # Create highlight rectangle
        rect = Rectangle(
            width=right - left,
            height=top - bottom,
            fill_color=color,
            fill_opacity=0.3,
            stroke_width=0
        )
        rect.move_to([(left + right)/2, (top + bottom)/2, 0])
        
        return rect