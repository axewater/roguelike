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

    def render_entities(self):
        """
        Render or update all game entities (player, enemies, items)

        For Phase 2, only player is rendered.
        Enemies and items will be added in Phase 4.
        """
        self.render_player()

        # TODO: Phase 4 - Render enemies
        # TODO: Phase 4 - Render items

    def update_camera(self):
        """
        Update camera to follow player with smooth interpolation
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
            camera.position = Vec3(cam_x, cam_y, cam_z)
            self.camera_initialized = True
            print(f"✓ Camera initialized at {camera.position}")
        else:
            # Smooth interpolation (lerp) for subsequent updates
            camera.position = Vec3(
                camera.position.x + (cam_x - camera.position.x) * self.camera_smooth_factor,
                camera.position.y + (cam_y - camera.position.y) * self.camera_smooth_factor,
                camera.position.z + (cam_z - camera.position.z) * self.camera_smooth_factor
            )

        # Look at player
        look_at_pos = Vec3(target_x, c.PLAYER_HEIGHT / 2, target_z)
        camera.look_at(look_at_pos)

    def update(self, dt: float):
        """
        Update renderer state (called every frame)

        Args:
            dt: Delta time since last frame
        """
        # Update entity positions
        self.render_entities()

        # Update camera
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

        # Destroy lights
        if self.ambient_light:
            self.ambient_light.disable()
        if self.sun_light:
            self.sun_light.disable()
        if self.player_light:
            self.player_light.disable()

        print("3D renderer cleaned up")
