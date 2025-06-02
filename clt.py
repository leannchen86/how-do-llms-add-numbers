from manim import *
import numpy as np

class MLPvsCLTComparison(Scene):
    def construct(self):
        # Set custom colors for better visual differentiation
        MLP_COLOR = "#87CEEB"  # Light blue
        CLT_COLOR = "#87CEEB"  # Light blue
        ACTIVE_MLP_COLOR = "#4682B4"  # Steel blue (darker than light blue for contrast)
        ACTIVE_CLT_COLOR = "#FF6B6B"  # Coral red for better contrast
        
        # Create MLP model positioned off-screen to the left
        mlp_model, mlp_inputs, mlp_output = self.create_mlp_model(MLP_COLOR)
        mlp_model.shift(LEFT * 12)  # Start off-screen to the left
        
        # Create MLP title positioned off-screen to the left
        mlp_title = Tex(r"\text{MLP (Polysemantic)}", font_size=38, color=MLP_COLOR)
        mlp_title.move_to([-15.5, 2.5, 0])  # Off-screen to the left
        
        # Add models to scene (but they're off-screen)
        self.add(mlp_model, mlp_title)
        
        # Slide MLP in from the left to center
        self.play(
            mlp_model.animate.move_to(ORIGIN).scale(1.2),
            mlp_title.animate.move_to(ORIGIN).scale(1.2).to_edge(UP, buff=0.7),
            rate_func=smooth,
            run_time=1.5
        )
        
        # Now add the neuron label and arrow pointing to a neuron
        neuron_label = Tex(r"\text{Neuron}", font_size=32, color=MLP_COLOR).move_to([3,2.5, 0])
        neuron_label.set_stroke(BLACK, width=3, opacity=0.8, background=True)

        # Show the label with highlight effects
        self.play(FadeIn(neuron_label, scale=1.2))
        
        # Create visually enhanced arrow pointing to a neuron
        # Get the network from the mlp_model
        network_group, connections = mlp_model
        network = network_group
        
        neuron_arrow = Arrow(
            neuron_label.get_bottom() + DOWN * 0.1,
            network[2][3].get_center() + UP * 0.2,  # Point to middle neuron in hidden layer
            buff=0.1,
            color=MLP_COLOR,
            stroke_width=3,
            tip_length=0.2
        )

        # Animate the arrow with glow effect
        self.play(GrowArrow(neuron_arrow))
        
        self.wait(0.7)
        self.play(
            FadeOut(neuron_arrow),
            FadeOut(neuron_label)
        )
        
        # Demonstrate polysemantic neurons with enhanced visual effects
        self.demonstrate_polysemantic_neurons(mlp_model, ACTIVE_MLP_COLOR, MLP_COLOR)
        
        # Create CLT model off-screen to the right
        clt_model, clt_inputs, clt_output = self.create_clt_model(CLT_COLOR)
        clt_model.shift(RIGHT * 12)  # Start off-screen to the right
        
        clt_title = Tex(r"\text{CLT (Monosemantic)}", font_size=38, color=CLT_COLOR)
        clt_title.move_to([15.5, 2.5, 0])  # Off-screen to the right
        
        # Position feature label closer to target feature
        feature_label = Tex(r"\text{Feature}", font_size=32, color=CLT_COLOR).move_to([30, 3.5, 0])
        feature_label.set_stroke(BLACK, width=3, opacity=0.8, background=True)
        
        # Add CLT components to scene (off-screen)
        self.add(clt_model, clt_title, feature_label)
        
        # Transition between models - move MLP off-screen left, bring CLT in from right
        self.play(
            mlp_model.animate.shift(LEFT * 12).scale(1/1.2),
            mlp_title.animate.shift(LEFT * 12),
            run_time=1.2,
            rate_func=rush_into
        )
        
        # Move CLT to center position
        self.play(
            clt_model.animate.move_to(ORIGIN).scale(1.2),
            clt_title.animate.move_to([0, 3.0, 0]).scale(0.8),
            feature_label.animate.move_to([5.5, 3.0, 0]),
            run_time=1.2,
            rate_func=smooth
        )
        
        # Add arrow pointing to a feature (similar to neuron arrow)
        clt_network_group, clt_connections = clt_model
        clt_network = clt_network_group
        
        # Point to a feature in layer 3 (one of the activated features)
        feature_arrow = Arrow(
            feature_label.get_bottom() + DOWN * 0.1,
            clt_network[3][3].get_center() + UP * 0.2,  # Point to middle feature in layer 3
            buff=0.1,
            color=CLT_COLOR,
            stroke_width=3,
            tip_length=0.2
        )

        # Animate the arrow with glow effect
        self.play(GrowArrow(feature_arrow))
        
        self.play(
            Flash(clt_network[3][1], color=CLT_COLOR, flash_radius=0.3),
        )
        
        self.wait(0.7)
        self.play(FadeOut(feature_arrow))
        
        # Demonstrate interpretable features with enhanced visuals
        self.demonstrate_interpretable_features(clt_model, ACTIVE_CLT_COLOR, CLT_COLOR)
        
        # Final fadeout
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1.5
        )
    
    def create_mlp_model(self, color=BLUE):
        # Create MLP model with enhanced visual style
        network = VGroup()
        layers = 4
        nodes_per_layer = [3, 5, 5, 1]
        
        # Create nodes with gradient fill and better styling
        for i in range(layers):
            layer = VGroup()
            for j in range(nodes_per_layer[i]):
                node = Circle(radius=0.2, color=color)
                node.set_fill(color, opacity=0.3)
                node.move_to([i * 2 - 6, j - (nodes_per_layer[i] - 1) / 2, 0])
                layer.add(node)
            network.add(layer)
        
        # Add connections with better styling
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
        
        # Input/output labels (empty initially)
        inputs = [
            Tex("", font_size=30).next_to(network[0][0], LEFT),
            Tex("", font_size=30).next_to(network[0][1], LEFT),
            Tex("", font_size=30).next_to(network[0][2], LEFT)
        ]
        
        output = Tex("", font_size=34, color=GREEN).next_to(network[3][0], RIGHT)
        
        return VGroup(network, connections), inputs, output
    
    def create_clt_model(self, color=BLUE):
        # Create CLT model with 5 layers for mathematical computation
        network = VGroup()
        layers = 5
        nodes_per_layer = [4, 5, 5, 5, 1]  # Updated to 5 layers
        
        # Create features with rounded rectangles for better aesthetics
        for i in range(layers):
            layer = VGroup()
            for j in range(nodes_per_layer[i]): # Feature layers - use rounded rectangles
                node = RoundedRectangle(
                    height=0.25, 
                    width=0.25, 
                    corner_radius=0.05, 
                    color=color
                )
                
                node.set_fill(color, opacity=0.2)
                # Adjust spacing for 5 layers
                node.move_to([i * 1.8 - 3.6, j - (nodes_per_layer[i] - 1) / 2, 0])
                layer.add(node)
            network.add(layer)
        
        # Create meaningful connections aligned with feature firing pattern
        connections = VGroup()
        
        connection_map = [
            # Layer 0 to Layer 1: Input tokens to feature extraction
            # "26" (input 0) -> magnitude and digit features
            (0, 0, 1, 0),  # 26 -> \approx 20 (magnitude)
            (0, 0, 1, 2),  # 26 -> ends in 6 (units digit)
            
            # "55" (input 2) -> magnitude and digit features  
            (0, 2, 1, 1),  # 55 -> \approx 50 (magnitude)
            (0, 2, 1, 3),  # 55 -> ends in 5 (units digit)
            
            # Layer 1 to Layer 2: Feature combination for arithmetic
            # Magnitude estimation: \approx 20 + \approx 50 = \approx 70
            (1, 0, 2, 0),  # \approx 20 -> magnitude sum (\approx 70)
            (1, 1, 2, 0),  # \approx 50 -> magnitude sum (\approx 70)
            
            # Units digit addition: 6 + 5 \rightarrow 11 (carry 1, units 1)
            (1, 2, 2, 1),  # ends in 6 -> 6+5=11, units=1, carry=1
            (1, 3, 2, 1),  # ends in 5 -> 6+5=11, units=1, carry=1
            
            # Tens digit computation: 2 + 5 + carry = 8
            (1, 0, 2, 2),  # From \approx 20, extract tens digit 2
            (1, 1, 2, 2),  # From \approx 50, extract tens digit 5
            (2, 1, 2, 2),  # Carry from units addition
            
            # Layer 2 to Layer 3: Final computation and validation
            # Final magnitude check: \approx 70 \rightarrow \approx 80 (with carry)
            (2, 0, 3, 0),  # \approx 70 -> final magnitude (\approx 80)
            
            # Units digit confirmation: value \equiv 1 \pmod{10}
            (2, 1, 3, 1),  # units calculation -> value \equiv 1 \pmod{10}
            
            # Tens digit with carry: final two-digit result \equiv 81 \pmod{100}
            (2, 2, 3, 2),  # tens + carry -> value \equiv 81 \pmod{100}
            (2, 1, 3, 2),  # units carry -> value \equiv 81 \pmod{100}
            
            # Layer 3 to Layer 4: All features converge to final output
            (3, 0, 4, 0),  # magnitude (\approx 80) -> 81
            (3, 1, 4, 0),  # units digit 1 -> 81  
            (3, 2, 4, 0),  # value \equiv 81 \pmod{100} -> 81
        ]
        
        # Add meaningful connections
        for layer1, node1, layer2, node2 in connection_map:
            connection = Line(
                network[layer1][node1].get_center(),
                network[layer2][node2].get_center(),
                stroke_opacity=0.3,
                stroke_width=0.5,
                stroke_color=color
            )
            connections.add(connection)
        
        # Add random additional connections to make the network look more web-like
        np.random.seed(42)  # For reproducible random connections
        for layer_idx in range(layers - 1):
            current_layer_size = nodes_per_layer[layer_idx]
            next_layer_size = nodes_per_layer[layer_idx + 1]
            
            # Add random connections (especially to nodes without meaningful connections)
            for i in range(current_layer_size):
                for j in range(next_layer_size):
                    existing = any(
                        l1 == layer_idx and n1 == i and l2 == layer_idx + 1 and n2 == j
                        for l1, n1, l2, n2 in connection_map
                    )
                    if not existing and np.random.random() < 0.3:
                        connection = Line(
                            network[layer_idx][i].get_center(),
                            network[layer_idx + 1][j].get_center(),
                            stroke_opacity=0.15,
                            stroke_width=0.3,
                            stroke_color=color
                        )
                        connections.add(connection)
        
        # Input/output labels (empty initially)
        inputs = [
            Tex("", font_size=24).next_to(network[0][i], LEFT) for i in range(4)
        ]
        
        output = Tex("", font_size=26).next_to(network[-1][0], RIGHT)
        
        return VGroup(network, connections), inputs, output

    def demonstrate_polysemantic_neurons(self, model, active_color=BLUE, base_color=BLUE):
        # Correctly unpack the model components
        network_group, connections = model
        network = network_group
        
        # Updated inputs and corresponding output labels
        inputs = ["26", "seattle", "bird"]
        output_labels = ["number", "city", "animal"]
        
        # Define TWO shared neurons that all inputs activate
        shared_neurons = [
            (1, 2),  # Original: layer 1, neuron index 2 (middle neuron in 5-neuron layer)
            (2, 1)   # New: layer 2, neuron index 1 (second neuron in second hidden layer)
        ]
        
        # Process each input sequentially
        for j, (input_text, output_label) in enumerate(zip(inputs, output_labels)):
            # Create input label
            if input_text.isnumeric() or input_text in ['+', '-', '=', '*', '/']:
                input_label = Tex(f"{input_text}", font_size=32, color=WHITE)
            else:
                input_label = Tex(rf"\text{{{input_text}}}", font_size=32, color=WHITE)
            input_label.next_to(network[0][1], LEFT, buff=0.5)
            
            bg = BackgroundRectangle(input_label, color=BLACK, fill_opacity=0.7, buff=0.1)
            current_input_display = VGroup(bg, input_label)
            
            # Create output label (but don't show it yet)
            if output_label.isnumeric() or output_label in ['+', '-', '=', '*', '/']:
                output_label_text = Tex(f"{output_label}", font_size=30, color=GREEN)
            else:
                output_label_text = Tex(rf"\text{{{output_label}}}", font_size=30, color=GREEN)
            output_label_text.next_to(network[-1][0], RIGHT, buff=0.5)
            
            output_bg = BackgroundRectangle(output_label_text, color=BLACK, fill_opacity=0.7, buff=0.1)
            current_output_display = VGroup(output_bg, output_label_text)
            
            # Show only input label initially
            self.play(FadeIn(current_input_display, shift=RIGHT*0.3))
            
            # Get input node
            input_node = network[0][1]  # Use middle input node
            
            # PHASE 1: Flash input and activate first shared neuron
            first_shared_neuron = network[shared_neurons[0][0]][shared_neurons[0][1]]
            
            input_to_first_animations = [
                Flash(input_node, color=WHITE, flash_radius=0.3),
                input_node.animate.set_fill(active_color, opacity=0.9),
                Flash(first_shared_neuron, color=active_color, flash_radius=0.4),
                first_shared_neuron.animate.set_fill(active_color, opacity=0.9)
            ]
            
            # Add connection pulse from input to first shared neuron
            for conn in connections:
                if (np.allclose(conn.get_start(), input_node.get_center(), atol=0.1) and 
                    np.allclose(conn.get_end(), first_shared_neuron.get_center(), atol=0.1)):
                    connection_pulse = conn.copy().set_stroke(active_color, width=4, opacity=0.8)
                    input_to_first_animations.append(ShowPassingFlash(connection_pulse, time_width=0.7))
                    break
            
            self.play(*input_to_first_animations, run_time=0.8)
            
            # PHASE 2: Activate second shared neuron with connection from first
            second_shared_neuron = network[shared_neurons[1][0]][shared_neurons[1][1]]
            
            first_to_second_animations = [
                Flash(second_shared_neuron, color=active_color, flash_radius=0.4),
                second_shared_neuron.animate.set_fill(active_color, opacity=0.9)
            ]
            
            # Add connection pulse from first shared neuron to second shared neuron
            for conn in connections:
                if (np.allclose(conn.get_start(), first_shared_neuron.get_center(), atol=0.1) and 
                    np.allclose(conn.get_end(), second_shared_neuron.get_center(), atol=0.1)):
                    connection_pulse = conn.copy().set_stroke(active_color, width=4, opacity=0.8)
                    first_to_second_animations.append(ShowPassingFlash(connection_pulse, time_width=0.7))
                    break
            
            self.play(*first_to_second_animations, run_time=0.8)
            
            # PHASE 3: Activate output with connections from both shared neurons
            output_node = network[-1][0]
            output_animations = [
                Flash(output_node, color=GREEN, flash_radius=0.4),
                output_node.animate.set_fill(GREEN, opacity=0.7)
            ]
            
            # Add connection pulses from both shared neurons to output
            for shared_neuron_pos in shared_neurons:
                shared_neuron = network[shared_neuron_pos[0]][shared_neuron_pos[1]]
                for conn in connections:
                    if (np.allclose(conn.get_start(), shared_neuron.get_center(), atol=0.1) and 
                        np.allclose(conn.get_end(), output_node.get_center(), atol=0.1)):
                        pulse = conn.copy().set_stroke(GREEN, width=4, opacity=0.8)
                        output_animations.append(ShowPassingFlash(pulse, time_width=0.6))
            
            # Play output activation with all connection pulses
            self.play(*output_animations, run_time=0.7)
            
            # NOW show the output label after the neuron fires
            self.play(FadeIn(current_output_display, shift=LEFT*0.3))
            
            self.wait(0.5)
            
            # Reset for next input
            reset_animations = [
                FadeOut(current_input_display),
                FadeOut(current_output_display),
                input_node.animate.set_fill(base_color, opacity=0.3),
                output_node.animate.set_fill(base_color, opacity=0.3),
                first_shared_neuron.animate.set_fill(base_color, opacity=0.3),
                second_shared_neuron.animate.set_fill(base_color, opacity=0.3)
            ]
            
            self.play(*reset_animations, run_time=0.5)
            
            if j < len(inputs) - 1:
                self.wait(0.2)
    
    def demonstrate_interpretable_features(self, model, active_color=RED, base_color=BLUE):
        # Correctly unpack the model components
        network_group, connections = model
        network = network_group

        # Define computation steps with correct feature indices
        computation_steps = [
            {
                "phase": "Number parsing",
                "inputs": ["26", "55"],  # Only numbers first
                "input_indices": [0, 2],  # tokens "26" and "55"
                "layer": 1,
                "features": [r"\approx 20", r"\approx 50", r"\text{ends in 6}", r"\text{ends in 5}"],
                "feature_indices": [0, 1, 2, 3]
            },
            {
                "phase": "Operation processing",
                "inputs": ["+"],  # Operation token
                "input_indices": [1],  # token "+"
                "layer": 2,
                "features": [
                    r"\approx 70",
                    r"6 + 5 \rightarrow 1,\,\text{carry}",
                    r"2 + 5 + 1 \rightarrow 8"
                ],
                "feature_indices": [0, 1, 2]  # Arithmetic computation features
            },
            {
                "phase": "Computation trigger and result",
                "inputs": ["="],  # Computation trigger
                "input_indices": [3],  # token "="
                "layer": 3,
                "features": [
                    r"\approx 80\,\text{final}",
                    r"\equiv 1 \pmod{10}",
                    r"\equiv 81 \pmod{100}"
                ],
                "feature_indices": [0, 1, 2]  # Final computation features
            }
        ]

        # Create and show all feature labels initially (only for non-empty features)
        all_feature_labels = []

        # Layer 1 features (now wrapped in \text{…} for “ends in …”, font_size bumped to 24)
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
            feature_group = VGroup(bg, feature_text)
            all_feature_labels.append(feature_group)

        # Layer 2 features (font_size bumped to  Twenty-two)
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
            feature_group = VGroup(bg, feature_text)
            all_feature_labels.append(feature_group)

        # Layer 3 features (font_size bumped to Twenty)
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
            feature_group = VGroup(bg, feature_text)
            all_feature_labels.append(feature_group)

        # Show all feature labels
        self.play(
            *[FadeIn(label, scale=0.8) for label in all_feature_labels],
            lag_ratio=0.05,
            run_time=2
        )

        self.wait(1)

        # Create all input displays upfront and show them all at once
        all_input_displays = {}
        for input_text, input_idx in [("26", 0), ("+", 1), ("55", 2), ("=", 3)]:
            input_node = network[0][input_idx]
            if input_text.isnumeric() or input_text in ['+', '-', '=', '*', '/']:
                input_label = Tex(f"{input_text}", font_size=26, color=WHITE)
            else:
                input_label = Tex(rf"\text{{{input_text}}}", font_size=26, color=WHITE)
            input_label.next_to(input_node, LEFT, buff=0.2)
            bg = BackgroundRectangle(input_label, color=BLACK, fill_opacity=0.8, buff=0.05)
            input_display = VGroup(bg, input_label)
            all_input_displays[input_idx] = (input_display, input_node, input_idx)

        # Show all input tokens at once
        self.play(*[FadeIn(display[0]) for display, _, _ in all_input_displays.values()], run_time=0.8)

        # Fire all tokens simultaneously and KEEP them filled throughout
        all_token_animations = []
        for display, input_node, _ in all_input_displays.values():
            all_token_animations.extend([
                Flash(input_node, color=active_color, flash_radius=0.25),
                input_node.animate.set_fill(active_color, opacity=0.8)
            ])
        self.play(*all_token_animations, run_time=0.8)
        self.wait(0.8)

        # Keep track of token circles for re-highlighting (create them now but don't show yet)
        token_circles = []
        for display, input_node, _ in all_input_displays.values():
            token_circle = Circle(
                radius=0.35,
                color=active_color,
                stroke_width=3,
                stroke_opacity=0  # Initially invisible
            ).move_to(input_node.get_center())
            token_circles.append(token_circle)
            self.add(token_circle)  # Add to scene but invisible
        self.wait(0.5)

        # Execute computation steps with proper connections
        for step_num, step in enumerate(computation_steps):
            # Re-highlight relevant tokens for this step using circles
            if step["inputs"]:
                current_input_displays = [all_input_displays[idx] for idx in step["input_indices"]]

                # Show and highlight token circles for this step
                relevant_circles = [token_circles[idx] for idx in step["input_indices"]]
                self.play(
                    *[circle.animate.set_stroke(opacity=1.0) for circle in relevant_circles],
                    run_time=0.4
                )

                # SYNCHRONIZED: Activate corresponding features with connections
                all_animations = []

                # Add feature activation animations
                target_layer = step["layer"]
                for feature_idx in step["feature_indices"]:
                    feature_node = network[target_layer][feature_idx]

                    # Add feature flash and fill animations
                    all_animations.extend([
                        Flash(feature_node, color=active_color, flash_radius=0.25),
                        feature_node.animate.set_fill(active_color, opacity=0.8)
                    ])

                    # Add connection pulses from current step inputs to features
                    for display, input_node, input_idx in current_input_displays:
                        for conn in connections:
                            if (np.allclose(conn.get_start(), input_node.get_center(), atol=0.1) and
                                np.allclose(conn.get_end(), feature_node.get_center(), atol=0.1)):
                                pulse = conn.copy().set_stroke(active_color, width=3, opacity=0.9)
                                all_animations.append(ShowPassingFlash(pulse, time_width=0.6))

                    # For layers beyond 1, also show connections from previously activated features
                    if target_layer > 1:
                        prev_layer = target_layer - 1
                        for prev_node in network[prev_layer]:
                            # Check if this previous node is still active (filled)
                            if hasattr(prev_node, 'fill_opacity') and prev_node.fill_opacity > 0.5:
                                for conn in connections:
                                    if (np.allclose(conn.get_start(), prev_node.get_center(), atol=0.1) and
                                        np.allclose(conn.get_end(), feature_node.get_center(), atol=0.1)):
                                        pulse = conn.copy().set_stroke(active_color, width=3, opacity=0.9)
                                        all_animations.append(ShowPassingFlash(pulse, time_width=0.6))

                # Play all animations simultaneously
                self.play(*all_animations, run_time=0.8)

                self.wait(0.6)

                # Gray out token circles again after step (except for last step)
                if step_num < len(computation_steps) - 1:
                    self.play(
                        *[circle.animate.set_stroke(opacity=0.0) for circle in relevant_circles],
                        run_time=0.4
                    )

        # Final output activation
        output_node = network[4][0]
        output_label = Tex("81", font_size=28, color=GREEN)
        output_label.next_to(output_node, RIGHT, buff=0.2)
        bg = BackgroundRectangle(output_label, color=BLACK, fill_opacity=0.8, buff=0.05)
        output_display = VGroup(bg, output_label)

        # SYNCHRONIZED: Show final connections from layer 3 to output with output activation
        final_animations = [
            FadeIn(output_display),
            Flash(output_node, color=GREEN, flash_radius=0.4),
            output_node.animate.set_fill(GREEN, opacity=0.8)
        ]

        # Add connection pulses from layer 3 activated features to output
        for i in range(3):  # Only the 3 features that were activated in layer 3
            feature_node = network[3][i]
            for conn in connections:
                if (np.allclose(conn.get_start(), feature_node.get_center(), atol=0.1) and
                    np.allclose(conn.get_end(), output_node.get_center(), atol=0.1)):
                    pulse = conn.copy().set_stroke(GREEN, width=3, opacity=0.9)
                    final_animations.append(ShowPassingFlash(pulse, time_width=0.8))

        # Play all final animations simultaneously
        self.play(*final_animations, run_time=1.0)

        self.wait(1.5)

        # Clean up - fade out all input displays, token circles, and reset everything
        cleanup_animations = [
            FadeOut(output_display),
            *[FadeOut(label) for label in all_feature_labels],
            *[FadeOut(display) for display, _, _ in all_input_displays.values()],
            *[FadeOut(circle) for circle in token_circles],  # Fade out token circles
        ]

        self.play(*cleanup_animations, run_time=1.2)

        self.wait(1)
