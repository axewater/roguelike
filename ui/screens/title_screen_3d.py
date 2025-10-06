"""
3D OpenGL Animated Title Screen
Features flying letters with particle effects
"""
import math
import random
import time
from typing import List, Tuple

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QFontMetrics, QImage, QPainter, QColor
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

from audio import get_audio_manager


class Letter3D:
    """Represents a single 3D animated letter"""
    def __init__(self, char: str, final_x: float, final_y: float, delay: float, duration: float, texture_id: int = 0):
        self.char = char
        self.final_x = final_x
        self.final_y = final_y
        self.final_z = 0.0
        self.texture_id = texture_id  # OpenGL texture ID for this letter

        # Animation timing
        self.delay = delay  # Delay before starting animation
        self.duration = duration  # How long the flight takes
        self.time = 0.0
        self.state = "waiting"  # waiting, flying, landed

        # Starting position (off-screen, far back, high up)
        angle = random.uniform(-30, 30)
        self.start_x = final_x + random.uniform(-15, 15)
        self.start_y = final_y + 20 + random.uniform(5, 10)
        self.start_z = -50 + random.uniform(-10, 10)

        # Current position
        self.x = self.start_x
        self.y = self.start_y
        self.z = self.start_z

        # Rotation for spinning effect
        self.rotation_x = random.uniform(720, 1080)  # Multiple spins
        self.rotation_y = random.uniform(360, 540)
        self.rotation_z = random.uniform(180, 360)
        self.current_rotation_x = 0.0
        self.current_rotation_y = 0.0
        self.current_rotation_z = 0.0

        # Particle burst flag
        self.has_burst = False

        # Color (purple-blue gradient)
        self.color = [0.6 + random.uniform(0, 0.2), 0.4 + random.uniform(0, 0.3), 1.0]

        # Glow intensity
        self.glow = 0.0

    def update(self, dt: float) -> Tuple[bool, bool]:
        """Update animation state. Returns (trigger_burst, started_flying)"""
        self.time += dt
        trigger_burst = False
        started_flying = False

        if self.state == "waiting":
            if self.time >= self.delay:
                self.state = "flying"
                started_flying = True
                return False, started_flying

        elif self.state == "flying":
            # Calculate progress through flight (0 to 1)
            flight_time = self.time - self.delay
            progress = min(flight_time / self.duration, 1.0)

            # Ease-out cubic for smooth deceleration
            eased = 1 - pow(1 - progress, 3)

            # Interpolate position
            self.x = self.start_x + (self.final_x - self.start_x) * eased
            self.y = self.start_y + (self.final_y - self.start_y) * eased
            self.z = self.start_z + (self.final_z - self.start_z) * eased

            # Rotation (spins faster at start, slows down)
            spin_progress = 1 - pow(1 - progress, 2)
            self.current_rotation_x = self.rotation_x * spin_progress
            self.current_rotation_y = self.rotation_y * spin_progress
            self.current_rotation_z = self.rotation_z * spin_progress

            # Check if landed
            if progress >= 1.0:
                self.state = "landed"
                self.x = self.final_x
                self.y = self.final_y
                self.z = self.final_z
                self.current_rotation_x = 0
                self.current_rotation_y = 0
                self.current_rotation_z = 0
                trigger_burst = True

        elif self.state == "landed":
            # Pulsing glow effect
            self.glow = 0.3 + 0.2 * math.sin(self.time * 3.0)

        return trigger_burst, started_flying


class Particle3D:
    """3D particle for burst effects"""
    def __init__(self, x: float, y: float, z: float, vx: float, vy: float, vz: float, color: List[float]):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.color = color[:]
        self.lifetime = 0.0
        self.max_lifetime = random.uniform(0.3, 0.8)
        self.size = random.uniform(0.05, 0.15)
        self.alpha = 1.0

    def update(self, dt: float) -> bool:
        """Update particle. Returns True if still alive"""
        self.lifetime += dt

        if self.lifetime >= self.max_lifetime:
            return False

        # Move
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt

        # Apply gravity
        self.vy -= 5.0 * dt

        # Friction
        self.vx *= 0.98
        self.vz *= 0.98

        # Fade out
        self.alpha = 1.0 - (self.lifetime / self.max_lifetime)

        return True


class TitleScreen3D(QOpenGLWidget):
    """3D animated title screen with flying letters"""
    continue_pressed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Animation state
        self.letters: List[Letter3D] = []
        self.particles: List[Particle3D] = []
        self.time_elapsed = 0.0
        self.last_time = time.time()
        self.animation_complete = False

        # Camera
        self.camera_shake = 0.0
        self.camera_zoom = 0.0

        # Prompt fade
        self.prompt_fade = 0.0

        # Letter textures (created in initializeGL)
        self.letter_textures = {}

        # Letters will be initialized in initializeGL (after OpenGL context is ready)

        # Timer for animation updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # ~60 FPS

        # Audio
        self.audio = get_audio_manager()

    def _generate_letter_textures(self):
        """Generate OpenGL textures for each unique letter"""
        text = "CLAUDE-LIKE"
        unique_chars = set(text.replace(' ', '').replace('-', ''))

        for char in unique_chars:
            # Create QImage to render text
            size = 256  # Texture size (power of 2)
            image = QImage(size, size, QImage.Format.Format_RGBA8888)
            image.fill(QColor(0, 0, 0, 0))  # Transparent background

            # Use QPainter to draw text
            painter = QPainter(image)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

            # Set font
            font = QFont("Arial", 180, QFont.Weight.Bold)
            painter.setFont(font)

            # Draw text in white
            painter.setPen(QColor(255, 255, 255, 255))
            painter.drawText(image.rect(), Qt.AlignmentFlag.AlignCenter, char)
            painter.end()

            # Convert to OpenGL texture
            # Flip image vertically for OpenGL coordinate system
            image = image.mirrored(False, True)

            # Generate texture
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)

            # Set texture parameters
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

            # Upload texture data
            img_data = image.constBits().asstring(size * size * 4)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, size, size, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

            # Store texture ID
            self.letter_textures[char] = texture_id

        print(f"✓ Generated {len(self.letter_textures)} letter textures")

    def _init_letters(self):
        """Initialize 3D letters with staggered timing"""
        text = "CLAUDE-LIKE"
        spacing = 1.2

        # Count actual letters (excluding spaces and hyphens)
        num_letters = len([c for c in text if c not in (' ', '-')])

        # Calculate total width to center text
        total_width = (num_letters - 1) * spacing
        start_x = -total_width / 2

        # Create letters with accelerating animation
        base_duration = 2.0
        duration_decrease = 0.12
        delay_offset = 0.15

        letter_index = 0
        for i, char in enumerate(text):
            if char in (' ', '-'):
                continue  # Skip spaces and hyphens (creates gap)

            x = start_x + letter_index * spacing
            y = 0.0

            # Each letter starts slightly later and moves faster
            delay = letter_index * delay_offset
            duration = max(base_duration - (letter_index * duration_decrease), 0.6)

            # Get texture ID for this character
            texture_id = self.letter_textures.get(char, 0)

            letter = Letter3D(char, x, y, delay, duration, texture_id)
            self.letters.append(letter)
            letter_index += 1

    def initializeGL(self):
        """Initialize OpenGL settings"""
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

        # Enable lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        # Set up light
        glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 10, 1])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.4, 1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 1.0, 1])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1])

        # Background color (dark blue-purple)
        glClearColor(0.05, 0.05, 0.15, 1.0)

        # Generate letter textures and initialize letters
        self._generate_letter_textures()
        self._init_letters()

    def resizeGL(self, w: int, h: int):
        """Handle window resize"""
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Set up perspective projection
        aspect = w / h if h > 0 else 1
        gluPerspective(45, aspect, 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        """Render the 3D scene"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Position camera with slight shake effect
        shake_x = math.sin(self.camera_shake * 20) * 0.1 if self.camera_shake > 0 else 0
        shake_y = math.cos(self.camera_shake * 25) * 0.1 if self.camera_shake > 0 else 0
        gluLookAt(
            shake_x, shake_y, 8 + self.camera_zoom,  # Camera position
            0, 0, 0,  # Look at origin
            0, 1, 0   # Up vector
        )

        # Draw starfield background
        self._draw_starfield()

        # Draw letters
        for letter in self.letters:
            if letter.state != "waiting":
                self._draw_letter(letter)

        # Draw particles
        glDisable(GL_LIGHTING)
        for particle in self.particles:
            self._draw_particle(particle)
        glEnable(GL_LIGHTING)

        # Draw 2D overlay (prompt text)
        if self.animation_complete:
            self._draw_overlay()

    def _draw_starfield(self):
        """Draw animated starfield background"""
        glDisable(GL_LIGHTING)
        glPointSize(2.0)
        glBegin(GL_POINTS)

        for i in range(200):
            # Pseudo-random star positions
            x = (math.sin(i * 12.345) * 20) % 40 - 20
            y = (math.cos(i * 23.456) * 15) % 30 - 15
            z = (math.sin(i * 34.567) * 30) % 60 - 50

            # Twinkle effect
            twinkle = 0.5 + 0.5 * math.sin(self.time_elapsed * 2 + i)
            brightness = 0.3 + twinkle * 0.3

            glColor4f(brightness, brightness, brightness + 0.2, 1.0)
            glVertex3f(x, y, z)

        glEnd()
        glEnable(GL_LIGHTING)

    def _draw_letter(self, letter: Letter3D):
        """Draw a 3D letter"""
        glPushMatrix()

        # Position
        glTranslatef(letter.x, letter.y, letter.z)

        # Rotation
        glRotatef(letter.current_rotation_x, 1, 0, 0)
        glRotatef(letter.current_rotation_y, 0, 1, 0)
        glRotatef(letter.current_rotation_z, 0, 0, 1)

        # Color with glow
        r = letter.color[0] + letter.glow
        g = letter.color[1] + letter.glow
        b = letter.color[2]
        glColor3f(r, g, b)

        # Draw extruded letter (3D box with textured character)
        self._draw_3d_char(letter.texture_id)

        glPopMatrix()

    def _draw_3d_char(self, texture_id: int):
        """Draw a 3D character using quads with texture mapping"""

        # Enable texturing for front face
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        # Disable lighting for textured face to show true colors
        glDisable(GL_LIGHTING)

        # Front face with texture
        glColor4f(1.0, 1.0, 1.0, 1.0)  # White to show texture as-is
        glBegin(GL_QUADS)
        glNormal3f(0, 0, 1)
        glTexCoord2f(0, 0)
        glVertex3f(-0.4, -0.5, 0.2)
        glTexCoord2f(1, 0)
        glVertex3f(0.4, -0.5, 0.2)
        glTexCoord2f(1, 1)
        glVertex3f(0.4, 0.5, 0.2)
        glTexCoord2f(0, 1)
        glVertex3f(-0.4, 0.5, 0.2)
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glEnable(GL_LIGHTING)

        # Draw 3D box sides (no texture)
        glBegin(GL_QUADS)

        # Back face (darker)
        glColor3f(0.3, 0.2, 0.5)
        glNormal3f(0, 0, -1)
        glVertex3f(-0.4, -0.5, -0.2)
        glVertex3f(-0.4, 0.5, -0.2)
        glVertex3f(0.4, 0.5, -0.2)
        glVertex3f(0.4, -0.5, -0.2)

        # Top face
        glNormal3f(0, 1, 0)
        glVertex3f(-0.4, 0.5, -0.2)
        glVertex3f(-0.4, 0.5, 0.2)
        glVertex3f(0.4, 0.5, 0.2)
        glVertex3f(0.4, 0.5, -0.2)

        # Bottom face
        glNormal3f(0, -1, 0)
        glVertex3f(-0.4, -0.5, -0.2)
        glVertex3f(0.4, -0.5, -0.2)
        glVertex3f(0.4, -0.5, 0.2)
        glVertex3f(-0.4, -0.5, 0.2)

        # Left face
        glNormal3f(-1, 0, 0)
        glVertex3f(-0.4, -0.5, -0.2)
        glVertex3f(-0.4, -0.5, 0.2)
        glVertex3f(-0.4, 0.5, 0.2)
        glVertex3f(-0.4, 0.5, -0.2)

        # Right face
        glNormal3f(1, 0, 0)
        glVertex3f(0.4, -0.5, -0.2)
        glVertex3f(0.4, 0.5, -0.2)
        glVertex3f(0.4, 0.5, 0.2)
        glVertex3f(0.4, -0.5, 0.2)

        glEnd()

    def _draw_particle(self, particle: Particle3D):
        """Draw a particle"""
        glPushMatrix()
        glTranslatef(particle.x, particle.y, particle.z)

        # Billboard (always face camera)
        # Simplified: just draw a quad
        glColor4f(particle.color[0], particle.color[1], particle.color[2], particle.alpha)

        size = particle.size
        glBegin(GL_QUADS)
        glVertex3f(-size, -size, 0)
        glVertex3f(size, -size, 0)
        glVertex3f(size, size, 0)
        glVertex3f(-size, size, 0)
        glEnd()

        glPopMatrix()

    def _draw_overlay(self):
        """Draw 2D overlay text"""
        # Switch to 2D orthographic projection
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.width(), self.height(), 0, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)

        # Draw "Press Any Key" with fade
        alpha = self.prompt_fade
        glColor4f(0.8, 0.8, 0.9, alpha)

        # Note: For proper text rendering, we'd use QPainter or texture-based text
        # This is a simplified placeholder

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)

        # Restore 3D projection
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def update_animation(self):
        """Update animation state"""
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        self.time_elapsed += dt

        # Update letters
        all_landed = True
        for letter in self.letters:
            trigger_burst, started_flying = letter.update(dt)

            # Play whoosh sound when letter starts flying
            if started_flying:
                self.audio.play_letter_whoosh()

            # Play impact sound and create particles when letter lands
            if trigger_burst and not letter.has_burst:
                letter.has_burst = True
                self._create_particle_burst(letter.x, letter.y, letter.z, letter.color)

                # Camera shake
                self.camera_shake = 0.2

                # Play impact sound
                self.audio.play_letter_impact()

            if letter.state != "landed":
                all_landed = False

        # Update particles
        self.particles = [p for p in self.particles if p.update(dt)]

        # Camera effects
        if self.camera_shake > 0:
            self.camera_shake -= dt * 2
            self.camera_shake = max(0, self.camera_shake)

        # Check if animation complete
        if all_landed and not self.animation_complete:
            self.animation_complete = True

        # Update prompt fade
        if self.animation_complete:
            self.prompt_fade = min(1.0, self.prompt_fade + dt)

        self.update()

    def _create_particle_burst(self, x: float, y: float, z: float, color: List[float]):
        """Create a burst of particles"""
        num_particles = 25

        for _ in range(num_particles):
            # Random direction
            angle_h = random.uniform(0, 2 * math.pi)
            angle_v = random.uniform(-math.pi/4, math.pi/4)
            speed = random.uniform(3, 8)

            vx = math.cos(angle_h) * math.cos(angle_v) * speed
            vy = math.sin(angle_v) * speed + random.uniform(2, 5)
            vz = math.sin(angle_h) * math.cos(angle_v) * speed

            # Color variation
            particle_color = [
                color[0] + random.uniform(-0.1, 0.1),
                color[1] + random.uniform(-0.1, 0.1),
                color[2]
            ]

            particle = Particle3D(x, y, z, vx, vy, vz, particle_color)
            self.particles.append(particle)

    def keyPressEvent(self, event):
        """Handle key press to continue"""
        if self.animation_complete:
            self.audio.play_ui_select()
            self.continue_pressed.emit()
        else:
            # Skip animation
            for letter in self.letters:
                letter.state = "landed"
                letter.x = letter.final_x
                letter.y = letter.final_y
                letter.z = letter.final_z
                letter.current_rotation_x = 0
                letter.current_rotation_y = 0
                letter.current_rotation_z = 0
            self.animation_complete = True
            self.audio.play_ui_select()
