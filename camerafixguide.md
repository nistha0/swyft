# 📷 CAMERA NOT WORKING? - Complete Fix Guide for Fedora

## The Problem

You selected "Gesture Control" but the game fell back to keyboard controls. This means your camera isn't accessible.

## Quick Fix (Most Common)

### Step 1: Add Yourself to Video Group

```bash
# Run this command
sudo usermod -a -G video $USER

# Check it worked
groups $USER
# Should show "video" in the list
```

### Step 2: **LOG OUT AND LOG BACK IN** ⚠️

This is **CRITICAL**! Group changes only take effect after you log out.

1. Save your work
2. Log out (not just close terminal!)
3. Log back in
4. Verify with: `groups` (should show "video")

### Step 3: Test Camera

```bash
cd ~/Pictures/camera
python3 test_gesture.py
```

If camera window appears with hand tracking → **FIXED!**

## Detailed Diagnostics

### Run the Diagnostic Tool

```bash
cd ~/Pictures/camera
python3 camera_diagnostic.py
```

This will check:
- ✓ Camera device exists
- ✓ You're in video group
- ✓ What's using the camera
- ✓ OpenCV can access it
- ✓ MediaPipe is installed

### Common Issues & Fixes

#### Issue 1: "Permission Denied"

**Symptom:** Camera exists but can't be opened

**Fix:**
```bash
# Add to video group
sudo usermod -a -G video $USER

# MUST log out and back in!
# Then verify:
groups | grep video
```

#### Issue 2: "Camera Already in Use"

**Symptom:** Camera opens in other apps but not in game

**Fix:**
```bash
# Check what's using it
sudo lsof /dev/video0

# Close the app shown (usually Cheese, Zoom, Teams, etc.)
# Or kill it:
sudo pkill cheese  # or zoom, teams, etc.
```

#### Issue 3: "No Camera Device Found"

**Symptom:** No /dev/video0 file

**Fix:**
```bash
# Check if camera is detected
lsusb | grep -i camera
# or
lsusb | grep -i webcam

# If nothing shows up:
# 1. Camera might be disabled in BIOS/UEFI
# 2. Camera driver not loaded
# 3. No physical camera present

# Try loading camera module
sudo modprobe uvcvideo

# Check dmesg for camera info
dmesg | grep -i camera
```

#### Issue 4: "Dependencies Missing"

**Fix:**
```bash
pip install --user opencv-python mediapipe
```

## Step-by-Step Full Fix

### 1. Check Camera Exists

```bash
ls -l /dev/video*
```

**Expected:** Should show `/dev/video0` (maybe also video1)

**If not found:**
- Your laptop might not have a camera
- Camera is disabled in BIOS
- Driver not loaded: `sudo modprobe uvcvideo`

### 2. Check Permissions

```bash
ls -l /dev/video0
```

**Expected:** Should show `crw-rw----+ 1 root video`

**Fix if different:**
```bash
sudo chmod 660 /dev/video0
sudo chown root:video /dev/video0
```

### 3. Add Yourself to Video Group

```bash
sudo usermod -a -G video $USER
```

### 4. **LOG OUT AND LOG BACK IN**

**This is NOT optional!** Group membership only updates on new login.

### 5. Verify Group Membership

```bash
groups
# Should include "video"
```

### 6. Test Camera with Simple Tool

```bash
# Test with cheese (install if needed)
sudo dnf install cheese
cheese
```

**If cheese shows camera:** Camera works, just need to fix game

**If cheese doesn't work:** System-level camera issue

### 7. Close Other Camera Apps

```bash
# Check what's using camera
sudo lsof /dev/video0

# Kill common camera apps
pkill cheese
pkill zoom
pkill teams
# Close Firefox if it has camera tab open
```

### 8. Test Game Gesture Control

```bash
cd ~/Pictures/camera
python3 test_gesture.py
```

**Expected:**
- Window opens showing camera feed
- Hand skeleton appears when you show hand
- Gestures detected

### 9. Run the Game

```bash
python3 main.py
```

Select "Gesture Control" → Camera window should appear!

## Fedora-Specific Fixes

### SELinux Might Be Blocking Camera

```bash
# Check SELinux status
getenforce

# If shows "Enforcing", try temporarily permissive mode
sudo setenforce 0

# Test camera
python3 test_gesture.py

# If it works, SELinux was the issue
# Re-enable SELinux
sudo setenforce 1

# Then add SELinux policy (advanced)
```

### Wayland vs X11

Fedora uses Wayland by default. Try X11:

1. Log out
2. At login screen, click gear icon
3. Select "GNOME on Xorg"
4. Log in
5. Test camera again

## Quick Test Script

Run this to test everything:

```bash
#!/bin/bash
echo "Camera Test"
echo "==========="

echo -n "1. Camera device exists: "
if [ -e /dev/video0 ]; then echo "✓"; else echo "✗"; fi

echo -n "2. In video group: "
if groups | grep -q video; then echo "✓"; else echo "✗ - Run: sudo usermod -a -G video \$USER"; fi

echo -n "3. OpenCV installed: "
if python3 -c "import cv2" 2>/dev/null; then echo "✓"; else echo "✗ - Run: pip install opencv-python"; fi

echo -n "4. MediaPipe installed: "
if python3 -c "import mediapipe" 2>/dev/null; then echo "✓"; else echo "✗ - Run: pip install mediapipe"; fi

echo -n "5. Camera accessible: "
if python3 -c "import cv2; cap=cv2.VideoCapture(0); print('✓' if cap.isOpened() else '✗'); cap.release()" 2>/dev/null; then
    :
else
    echo "✗"
fi
```

Save as `quick_test.sh`, run with `bash quick_test.sh`

## What Should Happen

### When It Works:

```
tadil@fedora:~/Pictures/camera$ python3 main.py

[Select "Gesture Control"]

==================================================
INITIALIZING GESTURE CONTROL
==================================================
→ Initializing MediaPipe (new API)...
✓ MediaPipe hand tracking initialized (v0.10.30+)

==================================================
STARTING CAMERA FOR GESTURE CONTROL
==================================================
→ Opening camera...
✓ Camera opened successfully
✓ Camera window created: 'Gesture Control - SWYFT'

✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓
GESTURE CONTROL ACTIVE!
✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓

[Camera window appears showing your webcam!]
```

### What You See:

1. **Game window:** Shows "GET READY" with gesture instructions
2. **Camera window:** "Gesture Control - SWYFT" showing:
   - Your camera feed (mirrored)
   - Green hand skeleton when hand visible
   - Status: "ACCELERATE" or "BRAKE" or "NEUTRAL"

## Still Not Working?

### Last Resort Checks:

```bash
# 1. Restart your computer
sudo reboot

# 2. Check BIOS/UEFI
# Reboot → Enter BIOS → Look for camera settings → Enable

# 3. Check if camera is hardware disabled
# Some laptops have physical camera switches

# 4. Update system
sudo dnf update

# 5. Reinstall camera drivers
sudo dnf install v4l-utils
v4l2-ctl --list-devices
```

## Summary Checklist

- [ ] Camera device exists (`ls /dev/video0`)
- [ ] In video group (`groups | grep video`)
- [ ] Logged out and back in after adding to group
- [ ] No other apps using camera (`sudo lsof /dev/video0`)
- [ ] OpenCV installed (`pip install opencv-python`)
- [ ] MediaPipe installed (`pip install mediapipe`)
- [ ] test_gesture.py shows camera window
- [ ] Hand skeleton appears in test

If ALL checked → Game gesture control will work!

If ANY unchecked → Fix that step first!

## Need More Help?

Run the diagnostic:
```bash
python3 camera_diagnostic.py
```

It will tell you exactly what's wrong!
