"""
3D mode entry point using Ursina Engine

This module provides the main game loop for 3D rendering mode.
All game logic remains in game.py - this only handles visualization and input.
"""

from ursina import Ursina, Entity, camera, held_keys, time as ursina_time, color, window
import constants as c
from game import Game
from renderer3d import Renderer3D


class GameController(Entity):
    """
    Main game controller using Ursina Entity pattern.
    Ursina automatically calls update() on all Entity subclasses.
    """
    def __init__(self, game, renderer):
        super().__init__()
        self.game = game
        self.renderer = renderer

        # Input cooldown to prevent holding keys
        self.move_cooldown = 0.0
        self.move_cooldown_time = 0.15  # Seconds between moves

        # Track if game is over
        self.game_over_displayed = False

        # Debug: Frame counter
        self.frame_count = 0

        print("✓ GameController initialized")

    def update(self):
        """Update function called every frame by Ursina"""
        dt = ursina_time.dt
        self.frame_count += 1

        # DEBUG: Heartbeat every 60 frames (~1 second at 60fps)
        if self.frame_count % 60 == 0:
            print(f"[HEARTBEAT] Frame {self.frame_count} | dt={dt:.4f} | FPS={1/dt:.1f}")

        self.move_cooldown -= dt

        # Check for game over
        if self.game.game_over or self.game.victory:
            if not self.game_over_displayed:
                print("\n" + "=" * 50)
                if self.game.victory:
                    print("🎉 VICTORY! You conquered all 25 levels!")
                else:
                    print("💀 GAME OVER! You were defeated.")
                print(f"Final Level: {self.game.current_level}")
                print(f"Final XP: {self.game.player.xp}")
                print("=" * 50)
                print("Press ESC to quit")
                self.game_over_displayed = True
            return

        # Handle movement input (only if cooldown expired)
        if self.move_cooldown <= 0:
            moved = False
            new_x, new_y = self.game.player.x, self.game.player.y
            direction = ""

            # WASD / Arrow Keys movement
            if held_keys['w'] or held_keys['up arrow']:
                new_x, new_y = self.game.player.x, self.game.player.y - 1
                moved = True
                direction = "UP"

            elif held_keys['s'] or held_keys['down arrow']:
                new_x, new_y = self.game.player.x, self.game.player.y + 1
                moved = True
                direction = "DOWN"

            elif held_keys['a'] or held_keys['left arrow']:
                new_x, new_y = self.game.player.x - 1, self.game.player.y
                moved = True
                direction = "LEFT"

            elif held_keys['d'] or held_keys['right arrow']:
                new_x, new_y = self.game.player.x + 1, self.game.player.y
                moved = True
                direction = "RIGHT"

            # DEBUG: Print key press
            if moved:
                print(f"[INPUT] Key pressed: {direction} | Target: ({new_x}, {new_y})")

            # Attempt move
            if moved:
                # Try to move player via game logic
                if self.game.dungeon.is_walkable(new_x, new_y):
                    # Check for enemy at target position
                    target_enemy = None
                    for enemy in self.game.enemies:
                        if enemy.x == new_x and enemy.y == new_y:
                            target_enemy = enemy
                            break

                    if target_enemy:
                        # Attack enemy
                        print(f"[COMBAT] Attacking enemy at ({new_x}, {new_y})")
                        self.game._player_attack(target_enemy)
                    else:
                        # Move player
                        old_pos = (self.game.player.x, self.game.player.y)
                        self.game.player.start_move(new_x, new_y)
                        self.game.update_camera()
                        self.game.update_fov()
                        print(f"[MOVE] Player moved: {old_pos} → ({self.game.player.x}, {self.game.player.y})")

                        # Check for stairs
                        if self.game.dungeon.get_tile(new_x, new_y) == c.TILE_STAIRS:
                            print(f"[EVENT] Player on stairs! Descending...")
                            self.game.descend_stairs()
                            # Re-render dungeon after descending
                            self.renderer.render_dungeon()

                        # Enemy turn
                        self.game._enemy_turn()

                    self.move_cooldown = self.move_cooldown_time  # Reset cooldown
                else:
                    print(f"[BLOCKED] Cannot move to ({new_x}, {new_y}) - not walkable")

        # Update game animations
        self.game.update(dt)

        # Update renderer
        self.renderer.update(dt)

        # Debug output (every 120 frames = ~2 seconds at 60fps)
        if self.frame_count % 120 == 0:
            print(f"Player: ({self.game.player.x}, {self.game.player.y}) | "
                  f"HP: {self.game.player.hp}/{self.game.player.max_hp} | "
                  f"Level: {self.game.current_level} | "
                  f"Enemies: {len(self.game.enemies)} | "
                  f"Camera: {camera.position}")


def main_3d():
    """Main entry point for 3D mode"""

    # Create Ursina app
    app = Ursina(
        title="Claude-Like 3D",
        borderless=False,
        fullscreen=False,
        development_mode=False  # Set to True for debug info
    )

    # Set window resolution to Full HD for better performance
    window.size = (1920, 1080)
    window.position = (0, 0)
    print(f"✓ Window resolution set to 1920x1080")

    # Set background color (dark blue, matching 2D title screen)
    window.color = color.rgb(0.05, 0.05, 0.15)
    print("✓ Window background set to dark blue")

    # Create game instance
    game = Game()
    game.selected_class = c.CLASS_WARRIOR  # Default class for Phase 2 testing
    game.start_new_game()

    # Create 3D renderer
    renderer = Renderer3D(game)
    renderer.render_dungeon()
    renderer.render_entities()

    # Create game controller (Ursina will automatically call its update() method)
    controller = GameController(game, renderer)

    # Print controls
    print("\n" + "=" * 50)
    print("CONTROLS:")
    print("  WASD / Arrow Keys - Move & Attack")
    print("  ESC - Quit")
    print("=" * 50)
    print("Starting game...")
    print(f"Class: {game.selected_class.title()}")
    print(f"Level: {game.current_level}")
    print(f"HP: {game.player.hp}/{game.player.max_hp}")
    print("=" * 50 + "\n")

    # Run Ursina app loop
    app.run()


if __name__ == "__main__":
    main_3d()
