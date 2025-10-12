#!/usr/bin/env python3
"""
Test script to verify Ursina installation and basic 3D rendering

This creates a simple 3D scene with a cube that can be moved with WASD.
Used for Phase 2 proof of concept.
"""

from ursina import Ursina, Entity, camera, color, held_keys, Vec3, time as ursina_time


def main():
    """Test Ursina basic functionality"""

    # Create Ursina app
    app = Ursina(title="Ursina Test - Claude-Like", borderless=False)

    # Create a simple cube (player)
    player_cube = Entity(
        model='cube',
        color=color.blue,
        position=(0, 0.5, 0),
        scale=(1, 1, 1)
    )

    # Create a floor
    floor = Entity(
        model='plane',
        color=color.gray,
        scale=(20, 1, 20),
        position=(0, 0, 0)
    )

    # Create some walls to test depth perception
    wall1 = Entity(
        model='cube',
        color=color.dark_gray,
        scale=(10, 2, 1),
        position=(0, 1, 5)
    )

    wall2 = Entity(
        model='cube',
        color=color.dark_gray,
        scale=(1, 2, 10),
        position=(5, 1, 0)
    )

    # Set up camera
    camera.position = (10, 8, -10)
    camera.look_at(player_cube)

    # Movement speed
    move_speed = 5

    def update():
        """Update function called every frame"""
        dt = ursina_time.dt

        # WASD movement
        if held_keys['w'] or held_keys['up arrow']:
            player_cube.z += move_speed * dt
        if held_keys['s'] or held_keys['down arrow']:
            player_cube.z -= move_speed * dt
        if held_keys['a'] or held_keys['left arrow']:
            player_cube.x -= move_speed * dt
        if held_keys['d'] or held_keys['right arrow']:
            player_cube.x += move_speed * dt

        # Camera follows player
        camera.position = Vec3(
            player_cube.x + 10,
            8,
            player_cube.z - 10
        )
        camera.look_at(player_cube)

        # Debug output (every 60 frames ~1 second)
        if int(ursina_time.time * 60) % 60 == 0:
            print(f"Player position: ({player_cube.x:.2f}, {player_cube.y:.2f}, {player_cube.z:.2f})")

    # Assign update function
    app.update = update

    print("=== Ursina Test ===")
    print("Controls:")
    print("  WASD / Arrow Keys - Move the blue cube")
    print("  ESC - Quit")
    print("==================")

    # Run the app
    app.run()


if __name__ == "__main__":
    main()
