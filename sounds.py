"""Optional sound effects.

Sounds are synthesized at runtime so no audio files are required. If the audio
device or numpy is unavailable everything degrades gracefully to silence, so the
game always runs.
"""

import pygame

try:
    import numpy as np
    _HAS_NUMPY = True
except ImportError:  # numpy is optional
    _HAS_NUMPY = False


class SoundManager:
    def __init__(self):
        self.enabled = False
        self.sounds = {}
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2)
            self.enabled = True
        except pygame.error:
            self.enabled = False
            return

        if _HAS_NUMPY:
            # (frequency Hz, duration seconds) for each effect.
            self._make("move", 220, 0.05)
            self._make("rotate", 330, 0.06)
            self._make("drop", 160, 0.09)
            self._make("clear", 520, 0.18)
            self._make("level", 660, 0.25)
            self._make("gameover", 110, 0.5)

    def _make(self, name, freq, duration):
        """Build a short fading square-ish tone as a pygame Sound."""
        sample_rate = 44100
        n = int(sample_rate * duration)
        t = np.linspace(0, duration, n, False)
        # Soft square wave with a linear fade-out to avoid clicks.
        wave = np.sign(np.sin(2 * np.pi * freq * t)) * 0.25
        fade = np.linspace(1.0, 0.0, n)
        wave = (wave * fade * 32767).astype(np.int16)
        stereo = np.column_stack((wave, wave))
        self.sounds[name] = pygame.sndarray.make_sound(np.ascontiguousarray(stereo))

    def play(self, name):
        if self.enabled and name in self.sounds:
            self.sounds[name].play()
