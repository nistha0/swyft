# 📥 SWYFT Installation Guide

## Quick Install (3 Steps)

### Step 1: Install Python
Make sure you have Python 3.7 or higher installed.

**Check if you have Python:**
```bash
python3 --version
```

**Don't have Python?**
- Windows: Download from [python.org](https://www.python.org/downloads/)
- Linux: `sudo apt install python3 python3-pip`
- Mac: `brew install python3`

### Step 2: Install Dependencies
```bash
# Essential (required)
pip install pygame

# For gesture control (optional but recommended)
pip install opencv-python mediapipe
```

**Or install everything at once:**
```bash
pip install -r requirements.txt
```

### Step 3: Run the Game
```bash
python3 main.py
```

**Or use the launcher scripts:**
```bash
# Linux/Mac
./run.sh

# Windows
run.bat
```

---

## Detailed Installation

### For Fedora (Your System)

```bash
# Install Python and pip (if not installed)
sudo dnf install python3 python3-pip

# Install game dependencies
pip3 install --user pygame opencv-python mediapipe

# Navigate to game folder
cd ~/Pictures/fix

# Run the game
python3 main.py
```

### For Ubuntu/Debian

```bash
# Install Python and pip
sudo apt update
sudo apt install python3 python3-pip

# Install dependencies
pip3 install pygame opencv-python mediapipe

# Run game
python3 main.py
```

### For Windows

```bash
# Install Python from python.org first, then:

# Open Command Prompt or PowerShell
pip install pygame opencv-python mediapipe

# Run game
python main.py
```

### For macOS

```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3

# Install dependencies
pip3 install pygame opencv-python mediapipe

# Run game
python3 main.py
```

---

## Troubleshooting

### "pygame not found"
```bash
pip install pygame --user
# or
pip3 install pygame --user
```

### "No module named cv2"
This means OpenCV isn't installed. Gesture control won't work, but keyboard will:
```bash
pip install opencv-python --user
```

### "No module named mediapipe"
Gesture control needs this:
```bash
pip install mediapipe --user
```

### "Permission denied" errors
Add `--user` flag:
```bash
pip install --user pygame opencv-python mediapipe
```

### Camera won't open (Linux)
```bash
# Check camera permissions
ls -l /dev/video0

# Add yourself to video group
sudo usermod -a -G video $USER

# Log out and log back in
```

### "Command 'python3' not found"
Try `python` instead of `python3`:
```bash
python main.py
```

---

## Verification

### Check Everything is Installed

```bash
# Check Python
python3 --version

# Check pygame
python3 -c "import pygame; print('pygame:', pygame.__version__)"

# Check OpenCV
python3 -c "import cv2; print('OpenCV:', cv2.__version__)"

# Check MediaPipe
python3 -c "import mediapipe; print('MediaPipe: OK')"
```

**Expected output:**
```
Python 3.x.x
pygame: 2.x.x
OpenCV: 4.x.x
MediaPipe: OK
```

---

## Optional: Virtual Environment

For a cleaner installation:

```bash
# Create virtual environment
python3 -m venv swyft_env

# Activate it
source swyft_env/bin/activate  # Linux/Mac
swyft_env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run game
python main.py

# When done, deactivate
deactivate
```

---

## What Each Dependency Does

| Package | Purpose | Required? |
|---------|---------|-----------|
| pygame | Game engine, graphics, sound | ✅ YES |
| opencv-python | Camera access, image processing | ⚠️ For gestures only |
| mediapipe | Hand tracking AI | ⚠️ For gestures only |

**Note:** The game works perfectly with just pygame! Gesture control is optional.

---

## File Sizes

- pygame: ~10 MB
- opencv-python: ~50 MB
- mediapipe: ~30 MB
- **Total:** ~90 MB

---

## Running the Game

### Method 1: Direct Python
```bash
python3 main.py
```

### Method 2: Launcher Script
```bash
./run.sh        # Linux/Mac
run.bat         # Windows
```

### Method 3: Make it Executable (Linux/Mac)
```bash
chmod +x main.py
./main.py
```

---

## First Time Running

When you first run the game:

1. **Menu appears** - Choose control mode
   - "Button Control" - Keyboard (always works)
   - "Gesture Control" - Hand tracking (needs camera)

2. **If you chose Gestures:**
   - Camera window appears (separate window)
   - Allow camera access if prompted
   - Position hand in view

3. **Game starts:**
   - "GET READY!" screen appears
   - Read instructions
   - Press control key or make gesture to start
   - Have fun!

---

## System Requirements

### Minimum:
- Python 3.7+
- 2 GB RAM
- Any graphics card
- Keyboard

### For Gesture Control:
- Webcam (built-in or USB)
- 4 GB RAM (recommended)
- Good lighting

### Tested On:
- ✅ Fedora 39
- ✅ Ubuntu 22.04
- ✅ Windows 10/11
- ✅ macOS 12+

---

## Need Help?

### Common Issues:

**"Game won't start"**
- Check Python version: `python3 --version`
- Reinstall pygame: `pip install --force-reinstall pygame`

**"Gesture control unavailable"**
- Install opencv and mediapipe
- Check camera with: `cheese` or other camera app
- Try restarting the game

**"Camera window not showing"**
- Look for separate window in taskbar
- Try Alt+Tab to find it
- Check if another app is using camera

**"Game too slow"**
- Close other applications
- Disable gesture control if not using it
- Reduce window size (edit config.py)

---

## Uninstall

To remove everything:

```bash
# Uninstall packages
pip uninstall pygame opencv-python mediapipe

# Delete game folder
rm -rf ~/Pictures/fix  # Or wherever you put it
```

---

## Ready to Play?

```bash
cd ~/Pictures/fix
python3 main.py
```

**Enjoy SWYFT! 🏎️💨**
