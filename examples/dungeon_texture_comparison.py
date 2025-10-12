"""
Dungeon Texture Comparison - Before/After Moss Adjustments

Shows the difference between:
- Heavy vs Medium moss on walls (25% less coverage)
- Plain brick vs Mossy brick on floors
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from textures import RandomSeed
from textures.organic import generate_moss_stone_texture, generate_moss_overlay
from textures.bricks import generate_brick_pattern

# Create output directory
output_dir = "output/dungeon_comparison"
os.makedirs(output_dir, exist_ok=True)

print("=" * 60)
print("DUNGEON TEXTURE COMPARISON - Moss Adjustments")
print("=" * 60)
print()

# Use same seed for fair comparison
SEED = 12345

# ===== WALL COMPARISON =====
print("WALLS - Heavy vs Medium moss density:")
print()

print("  Before: Heavy moss (original)...")
with RandomSeed(SEED):
    wall_heavy = generate_moss_stone_texture(size=256, moss_density='heavy')
    wall_heavy.save(f"{output_dir}/wall_before_heavy.png")
print(f"     ✓ Saved: {output_dir}/wall_before_heavy.png")

print("  After: Medium moss (25% less coverage)...")
with RandomSeed(SEED):
    wall_medium = generate_moss_stone_texture(size=256, moss_density='medium')
    wall_medium.save(f"{output_dir}/wall_after_medium.png")
print(f"     ✓ Saved: {output_dir}/wall_after_medium.png")

print()

# ===== FLOOR COMPARISON =====
print("FLOORS - Plain brick vs Mossy brick:")
print()

print("  Before: Plain dark brick (no moss)...")
with RandomSeed(SEED + 100):
    floor_plain = generate_brick_pattern(size=256, darkness=0.8)
    floor_plain.save(f"{output_dir}/floor_before_plain.png")
print(f"     ✓ Saved: {output_dir}/floor_before_plain.png")

print("  After: Brick with light moss accents...")
with RandomSeed(SEED + 100):
    floor_brick = generate_brick_pattern(size=256, darkness=0.8)
    floor_mossy = generate_moss_overlay(floor_brick, density='light')
    floor_mossy.save(f"{output_dir}/floor_after_mossy.png")
print(f"     ✓ Saved: {output_dir}/floor_after_mossy.png")

print()

# ===== GAME TEXTURES (EXACTLY AS USED) =====
print("EXACT GAME TEXTURES (as they appear in 3D):")
print()

print("  Wall texture (medium moss)...")
with RandomSeed(99999):
    game_wall = generate_moss_stone_texture(size=256, moss_density='medium')
    game_wall.save(f"{output_dir}/game_wall.png")
print(f"     ✓ Saved: {output_dir}/game_wall.png")

print("  Floor texture (brick + light moss)...")
with RandomSeed(99998):
    game_floor_brick = generate_brick_pattern(size=256, darkness=0.8)
    game_floor = generate_moss_overlay(game_floor_brick, density='light')
    game_floor.save(f"{output_dir}/game_floor.png")
print(f"     ✓ Saved: {output_dir}/game_floor.png")

print()
print("=" * 60)
print("✓ COMPLETE - 6 texture samples generated")
print(f"  Output directory: {output_dir}/")
print()
print("Changes made:")
print("  ✓ Walls: Reduced moss coverage by ~25% (heavy → medium)")
print("  ✓ Floors: Added subtle moss drops/stripes between bricks")
print()
print("=" * 60)
