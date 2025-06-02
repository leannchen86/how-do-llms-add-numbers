from manim import *
import random

class AdditionExamples(Scene):
    def construct(self):
        # Create training examples for a simple addition model
        self.create_training_examples()
        
    def create_training_examples(self):
        # Title
        title = Tex(r"\text{Training Data: Addition Examples}", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Generate multiple addition examples
        examples = [
            ("12 + 34", "46"),
            ("25 + 17", "42"), 
            ("9 + 8", "17"),
            ("33 + 22", "55"),
            ("45 + 15", "60"),
            ("7 + 13", "20")
        ]
        
        # Create a grid of examples
        example_groups = VGroup()
        
        for i, (problem, answer) in enumerate(examples):
            # Create input-output pair
            input_box = Rectangle(width=2.5, height=0.8, color=BLUE, fill_opacity=0.3)
            input_text = Tex(rf"\text{{{problem}}}", font_size=18)
            input_text.move_to(input_box)
            input_group = VGroup(input_box, input_text)
            
            # Arrow
            arrow = Arrow(ORIGIN, RIGHT * 1.5, stroke_width=3)
            
            # Output box
            output_box = Rectangle(width=1.5, height=0.8, color=GREEN, fill_opacity=0.3)
            output_text = Tex(answer, font_size=18)
            output_text.move_to(output_box)
            output_group = VGroup(output_box, output_text)
            
            # Arrange horizontally
            example = VGroup(input_group, arrow, output_group)
            example.arrange(RIGHT, buff=0.3)
            
            example_groups.add(example)
        
        # Arrange examples in a grid (2 columns, 3 rows)
        rows = VGroup()
        for i in range(0, len(example_groups), 2):
            if i + 1 < len(example_groups):
                row = VGroup(example_groups[i], example_groups[i + 1])
                row.arrange(RIGHT, buff=2)
            else:
                row = example_groups[i]
            rows.add(row)
        
        rows.arrange(DOWN, buff=1)
        rows.move_to(ORIGIN + DOWN * 0.5)
        
        # Animate examples appearing
        for row in rows:
            if isinstance(row, VGroup) and len(row) > 1:
                self.play(*[FadeIn(example, shift=UP*0.5) for example in row], run_time=1)
            else:
                self.play(FadeIn(row, shift=UP*0.5), run_time=1)
            self.wait(0.5)
        
        self.wait(2)
        
        # Add explanation
        explanation = Tex(
            r"\text{The model learns to map arithmetic expressions to their results}",
            font_size=24,
            color=GRAY
        ).to_edge(DOWN)
        
        self.play(Write(explanation))
        self.wait(2)