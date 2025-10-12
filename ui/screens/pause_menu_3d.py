"""
3D Pause Menu Overlay

Semi-transparent overlay that appears when ESC is pressed during gameplay.
"""

from ursina import Entity, camera, color, Text, Button, held_keys
from audio import get_audio_manager


class PauseMenu3D(Entity):
    """
    Pause menu overlay (does not replace current screen).

    Shows:
    - Semi-transparent dark overlay
    - "PAUSED" title
    - Options: Resume, Restart, Settings, Main Menu, Quit
    """

    def __init__(self, screen_manager):
        super().__init__()
        self.screen_manager = screen_manager
        self.audio = get_audio_manager()

        # UI elements
        self.ui_elements = []

        # Track ESC key state to prevent rapid toggling
        self.esc_pressed = False

        # Initialize
        self._create_ui()

        # Initially hidden
        self.enabled = False

        print("✓ PauseMenu3D initialized")

    def _create_ui(self):
        """Create UI overlay elements"""
        # Semi-transparent dark overlay - RGBA tuple
        self.overlay_bg = Entity(
            model='quad',
            color=(0, 0, 0, 180/255),  # Normalized RGBA (0-1 range)
            scale=(100, 100),
            position=(0, 0, -0.5),
            parent=camera.ui
        )
        self.ui_elements.append(self.overlay_bg)

        # Title "PAUSED"
        title = Text(
            text="PAUSED",
            position=(0, 0.35),
            origin=(0, 0),
            scale=4.0,
            color=color.rgb(220, 220, 230),
            parent=camera.ui
        )
        self.ui_elements.append(title)

        # Hint text
        hint = Text(
            text="Press ESC to Resume",
            position=(0, 0.23),
            origin=(0, 0),
            scale=1.3,
            color=color.rgb(150, 150, 170),
            parent=camera.ui
        )
        self.ui_elements.append(hint)

        # Buttons
        button_y = 0.08
        button_spacing = 0.11

        self.resume_button = Button(
            text="RESUME",
            scale=(0.28, 0.08),
            position=(0, button_y),
            color=color.rgb(60, 120, 60),
            parent=camera.ui,
            on_click=self._resume
        )
        self.ui_elements.append(self.resume_button)

        self.restart_button = Button(
            text="RESTART",
            scale=(0.28, 0.08),
            position=(0, button_y - button_spacing),
            color=color.rgb(100, 100, 120),
            parent=camera.ui,
            on_click=self._restart
        )
        self.ui_elements.append(self.restart_button)

        self.settings_button = Button(
            text="SETTINGS",
            scale=(0.28, 0.08),
            position=(0, button_y - button_spacing * 2),
            color=color.rgb(80, 80, 100),
            parent=camera.ui,
            on_click=self._settings
        )
        self.ui_elements.append(self.settings_button)

        self.main_menu_button = Button(
            text="MAIN MENU",
            scale=(0.28, 0.08),
            position=(0, button_y - button_spacing * 3),
            color=color.rgb(120, 100, 60),
            parent=camera.ui,
            on_click=self._main_menu
        )
        self.ui_elements.append(self.main_menu_button)

        self.quit_button = Button(
            text="QUIT",
            scale=(0.28, 0.08),
            position=(0, button_y - button_spacing * 4),
            color=color.rgb(120, 60, 60),
            parent=camera.ui,
            on_click=self._quit
        )
        self.ui_elements.append(self.quit_button)

    def _resume(self):
        """Resume game"""
        self.audio.play_ui_select()
        print("[PauseMenu] Resume clicked")
        self.screen_manager.resume_from_pause()

    def _restart(self):
        """Restart game (return to class selection)"""
        self.audio.play_ui_select()
        print("[PauseMenu] Restart clicked")
        # First resume from pause, then change to class selection
        self.screen_manager.resume_from_pause()
        from ui.screens.screen_manager_3d import ScreenState
        self.screen_manager.change_screen(ScreenState.CLASS_SELECTION)

    def _settings(self):
        """Open settings (placeholder for Phase 8)"""
        self.audio.play_ui_select()
        print("[PauseMenu] Settings clicked (not implemented yet)")
        # TODO: Implement settings screen in Phase 8

    def _main_menu(self):
        """Return to main menu"""
        self.audio.play_ui_select()
        print("[PauseMenu] Main Menu clicked")
        # First resume from pause, then change to main menu
        self.screen_manager.resume_from_pause()
        from ui.screens.screen_manager_3d import ScreenState
        self.screen_manager.change_screen(ScreenState.MAIN_MENU)

    def _quit(self):
        """Quit the game"""
        self.audio.play_ui_select()
        print("[PauseMenu] Quit clicked")
        self.screen_manager.quit_game()

    def update(self):
        """Handle input for resuming"""
        if not self.enabled:
            return

        # ESC key resumes game
        if held_keys['escape']:
            if not self.esc_pressed:
                self.esc_pressed = True
                self._resume()
        else:
            self.esc_pressed = False

    def show(self):
        """Show the pause menu"""
        self.enabled = True

        # Show all UI elements
        for element in self.ui_elements:
            element.enabled = True

        # Play pause sound
        self.audio.play_ui_select()

        print("[PauseMenu] Pause menu shown")

    def hide(self):
        """Hide the pause menu"""
        self.enabled = False

        # Hide all UI elements
        for element in self.ui_elements:
            element.enabled = False

        print("[PauseMenu] Pause menu hidden")
