"""
DragonCreature model - Space Harrier inspired segmented flying serpent.
Chain of spheres forming a snake-like body with smooth weaving/bobbing animation.
"""

from ursina import Entity, Vec3, color, destroy
import math
import random
from .eye import Eye
from ..core.curves import bezier_curve
from ..core.constants import GOLDEN_RATIO


class HornSegment:
    """Single segment in a branching horn structure (sphere with connector tube)."""

    def __init__(self, position, size, horn_color, parent_entity, toon_shader=None,
                 parent_segment=None):
        """
        Create a horn segment.

        Args:
            position: Vec3 position in world space
            size: Sphere scale
            horn_color: RGB tuple (0-1)
            parent_entity: Parent entity (scene root)
            toon_shader: Optional toon shader to apply
            parent_segment: Reference to parent HornSegment (None for base)
        """
        self.base_position = position
        self.size = size
        self.horn_color = horn_color
        self.parent_segment = parent_segment
        self.children = []  # Child HornSegments for branching
        self.connector_tube = None

        # Create sphere entity
        sphere_params = {
            'model': 'sphere',
            'color': color.rgb(*horn_color),
            'scale': size,
            'position': position,
            'parent': parent_entity
        }

        if toon_shader is not None:
            sphere_params['shader'] = toon_shader

        self.entity = Entity(**sphere_params)

        # Create connector tube to parent segment (if not base)
        if parent_segment is not None:
            self._create_connector_tube(parent_entity, horn_color, toon_shader)

    def _create_connector_tube(self, scene_parent, tube_color, toon_shader):
        """Create tube connecting this segment to parent segment."""
        if self.parent_segment is None:
            return

        # Calculate tube position, rotation, and length
        midpoint = (self.entity.position + self.parent_segment.entity.position) / 2
        length = (self.entity.position - self.parent_segment.entity.position).length()

        # Tube radius (average of both segment sizes)
        avg_size = (self.size + self.parent_segment.size) / 2
        tube_radius = avg_size * 0.35  # Slightly thicker for horns

        # Create tube entity (stretched cube along Y axis)
        tube_params = {
            'model': 'cube',
            'color': color.rgb(*tube_color),
            'position': midpoint,
            'scale': (tube_radius, length / 2, tube_radius),
            'parent': scene_parent
        }

        if toon_shader is not None:
            tube_params['shader'] = toon_shader

        self.connector_tube = Entity(**tube_params)

        # Orient tube from parent to current segment
        self.connector_tube.look_at(self.parent_segment.entity, axis=Vec3.up)

    def update_animation(self, time, base_offset, sway_amount):
        """
        Update horn segment animation.

        Args:
            time: Current animation time
            base_offset: Base position offset from head movement
            sway_amount: Intensity of horn sway
        """
        # Apply base offset from head movement
        animated_position = self.base_position + base_offset

        # Add subtle sway animation (horns are mostly rigid but have slight flex)
        if sway_amount > 0:
            # Sway increases toward tip (segments further from base move more)
            # Calculate depth in branch (root = 0, children = 1, grandchildren = 2, etc.)
            depth = 0
            parent = self.parent_segment
            while parent is not None:
                depth += 1
                parent = parent.parent_segment

            # Sway motion (slower and more subtle than body motion)
            sway_phase = time * 0.8 + depth * 0.5
            sway_x = math.sin(sway_phase) * sway_amount * depth * 0.03
            sway_z = math.cos(sway_phase * 1.2) * sway_amount * depth * 0.02

            animated_position += Vec3(sway_x, 0, sway_z)

        self.entity.position = animated_position

        # Update connector tube if present
        if self.connector_tube is not None and self.parent_segment is not None:
            # Recalculate midpoint
            midpoint = (self.entity.position + self.parent_segment.entity.position) / 2
            self.connector_tube.position = midpoint

            # Recalculate length
            length = (self.entity.position - self.parent_segment.entity.position).length()
            self.connector_tube.scale_y = length / 2

            # Update rotation
            self.connector_tube.look_at(self.parent_segment.entity, axis=Vec3.up)

    def destroy(self):
        """Cleanup segment entities."""
        if self.connector_tube is not None:
            destroy(self.connector_tube)
        destroy(self.entity)


class DragonSegment:
    """Single segment (sphere) in the dragon body with connector tube to previous segment."""

    def __init__(self, segment_index, total_segments, position, size,
                 segment_color, parent, toon_shader=None, previous_segment=None):
        """
        Create a dragon segment.

        Args:
            segment_index: Index of this segment (0 = head, increasing toward tail)
            total_segments: Total number of segments in dragon
            position: Vec3 position in world space
            size: Sphere scale
            segment_color: RGB tuple (0-1) for this segment
            parent: Parent entity (scene root)
            toon_shader: Optional toon shader to apply
            previous_segment: Reference to previous DragonSegment (None for head)
        """
        self.segment_index = segment_index
        self.total_segments = total_segments
        self.base_position = position
        self.size = size
        self.segment_color = segment_color
        self.previous_segment = previous_segment
        self.connector_tube = None

        # Create sphere entity
        sphere_params = {
            'model': 'sphere',
            'color': color.rgb(*segment_color),
            'scale': size,
            'position': position,
            'parent': parent
        }

        if toon_shader is not None:
            sphere_params['shader'] = toon_shader

        self.entity = Entity(**sphere_params)

        # Create connector tube to previous segment (if not head)
        if previous_segment is not None:
            self._create_connector_tube(parent, segment_color, toon_shader)

    def _create_connector_tube(self, scene_parent, tube_color, toon_shader):
        """Create tube connecting this segment to previous segment."""
        if self.previous_segment is None:
            return

        # Calculate tube position, rotation, and length
        midpoint = (self.entity.position + self.previous_segment.entity.position) / 2
        length = (self.entity.position - self.previous_segment.entity.position).length()

        # Tube radius (average of both segment sizes)
        avg_size = (self.size + self.previous_segment.size) / 2
        tube_radius = avg_size * 0.4  # Thicker tubes for dragon body

        # Create tube entity (stretched cube along Y axis)
        tube_params = {
            'model': 'cube',
            'color': color.rgb(*tube_color),
            'position': midpoint,
            'scale': (tube_radius, length / 2, tube_radius),
            'parent': scene_parent
        }

        if toon_shader is not None:
            tube_params['shader'] = toon_shader

        self.connector_tube = Entity(**tube_params)

        # Orient tube from previous to current segment
        self.connector_tube.look_at(self.previous_segment.entity, axis=Vec3.up)

    def update_connector_tube(self):
        """Update connector tube position to follow animated segments."""
        if self.connector_tube is None or self.previous_segment is None:
            return

        # Recalculate midpoint
        midpoint = (self.entity.position + self.previous_segment.entity.position) / 2
        self.connector_tube.position = midpoint

        # Recalculate length
        length = (self.entity.position - self.previous_segment.entity.position).length()
        self.connector_tube.scale_y = length / 2

        # Update rotation
        self.connector_tube.look_at(self.previous_segment.entity, axis=Vec3.up)

    def destroy(self):
        """Cleanup segment entities."""
        if self.connector_tube is not None:
            destroy(self.connector_tube)
        destroy(self.entity)


class DragonWhisker:
    """Thin, curved whisker extending from dragon's lower jaw/snout."""

    def __init__(self, anchor_position, direction_angle, head_radius, num_segments,
                 thickness, curve_intensity, whisker_color, parent_entity, toon_shader=None):
        """
        Create a curved whisker using Bezier curve.

        Args:
            anchor_position: Vec3 position on head surface where whisker attaches
            direction_angle: Angle (radians) for whisker direction (left/right)
            head_radius: Radius of head sphere (for calculating target point)
            num_segments: Number of segments in whisker chain (3-6)
            thickness: Base thickness of whisker
            curve_intensity: How much whisker curves (0.2-0.6)
            whisker_color: RGB tuple (0-1)
            parent_entity: Parent entity (scene root)
            toon_shader: Optional toon shader to apply
        """
        self.anchor_position = anchor_position
        self.num_segments = num_segments
        self.thickness = thickness
        self.whisker_color = whisker_color
        self.spheres = []
        self.connector_tubes = []

        # Random phase offset for animation variation
        self.animation_phase = random.random() * math.pi * 2

        # Calculate target point for whisker (downward and backward curve)
        whisker_length = head_radius * 1.2  # Whisker extends ~1.2x head radius

        # Target point calculation (relative to anchor):
        # - Downward (negative Y): -0.6 to -0.8 of whisker_length
        # - Backward (positive Z in dragon coords): +0.4 to +0.5 of whisker_length
        # - Outward (X follows direction_angle)
        target_offset = Vec3(
            math.sin(direction_angle) * whisker_length * 0.3,  # Outward to side
            -whisker_length * 0.7,  # Downward
            whisker_length * 0.45  # Backward (dragon faces -Z, so +Z is backward)
        )
        target_position = anchor_position + target_offset

        # Generate curve points using Bezier
        curve_points = bezier_curve(
            anchor_position,
            target_position,
            num_segments,
            control_strength=curve_intensity
        )

        # Create sphere chain along curve
        previous_sphere = None
        for i, point in enumerate(curve_points):
            # Calculate size with golden ratio tapering (thicker at base, thinner at tip)
            segment_size = thickness / (GOLDEN_RATIO ** (i * 0.8))
            segment_size = max(segment_size, 0.02)  # Minimum size

            # Slight color darkening toward tip
            color_factor = 1.0 - (i / num_segments) * 0.2
            segment_color = (
                whisker_color[0] * color_factor,
                whisker_color[1] * color_factor,
                whisker_color[2] * color_factor
            )

            # Create sphere entity
            sphere_params = {
                'model': 'sphere',
                'color': color.rgb(*segment_color),
                'scale': segment_size,
                'position': point,
                'parent': parent_entity
            }

            if toon_shader is not None:
                sphere_params['shader'] = toon_shader

            sphere = Entity(**sphere_params)
            sphere.base_position = point  # Store base position for animation
            sphere.segment_index = i
            self.spheres.append(sphere)

            # Create connector tube to previous sphere
            if previous_sphere is not None:
                self._create_connector_tube(previous_sphere, sphere, segment_color,
                                           parent_entity, toon_shader)

            previous_sphere = sphere

    def _create_connector_tube(self, sphere1, sphere2, tube_color, parent, toon_shader):
        """Create tube connecting two whisker spheres."""
        # Calculate tube position, rotation, and length
        midpoint = (sphere1.position + sphere2.position) / 2
        length = (sphere2.position - sphere1.position).length()

        # Tube radius (average of both sphere sizes, thinner than body tubes)
        avg_size = (sphere1.scale_x + sphere2.scale_x) / 2
        tube_radius = avg_size * 0.3

        # Create tube entity (stretched cube along Y axis)
        tube_params = {
            'model': 'cube',
            'color': color.rgb(*tube_color),
            'position': midpoint,
            'scale': (tube_radius, length / 2, tube_radius),
            'parent': parent
        }

        if toon_shader is not None:
            tube_params['shader'] = toon_shader

        tube = Entity(**tube_params)

        # Orient tube from sphere1 to sphere2
        tube.look_at(sphere1, axis=Vec3.up)

        # Store references for animation
        tube.sphere1 = sphere1
        tube.sphere2 = sphere2

        self.connector_tubes.append(tube)

    def update_animation(self, time, head_offset, sway_intensity):
        """
        Update whisker animation with gentle sway.

        Args:
            time: Current animation time
            head_offset: Offset from head movement (Vec3)
            sway_intensity: Base sway intensity multiplier
        """
        for sphere in self.spheres:
            i = sphere.segment_index
            segment_t = i / max(self.num_segments - 1, 1)

            # Apply head movement offset
            animated_position = sphere.base_position + head_offset

            # Gentle sway (increases toward tip)
            # Base is stable, tip waves more
            sway_multiplier = segment_t ** 1.5  # Exponential increase toward tip

            # Multi-frequency sway for organic motion
            sway_phase = time * 1.2 + self.animation_phase + i * 0.3
            sway_x = math.sin(sway_phase) * sway_intensity * sway_multiplier * 0.04
            sway_y = math.sin(sway_phase * 0.8 + 0.5) * sway_intensity * sway_multiplier * 0.03
            sway_z = math.cos(sway_phase * 1.1) * sway_intensity * sway_multiplier * 0.02

            animated_position += Vec3(sway_x, sway_y, sway_z)

            sphere.position = animated_position

        # Update all connector tubes
        for tube in self.connector_tubes:
            # Recalculate midpoint
            midpoint = (tube.sphere1.position + tube.sphere2.position) / 2
            tube.position = midpoint

            # Recalculate length
            length = (tube.sphere2.position - tube.sphere1.position).length()
            tube.scale_y = length / 2

            # Update rotation
            tube.look_at(tube.sphere1, axis=Vec3.up)

    def destroy(self):
        """Cleanup whisker entities."""
        for sphere in self.spheres:
            destroy(sphere)
        for tube in self.connector_tubes:
            destroy(tube)


class DragonCreature:
    """Space Harrier inspired dragon - segmented serpent with weaving/bobbing motion."""

    def __init__(self, num_segments=15, segment_thickness=0.3, taper_factor=0.6,
                 head_scale=3.0, body_color=(200, 40, 40), head_color=(255, 200, 50),
                 weave_amplitude=0.5, bob_amplitude=0.3, anim_speed=1.5,
                 num_eyes=2, eye_size=0.15, eyeball_color=(255, 200, 50), pupil_color=(20, 0, 0),
                 num_horns=2, horn_branch_depth=1, horn_branch_count=2, horn_base_size=0.15,
                 horn_color=(255, 220, 180),
                 num_whiskers_per_side=2, whisker_segments=4, whisker_thickness=0.05,
                 whisker_curve_intensity=0.4, whisker_color=None):
        """
        Create a dragon creature.

        Args:
            num_segments: Number of body segments (5-30)
            segment_thickness: Base segment size (0.1-0.8)
            taper_factor: Size reduction toward tail (0.0-0.9, higher = more taper)
            head_scale: Head size multiplier (1.0-3.5)
            body_color: RGB tuple for body (0-255 range - Ursina compat)
            head_color: RGB tuple for head (0-255 range)
            weave_amplitude: Side-to-side motion intensity (0.0-1.0)
            bob_amplitude: Up-down motion intensity (0.0-1.0)
            anim_speed: Animation speed multiplier (0.5-5.0)
            num_eyes: Number of eyes on head (0-8)
            eye_size: Size of each eye (0.05-0.3)
            eyeball_color: RGB tuple for eyeball (0-255 range)
            pupil_color: RGB tuple for pupil (0-255 range)
            num_horns: Number of horns on head (0-4)
            horn_branch_depth: Horn branching levels (0-2)
            horn_branch_count: Branches per horn segment (1-3)
            horn_base_size: Base horn segment size (0.05-0.4)
            horn_color: RGB tuple for horns (0-255 range)
            num_whiskers_per_side: Whiskers per side of jaw (1-3, total=2x)
            whisker_segments: Segments per whisker for length (3-6)
            whisker_thickness: Base whisker thickness (0.03-0.08)
            whisker_curve_intensity: Whisker curve amount (0.2-0.6)
            whisker_color: RGB tuple for whiskers (0-255, None=head_color*0.9)
        """
        # Create root entity
        self.root = Entity(position=(0, 0, 0))
        self.segments = []
        self.eyes = []
        self.eye_offsets = []  # Vec3 offsets from head center for each eye
        self.horns = []  # List of all horn segments (flattened tree structure)
        self.whiskers = []  # List of DragonWhisker objects

        # Store parameters
        self.num_segments = num_segments
        self.segment_thickness = segment_thickness
        self.taper_factor = taper_factor
        self.head_scale = head_scale
        # Convert RGB 0-255 to 0-1 for Ursina
        self.body_color = (body_color[0] / 255.0, body_color[1] / 255.0, body_color[2] / 255.0)
        self.head_color = (head_color[0] / 255.0, head_color[1] / 255.0, head_color[2] / 255.0)
        self.weave_amplitude = weave_amplitude
        self.bob_amplitude = bob_amplitude
        self.anim_speed = anim_speed
        self.num_eyes = num_eyes
        self.eye_size = eye_size
        self.eyeball_color = (eyeball_color[0] / 255.0, eyeball_color[1] / 255.0, eyeball_color[2] / 255.0)
        self.pupil_color = (pupil_color[0] / 255.0, pupil_color[1] / 255.0, pupil_color[2] / 255.0)
        self.num_horns = num_horns
        self.horn_branch_depth = horn_branch_depth
        self.horn_branch_count = horn_branch_count
        self.horn_base_size = horn_base_size
        self.horn_color = (horn_color[0] / 255.0, horn_color[1] / 255.0, horn_color[2] / 255.0)
        self.num_whiskers_per_side = num_whiskers_per_side
        self.whisker_segments = whisker_segments
        self.whisker_thickness = whisker_thickness
        self.whisker_curve_intensity = whisker_curve_intensity
        # Whisker color: default to slightly darker head color if not specified
        if whisker_color is None:
            self.whisker_color = (self.head_color[0] * 0.9, self.head_color[1] * 0.9, self.head_color[2] * 0.9)
        else:
            self.whisker_color = (whisker_color[0] / 255.0, whisker_color[1] / 255.0, whisker_color[2] / 255.0)

        # Attack animation state
        self.is_attacking = False
        self.attack_start_time = 0

        # Random phase offset for organic variation
        self.phase_offset = random.random() * math.pi * 2

        # Create toon shader (shared across all parts)
        from ..shaders import create_toon_shader
        self.toon_shader = create_toon_shader()
        if self.toon_shader is None:
            print("WARNING: Toon shader creation failed in DragonCreature, using default rendering")

        # Generate dragon body
        self._generate_dragon()

    def _generate_dragon(self):
        """Generate dragon body as chain of spheres."""
        # Clear existing segments
        for segment in self.segments:
            segment.destroy()
        self.segments.clear()

        # Dragon layout: horizontal chain extending forward
        # Segments arranged along +Z axis (head at origin, tail extends forward)
        segment_spacing = self.segment_thickness * 1.8  # Spacing between segment centers

        # Elevation (floating/hovering effect)
        base_elevation = 1.0

        previous_segment = None

        for i in range(self.num_segments):
            # Calculate position along chain
            # Head (i=0) at front, tail (i=max) at front
            z_offset = i * segment_spacing
            x_offset = 0  # No initial X offset (weaving happens in animation)
            y_offset = base_elevation  # Floating height

            position = Vec3(x_offset, y_offset, z_offset)

            # Calculate size with tapering
            # Head is largest, tail tapers down
            if i == 0:
                # Head segment
                segment_size = self.segment_thickness * self.head_scale
            else:
                # Body segments: taper from head to tail
                # t ranges from 0 (just after head) to 1 (tail tip)
                t = i / max(self.num_segments - 1, 1)
                # Apply exponential taper for smooth reduction
                taper_multiplier = 1.0 - (self.taper_factor * (t ** 0.7))
                segment_size = self.segment_thickness * taper_multiplier
                segment_size = max(segment_size, 0.1)  # Minimum size

            # Color: head uses head_color, body uses body_color with gradient
            if i == 0:
                segment_color = self.head_color
            else:
                # Gradual transition from head_color to body_color over first few segments
                if i < 3:
                    blend = i / 3.0
                    segment_color = (
                        self.head_color[0] * (1 - blend) + self.body_color[0] * blend,
                        self.head_color[1] * (1 - blend) + self.body_color[1] * blend,
                        self.head_color[2] * (1 - blend) + self.body_color[2] * blend
                    )
                else:
                    # Slight darkening toward tail for depth
                    darkness_factor = 1.0 - (i / self.num_segments) * 0.3
                    segment_color = (
                        self.body_color[0] * darkness_factor,
                        self.body_color[1] * darkness_factor,
                        self.body_color[2] * darkness_factor
                    )

            # Create segment
            segment = DragonSegment(
                segment_index=i,
                total_segments=self.num_segments,
                position=position,
                size=segment_size,
                segment_color=segment_color,
                parent=self.root,
                toon_shader=self.toon_shader,
                previous_segment=previous_segment
            )

            self.segments.append(segment)
            previous_segment = segment

        # Create eyes on head segment
        self._create_eyes()

        # Create horns on head segment
        self._create_horns()

        # Create whiskers on lower jaw/snout
        self._create_whiskers()

    def _create_eyes(self):
        """Create eyes on the dragon's head segment."""
        # Clear existing eyes and offsets
        for eye in self.eyes:
            eye.destroy()
        self.eyes.clear()
        self.eye_offsets.clear()

        if self.num_eyes == 0 or len(self.segments) == 0:
            return

        # Get head segment (first segment)
        head_segment = self.segments[0]
        head_position = head_segment.base_position
        # Ursina sphere: scale=X means radius=X/2 (default sphere has diameter 1)
        head_radius = head_segment.size / 2

        # Position eyes on the front of the head sphere using proper spherical coordinates
        # Dragon faces in -Z direction (forward)

        for i in range(self.num_eyes):
            if self.num_eyes == 1:
                # Single eye: center of head front
                # Spherical coords: theta=0 (front), phi=0 (equator)
                theta = 0  # Azimuthal angle (around Y axis)
                phi = math.pi / 2  # Polar angle from +Y axis (90° = equator)
            elif self.num_eyes == 2:
                # Two eyes: symmetrical left/right on front of head
                # Position at ±30° from center, slightly above equator
                theta = (math.pi / 6) if i == 0 else (-math.pi / 6)  # ±30° left/right
                phi = math.pi * 0.45  # Slightly above equator (0.45 * 180 = 81°)
            else:
                # Multiple eyes: distribute in a ring on front hemisphere
                # Ring around the front of the head
                ring_angle = (i / self.num_eyes) * math.pi * 2  # 0 to 360°
                # Position eyes in a cone pointing forward
                theta = math.sin(ring_angle) * (math.pi / 4)  # ±45° max
                phi = math.pi / 2 - math.cos(ring_angle) * (math.pi / 6)  # Vary elevation

            # Convert spherical to Cartesian coordinates on unit sphere
            # Standard spherical coordinates: x = sin(phi)*cos(theta), y = cos(phi), z = sin(phi)*sin(theta)
            # But we want front to be -Z, so we rotate the coordinate system
            x_normalized = math.sin(phi) * math.sin(theta)  # Left/right
            y_normalized = math.cos(phi)  # Up/down
            z_normalized = -math.sin(phi) * math.cos(theta)  # Front/back (negative for front)

            # Calculate eye offset from head center (0.9 to keep eyes slightly inside sphere edge)
            eye_offset = Vec3(
                x_normalized * head_radius * 0.9,
                y_normalized * head_radius * 0.9,
                z_normalized * head_radius * 0.9
            )
            eye_position = head_position + eye_offset

            # Create eye
            eye = Eye(
                position=eye_position,
                size=self.eye_size,
                eyeball_color=self.eyeball_color,
                pupil_color=self.pupil_color,
                parent=self.root,
                toon_shader=self.toon_shader
            )

            self.eyes.append(eye)
            self.eye_offsets.append(eye_offset)  # Store offset for animation updates

    def _create_horns(self):
        """Create horns on the dragon's head using golden angle placement."""
        from ..core.constants import GOLDEN_RATIO, GOLDEN_ANGLE

        # Clear existing horns
        for horn_segment in self.horns:
            horn_segment.destroy()
        self.horns.clear()

        if self.num_horns == 0 or len(self.segments) == 0:
            return

        # Get head segment (first segment)
        head_segment = self.segments[0]
        head_position = head_segment.base_position
        head_radius = head_segment.size / 2

        # Create horn anchor points on upper hemisphere of head
        for i in range(self.num_horns):
            if self.num_horns == 1:
                # Single horn: top center of head
                theta = 0
                phi = 0  # Top of sphere
            elif self.num_horns == 2:
                # Two horns: symmetrical left/right on top-front of head
                # Position at ±45° from center, slightly forward
                theta = (math.pi / 4) if i == 0 else (-math.pi / 4)  # ±45° left/right
                phi = math.pi * 0.25  # 25% down from top (still upper hemisphere)
            elif self.num_horns == 3:
                # Three horns: center + two sides (triceratops style)
                if i == 0:
                    theta = 0
                    phi = math.pi * 0.2  # Front-center horn
                else:
                    theta = (math.pi / 3) if i == 1 else (-math.pi / 3)  # ±60° for side horns
                    phi = math.pi * 0.3
            else:
                # Four or more horns: golden angle distribution on upper hemisphere
                # Bias toward upper hemisphere (0° to 90° from top)
                angle = i * GOLDEN_ANGLE
                # Map to upper hemisphere only (phi from 0 to π/2)
                phi = (i / self.num_horns) * (math.pi / 2)
                theta = angle

            # Convert spherical to Cartesian coordinates on unit sphere
            x_normalized = math.sin(phi) * math.sin(theta)
            y_normalized = math.cos(phi)  # Y up (top of sphere)
            z_normalized = -math.sin(phi) * math.cos(theta)  # Front facing

            # Calculate horn anchor position on head surface
            anchor_offset = Vec3(
                x_normalized * head_radius * 0.95,
                y_normalized * head_radius * 0.95,
                z_normalized * head_radius * 0.95
            )
            anchor_position = head_position + anchor_offset

            # Calculate horn growth direction (outward from head center + upward bias)
            direction = anchor_offset.normalized()
            # Add upward/outward bias for dramatic horn sweep
            direction = (direction + Vec3(0, 0.5, 0)).normalized()

            # Create base horn segment
            base_segment = HornSegment(
                position=anchor_position,
                size=self.horn_base_size,
                horn_color=self.horn_color,
                parent_entity=self.root,
                toon_shader=self.toon_shader,
                parent_segment=None
            )
            self.horns.append(base_segment)

            # Recursively generate branches
            if self.horn_branch_depth > 0:
                self._generate_horn_branches(base_segment, direction, current_depth=0)

    def _generate_horn_branches(self, parent_segment, growth_direction, current_depth):
        """
        Recursively generate horn branches.

        Args:
            parent_segment: Parent HornSegment to branch from
            growth_direction: Vec3 direction for branch growth
            current_depth: Current branching depth (0 = base)
        """
        from ..core.constants import GOLDEN_RATIO, GOLDEN_ANGLE

        if current_depth >= self.horn_branch_depth:
            return  # Max depth reached

        # Generate horn_branch_count children for this segment
        for i in range(self.horn_branch_count):
            # Calculate branch direction using golden angle for natural spacing
            if self.horn_branch_count == 1:
                # Single branch: continue straight with slight upward bias
                branch_direction = growth_direction
            elif self.horn_branch_count == 2:
                # Two branches: fork left/right (antler style)
                angle_offset = (math.pi / 6) if i == 0 else (-math.pi / 6)  # ±30°
                # Rotate growth_direction around Y axis
                cos_a = math.cos(angle_offset)
                sin_a = math.sin(angle_offset)
                branch_direction = Vec3(
                    growth_direction.x * cos_a - growth_direction.z * sin_a,
                    growth_direction.y,
                    growth_direction.x * sin_a + growth_direction.z * cos_a
                )
            else:
                # Three+ branches: use golden angle distribution
                angle = i * GOLDEN_ANGLE
                # Rotate around growth direction
                perpendicular = Vec3(1, 0, 0) if abs(growth_direction.x) < 0.9 else Vec3(0, 1, 0)
                perpendicular = perpendicular.cross(growth_direction).normalized()
                # Rotate perpendicular vector around growth direction
                branch_direction = growth_direction * 0.7 + perpendicular * 0.3

            # Normalize branch direction
            branch_direction = branch_direction.normalized()

            # Calculate child position (extend from parent)
            branch_length = self.horn_base_size * 2.5  # Length between segments
            child_position = parent_segment.base_position + branch_direction * branch_length

            # Size decreases by golden ratio
            child_size = parent_segment.size / GOLDEN_RATIO
            child_size = max(child_size, 0.05)  # Minimum size

            # Slight color variation with depth (darker toward tips)
            darkness_factor = 1.0 - (current_depth / max(self.horn_branch_depth, 1)) * 0.15
            child_color = (
                self.horn_color[0] * darkness_factor,
                self.horn_color[1] * darkness_factor,
                self.horn_color[2] * darkness_factor
            )

            # Create child segment
            child_segment = HornSegment(
                position=child_position,
                size=child_size,
                horn_color=child_color,
                parent_entity=self.root,
                toon_shader=self.toon_shader,
                parent_segment=parent_segment
            )

            parent_segment.children.append(child_segment)
            self.horns.append(child_segment)

            # Recurse to create grandchildren
            self._generate_horn_branches(child_segment, branch_direction, current_depth + 1)

    def _create_whiskers(self):
        """Create whiskers on the dragon's lower jaw/snout using golden angle placement."""
        from ..core.constants import GOLDEN_ANGLE

        # Clear existing whiskers
        for whisker in self.whiskers:
            whisker.destroy()
        self.whiskers.clear()

        if self.num_whiskers_per_side == 0 or len(self.segments) == 0:
            return

        # Get head segment (first segment)
        head_segment = self.segments[0]
        head_position = head_segment.base_position
        head_radius = head_segment.size / 2

        # Create whiskers on lower front sides of head
        # Total whiskers = num_whiskers_per_side * 2 (left and right)
        for side_idx in range(2):  # 0=left, 1=right
            for whisker_idx in range(self.num_whiskers_per_side):
                # Calculate placement using golden angle for natural spacing
                if self.num_whiskers_per_side == 1:
                    # Single whisker per side: place at 50° left/right, 105° from top
                    theta = (math.pi / 3.6) if side_idx == 0 else (-math.pi / 3.6)  # ±50°
                    phi = math.pi * 0.58  # 105° from top (below equator, on lower jaw)
                else:
                    # Multiple whiskers per side: use golden angle spacing
                    # Base angle offset for left/right side
                    base_theta = (math.pi / 4) if side_idx == 0 else (-math.pi / 4)  # ±45°

                    # Add golden angle offset for each whisker
                    theta_offset = whisker_idx * GOLDEN_ANGLE * 0.3  # Scaled for tighter spacing
                    theta = base_theta + theta_offset

                    # Phi (elevation): spread whiskers on lower front face
                    # Range: 100° to 115° from top (lower jaw/snout area)
                    phi_base = math.pi * 0.55  # 100° from top
                    phi_range = math.pi * 0.08  # 15° spread
                    phi = phi_base + (whisker_idx / max(self.num_whiskers_per_side - 1, 1)) * phi_range

                # Convert spherical to Cartesian coordinates on unit sphere
                # Dragon faces -Z (forward), so whiskers should point forward and down
                x_normalized = math.sin(phi) * math.sin(theta)  # Left/right
                y_normalized = math.cos(phi)  # Up/down (negative for below equator)
                z_normalized = -math.sin(phi) * math.cos(theta)  # Front/back

                # Calculate whisker anchor position on head surface
                anchor_position = head_position + Vec3(
                    x_normalized * head_radius * 0.95,
                    y_normalized * head_radius * 0.95,
                    z_normalized * head_radius * 0.95
                )

                # Create whisker
                whisker = DragonWhisker(
                    anchor_position=anchor_position,
                    direction_angle=theta,  # Pass theta for outward curve direction
                    head_radius=head_radius,
                    num_segments=self.whisker_segments,
                    thickness=self.whisker_thickness,
                    curve_intensity=self.whisker_curve_intensity,
                    whisker_color=self.whisker_color,
                    parent_entity=self.root,
                    toon_shader=self.toon_shader
                )

                self.whiskers.append(whisker)

    def rebuild(self, num_segments, segment_thickness, taper_factor, head_scale,
                body_color, head_color, weave_amplitude, bob_amplitude, anim_speed,
                num_eyes=2, eye_size=0.15, eyeball_color=(255, 200, 50), pupil_color=(20, 0, 0),
                num_horns=2, horn_branch_depth=1, horn_branch_count=2, horn_base_size=0.15,
                horn_color=(255, 220, 180),
                num_whiskers_per_side=2, whisker_segments=4, whisker_thickness=0.05,
                whisker_curve_intensity=0.4, whisker_color=None):
        """
        Rebuild dragon with new parameters.

        Args:
            num_segments: Number of segments
            segment_thickness: Base thickness
            taper_factor: Tail tapering amount
            head_scale: Head size multiplier
            body_color: Body RGB (0-255)
            head_color: Head RGB (0-255)
            weave_amplitude: Weaving intensity
            bob_amplitude: Bobbing intensity
            anim_speed: Animation speed
            num_eyes: Number of eyes on head (0-8)
            eye_size: Size of each eye (0.05-0.3)
            eyeball_color: Eyeball RGB (0-255)
            pupil_color: Pupil RGB (0-255)
            num_horns: Number of horns on head (0-4)
            horn_branch_depth: Horn branching levels (0-2)
            horn_branch_count: Branches per horn segment (1-3)
            horn_base_size: Base horn segment size (0.05-0.4)
            horn_color: Horn RGB (0-255)
            num_whiskers_per_side: Whiskers per side of jaw (1-3)
            whisker_segments: Segments per whisker (3-6)
            whisker_thickness: Base whisker thickness (0.03-0.08)
            whisker_curve_intensity: Whisker curve amount (0.2-0.6)
            whisker_color: Whisker RGB (0-255, None=head_color*0.9)
        """
        self.num_segments = num_segments
        self.segment_thickness = segment_thickness
        self.taper_factor = taper_factor
        self.head_scale = head_scale
        self.body_color = (body_color[0] / 255.0, body_color[1] / 255.0, body_color[2] / 255.0)
        self.head_color = (head_color[0] / 255.0, head_color[1] / 255.0, head_color[2] / 255.0)
        self.weave_amplitude = weave_amplitude
        self.bob_amplitude = bob_amplitude
        self.anim_speed = anim_speed
        self.num_eyes = num_eyes
        self.eye_size = eye_size
        self.eyeball_color = (eyeball_color[0] / 255.0, eyeball_color[1] / 255.0, eyeball_color[2] / 255.0)
        self.pupil_color = (pupil_color[0] / 255.0, pupil_color[1] / 255.0, pupil_color[2] / 255.0)
        self.num_horns = num_horns
        self.horn_branch_depth = horn_branch_depth
        self.horn_branch_count = horn_branch_count
        self.horn_base_size = horn_base_size
        self.horn_color = (horn_color[0] / 255.0, horn_color[1] / 255.0, horn_color[2] / 255.0)
        self.num_whiskers_per_side = num_whiskers_per_side
        self.whisker_segments = whisker_segments
        self.whisker_thickness = whisker_thickness
        self.whisker_curve_intensity = whisker_curve_intensity
        # Whisker color: default to slightly darker head color if not specified
        if whisker_color is None:
            self.whisker_color = (self.head_color[0] * 0.9, self.head_color[1] * 0.9, self.head_color[2] * 0.9)
        else:
            self.whisker_color = (whisker_color[0] / 255.0, whisker_color[1] / 255.0, whisker_color[2] / 255.0)

        # Regenerate dragon
        self._generate_dragon()

    def start_attack(self, camera_position):
        """Start attack animation (coil + strike)."""
        self.is_attacking = True
        self.attack_start_time = 0

    def start_attack_2(self, camera_position):
        """Start attack 2 animation (same as attack 1 for dragon)."""
        self.start_attack(camera_position)

    def update_animation(self, time, camera_position=None):
        """
        Update dragon animation with weaving/bobbing motion.

        Args:
            time: Current animation time
            camera_position: Optional camera position for attack targeting
        """
        # Handle attack state
        attack_progress = 0.0
        if self.is_attacking:
            # Initialize attack start time on first frame
            if self.attack_start_time == 0:
                self.attack_start_time = time

            # Calculate attack progress
            from ..core.constants import DRAGON_ATTACK_DURATION
            attack_elapsed = time - self.attack_start_time
            attack_progress = min(attack_elapsed / DRAGON_ATTACK_DURATION, 1.0)

            if attack_progress >= 1.0:
                # Attack complete
                self.is_attacking = False
                self.attack_start_time = 0

        # Animate each segment
        for segment in self.segments:
            i = segment.segment_index

            if self.is_attacking and attack_progress < 1.0:
                # Attack animation: coil inward → strike forward
                if attack_progress < 0.4:
                    # Coil phase (0.0 - 0.4): compress segments together
                    phase_t = attack_progress / 0.4
                    ease_t = phase_t * phase_t  # Ease-in

                    # Pull segments toward head (Z moves toward 0)
                    coil_offset_z = (segment.base_position.z * 0.5) * ease_t
                    # Add spiral motion during coil
                    spiral_x = math.sin(i * 0.5 + time * 3) * 0.3 * ease_t
                    spiral_y = math.cos(i * 0.5 + time * 3) * 0.2 * ease_t

                    segment.entity.position = segment.base_position + Vec3(
                        spiral_x,
                        spiral_y,
                        -coil_offset_z
                    )

                elif attack_progress < 0.7:
                    # Strike phase (0.4 - 0.7): extend forward rapidly
                    phase_t = (attack_progress - 0.4) / 0.3
                    ease_t = 1.0 - (1.0 - phase_t) ** 3  # Ease-out cubic

                    # Extend forward (positive Z direction)
                    strike_offset_z = ease_t * 2.0
                    # Segments follow in wave
                    wave_delay = i * 0.1
                    delayed_t = max(0, ease_t - wave_delay)

                    segment.entity.position = segment.base_position + Vec3(
                        0,
                        0,
                        strike_offset_z * delayed_t
                    )

                else:
                    # Return phase (0.7 - 1.0): snap back to original positions
                    phase_t = (attack_progress - 0.7) / 0.3
                    ease_t = 1.0 - (1.0 - phase_t) ** 2  # Ease-out quad

                    # Interpolate back to base position
                    strike_offset_z = 2.0 * (1.0 - ease_t)
                    segment.entity.position = segment.base_position + Vec3(0, 0, strike_offset_z)

            else:
                # Idle animation: weaving (X) and bobbing (Y) waves
                # Head stays stable, motion increases toward tail

                # Position along body (0 = head, 1 = tail tip)
                body_t = i / max(self.num_segments - 1, 1)

                # Motion multiplier: head barely moves, tail moves fully
                # Using quadratic curve: head (0) = 0.0, mid = 0.5, tail (1) = 1.5
                motion_multiplier = body_t ** 1.8 * 1.5

                # Wave propagates along body (each segment phase-delayed)
                wave_phase = time * self.anim_speed + self.phase_offset + i * 0.3

                # Weaving (left-right motion)
                weave_offset_x = math.sin(wave_phase) * self.weave_amplitude * 0.8
                # Additional secondary wave for organic motion
                weave_offset_x += math.sin(wave_phase * 1.5 + 1.0) * self.weave_amplitude * 0.3

                # Bobbing (up-down motion)
                bob_offset_y = math.cos(wave_phase * 1.2) * self.bob_amplitude * 0.5
                # Secondary bob wave
                bob_offset_y += math.sin(wave_phase * 0.7 - 0.5) * self.bob_amplitude * 0.2

                # Apply motion multiplier (head stays stable, tail whips)
                weave_offset_x *= motion_multiplier
                bob_offset_y *= motion_multiplier

                # Head floating: slow, gentle up-down motion for head and front segments
                # Inverse of motion_multiplier - strong at head, fades toward tail
                head_float_strength = (1.0 - body_t) ** 2  # Strong at head, zero at tail
                head_float_y = math.sin(time * 0.8 + self.phase_offset) * 0.15 * head_float_strength

                # Apply animation offset
                segment.entity.position = segment.base_position + Vec3(
                    weave_offset_x,
                    bob_offset_y + head_float_y,
                    0
                )

            # Update connector tube to follow segment
            segment.update_connector_tube()

        # Update eye positions to follow head movement
        if len(self.segments) > 0 and len(self.eyes) > 0 and len(self.eye_offsets) > 0:
            head_segment = self.segments[0]
            head_position = head_segment.base_position
            head_anim_offset = head_segment.entity.position - head_segment.base_position

            for i, (eye, eye_offset) in enumerate(zip(self.eyes, self.eye_offsets)):
                # Calculate animated eye position using stored offset
                animated_eye_position = head_position + eye_offset + head_anim_offset

                # Update eyeball position
                eye.eyeball.position = animated_eye_position
                eye.eyeball_base_position = animated_eye_position

                # Calculate surface normal from offset vector (points outward from head center)
                surface_normal = eye_offset.normalized()
                pupil_offset = surface_normal * (eye.base_size * 0.5)
                eye.pupil.position = animated_eye_position + pupil_offset
                eye.pupil_base_position = animated_eye_position + pupil_offset

                # Update eye animation (blinking)
                eye.update_animation(time)

        # Update horn positions to follow head movement
        if len(self.segments) > 0 and len(self.horns) > 0:
            head_segment = self.segments[0]
            head_anim_offset = head_segment.entity.position - head_segment.base_position

            # Sway intensity based on animation speed
            sway_amount = self.anim_speed if not self.is_attacking else 0.0

            for horn_segment in self.horns:
                horn_segment.update_animation(time, head_anim_offset, sway_amount)

        # Update whisker positions to follow head movement with sway
        if len(self.segments) > 0 and len(self.whiskers) > 0:
            head_segment = self.segments[0]
            head_anim_offset = head_segment.entity.position - head_segment.base_position

            # Sway intensity (whiskers sway independently from body motion)
            whisker_sway = 1.0 if not self.is_attacking else 0.3

            for whisker in self.whiskers:
                whisker.update_animation(time, head_anim_offset, whisker_sway)

    def destroy(self):
        """Cleanup all entities."""
        for segment in self.segments:
            segment.destroy()
        for eye in self.eyes:
            eye.destroy()
        for horn_segment in self.horns:
            horn_segment.destroy()
        for whisker in self.whiskers:
            whisker.destroy()
        destroy(self.root)
