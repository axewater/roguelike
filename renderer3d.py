"""
3D Rendering Manager using Ursina Engine

This module handles all 3D rendering for the game, converting the 2D game state
into a 3D visualization while keeping all game logic unchanged.
"""

from typing import Dict, List, Optional
from ursina import Entity, camera, Vec3, color as ursina_color, DirectionalLight, AmbientLight, PointLight
import constants as c
from game import Game
from graphics3d.tiles import create_floor_mesh, create_wall_mesh, create_stairs_mesh
from graphics3d.utils import world_to_3d_position, qcolor_to_ursina_color
from graphics3d.enemies import create_enemy_model_3d, update_enemy_animation, create_health_bar_billboard, update_health_bar
from graphics3d.items import create_item_model_3d, update_item_animation
from animations3d import AnimationManager3D


class Renderer3D:
    """
    3D rendering manager using Ursina Engine
    Interfaces with the Game class to render dungeon, entities, and effects
    """

    def __init__(self, game: Game):
        """
        Initialize the 3D renderer

        Args:
            game: Game instance to render
        """
        self.game = game

        # Entity tracking dictionaries
        self.dungeon_entities: List[Entity] = []
        self.player_entity: Optional[Entity] = None
        self.enemy_entities: Dict[int, Entity] = {}  # enemy id -> Entity
        self.item_entities: Dict[int, Entity] = {}   # item id -> Entity

        # Lighting
        self.ambient_light: Optional[AmbientLight] = None
        self.sun_light: Optional[DirectionalLight] = None
        self.player_light: Optional[PointLight] = None

        # Camera smoothing
        self.camera_target_pos = Vec3(0, c.CAMERA_HEIGHT, -c.CAMERA_DISTANCE)
        self.camera_smooth_factor = 0.3  # Increased from 0.1 for faster camera movement
        self.camera_initialized = False  # Track if camera has been positioned initially
        self.base_camera_pos = Vec3(0, 0, 0)  # Store base camera position for shake

        # 3D Animation Manager
        self.animation_manager = AnimationManager3D()

        # Setup
        self.setup_camera()
        self.setup_lighting()

    def setup_camera(self):
        """Configure third-person follow camera"""
        camera.position = (0, c.CAMERA_HEIGHT, -c.CAMERA_DISTANCE)
        camera.rotation_x = c.CAMERA_ANGLE
        camera.fov = c.FOV
        print(f"✓ Camera configured: pos={camera.position}, angle={c.CAMERA_ANGLE}°, fov={c.FOV}°")

    def setup_lighting(self):
        """Set up basic 3D lighting"""
        # Ambient light (general illumination) - BRIGHTENED FOR DEBUG
        self.ambient_light = AmbientLight(color=(0.8, 0.8, 0.8, 1))

        # Directional light (sun/moon)
        self.sun_light = DirectionalLight(
            position=(10, 20, 10),
            rotation=(45, 45, 0),
            color=(1.0, 1.0, 1.0, 1)  # Bright white for debug
        )

        # Point light following player (torch effect)
        self.player_light = PointLight(
            color=(1, 0.9, 0.7, 1),
            position=(0, 2, 0)
        )
        print("✓ Lighting configured (DEBUG MODE: very bright ambient)")

    def render_dungeon(self):
        """
        Render the entire dungeon from game.dungeon

        Clears old dungeon meshes and creates new ones based on current level.
        """
        # Clear old dungeon entities
        for entity in self.dungeon_entities:
            entity.disable()  # Disable instead of destroy for better performance
        self.dungeon_entities.clear()

        if not self.game.dungeon:
            return

        # Get biome colors
        biome = self.game.dungeon.biome
        biome_colors = c.BIOME_COLORS.get(biome, c.BIOME_COLORS[c.BIOME_DUNGEON])
        floor_color = biome_colors["floor"]
        wall_color = biome_colors["wall"]
        stairs_color = biome_colors["stairs"]

        # Render tiles
        for y in range(self.game.dungeon.height):
            for x in range(self.game.dungeon.width):
                tile = self.game.dungeon.get_tile(x, y)

                if tile == c.TILE_FLOOR:
                    entity = create_floor_mesh(x, y, floor_color)
                    self.dungeon_entities.append(entity)

                elif tile == c.TILE_WALL:
                    entity = create_wall_mesh(x, y, wall_color)
                    self.dungeon_entities.append(entity)

                elif tile == c.TILE_STAIRS:
                    # Render floor first
                    floor_entity = create_floor_mesh(x, y, floor_color)
                    self.dungeon_entities.append(floor_entity)

                    # Then stairs on top
                    stairs_entity = create_stairs_mesh(x, y, stairs_color)
                    self.dungeon_entities.append(stairs_entity)

        print(f"✓ Rendered dungeon: {len(self.dungeon_entities)} tiles")
        print(f"  - Dungeon size: {self.game.dungeon.width}x{self.game.dungeon.height}")
        if self.game.player:
            print(f"  - Player position: ({self.game.player.x}, {self.game.player.y})")
        print(f"  - Biome: {self.game.dungeon.biome}")

    def render_player(self):
        """
        Render or update the player entity

        Creates a simple colored cube for Phase 2 POC.
        Full character models will be implemented in Phase 4.
        """
        if not self.game.player:
            return

        # Player position
        pos = world_to_3d_position(
            self.game.player.x,
            self.game.player.y,
            c.PLAYER_HEIGHT / 2
        )

        # Get class color
        class_colors = {
            c.CLASS_WARRIOR: (100, 200, 255),   # Blue
            c.CLASS_MAGE: (150, 100, 255),      # Purple
            c.CLASS_ROGUE: (80, 80, 80),        # Gray
            c.CLASS_RANGER: (100, 220, 80),     # Green
        }

        color_rgb = class_colors.get(self.game.player.class_type, (100, 200, 255))
        player_color = ursina_color.rgb(color_rgb[0] / 255, color_rgb[1] / 255, color_rgb[2] / 255)

        # Create or update player entity
        if self.player_entity is None:
            self.player_entity = Entity(
                model='cube',
                color=player_color,
                scale=(c.ENTITY_SCALE, c.PLAYER_HEIGHT, c.ENTITY_SCALE),
                position=pos,
                texture='white_cube'
            )
            print(f"✓ Created player cube at 3D position {pos}")
            print(f"  - Grid position: ({self.game.player.x}, {self.game.player.y})")
            print(f"  - Class: {self.game.player.class_type}")
            print(f"  - Color: {player_color}")

            # Position camera immediately after creating player
            self.update_camera()
            print(f"✓ Camera positioned behind player at {camera.position}")
        else:
            # Update position
            self.player_entity.position = pos

        # Update player light position
        if self.player_light:
            self.player_light.position = (pos[0], pos[1] + 2, pos[2])

    def render_enemies(self):
        """
        Render or update all enemy entities with health bars
        """
        if not self.game.enemies:
            return

        # Track which enemies currently exist
        current_enemy_ids = set()

        for enemy in self.game.enemies:
            enemy_id = id(enemy)
            current_enemy_ids.add(enemy_id)

            # Calculate 3D position
            pos = world_to_3d_position(enemy.x, enemy.y, 0.5)

            # Create enemy model if it doesn't exist
            if enemy_id not in self.enemy_entities:
                enemy_model = create_enemy_model_3d(enemy.enemy_type, pos)

                # Create health bar billboard
                hp_pct = enemy.hp / enemy.max_hp
                health_bar = create_health_bar_billboard(hp_pct)
                health_bar.parent = enemy_model  # Attach to enemy

                # Store references
                self.enemy_entities[enemy_id] = {
                    'model': enemy_model,
                    'health_bar': health_bar,
                    'enemy_type': enemy.enemy_type
                }

                print(f"✓ Created 3D {enemy.enemy_type} at ({enemy.x}, {enemy.y})")
            else:
                # Update existing enemy position
                enemy_data = self.enemy_entities[enemy_id]
                enemy_data['model'].position = pos

                # Update health bar
                hp_pct = enemy.hp / enemy.max_hp
                update_health_bar(enemy_data['health_bar'], hp_pct)

        # Remove entities for enemies that no longer exist (died)
        dead_enemy_ids = set(self.enemy_entities.keys()) - current_enemy_ids
        for enemy_id in dead_enemy_ids:
            enemy_data = self.enemy_entities[enemy_id]
            enemy_data['model'].disable()  # Disable the model
            enemy_data['health_bar'].disable()  # Disable health bar
            del self.enemy_entities[enemy_id]
            print(f"✓ Removed dead enemy (ID: {enemy_id})")

    def render_items(self):
        """
        Render or update all item entities with floating/rotation animations
        """
        if not self.game.items:
            return

        # Track which items currently exist
        current_item_ids = set()

        for item in self.game.items:
            item_id = id(item)
            current_item_ids.add(item_id)

            # Calculate 3D position (items float above ground)
            pos = world_to_3d_position(item.x, item.y, 0.5)

            # Create item model if it doesn't exist
            if item_id not in self.item_entities:
                item_model = create_item_model_3d(item.item_type, item.rarity, pos)

                # Store reference
                self.item_entities[item_id] = item_model

                print(f"✓ Created 3D {item.rarity} {item.item_type} at ({item.x}, {item.y})")
            else:
                # Update existing item position (base position, animation handles float)
                item_entity = self.item_entities[item_id]
                # Only update X and Z, Y is controlled by float animation
                # pos is a tuple (x, y, z), not a Vec3
                item_entity.x = pos[0]
                item_entity.z = pos[2]

        # Remove entities for items that no longer exist (picked up)
        picked_up_item_ids = set(self.item_entities.keys()) - current_item_ids
        for item_id in picked_up_item_ids:
            item_entity = self.item_entities[item_id]
            item_entity.disable()  # Disable the model
            del self.item_entities[item_id]
            print(f"✓ Removed picked up item (ID: {item_id})")

    def render_entities(self):
        """
        Render or update all game entities (player, enemies, items)
        """
        self.render_player()
        self.render_enemies()
        self.render_items()

    def update_camera(self):
        """
        Update camera to follow player with smooth interpolation and screen shake
        """
        if not self.game.player:
            return

        # Target position behind and above player
        target_x = float(self.game.player.x)
        target_z = float(self.game.player.y)

        # Third-person camera position
        cam_x = target_x
        cam_y = c.CAMERA_HEIGHT
        cam_z = target_z - c.CAMERA_DISTANCE

        # On first call, jump directly to position (no smoothing)
        if not self.camera_initialized:
            self.base_camera_pos = Vec3(cam_x, cam_y, cam_z)
            camera.position = self.base_camera_pos
            self.camera_initialized = True
            print(f"✓ Camera initialized at {camera.position}")
        else:
            # Smooth interpolation (lerp) for subsequent updates
            self.base_camera_pos = Vec3(
                self.base_camera_pos.x + (cam_x - self.base_camera_pos.x) * self.camera_smooth_factor,
                self.base_camera_pos.y + (cam_y - self.base_camera_pos.y) * self.camera_smooth_factor,
                self.base_camera_pos.z + (cam_z - self.base_camera_pos.z) * self.camera_smooth_factor
            )

        # Apply screen shake offset
        shake_offset = self.animation_manager.get_screen_shake_offset()
        camera.position = self.base_camera_pos + shake_offset

        # Look at player (with shake offset)
        look_at_pos = Vec3(target_x, c.PLAYER_HEIGHT / 2, target_z) + shake_offset
        camera.look_at(look_at_pos)

    def update(self, dt: float):
        """
        Update renderer state (called every frame)

        Args:
            dt: Delta time since last frame
        """
        # Update entity positions
        self.render_entities()

        # Update enemy animations
        for enemy_id, enemy_data in self.enemy_entities.items():
            update_enemy_animation(
                enemy_data['model'],
                enemy_data['enemy_type'],
                dt
            )

        # Update item animations (floating and rotation)
        for item_id, item_entity in self.item_entities.items():
            update_item_animation(item_entity, dt)

        # Update 3D particle animations
        self.animation_manager.update(dt)

        # Update camera (includes screen shake)
        self.update_camera()

    def cleanup(self):
        """
        Clean up all 3D entities and resources
        """
        # Destroy dungeon
        for entity in self.dungeon_entities:
            entity.disable()
        self.dungeon_entities.clear()

        # Destroy player
        if self.player_entity:
            self.player_entity.disable()
            self.player_entity = None

        # Destroy enemies
        for enemy_id, enemy_data in self.enemy_entities.items():
            enemy_data['model'].disable()
            enemy_data['health_bar'].disable()
        self.enemy_entities.clear()

        # Destroy items
        for item_id, item_entity in self.item_entities.items():
            item_entity.disable()
        self.item_entities.clear()

        # Destroy lights
        if self.ambient_light:
            self.ambient_light.disable()
        if self.sun_light:
            self.sun_light.disable()
        if self.player_light:
            self.player_light.disable()

        # Clean up animations
        if self.animation_manager:
            self.animation_manager.clear_all()

        print("3D renderer cleaned up")
