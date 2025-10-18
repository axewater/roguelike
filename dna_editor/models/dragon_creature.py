"""
DragonCreature model - Space Harrier inspired segmented flying serpent.
Chain of spheres forming a snake-like body with smooth weaving/bobbing animation.
"""

from ursina import Entity, Vec3, color, destroy
import math
import random


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


class DragonCreature:
    """Space Harrier inspired dragon - segmented serpent with weaving/bobbing motion."""

    def __init__(self, num_segments=15, segment_thickness=0.3, taper_factor=0.6,
                 head_scale=2.0, body_color=(200, 40, 40), head_color=(255, 200, 50),
                 weave_amplitude=0.5, bob_amplitude=0.3, anim_speed=1.5):
        """
        Create a dragon creature.

        Args:
            num_segments: Number of body segments (5-30)
            segment_thickness: Base segment size (0.1-0.8)
            taper_factor: Size reduction toward tail (0.0-0.9, higher = more taper)
            head_scale: Head size multiplier (1.0-2.5)
            body_color: RGB tuple for body (0-255 range - Ursina compat)
            head_color: RGB tuple for head (0-255 range)
            weave_amplitude: Side-to-side motion intensity (0.0-1.0)
            bob_amplitude: Up-down motion intensity (0.0-1.0)
            anim_speed: Animation speed multiplier (0.5-5.0)
        """
        # Create root entity
        self.root = Entity(position=(0, 0, 0))
        self.segments = []

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

        # Dragon layout: horizontal chain extending backward
        # Segments arranged along -Z axis (head at origin, tail extends back)
        segment_spacing = self.segment_thickness * 1.8  # Spacing between segment centers

        # Elevation (floating/hovering effect)
        base_elevation = 1.0

        previous_segment = None

        for i in range(self.num_segments):
            # Calculate position along chain
            # Head (i=0) at front, tail (i=max) at back
            z_offset = -i * segment_spacing
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

    def rebuild(self, num_segments, segment_thickness, taper_factor, head_scale,
                body_color, head_color, weave_amplitude, bob_amplitude, anim_speed):
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

                # Tail segments move more (whip-like motion)
                tail_factor = (i / max(self.num_segments - 1, 1)) ** 1.5
                weave_offset_x *= (1.0 + tail_factor * 0.5)
                bob_offset_y *= (1.0 + tail_factor * 0.3)

                # Apply animation offset
                segment.entity.position = segment.base_position + Vec3(
                    weave_offset_x,
                    bob_offset_y,
                    0
                )

            # Update connector tube to follow segment
            segment.update_connector_tube()

    def destroy(self):
        """Cleanup all entities."""
        for segment in self.segments:
            segment.destroy()
        destroy(self.root)
