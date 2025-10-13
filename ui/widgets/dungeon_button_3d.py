"""
Dungeon-Styled Button Widget for Ursina 3D

Custom button with stone/dungeon aesthetic - simplified version.
"""

from ursina import Entity, color, Text, mouse, time as ursina_time, destroy, Vec3


class DungeonButton(Entity):
    """
    Custom dungeon-styled button widget.

    Simplified approach: All elements created as camera.ui children
    with absolute positions to avoid z-ordering issues.
    """

    def __init__(self, text="", position=(0, 0), scale=(0.3, 0.08),
                 on_click=None, parent=None, **kwargs):
        # Don't call super().__init__ yet - we'll set this up manually
        Entity.__init__(self, parent=parent, eternal=True)

        self.text_string = text
        self.on_click_callback = on_click
        self.base_scale = scale
        self.base_position = position
        self.ui_parent = parent  # Should be camera.ui

        # State tracking
        self.hovered = False
        self.pressed = False

        # Animation state
        self.hover_progress = 0.0  # 0 to 1
        self.press_offset = 0.0

        # Colors (dungeon theme) - use normalized 0-1 values
        self.color_bg = color.rgb(0.196, 0.188, 0.176)  # Dark stone (50, 48, 45)
        self.color_border = color.rgb(0.255, 0.235, 0.216)  # Brown border (65, 60, 55)
        self.color_border_hover = color.rgb(0.471, 0.392, 0.706)  # Purple glow (120, 100, 180)
        self.color_text = color.rgb(0.863, 0.863, 0.902)  # Light text (220, 220, 230)

        # Create button elements
        self._create_button_elements()

        # Position this container (but it's invisible - just for management)
        self.position = Vec3(position[0], position[1], 0)
        self.enabled = True

        # Debug
        print(f"[DungeonButton] Created '{text}' - bg color: {self.color_bg}, text color: {self.color_text}")

    def _create_button_elements(self):
        """Create button visual elements as direct UI children"""
        pos_x = self.base_position[0]
        pos_y = self.base_position[1]

        # Border (behind button)
        border_width = self.base_scale[0] + 0.016
        border_height = self.base_scale[1] + 0.016

        self.border = Entity(
            parent=self.ui_parent,
            model='quad',
            scale=(border_width, border_height),
            position=(pos_x, pos_y, 0.02),
            eternal=True
        )
        # Set color AFTER creation
        self.border.color = self.color_border
        print(f"  Border created at ({pos_x}, {pos_y}, 0.02) - color: {self.border.color}")

        # Button background
        self.button_bg = Entity(
            parent=self.ui_parent,
            model='quad',
            scale=self.base_scale,
            position=(pos_x, pos_y, 0.01),
            eternal=True
        )
        # Set color AFTER creation
        self.button_bg.color = self.color_bg
        print(f"  Button BG created at ({pos_x}, {pos_y}, 0.01) - color: {self.button_bg.color}")

        # Button text (on top)
        self.text_entity = Text(
            text=self.text_string,
            parent=self.ui_parent,
            origin=(0, 0),
            scale=1.8,
            position=(pos_x, pos_y, 0),
            eternal=True
        )
        # Set color AFTER creation
        self.text_entity.color = self.color_text
        print(f"  Text created at ({pos_x}, {pos_y}, 0) - text: '{self.text_string}', color: {self.text_entity.color}")

    def input(self, key):
        """Handle input events"""
        if not self.enabled:
            return

        if key == 'left mouse down':
            if self.hovered:
                self.pressed = True
                self.press_offset = -0.01

        elif key == 'left mouse up':
            if self.pressed and self.hovered:
                # Button clicked!
                if self.on_click_callback:
                    self.on_click_callback()
            self.pressed = False
            self.press_offset = 0.0

    def update(self):
        """Update hover state and animations"""
        if not self.enabled:
            return

        # Check if mouse is over button background
        if self.button_bg.hovered and mouse.visible:
            if not self.hovered:
                self.hovered = True
                self._on_hover_enter()
        else:
            if self.hovered:
                self.hovered = False
                self._on_hover_exit()

        # Animate hover effect
        dt = ursina_time.dt
        target_hover = 1.0 if self.hovered else 0.0
        self.hover_progress += (target_hover - self.hover_progress) * 8 * dt

        # Apply hover effects
        self._update_hover_visuals()

    def _on_hover_enter(self):
        """Called when mouse enters button"""
        # Play hover sound
        try:
            from audio import get_audio_manager
            audio = get_audio_manager()
            audio.play_ui_hover()
        except:
            pass

    def _on_hover_exit(self):
        """Called when mouse leaves button"""
        pass

    def _update_hover_visuals(self):
        """Update visual appearance based on hover state"""
        # Interpolate border color (brown -> purple)
        t = self.hover_progress
        border_r = self.color_border.r + (self.color_border_hover.r - self.color_border.r) * t
        border_g = self.color_border.g + (self.color_border_hover.g - self.color_border.g) * t
        border_b = self.color_border.b + (self.color_border_hover.b - self.color_border.b) * t

        # Apply color (values already in 0-1 range)
        self.border.color = color.rgb(border_r, border_g, border_b)

        # Slight scale up on hover
        scale_mult = 1.0 + (0.05 * self.hover_progress)
        border_w = (self.base_scale[0] + 0.016) * scale_mult
        border_h = (self.base_scale[1] + 0.016) * scale_mult
        self.border.scale = (border_w, border_h)

        btn_w = self.base_scale[0] * scale_mult
        btn_h = self.base_scale[1] * scale_mult
        self.button_bg.scale = (btn_w, btn_h)

        # Press-down offset
        pos_x = self.base_position[0]
        pos_y = self.base_position[1]
        self.button_bg.position = (pos_x, pos_y, 0.01 + self.press_offset)
        self.text_entity.position = (pos_x, pos_y, 0.0 + self.press_offset)

    def destroy_button(self):
        """Clean up button entities"""
        if self.text_entity:
            destroy(self.text_entity)
        if self.button_bg:
            destroy(self.button_bg)
        if self.border:
            destroy(self.border)
        destroy(self)


def create_dungeon_button(text, position, scale=(0.32, 0.08), on_click=None, parent=None):
    """
    Helper function to create a dungeon-styled button.

    Args:
        text: Button text
        position: (x, y) position in UI space
        scale: (width, height) button size
        on_click: Callback function when clicked
        parent: Parent entity (usually camera.ui)

    Returns:
        DungeonButton instance
    """
    return DungeonButton(
        text=text,
        position=position,
        scale=scale,
        on_click=on_click,
        parent=parent
    )
