"""
Shader library for post-processing effects

This package contains GLSL shaders for camera and rendering effects.
"""

from .barrel_distortion import create_barrel_distortion_shader

__all__ = ['create_barrel_distortion_shader']
