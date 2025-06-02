from manim import *

class MassiveTrainingData(Scene):
    def construct(self):
        # Create a much larger set of addition examples (40+)
        equation_data = [
            "1 + 2 = 3",
            "3 + 4 = 7", 
            "10 + 19 = 29",
            "5 + 7 = 12",
            "8 + 6 = 14",
            "23 + 45 = 68",
            "37 + 26 = 63",
            "42 + 58 = 100",
            "9 + 3 = 12",
            "15 + 7 = 22",
            "16 + 27 = 43",
            "19 + 31 = 50",
            "45 + 55 = 100",
            "72 + 39 = 111",
            "125 + 75 = 200",
            "64 + 17 = 81",
            "33 + 67 = 100",
            "82 + 9 = 91",
            "11 + 22 = 33",
            "44 + 88 = 132",
            "12 + 24 = 36",
            "51 + 49 = 100",
            "27 + 73 = 100",
            "13 + 57 = 70",
            "61 + 18 = 79",
            "256 + 144 = 400",
            "99 + 1 = 100",
            "88 + 12 = 100",
            "77 + 23 = 100",
            "66 + 34 = 100",
            "55 + 45 = 100",
            "144 + 36 = 180",
            "225 + 75 = 300",
            "17 + 28 = 45",
            "29 + 63 = 92",
            "41 + 59 = 100",
            "38 + 62 = 100",
            "49 + 51 = 100",
            "123 + 456 = 579",
            "321 + 654 = 975",
        ]
        
        # Define grid dimensions
        cols = 5
        rows = 8
        
        # Create math text objects for each equation and make them smaller
        equations = [MathTex(eq).scale(0.6) for eq in equation_data]
        
        # Position equations in a grid
        equation_group = VGroup(*equations).arrange_in_grid(
            rows=rows, cols=cols, buff=0.4
        ).scale(0.9).center()
        
        # Create a title to emphasize the "training data" concept
        title = Text("Training Data: Addition Examples", font_size=36).to_edge(UP)
        self.play(Write(title), run_time=0.5)
        
        # Group equations by row
        equation_rows = []
        for i in range(rows):
            start_idx = i * cols
            end_idx = min(start_idx + cols, len(equations))
            if start_idx < len(equations):
                row_equations = equations[start_idx:end_idx]
                equation_rows.append(VGroup(*row_equations))
        
        # Phase 1: Rapidly introduce equations row by row
        for i, row in enumerate(equation_rows):
            # Make rows appear faster as we go to convey increasing pace
            run_time = max(0.3 - i * 0.03, 0.1)
            
            # Slightly different animation for each row to add visual variety
            if i % 3 == 0:
                self.play(FadeIn(row, shift=0.1*DOWN), run_time=run_time)
            elif i % 3 == 1:
                self.play(Write(row), run_time=run_time)
            else:
                self.play(AddTextLetterByLetter(row), run_time=run_time)
        
        self.wait(0.5)  # Brief pause to see all equations
        
        # Phase 2: Rapidly fade out rows in reverse order
        # First half of rows fade one by one
        for row in equation_rows[::-1][:len(equation_rows)//2]:
            self.play(FadeOut(row), run_time=0.2)
        
        # Remaining rows disappear more quickly in groups
        remaining_rows = equation_rows[:len(equation_rows)//2]
        if remaining_rows:
            remaining_group = VGroup(*remaining_rows)
            self.play(FadeOut(remaining_group), run_time=0.3)
        
        # Fade out title
        self.play(FadeOut(title), run_time=0.2)