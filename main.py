#!/usr/bin/env python3
"""
Claude-Like - A simple roguelike game
Entry point with 2D/3D mode selection
"""
import sys
import argparse


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Claude-Like Roguelike - A dungeon crawler with 2D and 3D rendering modes'
    )
    parser.add_argument(
        '--mode',
        choices=['2d', '3d'],
        default='2d',
        help='Rendering mode: 2d (PyQt6) or 3d (Ursina). Default: 2d'
    )
    return parser.parse_args()


def main_2d():
    """Launch 2D mode using PyQt6"""
    from PyQt6.QtWidgets import QApplication
    from ui import MainWindow

    print("=== Claude-Like (2D Mode) ===")
    print("Launching PyQt6 2D renderer...")

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


def main_3d():
    """Launch 3D mode using Ursina"""
    print("=== Claude-Like (3D Mode) ===")
    print("Launching Ursina 3D renderer...")

    from main_3d import main_3d as run_3d_game
    run_3d_game()


def main():
    """Main entry point with mode selection"""
    args = parse_args()

    if args.mode == '3d':
        main_3d()
    else:
        main_2d()


if __name__ == "__main__":
    main()
