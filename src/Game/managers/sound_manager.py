from pathlib import Path

# Get current path
cwd = Path.cwd()
mod_path = Path(__file__).parent.parent

# Background music paths
grassplain_boss_path = "assets/sounds/bgm/grassfield_boss.mp3"
grassplain_boss = (mod_path / grassplain_boss_path).resolve()
grassplain_path = "assets/sounds/bgm/grassfield_bgm.mp3"
grassplain = (mod_path / grassplain_path).resolve()
menu_path = "assets/sounds/bgm/menu_bgm.mp3"
menu = (mod_path / menu_path).resolve()

# Sound effect paths
sfx_dir = "assets/sounds/sfx"

# Define all sound effects
collect_item_path = f"{sfx_dir}/collect_item.mp3"
collect_item_sfx = (mod_path / collect_item_path).resolve()

enemy_hit_path = f"{sfx_dir}/enemy_got_hit.mp3"
enemy_hit_sfx = (mod_path / enemy_hit_path).resolve()

game_over_path = f"{sfx_dir}/game_over.mp3"
game_over_sfx = (mod_path / game_over_path).resolve()

level_up_path = f"{sfx_dir}/level_up.mp3"
level_up_sfx = (mod_path / level_up_path).resolve()

pause_game_path = f"{sfx_dir}/pause_game.mp3"
pause_game_sfx = (mod_path / pause_game_path).resolve()

player_hit_path = f"{sfx_dir}/player_got_hit.mp3"
player_hit_sfx = (mod_path / player_hit_path).resolve()

select_button_path = f"{sfx_dir}/select_button.mp3"
select_button_sfx = (mod_path / select_button_path).resolve()

male_shot_path = f"{sfx_dir}/male_shot.wav"
male_shot_sfx = (mod_path / male_shot_path).resolve()

female_shot_path = f"{sfx_dir}/female_shot.wav"
female_shot_sfx = (mod_path / female_shot_path).resolve()

class SoundManager:
    """Manages all game sounds and music"""
    _sfx_volume = 1.0  # Default SFX volume
    _music_volume = 1.0  # Default music volume
    _sounds = {}  # Dictionary to store sound objects for volume control
    
    @classmethod
    def set_music_volume(cls, volume):
        """Set music volume
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        import pygame
        cls._music_volume = max(0.0, min(1.0, volume))  # Clamp between 0.0 and 1.0
        pygame.mixer.music.set_volume(cls._music_volume)
    
    @classmethod
    def set_sfx_volume(cls, volume):
        """Set sound effects volume
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        cls._sfx_volume = max(0.0, min(1.0, volume))  # Clamp between 0.0 and 1.0
        # Update volume for all currently playing sounds
        for sound in cls._sounds.values():
            if sound is not None:
                sound.set_volume(cls._sfx_volume)
    
    @classmethod
    def get_music_volume(cls):
        """Get current music volume"""
        return cls._music_volume
    
    @classmethod
    def get_sfx_volume(cls):
        """Get current SFX volume"""
        return cls._sfx_volume
    
    @classmethod
    def play_music(cls, music_path, loops=-1, fade_ms=0):
        """Play background music
        
        Args:
            music_path: Path to the music file
            loops: Number of times to repeat (-1 for infinite)
            fade_ms: Fade-in time in milliseconds
        """
        import pygame
        try:
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.set_volume(cls._music_volume)
            pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
        except Exception as e:
            print(f"Error playing music: {e}")
            
    @classmethod
    def stop_music(cls, fade_ms=0):
        """Stop currently playing music
        
        Args:
            fade_ms: Fade-out time in milliseconds
        """
        import pygame
        pygame.mixer.music.fadeout(fade_ms)
        
    @classmethod
    def pause_music(cls):
        """Pause currently playing music"""
        import pygame
        pygame.mixer.music.pause()
        
    @classmethod
    def unpause_music(cls):
        """Resume paused music"""
        import pygame
        pygame.mixer.music.unpause()
    
    @classmethod
    def play_sound(cls, sound_path, volume=1.0, loops=0, sound_id=None):
        """Play a sound effect
        
        Args:
            sound_path: Path to the sound file or pygame Sound object
            volume: Volume level (0.0 to 1.0)
            loops: Number of times to repeat (0 for once)
            sound_id: Optional ID to track and control this sound later
            
        Returns:
            The sound object if successful, None otherwise
        """
        import pygame
        try:
            if isinstance(sound_path, pygame.mixer.Sound):
                sound = sound_path
            else:
                sound = pygame.mixer.Sound(str(sound_path))
                
            # Apply global SFX volume
            sound.set_volume(volume * cls._sfx_volume)
            sound.play(loops=loops)
            
            # Store the sound if an ID was provided
            if sound_id is not None:
                cls._sounds[sound_id] = sound
                
            return sound
        except Exception as e:
            print(f"Error playing sound: {e}")
            return None
            
    @classmethod
    def stop_sound(cls, sound_id):
        """Stop a specific sound by its ID
        
        Args:
            sound_id: The ID of the sound to stop
        """
        if sound_id in cls._sounds:
            sound = cls._sounds.pop(sound_id)
            if sound is not None:
                sound.stop()
    
    @classmethod
    def stop_all_sounds(cls):
        """Stop all currently playing sounds"""
        for sound_id in list(cls._sounds.keys()):
            cls.stop_sound(sound_id)
    
    # Convenience methods for common sound effects
    @classmethod
    def play_collect_item(cls):
        """Play collect item sound"""
        return cls.play_sound(collect_item_sfx, volume=0.5)
    
    @classmethod
    def play_enemy_hit(cls):
        """Play enemy hit sound"""
        return cls.play_sound(enemy_hit_sfx, volume=0.4)
    
    @classmethod
    def play_game_over(cls):
        """Play game over sound"""
        return cls.play_sound(game_over_sfx, volume=0.6)
    
    @classmethod
    def play_level_up(cls):
        """Play level up sound"""
        return cls.play_sound(level_up_sfx, volume=0.5)
    
    @classmethod
    def play_pause_game(cls):
        """Play pause game sound"""
        return cls.play_sound(pause_game_sfx, volume=0.4)
    
    @classmethod
    def play_player_hit(cls):
        """Play player hit sound"""
        return cls.play_sound(player_hit_sfx, volume=0.5)
    
    @classmethod
    def play_male_shot(cls):
        """Play male character shooting sound effect"""
        return cls.play_sound(male_shot_sfx)
        
    @classmethod
    def play_female_shot(cls):
        """Play female character shooting sound effect"""
        return cls.play_sound(female_shot_sfx)
        
    @classmethod
    def play_button_select(cls):
        """Play button select sound effect"""
        return cls.play_sound(select_button_sfx, volume=0.4)
