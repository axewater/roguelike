#!/usr/bin/env python3
"""
Claude-Like - A simple roguelike game
Entry point
"""
import sys
from PyQt6.QtWidgets import QApplication
from ui import MainWindow


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
