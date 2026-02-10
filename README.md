🚗 SWYFT — 2D Hill Climb Racing Game (Gesture Controlled)

SWYFT is a fun and interactive 2D hill-climb racing game built with Python + Pygame, featuring hand-gesture controls using MediaPipe.
Drive across randomly generated terrain, avoid obstacles, and keep your car balanced to survive as long as possible.

✨ Features

🎮 Game Features

Procedurally generated endless terrain

Realistic car physics and suspension

Obstacles and difficulty progression

Menu screen, game over screen & music

Smooth camera tracking

Cross-platform run support (Windows/Linux)

🖐️ Gesture Control

Control the car using your hand via webcam

MediaPipe powered real-time detection

Keyboard fallback controls included

Diagnostic & troubleshooting tools provided

🎵 Audio

Background music for menu & gameplay

Easy music replacement support

🧠 Tech Stack
Area	Technology
Language	Python
Game Engine	Pygame
Computer Vision	MediaPipe
Physics	Custom Physics Engine
Version Control	Git & GitHub
📂 Project Structure
SWYFT/
│
├── main.py                # Entry point
├── game.py                # Core game loop
├── car.py                 # Car physics & behavior
├── terrain.py             # Procedural terrain generation
├── obstacles.py           # Obstacles & collisions
├── renderer.py            # Rendering engine
├── gesture_handler.py     # Hand gesture control
├── camera.py              # Webcam integration
├── music_manager.py       # Background music
│
├── music/                 # Game & menu music
├── run.bat / run.sh       # Quick run scripts
└── requirements.txt       # Dependencies

⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/nistha0/swyft.git
cd swyft

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the game

Windows:

run.bat


Linux/Mac:

bash run.sh


Or:

python main.py

🕹️ Controls
⌨️ Keyboard Mode
Key	Action
→	Accelerate
←	Brake / Reverse
R	Restart
ESC	Quit
🖐️ Gesture Mode
Gesture	Action
Hand Forward	Accelerate
Hand Back	Brake
No Hand	Idle

(Make sure your webcam is enabled)

📸 Screenshots

(You can add screenshots here later)

🎯 Learning Goals

This project was built as a Computer Science academic project to explore:

Game development fundamentals

Physics simulation

Computer vision integration

Real-time user interaction

👩‍💻 Author

Nistha Dhakal
Aakriti KC
Adhish Gurung
Tadillata Bhandari

Computer Science Student

GitHub: https://github.com/nistha0

⭐ If you like this project

Give it a ⭐ on GitHub!