"""
Audio system for Dungeon Delver
Handles all sound effects and background music with procedural sound generation
"""
import pygame
import numpy as np
import random
import io
from typing import Dict, Optional


class SoundSynthesizer:
    """Generate procedural retro-style game sounds"""

    SAMPLE_RATE = 22050  # Hz

    @staticmethod
    def generate_sine_wave(frequency: float, duration: float, volume: float = 0.5) -> np.ndarray:
        """Generate a sine wave"""
        samples = int(SoundSynthesizer.SAMPLE_RATE * duration)
        t = np.linspace(0, duration, samples, False)
        wave = np.sin(2 * np.pi * frequency * t)

        # Apply envelope (fade in/out)
        envelope = np.ones(samples)
        fade_samples = min(int(samples * 0.1), 1000)
        envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)

        wave = wave * envelope * volume
        return wave

    @staticmethod
    def generate_noise(duration: float, volume: float = 0.3) -> np.ndarray:
        """Generate white noise"""
        samples = int(SoundSynthesizer.SAMPLE_RATE * duration)
        noise = np.random.uniform(-1, 1, samples) * volume

        # Apply envelope
        envelope = np.ones(samples)
        fade_samples = int(samples * 0.5)
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)

        return noise * envelope

    @staticmethod
    def generate_sweep(start_freq: float, end_freq: float, duration: float, volume: float = 0.5) -> np.ndarray:
        """Generate frequency sweep"""
        samples = int(SoundSynthesizer.SAMPLE_RATE * duration)
        t = np.linspace(0, duration, samples, False)

        # Exponential sweep
        freq = start_freq * (end_freq / start_freq) ** (t / duration)
        phase = 2 * np.pi * freq * t
        wave = np.sin(phase) * volume

        # Apply envelope
        envelope = np.ones(samples)
        fade_samples = int(samples * 0.3)
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)

        return wave * envelope

    @staticmethod
    def generate_square_wave(frequency: float, duration: float, volume: float = 0.3) -> np.ndarray:
        """Generate square wave (retro game sound)"""
        samples = int(SoundSynthesizer.SAMPLE_RATE * duration)
        t = np.linspace(0, duration, samples, False)
        wave = np.sign(np.sin(2 * np.pi * frequency * t)) * volume

        # Apply envelope
        envelope = np.ones(samples)
        fade_samples = int(samples * 0.2)
        envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)

        return wave * envelope

    @staticmethod
    def combine_waves(*waves: np.ndarray) -> np.ndarray:
        """Combine multiple waveforms, padding to the longest duration"""
        if not waves:
            return np.array([])

        # Find the longest wave
        max_length = max(len(wave) for wave in waves)

        # Pad all waves to the same length and combine
        padded_waves = []
        for wave in waves:
            if len(wave) < max_length:
                padding = np.zeros(max_length - len(wave))
                wave = np.concatenate([wave, padding])
            padded_waves.append(wave)

        # Sum all waves
        return np.sum(padded_waves, axis=0)

    @staticmethod
    def array_to_sound(wave: np.ndarray) -> pygame.mixer.Sound:
        """Convert numpy array to pygame Sound object"""
        # Normalize to 16-bit range
        wave = np.int16(wave * 32767)

        # Create stereo sound
        stereo = np.repeat(wave.reshape(-1, 1), 2, axis=1)

        # Convert to bytes
        sound_data = stereo.tobytes()

        # Create Sound from bytes
        sound = pygame.mixer.Sound(buffer=sound_data)
        return sound


class AudioManager:
    """Manages all game audio - sound effects and music"""

    def __init__(self):
        """Initialize audio system"""
        pygame.mixer.pre_init(22050, -16, 2, 512)
        pygame.mixer.init()

        # Audio state
        self.enabled = True
        self.sfx_volume = 0.7
        self.music_volume = 0.4

        # Sound cache
        self.sounds: Dict[str, pygame.mixer.Sound] = {}

        # Music state
        self.current_music_intensity = 0.0  # 0.0 = calm, 1.0 = combat
        self.music_ducking = 1.0  # Multiplier for music volume
        self.music_track = None

        # Combat state for adaptive audio
        self.enemies_nearby = 0
        self.in_combat = False

        # Generate all sounds
        self._generate_sounds()

    def _generate_sounds(self):
        """Generate all procedural game sounds"""
        synth = SoundSynthesizer()

        # === COMBAT SOUNDS ===

        # Light attack - quick swish
        light_attack = synth.generate_sweep(400, 200, 0.1, 0.4)
        self.sounds['attack_light'] = synth.array_to_sound(light_attack)

        # Medium attack - deeper swish
        medium_attack = synth.generate_sweep(300, 150, 0.15, 0.5)
        self.sounds['attack_medium'] = synth.array_to_sound(medium_attack)

        # Heavy attack - powerful swish
        heavy_attack = synth.generate_sweep(250, 100, 0.2, 0.6)
        self.sounds['attack_heavy'] = synth.array_to_sound(heavy_attack)

        # Hit impact - thud
        hit = synth.combine_waves(
            synth.generate_noise(0.1, 0.4),
            synth.generate_sine_wave(80, 0.1, 0.3)
        )
        self.sounds['hit'] = synth.array_to_sound(hit)

        # Critical hit - special impact
        crit = synth.combine_waves(
            synth.generate_noise(0.15, 0.5),
            synth.generate_sine_wave(120, 0.15, 0.4),
            synth.generate_sine_wave(240, 0.15, 0.2)
        )
        self.sounds['crit'] = synth.array_to_sound(crit)

        # === ENEMY SOUNDS ===

        # Goblin death - high pitched squeal
        goblin_death = synth.generate_sweep(800, 400, 0.3, 0.5)
        self.sounds['enemy_death_goblin'] = synth.array_to_sound(goblin_death)

        # Skeleton death - bone rattle
        skeleton_death = synth.generate_noise(0.25, 0.4)
        self.sounds['enemy_death_skeleton'] = synth.array_to_sound(skeleton_death)

        # Dragon death - epic roar
        dragon_death = synth.combine_waves(
            synth.generate_sweep(200, 50, 0.5, 0.6),
            synth.generate_noise(0.5, 0.3)
        )
        self.sounds['enemy_death_dragon'] = synth.array_to_sound(dragon_death)

        # === ABILITY SOUNDS ===

        # Fireball - whoosh + explosion
        fireball = synth.combine_waves(
            synth.generate_sweep(600, 200, 0.3, 0.5),
            synth.generate_noise(0.15, 0.3)
        )
        self.sounds['ability_fireball'] = synth.array_to_sound(fireball)

        # Dash/Teleport - blink sound
        dash = synth.generate_sweep(1000, 2000, 0.15, 0.4)
        self.sounds['ability_dash'] = synth.array_to_sound(dash)

        # Healing - gentle chime
        heal = synth.combine_waves(
            synth.generate_sine_wave(523, 0.3, 0.3),  # C
            synth.generate_sine_wave(659, 0.3, 0.2),  # E
            synth.generate_sine_wave(784, 0.3, 0.2)   # G
        )
        self.sounds['ability_heal'] = synth.array_to_sound(heal)

        # Frost Nova - ice crystallization
        frost = synth.combine_waves(
            synth.generate_sine_wave(1200, 0.3, 0.3),
            synth.generate_sine_wave(1600, 0.3, 0.2)
        )
        self.sounds['ability_frost'] = synth.array_to_sound(frost)

        # Whirlwind - spinning blade
        whirlwind = synth.generate_sweep(300, 600, 0.4, 0.5)
        self.sounds['ability_whirlwind'] = synth.array_to_sound(whirlwind)

        # Shadow Step - dark energy
        shadow = synth.generate_sweep(400, 100, 0.25, 0.5)
        self.sounds['ability_shadow'] = synth.array_to_sound(shadow)

        # === MOVEMENT & INTERACTION ===

        # Footstep - soft thud
        footstep = synth.combine_waves(
            synth.generate_noise(0.05, 0.15),
            synth.generate_sine_wave(60, 0.05, 0.1)
        )
        self.sounds['footstep'] = synth.array_to_sound(footstep)

        # Item pickup - ascending notes
        pickup = synth.combine_waves(
            synth.generate_sine_wave(440, 0.1, 0.2),
            synth.generate_sine_wave(554, 0.1, 0.15)
        )
        self.sounds['item_pickup'] = synth.array_to_sound(pickup)

        # Rare item pickup - special sparkle
        pickup_rare = synth.combine_waves(
            synth.generate_sine_wave(659, 0.15, 0.25),
            synth.generate_sine_wave(784, 0.15, 0.2),
            synth.generate_sine_wave(988, 0.15, 0.15)
        )
        self.sounds['item_pickup_rare'] = synth.array_to_sound(pickup_rare)

        # Potion drink - gulp
        potion = synth.generate_sweep(300, 200, 0.2, 0.3)
        self.sounds['potion_drink'] = synth.array_to_sound(potion)

        # Equip item - clank
        equip = synth.combine_waves(
            synth.generate_noise(0.1, 0.3),
            synth.generate_sine_wave(150, 0.1, 0.3)
        )
        self.sounds['equip'] = synth.array_to_sound(equip)

        # Stairs descend - descending tones
        stairs = synth.generate_sweep(500, 250, 0.4, 0.4)
        self.sounds['stairs'] = synth.array_to_sound(stairs)

        # === UI SOUNDS ===

        # Level up - fanfare
        levelup = synth.combine_waves(
            synth.generate_sine_wave(523, 0.5, 0.3),   # C
            synth.generate_sine_wave(659, 0.5, 0.25),  # E
            synth.generate_sine_wave(784, 0.5, 0.3),   # G
            synth.generate_sine_wave(1047, 0.5, 0.25)  # C (octave)
        )
        self.sounds['levelup'] = synth.array_to_sound(levelup)

        # Game over - dramatic descending tones
        gameover = synth.generate_sweep(400, 100, 0.8, 0.6)
        self.sounds['gameover'] = synth.array_to_sound(gameover)

        # Menu select - click
        select = synth.generate_sine_wave(800, 0.05, 0.3)
        self.sounds['ui_select'] = synth.array_to_sound(select)

        print(f"✓ Generated {len(self.sounds)} procedural sound effects")

    def _generate_ambient_music(self):
        """Generate ambient background music loop"""
        synth = SoundSynthesizer()
        duration = 10.0  # 10 second loop

        # Layered ambient tones
        bass = synth.generate_sine_wave(110, duration, 0.15)  # A
        drone1 = synth.generate_sine_wave(220, duration, 0.1)  # A (octave)
        drone2 = synth.generate_sine_wave(165, duration, 0.08)  # E

        # Combine layers
        music = synth.combine_waves(bass, drone1, drone2)

        return synth.array_to_sound(music)

    def play_sound(self, sound_name: str, volume: float = 1.0, pitch_variation: float = 0.1,
                   position: tuple = None, player_position: tuple = None):
        """
        Play a sound effect with optional pitch variation and positional audio

        Args:
            sound_name: Name of the sound to play
            volume: Volume multiplier (0.0 to 1.0)
            pitch_variation: Random pitch variation amount (0.0 to 1.0)
            position: World position of sound source (x, y)
            player_position: Player position for positional audio (x, y)
        """
        if not self.enabled or sound_name not in self.sounds:
            return

        sound = self.sounds[sound_name]

        # Calculate volume based on distance (positional audio)
        final_volume = volume * self.sfx_volume
        if position and player_position:
            distance = abs(position[0] - player_position[0]) + abs(position[1] - player_position[1])
            # Volume falls off with distance (max range 10 tiles)
            distance_factor = max(0, 1.0 - (distance / 10.0))
            final_volume *= distance_factor

        # Set volume
        sound.set_volume(final_volume)

        # Play with pitch variation if supported
        channel = sound.play()

        if channel and pitch_variation > 0:
            # Simulate pitch variation by playing at different volumes
            # (pygame doesn't support pitch shifting directly, but this adds variety)
            variation = random.uniform(1.0 - pitch_variation, 1.0 + pitch_variation)
            sound.set_volume(final_volume * variation)

    def play_attack_sound(self, attack_strength: str = 'medium'):
        """Play attack sound based on strength"""
        sound_map = {
            'light': 'attack_light',
            'medium': 'attack_medium',
            'heavy': 'attack_heavy'
        }
        sound_name = sound_map.get(attack_strength, 'attack_medium')
        self.play_sound(sound_name, pitch_variation=0.15)

    def play_hit_sound(self, is_crit: bool = False, position: tuple = None, player_position: tuple = None):
        """Play hit impact sound"""
        sound_name = 'crit' if is_crit else 'hit'
        volume = 1.2 if is_crit else 1.0
        self.play_sound(sound_name, volume=volume, pitch_variation=0.2,
                       position=position, player_position=player_position)

    def play_enemy_death(self, enemy_type: str, position: tuple = None, player_position: tuple = None):
        """Play enemy death sound"""
        sound_name = f'enemy_death_{enemy_type}'
        if sound_name in self.sounds:
            self.play_sound(sound_name, volume=0.9, pitch_variation=0.1,
                           position=position, player_position=player_position)

    def play_ability_sound(self, ability_name: str):
        """Play ability sound effect"""
        # Map ability names to sound keys
        sound_map = {
            'Fireball': 'ability_fireball',
            'Dash': 'ability_dash',
            'Healing Touch': 'ability_heal',
            'Frost Nova': 'ability_frost',
            'Whirlwind': 'ability_whirlwind',
            'Shadow Step': 'ability_shadow',
        }

        sound_name = sound_map.get(ability_name)
        if sound_name:
            self.play_sound(sound_name, volume=1.0, pitch_variation=0.05)

    def play_footstep(self, position: tuple = None, player_position: tuple = None):
        """Play footstep sound"""
        # Quiet footsteps with variation
        self.play_sound('footstep', volume=0.3, pitch_variation=0.25,
                       position=position, player_position=player_position)

    def play_item_pickup(self, rarity: str = 'common'):
        """Play item pickup sound based on rarity"""
        if rarity in ['rare', 'epic', 'legendary']:
            self.play_sound('item_pickup_rare', volume=0.9)
        else:
            self.play_sound('item_pickup', volume=0.7, pitch_variation=0.2)

    def play_potion(self):
        """Play potion drinking sound"""
        self.play_sound('potion_drink', volume=0.8)

    def play_equip(self):
        """Play equipment sound"""
        self.play_sound('equip', volume=0.6, pitch_variation=0.15)

    def play_stairs(self):
        """Play stairs descending sound"""
        self.play_sound('stairs', volume=0.8)

    def play_levelup(self):
        """Play level up fanfare"""
        self.play_sound('levelup', volume=1.0)

    def play_gameover(self):
        """Play game over sound"""
        self.play_sound('gameover', volume=0.9)

    def play_ui_select(self):
        """Play UI selection sound"""
        self.play_sound('ui_select', volume=0.5)

    def start_background_music(self):
        """Start playing background music"""
        if not self.enabled:
            return

        # Generate and play ambient music
        self.music_track = self._generate_ambient_music()
        self.music_track.set_volume(self.music_volume * self.music_ducking)
        self.music_track.play(loops=-1)  # Loop forever

    def update_music_intensity(self, enemies_nearby: int, in_combat: bool):
        """Update music based on game state"""
        self.enemies_nearby = enemies_nearby
        self.in_combat = in_combat

        # Calculate target intensity
        if in_combat:
            target_intensity = 1.0
        elif enemies_nearby > 0:
            target_intensity = 0.5 + (min(enemies_nearby, 5) / 10)
        else:
            target_intensity = 0.0

        # Smooth transition
        self.current_music_intensity += (target_intensity - self.current_music_intensity) * 0.1

        # Update ducking (lower music during combat)
        target_ducking = 0.4 if in_combat else 1.0
        self.music_ducking += (target_ducking - self.music_ducking) * 0.05

        # Apply to music
        if self.music_track:
            self.music_track.set_volume(self.music_volume * self.music_ducking)

    def stop_music(self):
        """Stop background music"""
        if self.music_track:
            self.music_track.stop()

    def set_enabled(self, enabled: bool):
        """Enable/disable all audio"""
        self.enabled = enabled
        if not enabled:
            self.stop_music()
            pygame.mixer.stop()

    def set_sfx_volume(self, volume: float):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))

    def set_music_volume(self, volume: float):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.music_track:
            self.music_track.set_volume(self.music_volume * self.music_ducking)


# Global audio manager instance
_audio_manager: Optional[AudioManager] = None


def get_audio_manager() -> AudioManager:
    """Get or create global audio manager instance"""
    global _audio_manager
    if _audio_manager is None:
        try:
            _audio_manager = AudioManager()
        except Exception as e:
            print(f"Warning: Failed to initialize audio: {e}")
            # Create a dummy audio manager that does nothing
            class DummyAudioManager:
                def __getattr__(self, name):
                    return lambda *args, **kwargs: None
            _audio_manager = DummyAudioManager()
    return _audio_manager
