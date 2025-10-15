"""
DNA Editor - Creature Tentacle Generator

Interactive 3D editor for creating tentacle creatures using mathematical curves.

Two mathematical algorithms for generating organic tentacles:
1. Bezier Curves - Cubic polynomial curves with control points
2. Fourier Series - Wave composition for organic shapes

FEATURES:
- Real-time parameter sliders for all algorithms
- Thickness & taper controls with live preview
- Preset system (3 built-in presets)
- Undo/Redo system (up to 50 steps)
- Interactive help overlay (Press H)
- Enhanced UI with algorithm-specific controls

Usage:
    python3 dna_editor/main.py

Controls:
    H - Toggle help overlay
    1/2/3 - Set tentacle count
    Q/W - Switch algorithm
    +/- - Adjust segments
    Sliders - Adjust parameters
    Presets - Quick preset buttons
    Ctrl+Z - Undo
    Ctrl+Y - Redo
    Mouse Drag - Orbit camera
    Scroll - Zoom
    R - Reset camera
"""

from ursina import Ursina, Entity, camera, held_keys, mouse, Vec3, color, window, Sky
import math


# ============================================================================
# MATHEMATICAL CURVE GENERATORS
# ============================================================================

def bezier_curve(anchor, target, num_points, control_strength=0.4):
    """
    Generate points along a cubic Bezier curve.

    Bezier curve: B(t) = (1-t)³P₀ + 3(1-t)²tP₁ + 3(1-t)t²P₂ + t³P₃

    Args:
        anchor: Vec3 start point
        target: Vec3 end point
        num_points: Number of points to generate
        control_strength: How far control points are from endpoints (0-1)

    Returns:
        list of Vec3 points along the curve
    """
    points = []

    # Calculate control points
    # P0 = anchor, P3 = target
    # P1 and P2 are offset along normals for natural curve

    direction = (target - anchor).normalized()
    length = (target - anchor).length()

    # Create perpendicular vectors for control point offsets
    up = Vec3(0, 1, 0)
    if abs(direction.y) > 0.99:
        up = Vec3(1, 0, 0)

    side = direction.cross(up).normalized()

    # Control points offset to the side for natural S-curve
    p0 = anchor
    p1 = anchor + direction * (length * control_strength) + side * (length * 0.2)
    p2 = target - direction * (length * control_strength) - side * (length * 0.2)
    p3 = target

    # Generate points along cubic Bezier
    for i in range(num_points):
        t = i / max(1, num_points - 1)

        # Cubic Bezier formula
        b0 = (1 - t) ** 3
        b1 = 3 * (1 - t) ** 2 * t
        b2 = 3 * (1 - t) * t ** 2
        b3 = t ** 3

        point = p0 * b0 + p1 * b1 + p2 * b2 + p3 * b3
        points.append(point)

    return points


def fourier_curve(anchor, target, num_points, num_waves=3, amplitude=0.1):
    """
    Generate points along a curve defined by Fourier series (wave composition).

    Combines multiple sine waves at different frequencies for organic shapes.
    Formula: P(t) = base_curve(t) + Σ(Aₙ sin(nωt + φₙ))

    Args:
        anchor: Vec3 start point
        target: Vec3 end point
        num_points: Number of points to generate
        num_waves: Number of Fourier components (3-5 recommended)
        amplitude: Wave amplitude as fraction of length

    Returns:
        list of Vec3 points along the curve
    """
    points = []

    direction = (target - anchor).normalized()
    length = (target - anchor).length()

    # Create perpendicular basis vectors
    up = Vec3(0, 1, 0)
    if abs(direction.y) > 0.99:
        up = Vec3(1, 0, 0)

    right = direction.cross(up).normalized()
    up = right.cross(direction).normalized()

    # Generate points with Fourier wave composition
    for i in range(num_points):
        t = i / max(1, num_points - 1)

        # Base position (straight line)
        base = anchor + direction * (t * length)

        # Add Fourier components
        offset_x = 0
        offset_y = 0

        for n in range(1, num_waves + 1):
            # Each wave has different frequency and phase
            freq = n * 2.0
            phase = n * 0.7  # Offset phases for variety

            # Amplitude decreases with frequency (lower frequencies dominate)
            wave_amp = amplitude * length / n

            # Add wave components
            offset_x += wave_amp * math.sin(freq * t * math.pi + phase)
            offset_y += wave_amp * math.cos(freq * t * math.pi + phase * 1.3)

        # Apply offsets in local coordinate system
        point = base + right * offset_x + up * offset_y
        points.append(point)

    return points


# ============================================================================
# TENTACLE GENERATOR
# ============================================================================

class Tentacle:
    """A single tentacle made of connected segments"""

    def __init__(self, parent, anchor, target, segments, algorithm, color_rgb, algorithm_params, thickness_base=0.25, taper_factor=0.6):
        self.parent = parent
        self.anchor = anchor
        self.target = target
        self.segments = []
        self.algorithm = algorithm
        self.color_rgb = color_rgb

        # Generate curve points based on algorithm with dynamic parameters
        if algorithm == 'bezier':
            curve_points = bezier_curve(anchor, target, segments + 1,
                                       control_strength=algorithm_params.get('control_strength', 0.4))
        else:  # fourier
            curve_points = fourier_curve(anchor, target, segments + 1,
                                        num_waves=int(algorithm_params.get('num_waves', 3)),
                                        amplitude=algorithm_params.get('amplitude', 0.15))

        # Create segments along the curve
        for i in range(segments):
            p1 = curve_points[i]
            p2 = curve_points[i + 1]

            # Calculate segment position (midpoint) and length
            seg_pos = (p1 + p2) / 2
            seg_dir = (p2 - p1).normalized()
            seg_length = (p2 - p1).length()

            # Calculate thickness (taper from base to tip) with dynamic parameters
            thickness = thickness_base * (1.0 - i / segments * taper_factor)

            # Create segment as sphere
            segment = Entity(
                model='sphere',
                color=color.rgb(*color_rgb),
                position=seg_pos,
                scale=thickness,
                parent=parent
            )

            # Store for animation
            segment.base_position = seg_pos
            segment.segment_index = i
            segment.total_segments = segments

            self.segments.append(segment)

        # Debug output for first segment
        if self.segments:
            print(f"  Tentacle segment 0 at: {self.segments[0].position}, scale: {self.segments[0].scale}")

    def update_animation(self, time):
        """Animate tentacle with wave motion"""
        for segment in self.segments:
            i = segment.segment_index
            n = segment.total_segments

            # Wave travels from base to tip
            phase = time * 2.0 + i * 0.3

            # Amplitude increases toward tip
            wave_amplitude = 0.05 * (i / n)

            # Calculate offset
            offset_x = math.sin(phase) * wave_amplitude
            offset_y = math.cos(phase * 1.3) * wave_amplitude

            # Apply offset
            segment.position = segment.base_position + Vec3(offset_x, offset_y, 0)

    def destroy(self):
        """Remove all segment entities"""
        from ursina import destroy
        for segment in self.segments:
            destroy(segment)
        self.segments.clear()


# ============================================================================
# CREATURE GENERATOR
# ============================================================================

class TentacleCreature:
    """Creature with body and tentacles"""

    def __init__(self, num_tentacles=2, segments_per_tentacle=12, algorithm='bezier',
                 algorithm_params=None, thickness_base=0.25, taper_factor=0.6):
        # Create root entity (no parent = defaults to scene)
        self.root = Entity(position=(0, 0, 0))
        self.tentacles = []
        self.algorithm = algorithm
        self.algorithm_params = algorithm_params or {}
        self.thickness_base = thickness_base
        self.taper_factor = taper_factor

        # Create body (larger for better visibility)
        self.body = Entity(
            model='sphere',
            color=color.rgb(0.6, 0.3, 0.7),  # Purple
            scale=1.2,
            parent=self.root
        )

        print(f"Body created at position: {self.root.position}, scale: {self.body.scale}")
        print(f"Root parent: {self.root.parent}, Body parent: {self.body.parent}")
        print(f"Body enabled: {self.body.enabled}, visible: {self.body.visible}")

        # Generate tentacles
        self.rebuild(num_tentacles, segments_per_tentacle, algorithm, algorithm_params, thickness_base, taper_factor)

    def rebuild(self, num_tentacles, segments_per_tentacle, algorithm, algorithm_params=None, thickness_base=0.25, taper_factor=0.6):
        """Rebuild tentacles with new parameters"""
        # Clear existing tentacles
        for tentacle in self.tentacles:
            tentacle.destroy()
        self.tentacles.clear()

        self.algorithm = algorithm
        self.algorithm_params = algorithm_params or {}
        self.thickness_base = thickness_base
        self.taper_factor = taper_factor

        # Create new tentacles
        body_radius = self.body.scale_x / 2

        for i in range(num_tentacles):
            # Distribute tentacles evenly around body
            angle = (i / num_tentacles) * 2 * math.pi

            # Anchor on lower body
            anchor = Vec3(
                math.cos(angle) * body_radius * 0.8,
                -body_radius * 0.5,
                math.sin(angle) * body_radius * 0.8
            )

            # Target position (hanging down and out)
            target = Vec3(
                math.cos(angle) * 1.5,
                -2.5,
                math.sin(angle) * 1.5
            )

            # Color variation per tentacle
            hue_offset = i * 0.1
            tentacle_color = (0.6 + hue_offset, 0.3, 0.65 - hue_offset * 0.3)

            # Create tentacle with dynamic parameters
            tentacle = Tentacle(
                parent=self.root,
                anchor=anchor,
                target=target,
                segments=segments_per_tentacle,
                algorithm=algorithm,
                color_rgb=tentacle_color,
                algorithm_params=self.algorithm_params,
                thickness_base=thickness_base,
                taper_factor=taper_factor
            )

            self.tentacles.append(tentacle)

        print(f"Created {len(self.tentacles)} tentacles with {segments_per_tentacle} segments each")
        if self.tentacles:
            print(f"First tentacle anchor: {self.tentacles[0].anchor}, target: {self.tentacles[0].target}")
            print(f"First tentacle has {len(self.tentacles[0].segments)} segment entities")

    def update_animation(self, time):
        """Update creature animations"""
        # Pulse body (based on initial scale of 1.2)
        scale_pulse = 1.2 + math.sin(time * 1.5) * 0.05
        self.body.scale = scale_pulse

        # Animate tentacles
        for tentacle in self.tentacles:
            tentacle.update_animation(time)

    def destroy(self):
        """Cleanup"""
        for tentacle in self.tentacles:
            tentacle.destroy()
        # Properly destroy the root and all children
        from ursina import destroy
        destroy(self.root)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

class TentacleEditor:
    """Main editor application"""

    def __init__(self):
        # Create scene
        self.ground = Entity(
            model='plane',
            scale=20,
            color=color.rgb(0.1, 0.1, 0.15),
            position=(0, -1, 0)
        )

        self.sky = Sky(color=color.rgb(0.05, 0.05, 0.1))

        # DEBUG: Add a bright marker at origin to verify rendering works
        self.debug_marker = Entity(
            model='sphere',
            color=color.rgb(1, 1, 0),  # Bright yellow
            scale=0.3,
            position=(0, 0, 0)
        )
        print("DEBUG: Yellow marker created at origin (0, 0, 0)")

        # Creature parameters
        self.creature = None
        self.num_tentacles = 2
        self.segments = 12
        self.algorithm = 'bezier'

        # Algorithm-specific parameters
        self.params = {
            'bezier': {'control_strength': 0.4},
            'fourier': {'num_waves': 3, 'amplitude': 0.15}
        }

        # Thickness parameters
        self.thickness_base = 0.25
        self.taper_factor = 0.6

        # Undo/redo system
        self.history = []
        self.history_index = -1
        self.max_history = 50

        # Help overlay visible
        self.help_visible = False

        self.rebuild_creature()

        # Camera state
        self.camera_angle = 0
        self.camera_height = 2
        self.camera_distance = 6

        # Set initial camera position (CRITICAL - must happen before first frame)
        camera.position = Vec3(0, 2, -6)
        camera.look_at(Vec3(0, 0, 0))
        print(f"Camera initialized at: {camera.position}, looking at origin")

        # Animation
        self.time = 0

        # Create UI
        self.create_ui()

        print("\n" + "=" * 70)
        print("DNA EDITOR - CREATURE TENTACLE GENERATOR")
        print("=" * 70)
        print("FEATURES:")
        print("  - Real-time parameter sliders for algorithms")
        print("  - Thickness & taper controls")
        print("  - Preset system (3 presets)")
        print("  - Undo/Redo (Ctrl+Z / Ctrl+Y)")
        print("  - Help overlay (Press H)")
        print("")
        print("Quick Controls:")
        print("  H - Help  |  1/2/3 - Tentacles  |  Q/W - Algorithm")
        print("  +/- - Segments  |  R - Reset camera")
        print("  Use sliders for fine control!")
        print("=" * 70)
        print()

    def create_ui(self):
        """Create enhanced UI with sliders and controls"""
        from ursina import Text, Button, Slider, Panel

        # Store UI elements for later reference
        self.ui_elements = []

        # Title and info panel
        self.info_text = Text(
            text="",
            position=(-0.85, 0.47),
            origin=(0, 0),
            scale=1.0,
            color=color.white,
            background=True
        )
        self.ui_elements.append(self.info_text)

        # Algorithm buttons
        y_pos = 0.40

        self.btn_bezier = Button(
            text='BEZIER',
            color=color.rgb(0.3, 0.3, 0.4),
            scale=(0.15, 0.04),
            position=(-0.55, y_pos),
            on_click=lambda: self.set_algorithm('bezier')
        )
        self.ui_elements.append(self.btn_bezier)

        self.btn_fourier = Button(
            text='FOURIER',
            color=color.rgb(0.3, 0.3, 0.4),
            scale=(0.15, 0.04),
            position=(-0.25, y_pos),
            on_click=lambda: self.set_algorithm('fourier')
        )
        self.ui_elements.append(self.btn_fourier)

        # Algorithm parameters section
        y_pos = 0.32
        self.param_label = Text(
            text="Algorithm Parameters:",
            position=(-0.85, y_pos),
            origin=(0, 0),
            scale=0.9,
            color=color.rgb(0.7, 0.9, 1.0)
        )
        self.ui_elements.append(self.param_label)

        # Bezier sliders
        y_pos -= 0.05
        y_pos_bezier = y_pos
        self.bezier_strength_label = Text(
            text="Control Strength:",
            position=(-0.85, y_pos_bezier),
            origin=(0, 0),
            scale=0.8,
            color=color.white,
            visible=False
        )
        self.ui_elements.append(self.bezier_strength_label)

        self.bezier_strength_slider = Slider(
            min=0.1, max=0.8, default=0.4, step=0.05,
            position=(-0.6, y_pos_bezier - 0.01),
            width=0.2, height=0.02,
            on_value_changed=self.on_param_changed,
            visible=False
        )
        self.ui_elements.append(self.bezier_strength_slider)

        self.bezier_strength_value = Text(
            text="0.40",
            position=(-0.37, y_pos_bezier),
            origin=(0, 0),
            scale=0.8,
            color=color.rgb(0.5, 1.0, 0.5),
            visible=False
        )
        self.ui_elements.append(self.bezier_strength_value)

        # Fourier sliders
        y_pos_fourier = y_pos
        self.fourier_waves_label = Text(
            text="Wave Count:",
            position=(-0.85, y_pos_fourier),
            origin=(0, 0),
            scale=0.8,
            color=color.white,
            visible=False
        )
        self.ui_elements.append(self.fourier_waves_label)

        self.fourier_waves_slider = Slider(
            min=1, max=7, default=3, step=1,
            position=(-0.6, y_pos_fourier - 0.01),
            width=0.2, height=0.02,
            on_value_changed=self.on_param_changed,
            visible=False
        )
        self.ui_elements.append(self.fourier_waves_slider)

        self.fourier_waves_value = Text(
            text="3",
            position=(-0.37, y_pos_fourier),
            origin=(0, 0),
            scale=0.8,
            color=color.rgb(0.5, 1.0, 0.5),
            visible=False
        )
        self.ui_elements.append(self.fourier_waves_value)

        y_pos -= 0.05
        self.fourier_amp_label = Text(
            text="Amplitude:",
            position=(-0.85, y_pos),
            origin=(0, 0),
            scale=0.8,
            color=color.white,
            visible=False
        )
        self.ui_elements.append(self.fourier_amp_label)

        self.fourier_amp_slider = Slider(
            min=0.05, max=0.4, default=0.15, step=0.05,
            position=(-0.6, y_pos - 0.01),
            width=0.2, height=0.02,
            on_value_changed=self.on_param_changed,
            visible=False
        )
        self.ui_elements.append(self.fourier_amp_slider)

        self.fourier_amp_value = Text(
            text="0.15",
            position=(-0.37, y_pos),
            origin=(0, 0),
            scale=0.8,
            color=color.rgb(0.5, 1.0, 0.5),
            visible=False
        )
        self.ui_elements.append(self.fourier_amp_value)

        # Thickness parameters (always visible)
        y_pos = 0.19
        self.thickness_label = Text(
            text="Thickness:",
            position=(-0.85, y_pos),
            origin=(0, 0),
            scale=0.9,
            color=color.rgb(0.7, 0.9, 1.0)
        )
        self.ui_elements.append(self.thickness_label)

        y_pos -= 0.05
        self.thickness_base_label = Text(
            text="Base:",
            position=(-0.85, y_pos),
            origin=(0, 0),
            scale=0.8,
            color=color.white
        )
        self.ui_elements.append(self.thickness_base_label)

        self.thickness_base_slider = Slider(
            min=0.1, max=0.5, default=0.25, step=0.05,
            position=(-0.65, y_pos - 0.01),
            width=0.2, height=0.02,
            on_value_changed=self.on_thickness_changed
        )
        self.ui_elements.append(self.thickness_base_slider)

        self.thickness_base_value = Text(
            text="0.25",
            position=(-0.42, y_pos),
            origin=(0, 0),
            scale=0.8,
            color=color.rgb(0.5, 1.0, 0.5)
        )
        self.ui_elements.append(self.thickness_base_value)

        y_pos -= 0.05
        self.taper_label = Text(
            text="Taper:",
            position=(-0.85, y_pos),
            origin=(0, 0),
            scale=0.8,
            color=color.white
        )
        self.ui_elements.append(self.taper_label)

        self.taper_slider = Slider(
            min=0.0, max=1.0, default=0.6, step=0.1,
            position=(-0.65, y_pos - 0.01),
            width=0.2, height=0.02,
            on_value_changed=self.on_thickness_changed
        )
        self.ui_elements.append(self.taper_slider)

        self.taper_value = Text(
            text="0.6",
            position=(-0.42, y_pos),
            origin=(0, 0),
            scale=0.8,
            color=color.rgb(0.5, 1.0, 0.5)
        )
        self.ui_elements.append(self.taper_value)

        # Presets section
        y_pos = 0.01
        self.presets_label = Text(
            text="Presets:",
            position=(-0.85, y_pos),
            origin=(0, 0),
            scale=0.9,
            color=color.rgb(0.7, 0.9, 1.0)
        )
        self.ui_elements.append(self.presets_label)

        y_pos -= 0.05
        self.preset_buttons = []
        presets = [
            ('Default', 'bezier', {'control_strength': 0.4}),
            ('Wavy', 'fourier', {'num_waves': 4, 'amplitude': 0.25}),
            ('Tight', 'bezier', {'control_strength': 0.2})
        ]

        x_offset = 0
        for name, algo, params in presets:
            btn = Button(
                text=name,
                color=color.rgb(0.3, 0.4, 0.3),
                scale=(0.12, 0.035),
                position=(-0.85 + x_offset, y_pos),
                on_click=lambda a=algo, p=params: self.load_preset(a, p)
            )
            self.preset_buttons.append(btn)
            self.ui_elements.append(btn)
            x_offset += 0.30

        # Help text (bottom corner)
        self.help_text = Text(
            text="Press H for help",
            position=(-0.95, -0.45),
            origin=(0, 0),
            scale=0.8,
            color=color.rgb(0.5, 0.5, 0.6)
        )
        self.ui_elements.append(self.help_text)

        # Help overlay (initially hidden)
        self.help_overlay = None
        self.create_help_overlay()

        self.update_ui()

    def create_help_overlay(self):
        """Create help overlay panel"""
        from ursina import Text, Panel

        help_text = """DNA EDITOR - CONTROLS

CAMERA:
  Mouse Drag - Orbit camera
  Scroll - Zoom in/out
  R - Reset camera

TENTACLES:
  1/2/3 - Set tentacle count
  +/- - Adjust segment count (5-20)

ALGORITHM:
  Q - Bezier (smooth curves)
  W - Fourier (wave composition)
  Sliders - Adjust parameters

EDITING:
  Ctrl+Z - Undo
  Ctrl+Y - Redo
  Presets - Click preset buttons

OTHER:
  H - Toggle this help
  ESC - Quit"""

        self.help_overlay = Text(
            text=help_text,
            position=(0, 0),
            origin=(0, 0),
            scale=0.8,
            color=color.white,
            background=True,
            visible=False
        )
        self.ui_elements.append(self.help_overlay)

    def update_ui(self):
        """Update UI text and show/hide algorithm-specific sliders"""
        self.info_text.text = (
            f"Tentacles: {self.num_tentacles}  |  "
            f"Segments: {self.segments}  |  "
            f"Algorithm: {self.algorithm.upper()}"
        )

        # Highlight active button
        self.btn_bezier.color = color.rgb(0.5, 0.7, 0.5) if self.algorithm == 'bezier' else color.rgb(0.3, 0.3, 0.4)
        self.btn_fourier.color = color.rgb(0.5, 0.7, 0.5) if self.algorithm == 'fourier' else color.rgb(0.3, 0.3, 0.4)

        # Show/hide algorithm-specific sliders
        is_bezier = self.algorithm == 'bezier'
        is_fourier = self.algorithm == 'fourier'

        self.bezier_strength_label.visible = is_bezier
        self.bezier_strength_slider.visible = is_bezier
        self.bezier_strength_value.visible = is_bezier

        self.fourier_waves_label.visible = is_fourier
        self.fourier_waves_slider.visible = is_fourier
        self.fourier_waves_value.visible = is_fourier
        self.fourier_amp_label.visible = is_fourier
        self.fourier_amp_slider.visible = is_fourier
        self.fourier_amp_value.visible = is_fourier

        # Update slider values from current params
        if is_bezier:
            val = self.params['bezier']['control_strength']
            self.bezier_strength_slider.value = val
            self.bezier_strength_value.text = f"{val:.2f}"
        elif is_fourier:
            waves = self.params['fourier']['num_waves']
            amp = self.params['fourier']['amplitude']
            self.fourier_waves_slider.value = waves
            self.fourier_waves_value.text = f"{int(waves)}"
            self.fourier_amp_slider.value = amp
            self.fourier_amp_value.text = f"{amp:.2f}"

        # Update thickness values
        self.thickness_base_slider.value = self.thickness_base
        self.thickness_base_value.text = f"{self.thickness_base:.2f}"
        self.taper_slider.value = self.taper_factor
        self.taper_value.text = f"{self.taper_factor:.1f}"

    def on_param_changed(self):
        """Callback when algorithm parameter slider changes"""
        # Save state for undo
        self.save_state()

        # Update the parameter based on which slider changed
        if self.algorithm == 'bezier':
            self.params['bezier']['control_strength'] = self.bezier_strength_slider.value
            self.bezier_strength_value.text = f"{self.bezier_strength_slider.value:.2f}"
        elif self.algorithm == 'fourier':
            # Check which slider was modified (this is called for both)
            self.params['fourier']['num_waves'] = int(self.fourier_waves_slider.value)
            self.params['fourier']['amplitude'] = self.fourier_amp_slider.value
            self.fourier_waves_value.text = f"{int(self.fourier_waves_slider.value)}"
            self.fourier_amp_value.text = f"{self.fourier_amp_slider.value:.2f}"

        # Rebuild creature with new parameters
        self.rebuild_creature()

    def on_thickness_changed(self):
        """Callback when thickness slider changes"""
        self.save_state()

        self.thickness_base = self.thickness_base_slider.value
        self.taper_factor = self.taper_slider.value

        self.thickness_base_value.text = f"{self.thickness_base:.2f}"
        self.taper_value.text = f"{self.taper_factor:.1f}"

        self.rebuild_creature()

    def load_preset(self, algo, params):
        """Load a parameter preset"""
        self.save_state()

        self.algorithm = algo
        self.params[algo].update(params)

        self.rebuild_creature()
        self.update_ui()

        print(f"Loaded preset: {algo} with params {params}")

    def save_state(self):
        """Save current state to history for undo/redo"""
        state = {
            'num_tentacles': self.num_tentacles,
            'segments': self.segments,
            'algorithm': self.algorithm,
            'params': {k: v.copy() for k, v in self.params.items()},
            'thickness_base': self.thickness_base,
            'taper_factor': self.taper_factor
        }

        # Clear future history if we're not at the end
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]

        # Add new state
        self.history.append(state)

        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
        else:
            self.history_index += 1

    def undo(self):
        """Undo to previous state"""
        if self.history_index > 0:
            self.history_index -= 1
            self.restore_state(self.history[self.history_index])
            print(f"Undo (history {self.history_index + 1}/{len(self.history)})")

    def redo(self):
        """Redo to next state"""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.restore_state(self.history[self.history_index])
            print(f"Redo (history {self.history_index + 1}/{len(self.history)})")

    def restore_state(self, state):
        """Restore a saved state"""
        self.num_tentacles = state['num_tentacles']
        self.segments = state['segments']
        self.algorithm = state['algorithm']
        self.params = {k: v.copy() for k, v in state['params'].items()}
        self.thickness_base = state['thickness_base']
        self.taper_factor = state['taper_factor']

        self.rebuild_creature()
        self.update_ui()

    def toggle_help(self):
        """Toggle help overlay visibility"""
        self.help_visible = not self.help_visible
        self.help_overlay.visible = self.help_visible

    def rebuild_creature(self):
        """Rebuild creature with current parameters"""
        if self.creature:
            self.creature.destroy()

        self.creature = TentacleCreature(
            num_tentacles=self.num_tentacles,
            segments_per_tentacle=self.segments,
            algorithm=self.algorithm,
            algorithm_params=self.params[self.algorithm],
            thickness_base=self.thickness_base,
            taper_factor=self.taper_factor
        )

        print(f"Built: {self.num_tentacles} tentacles, {self.segments} segments, {self.algorithm}")
        print(f"Params: {self.params[self.algorithm]}")
        print(f"Thickness: base={self.thickness_base}, taper={self.taper_factor}")
        print(f"Creature root parent: {self.creature.root.parent}")

    def set_algorithm(self, algo):
        """Change algorithm"""
        self.save_state()
        self.algorithm = algo
        self.rebuild_creature()
        self.update_ui()

    def set_tentacles(self, count):
        """Change tentacle count"""
        self.save_state()
        self.num_tentacles = max(1, min(3, count))
        self.rebuild_creature()
        self.update_ui()

    def adjust_segments(self, delta):
        """Adjust segment count"""
        self.save_state()
        self.segments = max(5, min(20, self.segments + delta))
        self.rebuild_creature()
        self.update_ui()

    def update(self):
        """Update loop"""
        from ursina import time as ursina_time

        dt = ursina_time.dt
        self.time += dt

        # Update camera orbit
        if held_keys['left mouse']:
            self.camera_angle += mouse.velocity[0] * 200
            self.camera_height += mouse.velocity[1] * 5

        self.camera_height = max(0.5, min(5, self.camera_height))

        # Zoom
        if held_keys['scroll up']:
            self.camera_distance -= 0.5
        if held_keys['scroll down']:
            self.camera_distance += 0.5
        self.camera_distance = max(2, min(15, self.camera_distance))

        # Calculate camera position
        angle_rad = math.radians(self.camera_angle)
        cam_x = self.camera_distance * math.sin(angle_rad)
        cam_z = -self.camera_distance * math.cos(angle_rad)

        camera.position = Vec3(cam_x, self.camera_height, cam_z)
        camera.look_at((0, 0, 0))

        # Update creature animation
        if self.creature:
            self.creature.update_animation(self.time)

        # Handle keyboard
        if held_keys['1']:
            self.set_tentacles(1)
            held_keys['1'] = False
        if held_keys['2']:
            self.set_tentacles(2)
            held_keys['2'] = False
        if held_keys['3']:
            self.set_tentacles(3)
            held_keys['3'] = False

        if held_keys['q']:
            self.set_algorithm('bezier')
            held_keys['q'] = False
        if held_keys['w']:
            self.set_algorithm('fourier')
            held_keys['w'] = False

        if held_keys['+'] or held_keys['=']:
            self.adjust_segments(1)
            held_keys['+'] = False
            held_keys['='] = False
        if held_keys['-']:
            self.adjust_segments(-1)
            held_keys['-'] = False

        if held_keys['r']:
            self.camera_angle = 0
            self.camera_height = 2
            self.camera_distance = 6
            held_keys['r'] = False
            print("Camera reset")

        # Help overlay
        if held_keys['h']:
            self.toggle_help()
            held_keys['h'] = False

        # Undo/Redo
        if held_keys['control']:
            if held_keys['z']:
                self.undo()
                held_keys['z'] = False
            if held_keys['y']:
                self.redo()
                held_keys['y'] = False


def main():
    """Main entry point"""
    app = Ursina(
        title="DNA Editor - Creature Tentacle Generator",
        borderless=False,
        fullscreen=False
    )

    window.size = (1400, 900)
    window.position = (100, 50)
    window.color = color.rgb(0.05, 0.05, 0.1)

    camera.fov = 60

    editor = TentacleEditor()

    # Assign update function
    app.update = editor.update

    app.run()


if __name__ == "__main__":
    main()
