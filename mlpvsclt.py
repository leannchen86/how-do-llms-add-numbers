from manim import *
import numpy as np

class MLPvsCLTComparison(Scene):
    def construct(self):
        # Set custom colors for better visual differentiation
        MLP_COLOR = "#87CEEB"         # Light blue
        CLT_COLOR = "#87CEEB"         # Light blue
        ACTIVE_MLP_COLOR = "#4682B4"  # Steel blue
        ACTIVE_CLT_COLOR = "#FF6B6B"  # Coral red

        # Create MLP model positioned off-screen to the left
        mlp_model, mlp_inputs, mlp_output = self.create_mlp_model(MLP_COLOR)
        mlp_model.shift(LEFT * 12)

        # Create MLP title positioned off-screen to the left
        mlp_title = Tex(r"\text{MLP (Polysemantic)}", font_size=35, color=MLP_COLOR)
        mlp_title.move_to([-15.5, 2.5, 0])

        # Add models to scene (but they're off-screen)
        self.add(mlp_model, mlp_title)

        # Slide MLP in from the left to center
        self.play(
            mlp_model.animate.move_to(ORIGIN).scale(1.2),
            mlp_title.animate.move_to(ORIGIN).scale(1.2).to_edge(UP, buff=0.7),
            rate_func=smooth,
            run_time=1.5
        )

        # Now add a neuron label and arrow
        neuron_label = Tex(r"\text{Neuron}", font_size=32, color=MLP_COLOR).move_to([3, 2.5, 0])
        neuron_label.set_stroke(BLACK, width=3, opacity=0.8, background=True)
        self.play(FadeIn(neuron_label, scale=1.2))

        network_group, connections = mlp_model
        network = network_group  # unchanged 3→5→5→1 structure
        neuron_arrow = Arrow(
            neuron_label.get_bottom() + DOWN * 0.1,
            network[2][3].get_center() + UP * 0.2,  # middle neuron in hidden layer
            buff=0.1,
            color=MLP_COLOR,
            stroke_width=3,
            tip_length=0.2
        )
        self.play(GrowArrow(neuron_arrow))
        self.wait(0.7)
        self.play(FadeOut(neuron_arrow), FadeOut(neuron_label))

        # Demonstrate polysemantic neurons (with specific neurons firing together)
        self.demonstrate_polysemantic_neurons(mlp_model, ACTIVE_MLP_COLOR, MLP_COLOR)

        # Create CLT model off-screen to the right
        clt_model, clt_inputs, clt_output = self.create_clt_model(CLT_COLOR)
        clt_model.shift(RIGHT * 12)

        clt_title = Tex(r"\text{CLT (Monosemantic)}", font_size=35, color=CLT_COLOR)
        clt_title.move_to([15.5, 2.5, 0])

        feature_label = Tex(r"\text{Feature}", font_size=32, color=CLT_COLOR).move_to([30, 3.5, 0])
        feature_label.set_stroke(BLACK, width=3, opacity=0.8, background=True)

        self.add(clt_model, clt_title, feature_label)

        # Transition: MLP off, CLT in
        self.play(
            mlp_model.animate.shift(LEFT * 12).scale(1 / 1.2),
            mlp_title.animate.shift(LEFT * 12),
            run_time=1.2,
            rate_func=rush_into
        )
        self.play(
            clt_model.animate.move_to(ORIGIN).scale(1.2),
            clt_title.animate.move_to(ORIGIN).scale(1.2).to_edge(UP, buff=0.7),
            feature_label.animate.move_to([5.5, 3.0, 0]),
            run_time=1.2,
            rate_func=smooth
        )

        clt_network_group, clt_connections = clt_model
        clt_network = clt_network_group
        feature_arrow = Arrow(
            feature_label.get_bottom() + DOWN * 0.1,
            clt_network[3][3].get_center() + UP * 0.2,  # middle feature in layer 3
            buff=0.1,
            color=CLT_COLOR,
            stroke_width=3,
            tip_length=0.2
        )
        self.play(GrowArrow(feature_arrow))
        self.wait(0.7)
        self.play(FadeOut(feature_arrow), FadeOut(feature_label))

        # Demonstrate interpretable features (with the immediate token‐fade fix)
        self.demonstrate_interpretable_features(clt_model, ACTIVE_CLT_COLOR, CLT_COLOR)

        # Final fadeout
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.5)

    def create_mlp_model(self, color=BLUE):
        network = VGroup()
        layers = 4
        nodes_per_layer = [3, 5, 5, 1]

        for i in range(layers):
            layer = VGroup()
            for j in range(nodes_per_layer[i]):
                node = Circle(radius=0.2, color=color)
                node.set_fill(color, opacity=0.3)
                node.move_to([i * 2 - 6, j - (nodes_per_layer[i] - 1) / 2, 0])
                layer.add(node)
            network.add(layer)

        connections = VGroup()
        for i in range(layers - 1):
            for node1 in network[i]:
                for node2 in network[i + 1]:
                    connection = Line(
                        node1.get_center(),
                        node2.get_center(),
                        stroke_opacity=0.4,
                        stroke_width=0.7,
                        stroke_color=color
                    )
                    connections.add(connection)

        inputs = [
            Tex("", font_size=30).next_to(network[0][0], LEFT),
            Tex("", font_size=30).next_to(network[0][1], LEFT),
            Tex("", font_size=30).next_to(network[0][2], LEFT)
        ]
        output = Tex("", font_size=34, color=GREEN).next_to(network[3][0], RIGHT)

        return VGroup(network, connections), inputs, output

    def create_clt_model(self, color=BLUE):
        network = VGroup()
        layers = 5
        nodes_per_layer = [4, 5, 5, 5, 1]

        for i in range(layers):
            layer = VGroup()
            for j in range(nodes_per_layer[i]):
                node = RoundedRectangle(
                    height=0.25,
                    width=0.25,
                    corner_radius=0.05,
                    color=color
                )
                node.set_fill(color, opacity=0.2)
                node.move_to([i * 1.8 - 3.6, j - (nodes_per_layer[i] - 1) / 2, 0])
                layer.add(node)
            network.add(layer)

        connections = VGroup()
        connection_map = [
            (0, 0, 1, 0),  # 26 → ≈20
            (0, 0, 1, 2),  # 26 → ends in 6
            (0, 2, 1, 1),  # 55 → ≈50
            (0, 2, 1, 3),  # 55 → ends in 5
            (1, 0, 2, 0),  # ≈20 → ≈70
            (1, 1, 2, 0),  # ≈50 → ≈70
            (1, 2, 2, 1),  # ends in 6 → units=1, carry=1
            (1, 3, 2, 1),  # ends in 5 → units=1, carry=1
            (1, 0, 2, 2),  # 2 + 5 + carry=8 (tens)
            (1, 1, 2, 2),
            (2, 1, 2, 2),  # carry
            (2, 0, 3, 0),  # ≈70 → ≈80 final
            (2, 1, 3, 1),  # units ≡1 (mod10)
            (2, 2, 3, 2),  # tens+carry ≡81 (mod100)
            (2, 1, 3, 2),  # carry → ≡81
            (3, 0, 4, 0),  # ≈80 → 81
            (3, 1, 4, 0),
            (3, 2, 4, 0)
        ]
        # Add connections from connection_map
        for layer1, node1, layer2, node2 in connection_map:
            connection = Line(
                network[layer1][node1].get_center(),
                network[layer2][node2].get_center(),
                stroke_opacity=0.3,
                stroke_width=0.5,
                stroke_color=color
            )
            connections.add(connection)

        # Add random connections
        np.random.seed(42)
        for layer_idx in range(layers - 1):
            current_layer_size = nodes_per_layer[layer_idx]
            next_layer_size = nodes_per_layer[layer_idx + 1]
            for i in range(current_layer_size):
                for j in range(next_layer_size):
                    existing = any(
                        (l1 == layer_idx and n1 == i and l2 == layer_idx + 1 and n2 == j)
                        for l1, n1, l2, n2 in connection_map
                    )
                    if not existing and np.random.random() < 0.7:
                        connection = Line(
                            network[layer_idx][i].get_center(),
                            network[layer_idx + 1][j].get_center(),
                            stroke_opacity=0.3,
                            stroke_width=0.5,
                            stroke_color=color
                        )
                        connections.add(connection)

        inputs = [
            Tex("", font_size=24).next_to(network[0][i], LEFT)
            for i in range(4)
        ]
        output = Tex("", font_size=26).next_to(network[-1][0], RIGHT)
        return VGroup(network, connections), inputs, output

    def demonstrate_polysemantic_neurons(self, model, active_color=BLUE, base_color=BLUE):
        # Unpack the MLP: model is VGroup(network_VGroup, connections_VGroup)
        network_group, connections = model
        network = network_group  # preserves 4-layer structure

        inputs = ["26", "seattle", "bird"]
        output_labels = ["number", "city", "animal"]
        shared_neurons = [(1, 2), (2, 1)]  # same indices as before

        for j, (input_text, output_label) in enumerate(zip(inputs, output_labels)):
            # Input label
            if input_text.isnumeric() or input_text in ['+', '-', '=', '*', '/']:
                input_label = Tex(f"{input_text}", font_size=32, color=WHITE)
            else:
                input_label = Tex(rf"\text{{{input_text}}}", font_size=32, color=WHITE)
            input_node = network[0][1]  # second neuron in first layer
            input_label.next_to(input_node, LEFT, buff=0.5)
            current_input_display = VGroup(input_label)

            # Output label
            if output_label.isnumeric() or output_label in ['+', '-', '=', '*', '/']:
                output_label_text = Tex(f"{output_label}", font_size=30, color=GREEN)
            else:
                output_label_text = Tex(rf"\text{{{output_label}}}", font_size=30, color=GREEN)
            output_node = network[-1][0]  # only neuron in last layer
            output_label_text.next_to(output_node, RIGHT, buff=0.5)
            current_output_display = VGroup(output_label_text)

            # Show input label
            self.play(FadeIn(current_input_display, shift=RIGHT * 0.3))

            # Identify shared neurons
            first_shared_neuron = network[shared_neurons[0][0]][shared_neurons[0][1]]
            second_shared_neuron = network[shared_neurons[1][0]][shared_neurons[1][1]]

            # Build simultaneous activation animations:
            sim_anims = []
            # 1) Flash + fill input_node
            sim_anims.append(Flash(input_node, color=active_color, flash_radius=0.4))
            sim_anims.append(input_node.animate.set_fill(active_color, opacity=0.9))
            # 2) Flash + fill first_shared_neuron
            sim_anims.append(Flash(first_shared_neuron, color=active_color, flash_radius=0.4))
            sim_anims.append(first_shared_neuron.animate.set_fill(active_color, opacity=0.9))
            # 3) Flash + fill second_shared_neuron
            sim_anims.append(Flash(second_shared_neuron, color=active_color, flash_radius=0.4))
            sim_anims.append(second_shared_neuron.animate.set_fill(active_color, opacity=0.9))
            # 4) Flash + fill output_node (use GREEN for output)
            sim_anims.append(Flash(output_node, color=GREEN, flash_radius=0.4))
            sim_anims.append(output_node.animate.set_fill(GREEN, opacity=0.7))

            # Also identify and flash the three connecting edges:
            #   a) input_node → first_shared_neuron
            #   b) first_shared_neuron → second_shared_neuron
            #   c) second_shared_neuron → output_node
            for conn in connections:
                start_pt = conn.get_start()
                end_pt = conn.get_end()
                if (np.allclose(start_pt, input_node.get_center(), atol=0.1) and
                    np.allclose(end_pt, first_shared_neuron.get_center(), atol=0.1)):
                    sim_anims.append(ShowPassingFlash(conn.copy().set_stroke(active_color, width=4, opacity=0.8), time_width=0.7))
                if (np.allclose(start_pt, first_shared_neuron.get_center(), atol=0.1) and
                    np.allclose(end_pt, second_shared_neuron.get_center(), atol=0.1)):
                    sim_anims.append(ShowPassingFlash(conn.copy().set_stroke(active_color, width=4, opacity=0.8), time_width=0.7))
                if (np.allclose(start_pt, second_shared_neuron.get_center(), atol=0.1) and
                    np.allclose(end_pt, output_node.get_center(), atol=0.1)):
                    sim_anims.append(ShowPassingFlash(conn.copy().set_stroke(GREEN, width=4, opacity=0.8), time_width=0.7))

            # Play all flashes and fills together
            self.play(*sim_anims, run_time=1.0)

            # Show output label
            self.play(FadeIn(current_output_display, shift=LEFT * 0.3))
            self.wait(0.5)

            # Reset fills back to base color
            reset_anims = [
                input_node.animate.set_fill(base_color, opacity=0.3),
                first_shared_neuron.animate.set_fill(base_color, opacity=0.3),
                second_shared_neuron.animate.set_fill(base_color, opacity=0.3),
                output_node.animate.set_fill(base_color, opacity=0.3),
                FadeOut(current_input_display),
                FadeOut(current_output_display)
            ]
            self.play(*reset_anims, run_time=0.5)

            if j < len(inputs) - 1:
                self.wait(0.2)

    def demonstrate_interpretable_features(self, model, active_color=RED, base_color=BLUE):
        network_group, connections = model
        network = network_group

        # Step definitions for CLT computation
        computation_steps = [
            {
                "phase": "Number parsing",
                "input_indices": [0, 2],  # "26" and "55"
                "layer": 1,
                "feature_indices": [0, 1, 2, 3]
            },
            {
                "phase": "Operation processing",
                "input_indices": [1],  # "+"
                "layer": 2,
                "feature_indices": [0, 1, 2]
            },
            {
                "phase": "Computation trigger",
                "input_indices": [3],  # "="
                "layer": 3,
                "feature_indices": [0, 1, 2]
            }
        ]

        # Create & show all feature labels (Layer 1 → Layer 3)
        all_feature_labels = []

        # Layer 1
        layer1_labels = [
            r"\approx 20",
            r"\approx 50",
            r"\text{ends in 6}",
            r"\text{ends in 5}"
        ]
        for i, label in enumerate(layer1_labels):
            feature_node = network[1][i]
            feature_text = MathTex(label, font_size=24, color=base_color)
            feature_text.next_to(feature_node, UP, buff=0.15)
            bg = BackgroundRectangle(feature_text, color=BLACK, fill_opacity=0.7, buff=0.03)
            all_feature_labels.append(VGroup(bg, feature_text))

        # Layer 2
        layer2_labels = [
            r"\approx 70",
            r"6 + 5 \rightarrow 1,\,\text{carry}",
            r"2 + 5 + 1 \rightarrow 8"
        ]
        for i, label in enumerate(layer2_labels):
            feature_node = network[2][i]
            feature_text = MathTex(label, font_size=22, color=base_color)
            feature_text.next_to(feature_node, UP, buff=0.15)
            bg = BackgroundRectangle(feature_text, color=BLACK, fill_opacity=0.7, buff=0.03)
            all_feature_labels.append(VGroup(bg, feature_text))

        # Layer 3
        layer3_labels = [
            r"\approx 80\,\text{final}",
            r"\equiv 1 \pmod{10}",
            r"\equiv 81 \pmod{100}"
        ]
        for i, label in enumerate(layer3_labels):
            feature_node = network[3][i]
            feature_text = MathTex(label, font_size=20, color=base_color)
            feature_text.next_to(feature_node, UP, buff=0.15)
            bg = BackgroundRectangle(feature_text, color=BLACK, fill_opacity=0.7, buff=0.03)
            all_feature_labels.append(VGroup(bg, feature_text))

        # Show all feature labels at once
        self.play(
            *[FadeIn(label, scale=0.8) for label in all_feature_labels],
            lag_ratio=0.05,
            run_time=2
        )
        self.wait(0.2)

        # 1) Fade in ALL input tokens *immediately* (so they're clearly visible before "81")
        all_input_displays = {}
        for input_text, input_idx in [('26', 0), ('+', 1), ('55', 2), ('=', 3)]:
            input_node = network[0][input_idx]
            if input_text.isnumeric() or input_text in ['+', '-', '=', '*', '/']:
                input_label = Tex(f"{input_text}", font_size=26, color=WHITE)
            else:
                input_label = Tex(rf"\text{{{input_text}}}", font_size=26, color=WHITE)
            input_label.next_to(input_node, LEFT, buff=0.2)
            all_input_displays[input_idx] = (VGroup(input_label), input_node)

        # Show tokens, then flash & fill them
        self.play(
            *[FadeIn(display[0]) for display, _ in all_input_displays.values()],
            run_time=0.4
        )
        token_anims = []
        for _, input_node in all_input_displays.values():
            token_anims.append(Flash(input_node, color=active_color, flash_radius=0.25))
            token_anims.append(input_node.animate.set_fill(active_color, opacity=0.8))
        self.play(*token_anims, run_time=0.6)

        self.wait(0.2)

        # Create (invisible) circles around each token to re‐highlight by step
        token_circles = []
        for _, (input_display, input_node) in all_input_displays.items():
            token_circle = Circle(
                radius=0.35,
                color=active_color,
                stroke_width=3,
                stroke_opacity=0  # start invisible
            ).move_to(input_node.get_center())
            token_circles.append(token_circle)
            self.add(token_circle)

        # 2) Now run through each computation phase in order
        for step_num, step in enumerate(computation_steps):
            # Re‐highlight the relevant tokens for this step
            relevant_circles = [token_circles[idx] for idx in step["input_indices"]]
            self.play(
                *[circle.animate.set_stroke(opacity=1.0) for circle in relevant_circles],
                run_time=0.3
            )

            # Activate features and pulses
            animations = []
            target_layer = step["layer"]
            for feature_idx in step["feature_indices"]:
                feature_node = network[target_layer][feature_idx]
                animations.extend([
                    Flash(feature_node, color=active_color, flash_radius=0.25),
                    feature_node.animate.set_fill(active_color, opacity=0.8)
                ])
                # Connections from current tokens → feature
                for idx in step["input_indices"]:
                    input_node = all_input_displays[idx][1]
                    for conn in connections:
                        if (np.allclose(conn.get_start(), input_node.get_center(), atol=0.1) and
                            np.allclose(conn.get_end(), feature_node.get_center(), atol=0.1)):
                            animations.append(
                                ShowPassingFlash(
                                    conn.copy().set_stroke(active_color, width=3, opacity=0.9),
                                    time_width=0.6
                                )
                            )
                # Connections from previously‐activated features (if any)
                if target_layer > 1:
                    prev_layer = target_layer - 1
                    for prev_node in network[prev_layer]:
                        if hasattr(prev_node, "fill_opacity") and prev_node.fill_opacity > 0.5:
                            for conn in connections:
                                if (np.allclose(conn.get_start(), prev_node.get_center(), atol=0.1) and
                                    np.allclose(conn.get_end(), feature_node.get_center(), atol=0.1)):
                                    animations.append(
                                        ShowPassingFlash(
                                            conn.copy().set_stroke(active_color, width=3, opacity=0.9),
                                            time_width=0.6
                                        )
                                    )
            self.play(*animations, run_time=0.8)

            # Dim the token‐highlight circles again (unless it's the last step)
            if step_num < len(computation_steps) - 1:
                self.play(
                    *[circle.animate.set_stroke(opacity=0.0) for circle in relevant_circles],
                    run_time=0.3
                )
            self.wait(0.2)

        # 3) Finally, flash "81" with its connections
        output_node = network[4][0]
        output_label = Tex("81", font_size=28, color=GREEN)
        output_label.next_to(output_node, RIGHT, buff=0.2)
        output_display = VGroup(output_label)

        final_animations = [
            FadeIn(output_display),
            Flash(output_node, color=GREEN, flash_radius=0.4),
            output_node.animate.set_fill(GREEN, opacity=0.8)
        ]
        for i in range(3):  # three activated features in layer 3
            feature_node = network[3][i]
            for conn in connections:
                if (np.allclose(conn.get_start(), feature_node.get_center(), atol=0.1) and
                    np.allclose(conn.get_end(), output_node.get_center(), atol=0.1)):
                    final_animations.append(
                        ShowPassingFlash(
                            conn.copy().set_stroke(GREEN, width=3, opacity=0.9),
                            time_width=0.8
                        )
                    )
        self.play(*final_animations, run_time=1.0)

        self.wait(1.0)

        # Cleanup everything
        cleanup = [
            FadeOut(output_display),
            *[FadeOut(label) for label in all_feature_labels],
            *[FadeOut(display[0]) for display in all_input_displays.values()],
            *[FadeOut(circle) for circle in token_circles]
        ]
        self.play(*cleanup, run_time=1.2)
        self.wait(0.5)
