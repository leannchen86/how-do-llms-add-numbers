from manim import *
import numpy as np

class LLMAttentionMechanism(Scene):
    def construct(self):
        # Run the attention mechanism visualization
        self.attention_mechanism()
        
    def attention_mechanism(self):
        # Title for the scene
        title = Text("Self-Attention in Transformer Models", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Create token sequence explanation
        token_seq = Text("Token Sequence: \"26 + 55 = \"", font_size=30)
        token_seq.next_to(title, DOWN)
        self.play(Write(token_seq))
        self.wait(1)
        
        # Step 1: Show that we're focusing on the "=" token
        step1 = Text("Step 1: Processing the \"=\" token", font_size=28)
        step1.next_to(token_seq, DOWN)
        self.play(Write(step1))
        
        # Create token boxes for the sequence
        tokens = ["26", "+", "55", "="]
        token_colors = [BLUE_D, GREEN_D, YELLOW_D, RED_D]
        token_boxes = VGroup()
        
        for i, (token, color) in enumerate(zip(tokens, token_colors)):
            box = VGroup()
            rect = Rectangle(height=0.8, width=1.2, fill_color=color, fill_opacity=0.3, stroke_color=color)
            text = Text(token, font_size=24)
            text.move_to(rect.get_center())
            box.add(rect, text)
            
            # Position boxes horizontally
            if i == 0:
                box.to_edge(LEFT).shift(RIGHT * 3 + DOWN * 2)
            else:
                box.next_to(token_boxes[-1], RIGHT, buff=0.5)
            
            token_boxes.add(box)
        
        # Highlight the = token
        highlight_rect = SurroundingRectangle(token_boxes[-1], color=RED, buff=0.1, stroke_width=3)
        
        self.play(FadeIn(token_boxes))
        self.play(Create(highlight_rect))
        self.wait(1)
        
        # Clear previous steps to make space
        self.play(FadeOut(step1))
        
        # Step 2: Create Query, Key, Value matrices
        step2 = Text("Step 2: Generate Query, Key, and Value matrices", font_size=28)
        step2.next_to(token_seq, DOWN)
        self.play(Write(step2))
        
        # Create matrix headers
        query_title = Text("Query (Q)", font_size=24, color=RED)
        key_title = Text("Key (K)", font_size=24, color=BLUE)
        value_title = Text("Value (V)", font_size=24, color=GREEN)
        
        # Position matrix headers
        query_title.next_to(step2, DOWN, buff=0.8).to_edge(LEFT).shift(RIGHT * 3)
        key_title.next_to(query_title, RIGHT, buff=3.5)
        value_title.next_to(key_title, RIGHT, buff=3.5)
        
        self.play(Write(query_title), Write(key_title), Write(value_title))
        
        # Create matrix visualization function
        def create_matrix(rows, cols, color, position, opacity_range=(0.2, 0.8), highlight_row=None):
            matrix = VGroup()
            cell_size = 0.4
            
            for i in range(rows):
                row_group = VGroup()
                highlight = (i == highlight_row)
                
                for j in range(cols):
                    opacity = np.random.uniform(*opacity_range)
                    # Ensure highlight row is more visible
                    if highlight:
                        opacity = min(opacity + 0.2, 1.0)
                    
                    cell = Square(
                        side_length=cell_size,
                        fill_color=color,
                        fill_opacity=opacity,
                        stroke_width=1,
                        stroke_color=WHITE if highlight else GRAY
                    )
                    cell.move_to([
                        position[0] + j * cell_size,
                        position[1] - i * cell_size,
                        0
                    ])
                    row_group.add(cell)
                
                matrix.add(row_group)
            
            # Add a surrounding box for highlighted row if specified
            if highlight_row is not None:
                highlight_box = SurroundingRectangle(
                    matrix[highlight_row], 
                    color=RED, 
                    buff=0.05,
                    stroke_width=2
                )
                matrix.add(highlight_box)
            
            return matrix
        
        # For Query, only show the current token (=)
        query_matrix = create_matrix(1, 3, RED_E, [query_title.get_center()[0], query_title.get_bottom()[1] - 0.8, 0])
        query_token_label = Text("=", font_size=18).next_to(query_matrix, LEFT, buff=0.2)
        
        # For Key and Value, show all tokens so far in sequence
        key_matrix = create_matrix(4, 3, BLUE_E, [key_title.get_center()[0], key_title.get_bottom()[1] - 0.8, 0], highlight_row=3)
        key_token_labels = VGroup()
        for i, token in enumerate(tokens):
            label = Text(token, font_size=18)
            label.next_to(key_matrix[i], LEFT, buff=0.2)
            key_token_labels.add(label)
        
        value_matrix = create_matrix(4, 3, GREEN_E, [value_title.get_center()[0], value_title.get_bottom()[1] - 0.8, 0], highlight_row=3)
        value_token_labels = VGroup()
        for i, token in enumerate(tokens):
            label = Text(token, font_size=18)
            label.next_to(value_matrix[i], LEFT, buff=0.2)
            value_token_labels.add(label)
        
        # Create explanation text
        query_explanation = Text("Query for current token (=)", font_size=16, color=RED).next_to(query_matrix, DOWN, buff=0.5)
        key_explanation = Text("Keys from all tokens so far", font_size=16, color=BLUE).next_to(key_matrix, DOWN, buff=0.5)
        value_explanation = Text("Values from all tokens so far", font_size=16, color=GREEN).next_to(value_matrix, DOWN, buff=0.5)
        
        # Fade in matrices
        self.play(
            FadeIn(query_matrix), Write(query_token_label), Write(query_explanation),
            FadeIn(key_matrix), Write(key_token_labels), Write(key_explanation),
            FadeIn(value_matrix), Write(value_token_labels), Write(value_explanation)
        )
        self.wait(2)
        
        # Clear previous step
        self.play(
            FadeOut(step2),
            FadeOut(query_explanation),
            FadeOut(key_explanation),
            FadeOut(value_explanation)
        )
        
        # Step 3: Compute attention scores
        step3 = Text("Step 3: Compute attention scores (Q·K^T)", font_size=28)
        step3.next_to(token_seq, DOWN)
        self.play(Write(step3))
        
        # Create QK^T calculation visualization
        qk_formula = MathTex("Q \\cdot K^{T} = ").scale(1.2)
        qk_formula.next_to(step3, DOWN, buff=1.0).to_edge(LEFT).shift(RIGHT * 3)
        
        # Create attention score matrix (1x4 - one score per token)
        attention_scores = VGroup()
        
        # Create random scores that decrease for earlier tokens
        # (reflecting how attention often focuses more on recent tokens)
        scores = [0.15, 0.2, 0.25, 0.4]  # Example scores summing to 1
        
        for i, score in enumerate(scores):
            score_box = Rectangle(height=0.6, width=0.8, fill_color=YELLOW, fill_opacity=score)
            score_text = Text(f"{score:.2f}", font_size=16)
            score_text.move_to(score_box.get_center())
            
            if i == 0:
                score_box.next_to(qk_formula, RIGHT, buff=0.5)
            else:
                score_box.next_to(attention_scores[-1], RIGHT, buff=0.2)
            
            score_group = VGroup(score_box, score_text)
            attention_scores.add(score_group)
        
        # Add token labels below attention scores
        score_token_labels = VGroup()
        for i, token in enumerate(tokens):
            label = Text(token, font_size=16)
            label.next_to(attention_scores[i], DOWN, buff=0.2)
            score_token_labels.add(label)
        
        self.play(Write(qk_formula))
        self.play(FadeIn(attention_scores), Write(score_token_labels))
        
        # Add explanation for dot product
        dot_product_explanation = Text(
            "Each score shows how much \"=\" should attend to each token",
            font_size=16
        ).next_to(attention_scores, DOWN, buff=0.8)
        self.play(Write(dot_product_explanation))
        self.wait(2)
        
        # Step 4: Apply Softmax to get attention weights
        self.play(
            FadeOut(step3),
            FadeOut(dot_product_explanation)
        )
        
        step4 = Text("Step 4: Apply Softmax to get attention weights", font_size=28)
        step4.next_to(token_seq, DOWN)
        self.play(Write(step4))
        
        # Softmax formula
        softmax_formula = MathTex("\\text{softmax}(Q \\cdot K^{T}) = ").scale(1.2)
        softmax_formula.next_to(step4, DOWN, buff=1.0).to_edge(LEFT).shift(RIGHT * 3)
        
        # Transform from raw scores to softmax
        softmax_scores = VGroup()
        
        # Create softmax weights (normalized, sum to 1)
        weights = [0.1, 0.15, 0.25, 0.5]  # Example weights after softmax
        
        for i, weight in enumerate(weights):
            weight_box = Rectangle(height=0.6, width=0.8, fill_color=YELLOW, fill_opacity=weight)
            weight_text = Text(f"{weight:.2f}", font_size=16)
            weight_text.move_to(weight_box.get_center())
            
            if i == 0:
                weight_box.next_to(softmax_formula, RIGHT, buff=0.5)
            else:
                weight_box.next_to(softmax_scores[-1], RIGHT, buff=0.2)
            
            weight_group = VGroup(weight_box, weight_text)
            softmax_scores.add(weight_group)
        
        # Keep token labels for softmax outputs
        softmax_token_labels = VGroup()
        for i, token in enumerate(tokens):
            label = Text(token, font_size=16)
            label.next_to(softmax_scores[i], DOWN, buff=0.2)
            softmax_token_labels.add(label)
        
        # Animation: transform from raw scores to softmax
        self.play(
            Transform(qk_formula, softmax_formula),
            Transform(attention_scores, softmax_scores),
            FadeOut(score_token_labels)
        )
        self.play(Write(softmax_token_labels))
        
        # Explanation of softmax
        softmax_explanation = Text(
            "Softmax normalizes scores into a probability distribution",
            font_size=16
        ).next_to(softmax_scores, DOWN, buff=0.8)
        self.play(Write(softmax_explanation))
        self.wait(2)
        
        # Step 5: Calculate weighted sum of values
        self.play(
            FadeOut(step4),
            FadeOut(softmax_explanation)
        )
        
        step5 = Text("Step 5: Calculate weighted sum of values", font_size=28)
        step5.next_to(token_seq, DOWN)
        self.play(Write(step5))
        
        # Create visualization of weighted values
        weighted_sum_formula = MathTex("\\text{Attention} = \\text{softmax}(Q \\cdot K^{T}) \\cdot V").scale(1.2)
        weighted_sum_formula.next_to(step5, DOWN, buff=1.0)
        
        self.play(Write(weighted_sum_formula))
        
        # Visualization of weighted value vectors
        weighted_values = VGroup()
        
        # Create a visualization of weighting the value vectors
        for i, weight in enumerate(weights):
            # Create a row from the value matrix (simplified)
            value_row = Rectangle(
                height=0.6, 
                width=2.0, 
                fill_color=GREEN, 
                fill_opacity=weight
            )
            
            if i == 0:
                value_row.next_to(weighted_sum_formula, DOWN, buff=1.0).to_edge(LEFT).shift(RIGHT * 3)
            else:
                value_row.next_to(weighted_values[-1], DOWN, buff=0.2)
            
            # Add token and weight
            token_text = Text(f"{tokens[i]}: ", font_size=16).next_to(value_row, LEFT, buff=0.2)
            weight_text = Text(f"× {weight:.2f}", font_size=16).next_to(value_row, RIGHT, buff=0.2)
            
            row_group = VGroup(value_row, token_text, weight_text)
            weighted_values.add(row_group)
        
        self.play(FadeIn(weighted_values))
        
        # Create output vector
        output_arrow = Arrow(weighted_values[-1].get_bottom() + DOWN * 0.5, weighted_values[-1].get_bottom() + DOWN * 1.0, buff=0.1)
        output_text = Text("Sum", font_size=18).next_to(output_arrow, RIGHT, buff=0.2)
        
        self.play(GrowArrow(output_arrow), Write(output_text))
        
        # Output vector (weighted sum of values)
        output_vector = Rectangle(
            height=0.6, 
            width=2.0, 
            fill_color=PURPLE, 
            fill_opacity=0.8
        ).next_to(output_arrow, DOWN, buff=0.2)
        output_label = Text("Output context vector", font_size=16).next_to(output_vector, RIGHT, buff=0.2)
        
        self.play(FadeIn(output_vector), Write(output_label))
        self.wait(2)
        
        # Step 6: Final projection and residual connection
        self.play(
            FadeOut(step5),
            FadeOut(weighted_sum_formula),
            FadeOut(weighted_values),
            FadeOut(output_arrow),
            FadeOut(output_text),
        )
        
        step6 = Text("Step 6: Project and add residual connection", font_size=28)
        step6.next_to(token_seq, DOWN)
        self.play(Write(step6))
        
        # Final formula showing the whole process
        final_formula = MathTex(
            "\\text{Output}_{=} = W^{\\text{proj}} \\cdot (\\text{Attention}) + \\text{Residual}_{=}"
        ).scale(1.2)
        final_formula.next_to(step6, DOWN, buff=1.0)
        
        self.play(Write(final_formula))
        
        # Create visual of projection and residual connection
        projection_rect = Rectangle(
            height=0.6, 
            width=2.0, 
            fill_color=PURPLE_A, 
            fill_opacity=0.8
        ).next_to(final_formula, DOWN, buff=1.0)
        
        plus_symbol = MathTex("+").next_to(projection_rect, RIGHT, buff=0.5)
        
        residual_rect = Rectangle(
            height=0.6, 
            width=2.0, 
            fill_color=BLUE_A, 
            fill_opacity=0.8
        ).next_to(plus_symbol, RIGHT, buff=0.5)
        
        equals_symbol = MathTex("=").next_to(residual_rect, RIGHT, buff=0.5)
        
        output_rect = Rectangle(
            height=0.6, 
            width=2.0, 
            fill_color=YELLOW_A, 
            fill_opacity=0.8
        ).next_to(equals_symbol, RIGHT, buff=0.5)
        
        projection_label = Text("Projected\nattention", font_size=14).next_to(projection_rect, DOWN, buff=0.2)
        residual_label = Text("Residual\nconnection", font_size=14).next_to(residual_rect, DOWN, buff=0.2)
        output_label_final = Text("Final output\nfor \"=\" token", font_size=14).next_to(output_rect, DOWN, buff=0.2)
        
        self.play(
            FadeIn(projection_rect), Write(projection_label),
            Write(plus_symbol),
            FadeIn(residual_rect), Write(residual_label),
            Write(equals_symbol),
            FadeIn(output_rect), Write(output_label_final)
        )
        
        # Key insight - relate back to the math example
        self.wait(2)
        
        # Show the final calculation from the original code
        final_result = Text("26 + 55 = 81", font_size=36, color=YELLOW)
        final_result.move_to([0, -5, 0])
        
        highlight_rect = SurroundingRectangle(final_result, color=YELLOW, buff=0.3)
        
        self.play(
            Write(final_result),
            Create(highlight_rect),
            run_time=2
        )
        
        # Explanation connecting the attention mechanism to solving math
        math_insight = Text(
            "Through self-attention, the \"=\" token can look back at \"26\", \"+\", and \"55\"\nto compute the correct result: 81",
            font_size=24,
            color=WHITE
        ).next_to(final_result, DOWN, buff=0.5)
        
        self.play(Write(math_insight))
        
        self.wait(3)
        
        # Fade everything out
        self.play(FadeOut(Group(*self.mobjects)))