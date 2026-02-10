"""
SWYFT - Music and Sound Manager
Handles background music and sound effects
"""
import pygame
import os
import random

class MusicManager:
    """Manages background music and sound effects"""
    
    def __init__(self):
        """Initialize the music manager"""
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Music settings
        self.music_enabled = True
        self.music_volume = 0.3  # 30% volume for background music
        self.sfx_volume = 0.5    # 50% volume for sound effects
        
        # Music folder path
        self.music_folder = "music"
        
        # Create music folder if it doesn't exist
        if not os.path.exists(self.music_folder):
            os.makedirs(self.music_folder)
        
        # Available music tracks
        self.menu_music = []
        self.gameplay_music = []
        
        # Current music state
        self.current_track = None
        self.current_type = None  # "menu" or "gameplay"
        
        # Load available music
        self.load_music_files()
        
        # Generate simple tones if no music files found
        if not self.menu_music and not self.gameplay_music:
            self.create_placeholder_info()
    
    def load_music_files(self):
        """Load music files from the music folder"""
        if not os.path.exists(self.music_folder):
            return
        
        # Look for music files
        music_extensions = ['.mp3', '.ogg', '.wav']
        
        for filename in os.listdir(self.music_folder):
            file_path = os.path.join(self.music_folder, filename)
            ext = os.path.splitext(filename)[1].lower()
            
            if ext in music_extensions:
                # Categorize by filename
                if 'menu' in filename.lower():
                    self.menu_music.append(file_path)
                elif 'game' in filename.lower() or 'play' in filename.lower():
                    self.gameplay_music.append(file_path)
                else:
                    # Default to gameplay music
                    self.gameplay_music.append(file_path)
    
    def create_placeholder_info(self):
        """Create info file about adding music"""
        info_path = os.path.join(self.music_folder, "HOW_TO_ADD_MUSIC.txt")
        
        if not os.path.exists(info_path):
            with open(info_path, 'w', encoding='utf-8') as f:
                f.write("SWYFT - How to Add Custom Music\n")
                f.write("=" * 50 + "\n\n")
                f.write("To add your own music to the game:\n\n")
                f.write("1. Place your music files in this 'music' folder\n")
                f.write("2. Supported formats: .mp3, .ogg, .wav\n")
                f.write("3. Name your files:\n")
                f.write("   - For MENU music: Include 'menu' in the filename\n")
                f.write("     Example: menu_theme.mp3, background_menu.ogg\n")
                f.write("   - For GAMEPLAY music: Include 'game' or 'play' in the filename\n")
                f.write("     Example: gameplay1.mp3, game_music.ogg, play_theme.wav\n\n")
                f.write("4. Restart the game to load your music!\n\n")
                f.write("Notes:\n")
                f.write("- The game will randomly select from available tracks\n")
                f.write("- Music loops automatically\n")
                f.write("- You can have multiple tracks for variety\n")
                f.write("- If no music files are found, the game runs silently\n\n")
                f.write("Recommended free music sources:\n")
                f.write("- incompetech.com (Kevin MacLeod)\n")
                f.write("- freemusicarchive.org\n")
                f.write("- bensound.com\n")
                f.write("- youtube.com/audiolibrary\n\n")
                f.write("Enjoy your game with music!\n")
    
    def play_menu_music(self):
        """Start playing menu music"""
        if not self.music_enabled:
            return
        
        if self.current_type == "menu" and pygame.mixer.music.get_busy():
            return  # Already playing menu music
        
        if self.menu_music:
            track = random.choice(self.menu_music)
            try:
                pygame.mixer.music.load(track)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                self.current_track = track
                self.current_type = "menu"
            except:
                pass  # Silently fail if music can't load
    
    def play_gameplay_music(self):
        """Start playing gameplay music"""
        if not self.music_enabled:
            return
        
        if self.current_type == "gameplay" and pygame.mixer.music.get_busy():
            return  # Already playing gameplay music
        
        if self.gameplay_music:
            track = random.choice(self.gameplay_music)
            try:
                pygame.mixer.music.load(track)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                self.current_track = track
                self.current_type = "gameplay"
            except:
                pass  # Silently fail if music can't load
    
    def stop_music(self):
        """Stop all music"""
        pygame.mixer.music.stop()
        self.current_track = None
        self.current_type = None
    
    def pause_music(self):
        """Pause the current music"""
        pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Resume the paused music"""
        pygame.mixer.music.unpause()
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def toggle_music(self):
        """Toggle music on/off"""
        self.music_enabled = not self.music_enabled
        if not self.music_enabled:
            self.stop_music()
        return self.music_enabled
    
    def is_music_enabled(self):
        """Check if music is enabled"""
        return self.music_enabled
    
    def has_music_files(self):
        """Check if any music files are available"""
        return len(self.menu_music) > 0 or len(self.gameplay_music) > 0

# Global music manager instance
music_manager = None

def get_music_manager():
    """Get or create the global music manager"""
    global music_manager
    if music_manager is None:
        music_manager = MusicManager()
    return music_manager
