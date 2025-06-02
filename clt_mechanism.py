from manim import *
import numpy as np

class CLTAnimation(Scene):
    def construct(self):
        # Title
        title = Tex(r"\text{Cross-Layer Transcoder (CLT)}", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Create the main architecture
        self.setup_architecture()
        
    def setup_architecture(self):
        # Create three main components
        self.encoder_box = Rectangle(width=2.5, height=1.5, color=GREEN)
        self.sparse_box = Rectangle(width=2.5, height=1.5, color=ORANGE)
        self.decoder_box = Rectangle(width=2.5, height=1.5, color=BLUE)
        
        # Position them
        self.encoder_box.shift(LEFT * 4)
        self.sparse_box.shift(ORIGIN)
        self.decoder_box.shift(RIGHT * 4)
        
        # Labels
        encoder_label = Tex(r"\text{Encoder}\\\text{(dense)}", font_size=30, color=WHITE)
        sparse_label = Tex(r"\text{Sparse}\\\text{Activation}", font_size=30, color=WHITE)
        decoder_label = Tex(r"\text{Decoder}\\\text{(dense)}", font_size=30, color=WHITE)
        
        encoder_label.move_to(self.encoder_box.get_center())
        sparse_label.move_to(self.sparse_box.get_center())
        decoder_label.move_to(self.decoder_box.get_center())
        
        # Weight matrices labels
        w_e_label = MathTex("W_e", font_size=24, color=GREEN).next_to(self.encoder_box, DOWN)
        w_d_label = MathTex("W_d", font_size=24, color=BLUE).next_to(self.decoder_box, DOWN)
        
        # Dimension labels
        input_dim = Tex(r"\text{768-D}\\\text{embeddings}", font_size=25, color=GRAY).next_to(self.encoder_box, LEFT)
        sparse_dim = Tex(r"\text{16,384 features}\\\text{(\textasciitilde5 active)}", font_size=25, color=GRAY).next_to(self.sparse_box, DOWN, buff=0.5)
        output_dim = Tex(r"\text{768-D}\\\text{embeddings}", font_size=25, color=GRAY).next_to(self.decoder_box, RIGHT)
        
        # ReLU + L1 loss label
        loss_label = Tex(r"\text{ReLU + L1 loss}", font_size=25, color=RED).next_to(self.sparse_box, UP)
        
        # Arrows
        arrow1 = Arrow(self.encoder_box.get_right(), self.sparse_box.get_left(), color=WHITE)
        arrow2 = Arrow(self.sparse_box.get_right(), self.decoder_box.get_left(), color=WHITE)
        
        # Animate the setup
        self.play(
            Create(self.encoder_box),
            Create(self.sparse_box),
            Create(self.decoder_box),
            Write(encoder_label),
            Write(sparse_label),
            Write(decoder_label)
        )
        
        self.play(
            Write(w_e_label),
            Write(w_d_label),
            Write(input_dim),
            Write(sparse_dim),
            Write(output_dim),
            Write(loss_label)
        )
        
        self.play(Create(arrow1), Create(arrow2))
        self.wait(1)
        
        # Store references
        self.components = VGroup(
            self.encoder_box, self.sparse_box, self.decoder_box,
            encoder_label, sparse_label, decoder_label,
            w_e_label, w_d_label, input_dim, sparse_dim, output_dim,
            loss_label, arrow1, arrow2
        )