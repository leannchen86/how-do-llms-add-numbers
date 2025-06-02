from manim import *

class VectorComparison(Scene):
    def construct(self):
        # Title
        title = Text("Sparse vs Dense Vectors").scale(0.8)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))
        
        # Create sparse and dense vector data
        sparse_vector = [0, 0, 3, 0, 2, 0, 0, 1, 0, 0]
        dense_vector = [0.1, -0.3, 0.7, 0.2, 0.5, -0.1, 0.4, 0.6, -0.2, 0.3]
        
        # Create document examples that match sparse vector frequencies
        documents = [
            "The quick brown fox jumps over the lazy dog.",
            "His brown eyes watched the fox carefully.",
            "She wore a brown coat walking through the park."
        ]
        
        # Keywords that correspond to non-zero values in sparse vector
        keywords = {
            "brown": 2,  # Index 2 has value 3 (frequency count)
            "fox": 4,    # Index 4 has value 2 (frequency count)
            "dog": 7     # Index 7 has value 1 (frequency count)
        }
        
        # Create frequency counter visualization
        freq_counter = self.create_frequency_counter(documents, keywords)
        freq_counter.to_edge(UP).shift(DOWN * 0.8 + LEFT * 2)
        
        # Show documents first with enhanced highlighting
        doc_viz = self.create_document_visualization(documents, keywords)
        doc_viz.to_edge(UP).shift(DOWN * 0.8 + RIGHT * 2)
        
        self.play(Create(doc_viz))
        self.wait(0.5)
        self.play(Create(freq_counter))
        self.wait(1)
        
        # Create vector visuals
        sparse_visual = self.create_vector_visual(
            sparse_vector,
            "Sparse Vector",
            fill_colors=[YELLOW if val != 0 else None for val in sparse_vector]
        )
        sparse_visual.next_to(VGroup(doc_viz, freq_counter), DOWN, buff=0.8)
        
        dense_visual = self.create_vector_visual(
            dense_vector,
            "Dense Vector",
            # Gradient colors for dense vector
            fill_colors=[
                interpolate_color(BLUE, RED, (val + 0.3)/0.8) if val < 0 
                else interpolate_color(WHITE, GREEN, val/0.7)
                for val in dense_vector
            ]
        )
        dense_visual.next_to(sparse_visual, DOWN, buff=0.8)
        
        # Show sparse vector and connect to keywords with better connections
        self.play(Create(sparse_visual))
        self.wait(0.5)
        
        # Create clearer connections between keywords and sparse vector
        connections = self.create_keyword_connections(doc_viz, freq_counter, sparse_visual, keywords)
        self.play(Create(connections))
        self.wait(2)
        
        # Add frequency labels to show counts more clearly
        freq_labels = self.create_frequency_labels(freq_counter, sparse_visual, keywords)
        self.play(Write(freq_labels))
        self.wait(1.5)
        
        # Show dense vector
        self.play(Create(dense_visual))
        self.wait(1)
        
        # Highlight all values in dense vector to show they all matter
        self.highlight_dense_values(dense_visual)
        self.wait(2)
        
        # Fade out connections and frequency labels
        self.play(FadeOut(connections), FadeOut(freq_labels))
        self.wait(1)
        
        # Show vector space visualization
        vector_space = self.create_vector_space()
        vector_space.scale(0.8).to_corner(DR)
        self.play(
            *[FadeOut(obj) for obj in [doc_viz, freq_counter, sparse_visual, dense_visual]],
            Create(vector_space)
        )
        self.wait(2)
    
    def create_frequency_counter(self, documents, keywords):
        """Create a visual frequency counter for keywords."""
        counts = {keyword: 0 for keyword in keywords}
        
        # Count occurrences
        for doc in documents:
            for keyword in keywords:
                # Count all occurrences in the document
                counts[keyword] += doc.lower().count(keyword.lower())
        
        # Create visual counter
        counter_group = VGroup()
        
        # Title for the counter
        counter_title = Text("Keyword Frequencies", font_size=20)
        counter_group.add(counter_title)
        
        # Create counter visuals
        for keyword, count in counts.items():
            keyword_text = Text(f"{keyword}:", font_size=18)
            
            # Create count circles
            count_circles = VGroup()
            for i in range(count):
                circle = Circle(radius=0.15, color=YELLOW, fill_opacity=0.8, fill_color=YELLOW)
                count_circles.add(circle)
            
            count_circles.arrange(RIGHT, buff=0.1)
            
            # Add count number
            count_text = Text(f"{count}", font_size=18).next_to(count_circles, RIGHT)
            
            row = VGroup(keyword_text, count_circles, count_text).arrange(RIGHT, buff=0.3)
            counter_group.add(row)
        
        # Arrange all elements
        counter_group.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        return counter_group
        
    def create_document_visualization(self, documents, keywords):
        """Create a visualization of documents with highlighted keywords."""
        doc_rects = VGroup()
        
        for i, doc in enumerate(documents):
            # Create base rectangle for document
            rect = Rectangle(height=0.6, width=5, fill_color=GREY_E, fill_opacity=0.2)
            
            # Create text lines (abstract representation)
            lines = VGroup(*[
                Line(
                    start=rect.get_left() + RIGHT * 0.2 + DOWN * (0.1 * j - 0.15),
                    end=rect.get_right() + LEFT * 0.2 + DOWN * (0.1 * j - 0.15),
                    stroke_width=1, stroke_opacity=0.5, color=GREY
                )
                for j in range(3)
            ])
            
            # Add actual text for the document (small)
            doc_text = Text(doc, font_size=14)
            doc_text.set_width(rect.width - 0.4)
            doc_text.move_to(rect)
            
            # Highlight keywords with more emphasis
            keyword_highlights = VGroup()
            for keyword, idx in keywords.items():
                if keyword in doc.lower():
                    # Find all occurrences of the keyword
                    start_idx = 0
                    while True:
                        start_idx = doc.lower().find(keyword, start_idx)
                        if start_idx == -1:
                            break
                        end_idx = start_idx + len(keyword)
                        
                        # Create highlighted keyword with background highlight
                        keyword_text = Text(doc[start_idx:end_idx], font_size=14, color=BLACK)
                        highlight_box = Rectangle(
                            height=keyword_text.height + 0.05,
                            width=keyword_text.width + 0.05,
                            fill_color=YELLOW,
                            fill_opacity=1,
                            stroke_width=0
                        )
                        highlight_box.move_to(keyword_text)
                        
                        # Group the highlight and text
                        keyword_group = VGroup(highlight_box, keyword_text)
                        
                        # Position it based on the original text
                        orig_text_width = doc_text.width
                        relative_pos = (start_idx / len(doc) - 0.5) * orig_text_width
                        keyword_group.move_to(doc_text).shift(RIGHT * relative_pos)
                        
                        # Add to keyword highlights
                        keyword_highlights.add(keyword_group)
                        start_idx = end_idx
            
            # Combine elements (add keyword highlights as separate group)
            doc_group = VGroup(rect, lines, doc_text, keyword_highlights)
            doc_rects.add(doc_group)
        
        # Arrange documents vertically
        doc_rects.arrange(DOWN, buff=0.2)
        
        # Add label
        label = Text("Documents", font_size=20).next_to(doc_rects, UP)
        
        return VGroup(label, doc_rects)
    
    def create_vector_visual(self, vector, label, fill_colors=None):
        """Create visualization of a vector."""
        cells = VGroup(*[
            Square(side_length=0.5)
            for _ in vector
        ]).arrange(RIGHT, buff=0.05)
        
        # Add dimension indices
        dim_indices = VGroup(*[
            Text(f"{i}", font_size=12).next_to(cell, DOWN, buff=0.1)
            for i, cell in enumerate(cells)
        ])
        
        # Apply colors to cells
        if fill_colors:
            for cell, color in zip(cells, fill_colors):
                if color:
                    cell.set_fill(color=color, opacity=0.7)
                    cell.set_stroke(color=WHITE, width=2)
                else:
                    cell.set_fill(opacity=0.1)
                    cell.set_stroke(color=GREY, width=1)
        
        # Add values
        values = VGroup(*[
            Text(f"{val:.1f}" if isinstance(val, float) else str(val), 
                 font_size=16, 
                 color=BLACK if val != 0 and (isinstance(val, int) or abs(val) > 0.3) else WHITE
                ).move_to(cell)
            for val, cell in zip(vector, cells)
        ])
        
        label_text = Text(label, font_size=20).next_to(cells, LEFT)
        return VGroup(cells, values, dim_indices, label_text)
    
    def create_keyword_connections(self, doc_viz, freq_counter, sparse_visual, keywords):
        """Create clearer connections between keywords, frequency counters and sparse vector cells."""
        connections = VGroup()
        doc_rects = doc_viz[1]
        freq_rows = freq_counter[1:]  # Skip the title
        cells = sparse_visual[0]
        
        # Connect from frequency counter to sparse vector
        for i, (keyword, idx) in enumerate(keywords.items()):
            freq_row = freq_rows[i]
            
            # Create a curved arrow from frequency counter to vector cell
            arrow = CurvedArrow(
                start_point=freq_row.get_right(),
                end_point=cells[idx].get_top(),
                angle=TAU/4,
                color=YELLOW,
                stroke_width=2
            )
            connections.add(arrow)
        
        # Connect from document keywords to frequency counter
        for keyword, idx in keywords.items():
            # Find the corresponding frequency row
            freq_row_idx = list(keywords.keys()).index(keyword)
            freq_row = freq_rows[freq_row_idx]
            
            # Find all occurrences of highlighted keywords
            for doc_group in doc_rects:
                keyword_highlights = doc_group[3]  # The keyword highlights group
                
                for highlight_group in keyword_highlights:
                    highlight_box = highlight_group[0]  # The highlight box
                    keyword_text = highlight_group[1]  # The keyword text
                    
                    if keyword_text.text.lower() == keyword.lower():
                        # Create dashed line from keyword to frequency counter
                        dashed_line = DashedLine(
                            start=highlight_box.get_edge_center(RIGHT),
                            end=freq_row.get_edge_center(LEFT),
                            dash_length=0.05,
                            dashed_ratio=0.5,
                            color=YELLOW,
                            stroke_width=1
                        )
                        connections.add(dashed_line)
        
        return connections
    
    def create_frequency_labels(self, freq_counter, sparse_visual, keywords):
        """Create labels that explicitly show how frequencies map to sparse vector values."""
        labels = VGroup()
        freq_rows = freq_counter[1:]  # Skip the title
        cells = sparse_visual[0]
        values = sparse_visual[1]
        
        for i, (keyword, idx) in enumerate(keywords.items()):
            freq_row = freq_rows[i]
            cell = cells[idx]
            value = values[idx]
            
            # Create an arrow pointing to the value in the sparse vector
            annotation = Text(
                f"Frequency of '{keyword}' = {value.text}",
                font_size=14,
                color=YELLOW
            )
            
            annotation.next_to(cell, UP, buff=0.7)
            labels.add(annotation)
            
            # Add arrow
            arrow = Arrow(
                start=annotation.get_bottom(),
                end=cell.get_top(),
                buff=0.1,
                color=YELLOW,
                stroke_width=2
            )
            labels.add(arrow)
        
        return labels
    
    def highlight_dense_values(self, dense_visual):
        """Animate highlighting all values in the dense vector."""
        cells = dense_visual[0]
        values = dense_visual[1]
        
        # Highlight groups of cells to show patterns
        groups = [
            [0, 1, 2],   # First few dimensions
            [3, 4, 5],   # Middle dimensions  
            [6, 7, 8, 9] # Last dimensions
        ]
        
        for group in groups:
            self.play(*[
                Flash(cells[i], color=BLUE if float(values[i].text) < 0 else GREEN, flash_radius=0.3)
                for i in group
            ], run_time=0.7)
    
    def create_vector_space(self):
        """Create a 2D visualization of vector space with documents."""
        # Create axes
        axes = Axes(
            x_range=[-3, 3], y_range=[-3, 3],
            axis_config={"include_tip": True}
        ).scale(0.7)
        
        # Add labels
        x_label = Text("Dimension 1", font_size=16).next_to(axes.x_axis, DOWN)
        y_label = Text("Dimension 2", font_size=16).next_to(axes.y_axis, LEFT)
        
        # Create sparse vector points (only along axes)
        sparse_docs = VGroup(*[
            Dot(point=axes.c2p(2, 0), color=RED),   # Documents with "fox"
            Dot(point=axes.c2p(0, 2), color=RED),   # Documents with "dog"
            Dot(point=axes.c2p(-2, 0), color=RED),  # Documents with "brown"
            Dot(point=axes.c2p(0, 0), color=RED),   # Documents with nothing
        ])
        
        # Create dense vector points (distributed across space)
        dense_docs = VGroup(*[
            Dot(point=axes.c2p(2.2, 1.5), color=BLUE),   # Dog and fox
            Dot(point=axes.c2p(1.8, 1.7), color=BLUE),   # Puppy
            Dot(point=axes.c2p(1.5, 0.5), color=BLUE),   # Animal
            Dot(point=axes.c2p(-1.8, -0.2), color=BLUE), # Color
            Dot(point=axes.c2p(-1.2, 1.2), color=BLUE),  # Pet
            Dot(point=axes.c2p(0.8, -1.5), color=BLUE),  # Hunting
        ])
        
        # Labels
        sparse_label = Text("Sparse", color=RED, font_size=16).next_to(sparse_docs, RIGHT)
        dense_label = Text("Dense", color=BLUE, font_size=16).next_to(dense_docs, LEFT)
        
        return VGroup(axes, x_label, y_label, sparse_docs, dense_docs, sparse_label, dense_label)