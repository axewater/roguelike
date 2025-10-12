"""
3D Settings Screen

Settings screen with volume controls for music and sound effects.
Uses Ursina UI elements.
"""

from ursina import Entity, camera, color, Text, Button, Slider, time as ursina_time
import constants as c
from audio import get_audio_manager


class Settings3D(Entity):
    """
    Settings screen with volume controls.

    Features:
    - Music volume slider
    - SFX volume slider
    - Back button (returns to previous screen)
    """

    def __init__(self, screen_manager):
        super().__init__()
        self.screen_manager = screen_manager
        self.audio = get_audio_manager()

        # UI elements
        self.ui_elements = []

        # Slider references
        self.music_slider = None
        self.sfx_slider = None
        self.music_value_text = None
        self.sfx_value_text = None

        # Track previous screen for navigation
        self.previous_screen = None

        # Initialize
        self._create_ui()

        # Initially hidden
        self.enabled = False

        print("✓ Settings3D initialized")

    def _create_ui(self):
        """Create UI overlay elements"""
        # Background overlay (semi-transparent dark)
        bg = Entity(
            model='quad',
            color=(0.05, 0.05, 0.15, 0.95),
            scale=(100, 100),
            position=(0, 0, -0.9),
            parent=camera.ui
        )
        self.ui_elements.append(bg)

        # Title
        title = Text(
            text="SETTINGS",
            position=(0, 0.42),
            origin=(0, 0),
            scale=3.5,
            color=color.rgb(220, 220, 230),
            parent=camera.ui
        )
        self.ui_elements.append(title)

        # Settings panel background
        panel_bg = Entity(
            model='quad',
            color=color.rgb(45, 45, 50),
            scale=(1.2, 0.9),
            position=(0, 0.02, -0.8),
            parent=camera.ui
        )
        self.ui_elements.append(panel_bg)

        # Music Volume Section
        music_label = Text(
            text="Music Volume",
            position=(-0.48, 0.22),
            origin=(0, 0),
            scale=1.8,
            color=color.rgb(220, 220, 230),
            parent=camera.ui
        )
        self.ui_elements.append(music_label)

        # Music slider
        self.music_slider = Slider(
            min=0, max=100,
            default=int(self.audio.music_volume * 100),
            step=1,
            height=0.04,
            width=0.7,
            position=(-0.48, 0.12),
            parent=camera.ui,
            on_value_changed=self._on_music_volume_changed
        )
        self.music_slider.knob.color = color.rgb(150, 100, 255)
        self.music_slider.bg.color = color.rgb(60, 60, 70)
        self.ui_elements.append(self.music_slider)

        # Music value display
        self.music_value_text = Text(
            text=f"{int(self.audio.music_volume * 100)}%",
            position=(0.35, 0.12),
            origin=(0, 0),
            scale=1.5,
            color=color.rgb(200, 200, 200),
            parent=camera.ui
        )
        self.ui_elements.append(self.music_value_text)

        # SFX Volume Section
        sfx_label = Text(
            text="Sound Effects Volume",
            position=(-0.48, -0.05),
            origin=(0, 0),
            scale=1.8,
            color=color.rgb(220, 220, 230),
            parent=camera.ui
        )
        self.ui_elements.append(sfx_label)

        # SFX slider
        self.sfx_slider = Slider(
            min=0, max=100,
            default=int(self.audio.sfx_volume * 100),
            step=1,
            height=0.04,
            width=0.7,
            position=(-0.48, -0.15),
            parent=camera.ui,
            on_value_changed=self._on_sfx_volume_changed
        )
        self.sfx_slider.knob.color = color.rgb(100, 200, 255)
        self.sfx_slider.bg.color = color.rgb(60, 60, 70)
        self.ui_elements.append(self.sfx_slider)

        # SFX value display
        self.sfx_value_text = Text(
            text=f"{int(self.audio.sfx_volume * 100)}%",
            position=(0.35, -0.15),
            origin=(0, 0),
            scale=1.5,
            color=color.rgb(200, 200, 200),
            parent=camera.ui
        )
        self.ui_elements.append(self.sfx_value_text)

        # Back button
        self.back_button = Button(
            text="BACK",
            scale=(0.28, 0.08),
            position=(0, -0.38),
            color=color.rgb(80, 80, 100),
            highlight_color=color.rgb(100, 100, 130),
            parent=camera.ui,
            on_click=self._on_back
        )
        self.ui_elements.append(self.back_button)

    def _on_music_volume_changed(self):
        """Handle music volume slider change"""
        value = int(self.music_slider.value)
        volume = value / 100.0
        self.audio.set_music_volume(volume)
        self.music_value_text.text = f"{value}%"
        print(f"[Settings] Music volume: {value}%")

    def _on_sfx_volume_changed(self):
        """Handle SFX volume slider change"""
        value = int(self.sfx_slider.value)
        volume = value / 100.0
        self.audio.set_sfx_volume(volume)
        self.sfx_value_text.text = f"{value}%"

        # Play a test sound (if volume > 0)
        if value > 0:
            self.audio.play_ui_select()

        print(f"[Settings] SFX volume: {value}%")

    def _on_back(self):
        """Handle back button click"""
        self.audio.play_ui_select()
        print("[Settings] Back clicked")

        # Return to previous screen
        if self.previous_screen:
            self.screen_manager.change_screen(self.previous_screen)
        else:
            # Default: return to main menu
            from ui.screens.screen_manager_3d import ScreenState
            self.screen_manager.change_screen(ScreenState.MAIN_MENU)

    def set_previous_screen(self, screen_state):
        """Set the screen to return to when Back is clicked"""
        self.previous_screen = screen_state

    def update(self):
        """Update (currently no animations)"""
        if not self.enabled:
            return
        # No active animations for settings screen
        pass

    def show(self):
        """Show the settings screen"""
        self.enabled = True

        # Show all UI elements
        for element in self.ui_elements:
            element.enabled = True

        # Update slider values to current audio settings
        self.music_slider.value = int(self.audio.music_volume * 100)
        self.sfx_slider.value = int(self.audio.sfx_volume * 100)
        self.music_value_text.text = f"{int(self.audio.music_volume * 100)}%"
        self.sfx_value_text.text = f"{int(self.audio.sfx_volume * 100)}%"

        print("[Settings] Settings screen shown")

    def hide(self):
        """Hide the settings screen"""
        self.enabled = False

        # Hide all UI elements
        for element in self.ui_elements:
            element.enabled = False

        print("[Settings] Settings screen hidden")
