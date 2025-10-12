#!/usr/bin/env python3
"""
Brick Texture Demo

Generates sample brick textures for visual verification.
Saves PNG files to demonstrate different parameters.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from textures.bricks import generate_brick_pattern
from textures import RandomSeed


def main():
    """Generate and save sample brick textures."""
    # Create output directory
    output_dir = "output/brick_samples"
    os.makedirs(output_dir, exist_ok=True)

    print("Generating brick texture samples...")

    # Sample 1: Normal brick (256x256)
    print("  - brick_normal_256.png")
    with RandomSeed(12345):
        brick = generate_brick_pattern(size=256, darkness=1.0)
        brick.save(f"{output_dir}/brick_normal_256.png")

    # Sample 2: Dark brick
    print("  - brick_dark_256.png")
    with RandomSeed(12345):
        brick_dark = generate_brick_pattern(size=256, darkness=0.6)
        brick_dark.save(f"{output_dir}/brick_dark_256.png")

    # Sample 3: Very dark brick
    print("  - brick_very_dark_256.png")
    with RandomSeed(12345):
        brick_very_dark = generate_brick_pattern(size=256, darkness=0.4)
        brick_very_dark.save(f"{output_dir}/brick_very_dark_256.png")

    # Sample 4: Larger size (512x512)
    print("  - brick_normal_512.png")
    with RandomSeed(12345):
        brick_large = generate_brick_pattern(size=512, darkness=1.0)
        brick_large.save(f"{output_dir}/brick_normal_512.png")

    # Sample 5: Different random seed
    print("  - brick_alt_pattern_256.png")
    with RandomSeed(99999):
        brick_alt = generate_brick_pattern(size=256, darkness=1.0)
        brick_alt.save(f"{output_dir}/brick_alt_pattern_256.png")

    # Sample 6: Small size for tiling test (128x128)
    print("  - brick_small_128.png")
    with RandomSeed(12345):
        brick_small = generate_brick_pattern(size=128, darkness=1.0)
        brick_small.save(f"{output_dir}/brick_small_128.png")

    print(f"\n✓ Saved 6 sample brick textures to {output_dir}/")
    print("\nSamples generated:")
    print("  • brick_normal_256.png      - Standard brick texture")
    print("  • brick_dark_256.png        - 60% darkness for shadows")
    print("  • brick_very_dark_256.png   - 40% darkness for deep shadows")
    print("  • brick_normal_512.png      - High-res version")
    print("  • brick_alt_pattern_256.png - Different random pattern")
    print("  • brick_small_128.png       - Small for tiling tests")


if __name__ == '__main__':
    main()
