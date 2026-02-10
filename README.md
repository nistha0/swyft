# 🚗 SWYFT

> A gesture-controlled 2D hill climb racing game built with Python and MediaPipe.

## 👥 Team

This project was developed by:

- **Nistha Dhakal** - UI 
- **Aakriti KC** - UI
- **Adhish Gurung** - Game Design & Physics
- **Tadillata Bhandari** - Gesture Control System

*Computer Science Academic Project*

## 🎮 About

**SWYFT** is an innovative 2D racing game that combines classic hill climb physics with modern computer vision. Control your car using hand gestures captured through your webcam, or fall back to traditional keyboard controls. Navigate procedurally generated terrain and try to survive as long as possible!

Built as a Computer Science academic project, SWYFT demonstrates real-world applications of game physics, computer vision, and human-computer interaction.

## ✨ Features

### 🎯 Gameplay
- **Procedurally Generated Terrain** 
- **Realistic Physics** 
- **Progressive Difficulty**
- **Score Tracking** 
- **Smooth Visuals**

### 🖐️ Gesture Control
- **Real-time Hand Detection** - Powered by MediaPipe's machine learning models
- **Intuitive Controls** - Natural hand movements control acceleration and braking
- **Webcam Integration** - Works with any standard webcam
- **Diagnostic Tools** - Built-in troubleshooting for gesture detection
- **Keyboard Fallback** - Traditional controls available anytime

### 🎵 Audio
- **Background Music** - Immersive soundtracks for menu and gameplay
- **Easy Customization** - Replace music files effortlessly

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.8+ |
| Game Engine | Pygame |
| Computer Vision | MediaPipe |
| Physics | Custom Physics Engine |
| Audio | Pygame Mixer |

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Webcam (for gesture control)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/nistha0/swyft.git
   cd swyft
   ```

2. **Run the game**

   ```bash
   python main.py
   ```

## 🕹️ How to Play

### Keyboard Controls

| Key | Action |
|-----|--------|
| `→` | Accelerate |
| `←` | Brake / Reverse |
| `R` | Restart Game |
| `ESC` | Return to Menu / Quit |

### Gesture Controls

| Gesture | Action |
|---------|--------|
| Open hand | Accelerate |
| Closed fist | Brake |
| No Hand Detected | Pause |

**Tips:**
- Ensure good lighting for optimal gesture detection
- Keep your hand within the webcam frame
- Use the diagnostic tool (`python camera_diagnostic.py`) to test your setup

## 📁 Project Structure

```
swyft/
│
├── main.py                  # Game entry point
├── game.py                  # Core game loop and logic
├── car.py                   # Car physics and behavior
├── terrain.py               # Procedural terrain generation
├── obstacles.py             # Obstacle system and collision
├── renderer.py              # Graphics rendering engine
├── gesture_handler.py       # Gesture recognition system
├── camera.py                # Webcam capture and processing
├── physics.py               # Physics calculations
├── music_manager.py         # Audio management
├── menu.py                  # Menu interface
├── game_state.py            # Game state management
├── entities.py              # Game entities and sprites
├── config.py                # Configuration settings
│
├── music/                   # Audio files
├── test_gesture.py          # Gesture testing utility
├── camera_diagnostic.py     # Camera troubleshooting tool
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🎯 Objective

Drive your car across an infinite procedurally generated landscape. Balance speed with control to:
- Avoid flipping over
- Navigate steep hills and valleys
- Dodge obstacles
- Maximize your distance traveled

The terrain gets progressively harder - how far can you go?

## 🐛 Troubleshooting

### Gesture Controls Not Working?

1. **Run the diagnostic tool:**
   ```bash
   python camera_diagnostic.py
   ```

2. **Check camera permissions** - Ensure Python has webcam access

3. **Test gesture recognition:**
   ```bash
   python test_gesture.py
   ```

4. **Common fixes:**
   - Ensure adequate lighting
   - Update webcam drivers
   - Check `config.py` for gesture sensitivity settings


## 🚀 Future Enhancements

- [ ] Multiplayer mode
- [ ] Power-ups and collectibles
- [ ] Level editor
- [ ] Mobile version
- [ ] Advanced gesture controls (both hands)


## 🙏 Acknowledgments

- MediaPipe team for hand tracking technology
- Pygame community for excellent documentation
- Hill Climb Racing for inspiration

