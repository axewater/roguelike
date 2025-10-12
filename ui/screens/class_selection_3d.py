"""
3D Class Selection Screen

Displays 4 class models in a circular formation with stats and ability descriptions.
Player can rotate between classes and select one to start the game.
"""

from ursina import Entity, camera, color, Text, Button, Vec3, held_keys, mouse, time as ursina_time
import math
import constants as c
from audio import get_audio_manager


class ClassSelection3D(Entity):
    """
    3D class selection screen with rotating character models.

    Layout:
    - Center: Rotating 3D class model (large)
    - Left/Right arrows: Navigate between classes
    - Top: Class name and description
    - Bottom: Stats bars (HP, Attack, Defense)
    - Bottom-right: "Start Game" button
    """

    def __init__(self, screen_manager):
        super().__init__()
        self.screen_manager = screen_manager
        self.audio = get_audio_manager()

        # Class data
        self.classes = [c.CLASS_WARRIOR, c.CLASS_MAGE, c.CLASS_ROGUE, c.CLASS_RANGER]
        self.current_class_index = 0
        self.current_class = self.classes[self.current_class_index]

        # Class models (lazy loaded)
        self.class_models = {}

        # UI elements
        self.ui_elements = []
        self.class_name_text = None
        self.class_desc_text = None
        self.stat_texts = {}
        self.ability_texts = []
        self.start_button = None
        self.left_arrow = None
        self.right_arrow = None

        # Animation
        self.model_rotation = 0.0
        self.model_rotation_speed = 30.0  # Degrees per second
        self.transition_progress = 0.0
        self.transitioning = False

        # Camera position
        self.camera_distance = 5.0
        self.camera_height = 1.5

        # Initialize
        self._create_ui()
        self._load_current_model()
        self._update_ui_for_class()

        # Initially hidden
        self.enabled = False

        print(f"✓ ClassSelection3D initialized")

    def _create_ui(self):
        """Create UI overlay elements"""
        # Title
        title = Text(
            text="SELECT YOUR CLASS",
            position=(0, 0.45),
            origin=(0, 0),
            scale=2.5,
            color=color.rgb(220, 220, 220),
            parent=camera.ui
        )
        self.ui_elements.append(title)

        # Class name (large, centered)
        self.class_name_text = Text(
            text="WARRIOR",
            position=(0, 0.35),
            origin=(0, 0),
            scale=3.0,
            color=color.rgb(180, 60, 40),
            parent=camera.ui
        )
        self.ui_elements.append(self.class_name_text)

        # Class description
        self.class_desc_text = Text(
            text="High HP tank with strong defense",
            position=(0, 0.28),
            origin=(0, 0),
            scale=1.2,
            color=color.rgb(180, 180, 200),
            parent=camera.ui
        )
        self.ui_elements.append(self.class_desc_text)

        # Stat display (bottom-left)
        stat_y_start = -0.25
        stat_spacing = 0.08

        # HP
        hp_label = Text(
            text="HP:",
            position=(-0.45, stat_y_start),
            origin=(0, 0),
            scale=1.5,
            color=color.rgb(220, 220, 220),
            parent=camera.ui
        )
        self.ui_elements.append(hp_label)
        self.stat_texts['hp'] = Text(
            text="120",
            position=(-0.35, stat_y_start),
            origin=(0, 0),
            scale=1.8,
            color=color.rgb(100, 200, 120),
            parent=camera.ui
        )
        self.ui_elements.append(self.stat_texts['hp'])

        # Attack
        attack_label = Text(
            text="ATK:",
            position=(-0.45, stat_y_start - stat_spacing),
            origin=(0, 0),
            scale=1.5,
            color=color.rgb(220, 220, 220),
            parent=camera.ui
        )
        self.ui_elements.append(attack_label)
        self.stat_texts['attack'] = Text(
            text="12",
            position=(-0.35, stat_y_start - stat_spacing),
            origin=(0, 0),
            scale=1.8,
            color=color.rgb(255, 100, 100),
            parent=camera.ui
        )
        self.ui_elements.append(self.stat_texts['attack'])

        # Defense
        defense_label = Text(
            text="DEF:",
            position=(-0.45, stat_y_start - stat_spacing * 2),
            origin=(0, 0),
            scale=1.5,
            color=color.rgb(220, 220, 220),
            parent=camera.ui
        )
        self.ui_elements.append(defense_label)
        self.stat_texts['defense'] = Text(
            text="8",
            position=(-0.35, stat_y_start - stat_spacing * 2),
            origin=(0, 0),
            scale=1.8,
            color=color.rgb(100, 150, 255),
            parent=camera.ui
        )
        self.ui_elements.append(self.stat_texts['defense'])

        # Abilities (bottom-right)
        abilities_label = Text(
            text="ABILITIES:",
            position=(0.25, stat_y_start),
            origin=(0, 0),
            scale=1.5,
            color=color.rgb(220, 220, 220),
            parent=camera.ui
        )
        self.ui_elements.append(abilities_label)

        # Create 3 ability text slots
        for i in range(3):
            ability_text = Text(
                text=f"Ability {i+1}",
                position=(0.25, stat_y_start - stat_spacing * (i + 1)),
                origin=(0, 0),
                scale=1.3,
                color=color.rgb(150, 180, 255),
                parent=camera.ui
            )
            self.ability_texts.append(ability_text)
            self.ui_elements.append(ability_text)

        # Navigation arrows (use text labels to avoid Ursina text rendering bug)
        self.left_arrow = Button(
            text="PREV",
            scale=(0.12, 0.06),
            position=(-0.6, 0),
            color=color.rgb(80, 80, 90),
            parent=camera.ui,
            on_click=self._previous_class
        )
        self.ui_elements.append(self.left_arrow)

        self.right_arrow = Button(
            text="NEXT",
            scale=(0.12, 0.06),
            position=(0.6, 0),
            color=color.rgb(80, 80, 90),
            parent=camera.ui,
            on_click=self._next_class
        )
        self.ui_elements.append(self.right_arrow)

        # Start button
        self.start_button = Button(
            text="START GAME",
            scale=(0.2, 0.08),
            position=(0, -0.42),
            color=color.rgb(60, 120, 60),
            parent=camera.ui,
            on_click=self._start_game
        )
        self.ui_elements.append(self.start_button)

        # Instructions
        instructions = Text(
            text="Arrow Keys: Navigate  |  Enter/Click: Start Game",
            position=(0, -0.48),
            origin=(0, 0),
            scale=1.0,
            color=color.rgb(120, 120, 130),
            parent=camera.ui
        )
        self.ui_elements.append(instructions)

    def _load_current_model(self):
        """Load and display the current class model"""
        # Clear previous model
        for class_type, model in self.class_models.items():
            if model:
                model.enabled = False

        # Load model if not cached
        if self.current_class not in self.class_models:
            self._create_class_model(self.current_class)

        # Show current model
        if self.current_class in self.class_models:
            self.class_models[self.current_class].enabled = True

    def _create_class_model(self, class_type: str):
        """Create a 3D model for the class"""
        # Import the appropriate player model
        if class_type == c.CLASS_WARRIOR:
            from graphics3d.players.warrior import create_warrior_model
            model_func = create_warrior_model
            model_color = color.rgb(180, 60, 40)
        elif class_type == c.CLASS_MAGE:
            from graphics3d.players.mage import create_mage_model
            model_func = create_mage_model
            model_color = color.rgb(100, 150, 255)
        elif class_type == c.CLASS_ROGUE:
            from graphics3d.players.rogue import create_rogue_model
            model_func = create_rogue_model
            model_color = color.rgb(180, 100, 255)
        elif class_type == c.CLASS_RANGER:
            from graphics3d.players.ranger import create_ranger_model
            model_func = create_ranger_model
            model_color = color.rgb(100, 200, 100)
        else:
            print(f"[ClassSelection] Unknown class type: {class_type}")
            return

        # Create model entity
        model = model_func(position=Vec3(0, 0, 0), scale=Vec3(2, 2, 2))
        model.color = model_color
        model.rotation_y = 0

        # Position in front of camera
        model.position = Vec3(0, 0, -self.camera_distance)
        model.y = self.camera_height - 1.5  # Adjust height

        self.class_models[class_type] = model

        print(f"✓ Created model for {class_type}")

    def _update_ui_for_class(self):
        """Update UI text and colors for current class"""
        # Get class data
        stats = c.CLASS_STATS.get(self.current_class, {})
        class_colors = {
            c.CLASS_WARRIOR: color.rgb(180, 60, 40),
            c.CLASS_MAGE: color.rgb(100, 150, 255),
            c.CLASS_ROGUE: color.rgb(180, 100, 255),
            c.CLASS_RANGER: color.rgb(100, 200, 100),
        }
        class_names = {
            c.CLASS_WARRIOR: "WARRIOR",
            c.CLASS_MAGE: "MAGE",
            c.CLASS_ROGUE: "ROGUE",
            c.CLASS_RANGER: "RANGER",
        }
        class_abilities = {
            c.CLASS_WARRIOR: ["Healing Touch", "Whirlwind", "Dash"],
            c.CLASS_MAGE: ["Fireball", "Frost Nova", "Healing Touch"],
            c.CLASS_ROGUE: ["Shadow Step", "Dash", "Healing Touch"],
            c.CLASS_RANGER: ["Fireball", "Dash", "Healing Touch"],
        }

        # Update class name
        self.class_name_text.text = class_names.get(self.current_class, "UNKNOWN")
        self.class_name_text.color = class_colors.get(self.current_class, color.white)

        # Update description
        self.class_desc_text.text = stats.get("description", "")

        # Update stats
        self.stat_texts['hp'].text = str(stats.get('hp', 0))
        self.stat_texts['attack'].text = str(stats.get('attack', 0))
        self.stat_texts['defense'].text = str(stats.get('defense', 0))

        # Update abilities
        abilities = class_abilities.get(self.current_class, [])
        for i, ability_text in enumerate(self.ability_texts):
            if i < len(abilities):
                ability_text.text = f"{i+1}. {abilities[i]}"
            else:
                ability_text.text = ""

    def _next_class(self):
        """Navigate to next class"""
        self.audio.play_ui_hover()
        self.current_class_index = (self.current_class_index + 1) % len(self.classes)
        self.current_class = self.classes[self.current_class_index]
        self._load_current_model()
        self._update_ui_for_class()
        print(f"[ClassSelection] Selected: {self.current_class}")

    def _previous_class(self):
        """Navigate to previous class"""
        self.audio.play_ui_hover()
        self.current_class_index = (self.current_class_index - 1) % len(self.classes)
        self.current_class = self.classes[self.current_class_index]
        self._load_current_model()
        self._update_ui_for_class()
        print(f"[ClassSelection] Selected: {self.current_class}")

    def _start_game(self):
        """Start game with selected class"""
        self.audio.play_ui_select()

        # Play class name voice
        class_names = {
            c.CLASS_WARRIOR: "Warrior",
            c.CLASS_MAGE: "Mage",
            c.CLASS_ROGUE: "Rogue",
            c.CLASS_RANGER: "Ranger",
        }
        class_name = class_names.get(self.current_class, "")
        if class_name:
            self.audio.play_voice_class(class_name)

        print(f"[ClassSelection] Starting game with {self.current_class}")

        # Notify screen manager
        self.screen_manager.start_game_with_class(self.current_class)

    def update(self):
        """Update animations and input"""
        if not self.enabled:
            return

        dt = ursina_time.dt

        # Rotate model
        if self.current_class in self.class_models:
            model = self.class_models[self.current_class]
            if model and model.enabled:
                model.rotation_y += self.model_rotation_speed * dt

        # Handle keyboard input
        if held_keys['left arrow'] or held_keys['a']:
            # Debounce by checking if we just changed
            if not hasattr(self, '_last_nav_time') or (ursina_time.time() - self._last_nav_time) > 0.3:
                self._previous_class()
                self._last_nav_time = ursina_time.time()

        if held_keys['right arrow'] or held_keys['d']:
            if not hasattr(self, '_last_nav_time') or (ursina_time.time() - self._last_nav_time) > 0.3:
                self._next_class()
                self._last_nav_time = ursina_time.time()

        if held_keys['enter'] or held_keys['space']:
            if not hasattr(self, '_last_start_time') or (ursina_time.time() - self._last_start_time) > 0.5:
                self._start_game()
                self._last_start_time = ursina_time.time()

    def show(self):
        """Show the class selection screen"""
        self.enabled = True

        # Show all UI elements
        for element in self.ui_elements:
            element.enabled = True

        # Show current model
        self._load_current_model()

        # Position camera
        camera.position = Vec3(0, self.camera_height, 0)
        camera.rotation = Vec3(0, 0, 0)

        print("[ClassSelection] Screen shown")

    def hide(self):
        """Hide the class selection screen"""
        self.enabled = False

        # Hide all UI elements
        for element in self.ui_elements:
            element.enabled = False

        # Hide all models
        for model in self.class_models.values():
            if model:
                model.enabled = False

        print("[ClassSelection] Screen hidden")
