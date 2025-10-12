"""
3D mode entry point using Ursina Engine

This module provides the main game loop for 3D rendering mode.
All game logic remains in game.py - this only handles visualization and input.
"""

from ursina import Ursina, Entity, camera, held_keys, time as ursina_time, color
import constants as c
from game import Game
from renderer3d import Renderer3D


def main_3d():
    """Main entry point for 3D mode"""

    # Create Ursina app
    app = Ursina(
        title="Claude-Like 3D",
        borderless=False,
        fullscreen=False,
        development_mode=False  # Set to True for debug info
    )

    # Create game instance
    game = Game()
    game.selected_class = c.CLASS_WARRIOR  # Default class for Phase 2 testing
    game.start_new_game()

    # Create 3D renderer
    renderer = Renderer3D(game)
    renderer.render_dungeon()
    renderer.render_entities()

    # Input cooldown to prevent holding keys
    move_cooldown = 0.0
    move_cooldown_time = 0.15  # Seconds between moves

    # Track if game is over
    game_over_displayed = False

    def update():
        """Update function called every frame by Ursina"""
        nonlocal move_cooldown, game_over_displayed

        dt = ursina_time.dt
        move_cooldown -= dt

        # Check for game over
        if game.game_over or game.victory:
            if not game_over_displayed:
                print("\n" + "=" * 50)
                if game.victory:
                    print("🎉 VICTORY! You conquered all 25 levels!")
                else:
                    print("💀 GAME OVER! You were defeated.")
                print(f"Final Level: {game.current_level}")
                print(f"Final XP: {game.player.xp}")
                print("=" * 50)
                print("Press ESC to quit")
                game_over_displayed = True
            return

        # Handle movement input (only if cooldown expired)
        if move_cooldown <= 0:
            moved = False
            new_x, new_y = game.player.x, game.player.y

            # WASD / Arrow Keys movement
            if held_keys['w'] or held_keys['up arrow']:
                new_x, new_y = game.player.x, game.player.y - 1
                moved = True

            elif held_keys['s'] or held_keys['down arrow']:
                new_x, new_y = game.player.x, game.player.y + 1
                moved = True

            elif held_keys['a'] or held_keys['left arrow']:
                new_x, new_y = game.player.x - 1, game.player.y
                moved = True

            elif held_keys['d'] or held_keys['right arrow']:
                new_x, new_y = game.player.x + 1, game.player.y
                moved = True

            # Attempt move
            if moved:
                # Try to move player via game logic
                if game.dungeon.is_walkable(new_x, new_y):
                    # Check for enemy at target position
                    target_enemy = None
                    for enemy in game.enemies:
                        if enemy.x == new_x and enemy.y == new_y:
                            target_enemy = enemy
                            break

                    if target_enemy:
                        # Attack enemy
                        game.player_attack(target_enemy)
                    else:
                        # Move player
                        game.player.start_move(new_x, new_y)
                        game.update_camera()
                        game.update_fov()

                        # Check for stairs
                        if game.dungeon.get_tile(new_x, new_y) == c.TILE_STAIRS:
                            game.descend_stairs()
                            # Re-render dungeon after descending
                            renderer.render_dungeon()

                        # Enemy turn
                        game.enemy_turn()

                    move_cooldown = move_cooldown_time  # Reset cooldown

        # Update game animations
        game.update(dt)

        # Update renderer
        renderer.update(dt)

        # Debug output (every 2 seconds)
        if int(ursina_time.time * 0.5) % 2 == 0:
            if hasattr(update, '_last_debug_time') and ursina_time.time - update._last_debug_time < 1.9:
                pass  # Skip
            else:
                update._last_debug_time = ursina_time.time
                print(f"Player: ({game.player.x}, {game.player.y}) | "
                      f"HP: {game.player.hp}/{game.player.max_hp} | "
                      f"Level: {game.current_level} | "
                      f"Enemies: {len(game.enemies)}")

    # Assign update function to Ursina
    app.update = update

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
