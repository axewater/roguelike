"""
Animation and visual effects system for Dungeon Delver
"""
import random
from typing import List, Tuple
from PyQt6.QtGui import QColor
import constants as c


class FloatingText:
    """Floating damage/heal numbers that rise and fade"""
    def __init__(self, x: int, y: int, text: str, color: QColor, is_crit: bool = False):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.is_crit = is_crit

        # Animation properties
        self.offset_y = 0.0
        self.lifetime = 0.0
        self.max_lifetime = 1.0 if not is_crit else 1.2  # Crits last longer
        self.alpha = 255

        # Random drift
        self.drift_x = random.uniform(-0.3, 0.3)

    def update(self, dt: float) -> bool:
        """Update animation. Returns False when animation is complete"""
        self.lifetime += dt

        if self.lifetime >= self.max_lifetime:
            return False

        # Rise up
        self.offset_y -= 1.5 * dt

        # Fade out in last 30% of lifetime
        fade_start = self.max_lifetime * 0.7
        if self.lifetime > fade_start:
            fade_progress = (self.lifetime - fade_start) / (self.max_lifetime - fade_start)
            self.alpha = int(255 * (1.0 - fade_progress))

        return True


class FlashEffect:
    """Flash entity white/red when hit"""
    def __init__(self, x: int, y: int, color: QColor, duration: float = 0.15):
        self.x = x
        self.y = y
        self.color = color
        self.duration = duration
        self.lifetime = 0.0
        self.alpha = 200

    def update(self, dt: float) -> bool:
        """Update animation. Returns False when complete"""
        self.lifetime += dt

        if self.lifetime >= self.duration:
            return False

        # Fade out
        progress = self.lifetime / self.duration
        self.alpha = int(200 * (1.0 - progress))

        return True


class Particle:
    """Generic particle for blood, sparks, explosions, etc."""
    def __init__(self, x: float, y: float, vx: float, vy: float, color: QColor,
                 size: float = 3.0, lifetime: float = 0.5, particle_type: str = "square"):
        self.x = x
        self.y = y
        self.vx = vx  # Velocity X
        self.vy = vy  # Velocity Y
        self.color = color
        self.size = size
        self.max_lifetime = lifetime
        self.lifetime = 0.0
        self.alpha = 255
        self.particle_type = particle_type  # "square", "circle", "star"

    def update(self, dt: float) -> bool:
        """Update particle physics. Returns False when dead"""
        self.lifetime += dt

        if self.lifetime >= self.max_lifetime:
            return False

        # Apply velocity
        self.x += self.vx * dt * 30
        self.y += self.vy * dt * 30

        # Apply gravity (for blood splatter)
        self.vy += 0.5 * dt * 30

        # Fade out
        progress = self.lifetime / self.max_lifetime
        self.alpha = int(255 * (1.0 - progress))

        return True


class ScreenShake:
    """Screen shake effect"""
    def __init__(self, intensity: float = 5.0, duration: float = 0.2):
        self.intensity = intensity
        self.duration = duration
        self.lifetime = 0.0
        self.offset_x = 0
        self.offset_y = 0

    def update(self, dt: float) -> bool:
        """Update shake. Returns False when complete"""
        self.lifetime += dt

        if self.lifetime >= self.duration:
            self.offset_x = 0
            self.offset_y = 0
            return False

        # Diminishing shake
        progress = self.lifetime / self.duration
        current_intensity = self.intensity * (1.0 - progress)

        self.offset_x = random.randint(-int(current_intensity), int(current_intensity))
        self.offset_y = random.randint(-int(current_intensity), int(current_intensity))

        return True


class AnimationManager:
    """Manages all active animations and effects"""
    def __init__(self):
        self.floating_texts: List[FloatingText] = []
        self.flash_effects: List[FlashEffect] = []
        self.particles: List[Particle] = []
        self.screen_shake: ScreenShake = None
        self.last_update_time = 0.0

    def add_floating_text(self, x: int, y: int, text: str, color: QColor, is_crit: bool = False):
        """Add floating damage/heal text"""
        self.floating_texts.append(FloatingText(x, y, text, color, is_crit))

    def add_flash_effect(self, x: int, y: int, color: QColor = None):
        """Add hit flash effect"""
        if color is None:
            color = QColor(255, 255, 255)
        self.flash_effects.append(FlashEffect(x, y, color))

    def add_particle_burst(self, x: int, y: int, color: QColor, count: int = 8,
                          particle_type: str = "square"):
        """Create burst of particles"""
        center_x = x * c.TILE_SIZE + c.TILE_SIZE / 2
        center_y = y * c.TILE_SIZE + c.TILE_SIZE / 2

        for _ in range(count):
            # Random direction
            angle = random.uniform(0, 3.14159 * 2)
            speed = random.uniform(2, 6)
            vx = speed * (angle % 3.14159) / 3.14159
            vy = speed * (angle / 3.14159) - speed

            lifetime = random.uniform(0.3, 0.7)
            size = random.uniform(2, 5)

            self.particles.append(
                Particle(center_x, center_y, vx, vy, color, size, lifetime, particle_type)
            )

    def add_blood_splatter(self, x: int, y: int):
        """Create blood splatter effect"""
        blood_color = QColor(180, 0, 0)
        self.add_particle_burst(x, y, blood_color, count=12, particle_type="circle")

    def add_heal_sparkles(self, x: int, y: int):
        """Create healing sparkle effect"""
        heal_color = QColor(100, 255, 100)
        self.add_particle_burst(x, y, heal_color, count=8, particle_type="star")

    def add_screen_shake(self, intensity: float = 5.0, duration: float = 0.2):
        """Add screen shake effect"""
        self.screen_shake = ScreenShake(intensity, duration)

    def update(self, dt: float):
        """Update all animations"""
        # Update floating texts
        self.floating_texts = [ft for ft in self.floating_texts if ft.update(dt)]

        # Update flash effects
        self.flash_effects = [fe for fe in self.flash_effects if fe.update(dt)]

        # Update particles
        self.particles = [p for p in self.particles if p.update(dt)]

        # Update screen shake
        if self.screen_shake:
            if not self.screen_shake.update(dt):
                self.screen_shake = None

    def get_screen_offset(self) -> Tuple[int, int]:
        """Get current screen shake offset"""
        if self.screen_shake:
            return (self.screen_shake.offset_x, self.screen_shake.offset_y)
        return (0, 0)

    def clear_all(self):
        """Clear all active animations"""
        self.floating_texts.clear()
        self.flash_effects.clear()
        self.particles.clear()
        self.screen_shake = None
