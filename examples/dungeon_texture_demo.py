"""
Dungeon Texture Demo - Phase 3 Integration Test

Generates visual samples of the procedural textures that will be used
in the 3D dungeon (moss-covered stone walls and brick floors).
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from textures import get_moss_stone_texture, get_brick_texture, RandomSeed
from textures.organic import generate_moss_stone_texture
from textures.bricks import generate_brick_pattern

# Create output directory
output_dir = "output/dungeon_samples"
os.makedirs(output_dir, exist_ok=True)

print("=" * 60)
print("DUNGEON TEXTURE DEMO - Phase 3 Integration")
print("=" * 60)
print()

# ===== WALL TEXTURES =====
print("Generating wall textures (moss-covered stone)...")

# 1. Standard dungeon wall (heavy moss)
print("  1. Standard dungeon wall (heavy moss, 256x256)...")
with RandomSeed(12345):
    wall_heavy = generate_moss_stone_texture(size=256, moss_density='heavy')
    wall_heavy.save(f"{output_dir}/dungeon_wall_heavy.png")
print(f"     ✓ Saved: {output_dir}/dungeon_wall_heavy.png")

# 2. Medium moss variation
print("  2. Medium moss variation (256x256)...")
with RandomSeed(12346):
    wall_medium = generate_moss_stone_texture(size=256, moss_density='medium')
    wall_medium.save(f"{output_dir}/dungeon_wall_medium.png")
print(f"     ✓ Saved: {output_dir}/dungeon_wall_medium.png")

# 3. Light moss variation
print("  3. Light moss variation (256x256)...")
with RandomSeed(12347):
    wall_light = generate_moss_stone_texture(size=256, moss_density='light')
    wall_light.save(f"{output_dir}/dungeon_wall_light.png")
print(f"     ✓ Saved: {output_dir}/dungeon_wall_light.png")

# 4. High-res wall for close inspection
print("  4. High-resolution wall (512x512)...")
with RandomSeed(99999):
    wall_hires = generate_moss_stone_texture(size=512, moss_density='heavy')
    wall_hires.save(f"{output_dir}/dungeon_wall_hires.png")
print(f"     ✓ Saved: {output_dir}/dungeon_wall_hires.png")

print()

# ===== FLOOR TEXTURES =====
print("Generating floor textures (brick patterns)...")

# 5. Standard dungeon floor (dark brick)
print("  5. Standard dungeon floor (dark brick, 256x256)...")
with RandomSeed(54321):
    floor_standard = generate_brick_pattern(size=256, darkness=0.8)
    floor_standard.save(f"{output_dir}/dungeon_floor_standard.png")
print(f"     ✓ Saved: {output_dir}/dungeon_floor_standard.png")

# 6. Normal brightness floor
print("  6. Normal brightness floor (256x256)...")
with RandomSeed(54322):
    floor_normal = generate_brick_pattern(size=256, darkness=1.0)
    floor_normal.save(f"{output_dir}/dungeon_floor_normal.png")
print(f"     ✓ Saved: {output_dir}/dungeon_floor_normal.png")

# 7. Very dark floor (for deep dungeons)
print("  7. Very dark floor (256x256)...")
with RandomSeed(54323):
    floor_dark = generate_brick_pattern(size=256, darkness=0.5)
    floor_dark.save(f"{output_dir}/dungeon_floor_dark.png")
print(f"     ✓ Saved: {output_dir}/dungeon_floor_dark.png")

print()
print("=" * 60)
print("✓ COMPLETE - 7 texture samples generated")
print(f"  Output directory: {output_dir}/")
print()
print("These textures will be used in the 3D game:")
print("  - Walls: moss-covered stone (heavy moss)")
print("  - Floors: dark brick (0.8 darkness)")
print()
print("To view textures, open the PNG files in an image viewer.")
print("=" * 60)
