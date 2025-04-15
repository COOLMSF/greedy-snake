"""
Fancy Snake Game - Sound Manager with Error Handling

This file implements sound effects and background music for our fancy Snake game.
"""

import pygame
import os
import random
import sys

class SoundManager:
    def __init__(self):
        # Initialize variables
        self.sounds = {}
        self.sound_volume = 0.7
        self.music_volume = 0.5
        self.audio_enabled = True
        
        # Create directories for sounds if they don't exist
        os.makedirs('sounds', exist_ok=True)
        
        # Sound effect file paths
        self.sound_files = {
            'eat': 'sounds/eat.wav',
            'game_over': 'sounds/game_over.wav',
            'menu_select': 'sounds/menu_select.wav',
            'menu_navigate': 'sounds/menu_navigate.wav',
            'power_up': 'sounds/power_up.wav',
            'level_up': 'sounds/level_up.wav',
            'move': 'sounds/move.wav'
        }
        
        # Music file paths
        self.music_files = {
            'menu': 'sounds/menu_music.wav',
            'gameplay': 'sounds/gameplay_music.wav',
            'game_over': 'sounds/game_over_music.wav'
        }
        
        # Try to initialize pygame mixer
        try:
            pygame.mixer.init()
            print("Audio system initialized successfully")
        except pygame.error as e:
            print(f"Warning: Audio system could not be initialized: {e}")
            print("Game will run without sound")
            self.audio_enabled = False
        
        # Create sound files and load sounds only if audio is enabled
        if self.audio_enabled:
            self.create_sound_files()
            self.load_sounds()
    
    def create_sound_files(self):
        """Create sound files using pygame's built-in synth capabilities"""
        try:
            self.create_eat_sound()
            self.create_game_over_sound()
            self.create_menu_sounds()
            self.create_power_up_sound()
            self.create_level_up_sound()
            self.create_move_sound()
            self.create_music_files()
        except Exception as e:
            print(f"Warning: Could not create sound files: {e}")
            self.audio_enabled = False
    
    def create_eat_sound(self):
        """Create a sound for eating food"""
        sound_array = pygame.sndarray.array([0] * 11025)  # 0.25 seconds at 44.1kHz
        
        # Create a short rising tone
        for i in range(11025):
            t = i / 44100
            freq = 300 + 1200 * t  # Rising frequency
            amplitude = 32767 * 0.7 * (1 - t/0.25)  # Decreasing amplitude
            sound_array[i] = int(amplitude * pygame.math.sin(2 * 3.14159 * freq * t))
        
        sound = pygame.sndarray.make_sound(sound_array)
        pygame.mixer.Sound.save(sound, self.sound_files['eat'])
    
    def create_game_over_sound(self):
        """Create a sound for game over"""
        sound_array = pygame.sndarray.array([0] * 44100)  # 1 second at 44.1kHz
        
        # Create a descending tone with vibrato
        for i in range(44100):
            t = i / 44100
            freq = 400 - 200 * t  # Descending frequency
            vibrato = 20 * pygame.math.sin(2 * 3.14159 * 10 * t)  # Vibrato
            amplitude = 32767 * 0.8 * (1 - t/1.2)  # Decreasing amplitude
            sound_array[i] = int(amplitude * pygame.math.sin(2 * 3.14159 * (freq + vibrato) * t))
        
        sound = pygame.sndarray.make_sound(sound_array)
        pygame.mixer.Sound.save(sound, self.sound_files['game_over'])
    
    def create_menu_sounds(self):
        """Create sounds for menu navigation and selection"""
        # Menu navigate sound (short blip)
        nav_array = pygame.sndarray.array([0] * 4410)  # 0.1 seconds
        for i in range(4410):
            t = i / 44100
            freq = 500
            amplitude = 32767 * 0.5 * (1 - t/0.1)
            nav_array[i] = int(amplitude * pygame.math.sin(2 * 3.14159 * freq * t))
        
        nav_sound = pygame.sndarray.make_sound(nav_array)
        pygame.mixer.Sound.save(nav_sound, self.sound_files['menu_navigate'])
        
        # Menu select sound (two-tone blip)
        select_array = pygame.sndarray.array([0] * 8820)  # 0.2 seconds
        for i in range(8820):
            t = i / 44100
            freq = 400 if t < 0.1 else 600  # Change frequency halfway
            amplitude = 32767 * 0.6 * (1 - t/0.2)
            select_array[i] = int(amplitude * pygame.math.sin(2 * 3.14159 * freq * t))
        
        select_sound = pygame.sndarray.make_sound(select_array)
        pygame.mixer.Sound.save(select_sound, self.sound_files['menu_select'])
    
    def create_power_up_sound(self):
        """Create a sound for collecting power-ups"""
        sound_array = pygame.sndarray.array([0] * 22050)  # 0.5 seconds
        
        # Create a rising tone with harmonics
        for i in range(22050):
            t = i / 44100
            freq1 = 300 + 900 * t  # Rising frequency
            freq2 = 450 + 1350 * t  # Harmonic at 1.5x
            amplitude = 32767 * 0.7 * (1 - t/0.6)  # Decreasing amplitude
            
            # Mix the two frequencies
            val1 = pygame.math.sin(2 * 3.14159 * freq1 * t)
            val2 = 0.3 * pygame.math.sin(2 * 3.14159 * freq2 * t)
            sound_array[i] = int(amplitude * (val1 + val2))
        
        sound = pygame.sndarray.make_sound(sound_array)
        pygame.mixer.Sound.save(sound, self.sound_files['power_up'])
    
    def create_level_up_sound(self):
        """Create a sound for leveling up"""
        sound_array = pygame.sndarray.array([0] * 44100)  # 1 second
        
        # Create a series of rising tones
        for i in range(44100):
            t = i / 44100
            
            # Three rising tones in sequence
            if t < 0.33:
                freq = 300 + 300 * (t/0.33)
            elif t < 0.66:
                freq = 400 + 300 * ((t-0.33)/0.33)
            else:
                freq = 500 + 300 * ((t-0.66)/0.34)
            
            amplitude = 32767 * 0.8 * (1 - (t-0.5)*(t-0.5)/0.5)  # Bell curve amplitude
            sound_array[i] = int(amplitude * pygame.math.sin(2 * 3.14159 * freq * t))
        
        sound = pygame.sndarray.make_sound(sound_array)
        pygame.mixer.Sound.save(sound, self.sound_files['level_up'])
    
    def create_move_sound(self):
        """Create a subtle sound for snake movement"""
        sound_array = pygame.sndarray.array([0] * 2205)  # 0.05 seconds (very short)
        
        # Create a very short, subtle sound
        for i in range(2205):
            t = i / 44100
            freq = 100
            amplitude = 32767 * 0.2 * (1 - t/0.05)  # Low amplitude, quick fade
            sound_array[i] = int(amplitude * pygame.math.sin(2 * 3.14159 * freq * t))
        
        sound = pygame.sndarray.make_sound(sound_array)
        pygame.mixer.Sound.save(sound, self.sound_files['move'])
    
    def create_music_files(self):
        """
        Create placeholder music files
        
        Note: In a real game, you would use actual music files instead of
        these simple synthesized tones. These are just placeholders.
        """
        # For menu music, create a simple looping pattern
        menu_array = pygame.sndarray.array([0] * (44100 * 5))  # 5 seconds
        
        # Create a simple arpeggio pattern
        notes = [261.63, 329.63, 392.00, 523.25]  # C4, E4, G4, C5
        note_duration = 44100 // 4  # 0.25 seconds per note
        
        for i in range(len(menu_array)):
            t = i / 44100
            note_idx = (i // note_duration) % len(notes)
            freq = notes[note_idx]
            
            # Add some variation
            if (i // (note_duration * len(notes))) % 2 == 1:
                freq *= 0.8
            
            amplitude = 32767 * 0.3  # Low amplitude for background music
            menu_array[i] = int(amplitude * pygame.math.sin(2 * 3.14159 * freq * t))
        
        # Save as WAV since MP3 encoding is not available
        menu_music = pygame.sndarray.make_sound(menu_array)
        pygame.mixer.Sound.save(menu_music, 'sounds/menu_music.wav')
        self.music_files['menu'] = 'sounds/menu_music.wav'
        
        # For gameplay music, create a different pattern
        gameplay_array = pygame.sndarray.array([0] * (44100 * 5))  # 5 seconds
        
        # Create a simple bass line with higher notes
        bass_notes = [65.41, 73.42, 82.41, 98.00]  # C2, D2, E2, G2
        high_notes = [523.25, 587.33, 659.26, 783.99]  # C5, D5, E5, G5
        
        for i in range(len(gameplay_array)):
            t = i / 44100
            bass_idx = (i // (note_duration * 2)) % len(bass_notes)
            high_idx = (i // note_duration) % len(high_notes)
            
            bass_freq = bass_notes[bass_idx]
            high_freq = high_notes[high_idx] if (i // note_duration) % 8 >= 4 else 0
            
            bass_val = 0.4 * pygame.math.sin(2 * 3.14159 * bass_freq * t)
            high_val = 0.2 * pygame.math.sin(2 * 3.14159 * high_freq * t)
            
            amplitude = 32767 * 0.3
            gameplay_array[i] = int(amplitude * (bass_val + high_val))
        
        gameplay_music = pygame.sndarray.make_sound(gameplay_array)
        pygame.mixer.Sound.save(gameplay_music, 'sounds/gameplay_music.wav')
        self.music_files['gameplay'] = 'sounds/gameplay_music.wav'
        
        # For game over music, create a sad pattern
        gameover_array = pygame.sndarray.array([0] * (44100 * 3))  # 3 seconds
        
        # Create a descending pattern
        notes = [392.00, 349.23, 329.63, 261.63]  # G4, F4, E4, C4
        
        for i in range(len(gameover_array)):
            t = i / 44100
            section = i // (44100 // 2)  # 0.5 seconds per note
            if section < len(notes):
                freq = notes[section]
                amplitude = 32767 * 0.3 * (1 - t/3)  # Fade out
                gameover_array[i] = int(amplitude * pygame.math.sin(2 * 3.14159 * freq * t))
        
        gameover_music = pygame.sndarray.make_sound(gameover_array)
        pygame.mixer.Sound.save(gameover_music, 'sounds/game_over_music.wav')
        self.music_files['game_over'] = 'sounds/game_over_music.wav'
    
    def load_sounds(self):
        """Load all sound effects"""
        for name, file_path in self.sound_files.items():
            try:
                self.sounds[name] = pygame.mixer.Sound(file_path)
                self.sounds[name].set_volume(self.sound_volume)
            except pygame.error as e:
                print(f"Warning: Could not load sound {file_path}: {e}")
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if not self.audio_enabled:
            return
            
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Warning: Could not play sound {sound_name}: {e}")
    
    def play_music(self, music_name):
        """Play background music"""
        if not self.audio_enabled:
            return
            
        if music_name in self.music_files:
            try:
                pygame.mixer.music.load(self.music_files[music_name])
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)  # Loop indefinitely
            except Exception as e:
                print(f"Warning: Could not play music {self.music_files[music_name]}: {e}")
    
    def stop_music(self):
        """Stop the currently playing music"""
        if not self.audio_enabled:
            return
            
        try:
            pygame.mixer.music.stop()
        except Exception as e:
            print(f"Warning: Could not stop music: {e}")
    
    def set_sound_volume(self, volume):
        """Set volume for sound effects (0.0 to 1.0)"""
        if not self.audio_enabled:
            return
            
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)
    
    def set_music_volume(self, volume):
        """Set volume for background music (0.0 to 1.0)"""
        if not self.audio_enabled:
            return
            
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)


# Test function
def test_sound_manager():
    pygame.init()
    sound_manager = SoundManager()
    
    if not sound_manager.audio_enabled:
        print("Audio is disabled, skipping sound tests")
        return
    
    # Play each sound
    for sound_name in sound_manager.sounds:
        print(f"Playing {sound_name} sound...")
        sound_manager.play_sound(sound_name)
        pygame.time.wait(1000)  # Wait 1 second between sounds
    
    # Play music
    print("Playing menu music...")
    sound_manager.play_music('menu')
    pygame.time.wait(5000)  # Wait 5 seconds
    
    print("Playing gameplay music...")
    sound_manager.play_music('gameplay')
    pygame.time.wait(5000)  # Wait 5 seconds
    
    print("Playing game over music...")
    sound_manager.play_music('game_over')
    pygame.time.wait(3000)  # Wait 3 seconds
    
    sound_manager.stop_music()

if __name__ == "__main__":
    test_sound_manager()
