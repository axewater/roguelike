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

        # Face textures for cube sides (created in initializeGL)
        self.brick_side_texture = None
        self.brick_back_texture = None
        self.stone_top_texture = None
        self.stone_bottom_texture = None

        # Letters will be initialized in initializeGL (after OpenGL context is ready)

        # Timer for animation updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # ~60 FPS

        # Audio
        self.audio = get_audio_manager()

    def _draw_brick_pattern(self, painter: QPainter, width: int, height: int):
        """Draw brick pattern with mortar lines"""
        # Brick colors (varied gray-brown tones)
        brick_base = QColor(65, 60, 55)
        mortar = QColor(95, 90, 85)

        # Fill with mortar color first
        painter.fillRect(0, 0, width, height, mortar)

        # Draw bricks in rows
        brick_height = height // 4
        brick_width = width // 3
        mortar_size = 3

        for row in range(4):
            y = row * brick_height
            # Stagger every other row
            offset = (brick_width // 2) if row % 2 == 1 else 0

            for col in range(-1, 4):  # Extra columns for offset
                x = col * brick_width + offset

                # Vary brick color slightly
                variation = random.randint(-8, 8)
                brick_color = QColor(
                    brick_base.red() + variation,
                    brick_base.green() + variation,
                    brick_base.blue() + variation
                )

                # Draw brick (leaving mortar gaps)
                brick_rect = (
                    x + mortar_size,
                    y + mortar_size,
                    brick_width - mortar_size * 2,
                    brick_height - mortar_size * 2
                )
                painter.fillRect(*brick_rect, brick_color)

                # Add some texture/cracks to brick
                painter.setPen(QColor(brick_base.red() - 15, brick_base.green() - 15, brick_base.blue() - 15))
                for _ in range(2):
                    crack_x = x + random.randint(mortar_size, brick_width - mortar_size)
                    crack_y = y + random.randint(mortar_size, brick_height - mortar_size)
                    crack_len = random.randint(5, 15)
                    painter.drawLine(crack_x, crack_y, crack_x + crack_len, crack_y + random.randint(-3, 3))

    def _add_weathering(self, painter: QPainter, width: int, height: int):
        """Add weathering effects (age marks, stains)"""
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Multiply)

        # Random dark spots and stains
        for _ in range(15):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(8, 25)
            opacity = random.randint(30, 80)

            stain_color = QColor(50, 45, 40, opacity)
            painter.setBrush(stain_color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(x - size // 2, y - size // 2, size, size)

        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)

    def _generate_moss_overlay(self, image: QImage):
        """Add moss/grass growth to existing texture"""
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Moss colors (varied dark greens)
        moss_colors = [
            QColor(40, 80, 35),
            QColor(35, 75, 30),
            QColor(45, 85, 40),
            QColor(30, 70, 25),
        ]

        # Draw irregular moss patches
        num_patches = random.randint(20, 35)
        for _ in range(num_patches):
            x = random.randint(-10, image.width() + 10)
            y = random.randint(0, image.height() // 3)  # Concentrate on top third
            size = random.randint(10, 40)
            opacity = random.randint(100, 200)

            moss = random.choice(moss_colors)
            moss.setAlpha(opacity)
            painter.setBrush(moss)
            painter.setPen(Qt.PenStyle.NoPen)

            # Draw irregular shape
            painter.drawEllipse(x - size // 2, y - size // 2, size, int(size * random.uniform(0.6, 1.4)))

        painter.end()

    def _generate_stone_texture(self, size: int, darkness: float = 1.0) -> QImage:
        """Generate procedural stone/brick texture"""
        image = QImage(size, size, QImage.Format.Format_RGBA8888)
        image.fill(QColor(95, 90, 85))  # Base mortar color

        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw brick pattern
        self._draw_brick_pattern(painter, size, size)

        # Add weathering
        self._add_weathering(painter, size, size)

        # Apply darkness multiplier
        if darkness != 1.0:
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Multiply)
            dark_overlay = QColor(int(255 * darkness), int(255 * darkness), int(255 * darkness))
            painter.fillRect(0, 0, size, size, dark_overlay)

        painter.end()
        return image

    def _generate_letter_textures(self):
        """Generate OpenGL textures for each unique letter with carved stone effect"""
        text = "CLAUDE-LIKE"
        unique_chars = set(text.replace(' ', '').replace('-', ''))

        for char in unique_chars:
            size = 256  # Texture size (power of 2)

            # Generate stone background
            image = self._generate_stone_texture(size, darkness=1.0)

            # Now carve the letter into the stone
            painter = QPainter(image)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

            # Set font
            font = QFont("Arial", 180, QFont.Weight.Bold)
            painter.setFont(font)

            # Create carved effect with 3 layers:
            # 1. Shadow (carved depth) - dark, offset down+right
            painter.setPen(QColor(15, 15, 20, 255))
            painter.drawText(image.rect().adjusted(3, 3, 3, 3), Qt.AlignmentFlag.AlignCenter, char)

            # 2. Highlight (carved edge) - light, offset up+left
            painter.setPen(QColor(100, 95, 90, 180))
            painter.drawText(image.rect().adjusted(-2, -2, -2, -2), Qt.AlignmentFlag.AlignCenter, char)

            # 3. Main letter (carved surface) - medium stone color
            painter.setPen(QColor(50, 48, 45, 255))
            painter.drawText(image.rect(), Qt.AlignmentFlag.AlignCenter, char)

            # Add subtle moss around letter edges
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Multiply)
            moss_color = QColor(40, 80, 35, 40)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(moss_color)
            # Small moss spots near letter
            for _ in range(5):
                mx = random.randint(size // 4, 3 * size // 4)
                my = random.randint(size // 4, 3 * size // 4)
                ms = random.randint(8, 20)
                painter.drawEllipse(mx - ms // 2, my - ms // 2, ms, ms)

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

        print(f"✓ Generated {len(self.letter_textures)} carved stone letter textures")

    def _generate_face_textures(self):
        """Generate textures for different cube faces"""
        size = 256

        # 1. Brick texture for side faces (normal brightness)
        side_image = self._generate_stone_texture(size, darkness=1.0)
        side_image = side_image.mirrored(False, True)
        self.brick_side_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.brick_side_texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        img_data = side_image.constBits().asstring(size * size * 4)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, size, size, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        # 2. Darker brick texture for back face
        back_image = self._generate_stone_texture(size, darkness=0.7)
        back_image = back_image.mirrored(False, True)
        self.brick_back_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.brick_back_texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        img_data = back_image.constBits().asstring(size * size * 4)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, size, size, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        # 3. Stone texture with heavy moss for top face
        top_image = self._generate_stone_texture(size, darkness=1.0)
        self._generate_moss_overlay(top_image)  # Add heavy moss growth
        top_image = top_image.mirrored(False, True)
        self.stone_top_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.stone_top_texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        img_data = top_image.constBits().asstring(size * size * 4)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, size, size, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        # 4. Darker stone for bottom face (less light)
        bottom_image = self._generate_stone_texture(size, darkness=0.6)
        bottom_image = bottom_image.mirrored(False, True)
        self.stone_bottom_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.stone_bottom_texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        img_data = bottom_image.constBits().asstring(size * size * 4)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, size, size, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        print("✓ Generated face textures (sides, top, bottom, back)")

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

        # Generate letter textures and face textures
        self._generate_letter_textures()
        self._generate_face_textures()
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
        """Draw a 3D character as textured dungeon stone block"""
        glEnable(GL_TEXTURE_2D)
        glColor4f(1.0, 1.0, 1.0, 1.0)  # White to show textures as-is

        # Front face - Carved letter texture
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glBegin(GL_QUADS)
        glNormal3f(0, 0, 1)
        glTexCoord2f(0, 0); glVertex3f(-0.4, -0.5, 0.2)
        glTexCoord2f(1, 0); glVertex3f(0.4, -0.5, 0.2)
        glTexCoord2f(1, 1); glVertex3f(0.4, 0.5, 0.2)
        glTexCoord2f(0, 1); glVertex3f(-0.4, 0.5, 0.2)
        glEnd()

        # Back face - Dark brick texture
        glBindTexture(GL_TEXTURE_2D, self.brick_back_texture)
        glBegin(GL_QUADS)
        glNormal3f(0, 0, -1)
        glTexCoord2f(0, 0); glVertex3f(-0.4, -0.5, -0.2)
        glTexCoord2f(1, 0); glVertex3f(0.4, -0.5, -0.2)
        glTexCoord2f(1, 1); glVertex3f(0.4, 0.5, -0.2)
        glTexCoord2f(0, 1); glVertex3f(-0.4, 0.5, -0.2)
        glEnd()

        # Top face - Mossy stone texture
        glBindTexture(GL_TEXTURE_2D, self.stone_top_texture)
        glBegin(GL_QUADS)
        glNormal3f(0, 1, 0)
        glTexCoord2f(0, 0); glVertex3f(-0.4, 0.5, -0.2)
        glTexCoord2f(1, 0); glVertex3f(0.4, 0.5, -0.2)
        glTexCoord2f(1, 1); glVertex3f(0.4, 0.5, 0.2)
        glTexCoord2f(0, 1); glVertex3f(-0.4, 0.5, 0.2)
        glEnd()

        # Bottom face - Dark stone texture
        glBindTexture(GL_TEXTURE_2D, self.stone_bottom_texture)
        glBegin(GL_QUADS)
        glNormal3f(0, -1, 0)
        glTexCoord2f(0, 0); glVertex3f(-0.4, -0.5, -0.2)
        glTexCoord2f(1, 0); glVertex3f(0.4, -0.5, -0.2)
        glTexCoord2f(1, 1); glVertex3f(0.4, -0.5, 0.2)
        glTexCoord2f(0, 1); glVertex3f(-0.4, -0.5, 0.2)
        glEnd()

        # Left face - Brick texture
        glBindTexture(GL_TEXTURE_2D, self.brick_side_texture)
        glBegin(GL_QUADS)
        glNormal3f(-1, 0, 0)
        glTexCoord2f(0, 0); glVertex3f(-0.4, -0.5, -0.2)
        glTexCoord2f(1, 0); glVertex3f(-0.4, -0.5, 0.2)
        glTexCoord2f(1, 1); glVertex3f(-0.4, 0.5, 0.2)
        glTexCoord2f(0, 1); glVertex3f(-0.4, 0.5, -0.2)
        glEnd()

        # Right face - Brick texture
        glBindTexture(GL_TEXTURE_2D, self.brick_side_texture)
        glBegin(GL_QUADS)
        glNormal3f(1, 0, 0)
        glTexCoord2f(0, 0); glVertex3f(0.4, -0.5, -0.2)
        glTexCoord2f(1, 0); glVertex3f(0.4, 0.5, -0.2)
        glTexCoord2f(1, 1); glVertex3f(0.4, 0.5, 0.2)
        glTexCoord2f(0, 1); glVertex3f(0.4, -0.5, 0.2)
        glEnd()

        glDisable(GL_TEXTURE_2D)

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

    def mousePressEvent(self, event):
        """Handle mouse press to continue"""
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
