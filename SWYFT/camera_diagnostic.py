#!/usr/bin/env python3
"""
Camera Diagnostic Tool for Fedora
"""
import subprocess
import os

print("="*70)
print("CAMERA DIAGNOSTIC TOOL")
print("="*70)

# Check 1: Video devices
print("\n[1] Checking for camera devices...")
try:
    result = subprocess.run(['ls', '-l', '/dev/video*'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("✓ Camera devices found:")
        print(result.stdout)
    else:
        print("✗ No camera devices found!")
        print("  Your system may not have a camera or drivers aren't loaded")
except Exception as e:
    print(f"✗ Error checking devices: {e}")

# Check 2: Camera permissions
print("\n[2] Checking camera permissions...")
try:
    import pwd
    username = pwd.getpwuid(os.getuid()).pw_name
    result = subprocess.run(['groups', username], 
                          capture_output=True, text=True)
    groups = result.stdout
    
    if 'video' in groups:
        print(f"✓ User '{username}' is in 'video' group")
    else:
        print(f"✗ User '{username}' is NOT in 'video' group")
        print("  Run: sudo usermod -a -G video $USER")
        print("  Then log out and log back in")
except Exception as e:
    print(f"✗ Error checking groups: {e}")

# Check 3: What's using the camera
print("\n[3] Checking what's using the camera...")
try:
    result = subprocess.run(['sudo', 'lsof', '/dev/video0'], 
                          capture_output=True, text=True)
    if result.returncode == 0 and result.stdout:
        print("⚠ Camera is currently in use by:")
        print(result.stdout)
    else:
        print("✓ Camera is not in use")
except Exception as e:
    print("⚠ Cannot check (run with sudo or check manually)")

# Check 4: Test with OpenCV
print("\n[4] Testing camera with OpenCV...")
try:
    import cv2
    print("✓ OpenCV is installed")
    
    print("→ Attempting to open camera...")
    cap = cv2.VideoCapture(0)
    
    if cap.isOpened():
        print("✓ Camera opened successfully!")
        ret, frame = cap.read()
        if ret:
            print("✓ Can read frames!")
            print(f"  Frame size: {frame.shape[1]}x{frame.shape[0]}")
        else:
            print("✗ Camera opened but cannot read frames")
        cap.release()
    else:
        print("✗ Failed to open camera")
        print("  Possible reasons:")
        print("  - Camera is in use by another app")
        print("  - No camera permissions")
        print("  - Camera is disabled in BIOS/UEFI")
except ImportError:
    print("✗ OpenCV not installed")
    print("  Install: pip install opencv-python")
except Exception as e:
    print(f"✗ Error testing camera: {e}")

# Check 5: MediaPipe
print("\n[5] Checking MediaPipe...")
try:
    import mediapipe as mp
    print(f"✓ MediaPipe installed (version {mp.__version__})")
    
    if hasattr(mp, 'solutions'):
        print("  Using old API (solutions)")
    else:
        print("  Using new API (tasks)")
except ImportError:
    print("✗ MediaPipe not installed")
    print("  Install: pip install mediapipe")
except Exception as e:
    print(f"✗ Error checking MediaPipe: {e}")

# Summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print("\nTo fix camera issues:")
print("1. Close all apps that might use camera (Zoom, Teams, Discord, etc.)")
print("2. Add yourself to video group:")
print("   sudo usermod -a -G video $USER")
print("   Then LOG OUT and LOG BACK IN")
print("3. Install dependencies:")
print("   pip install opencv-python mediapipe")
print("4. Test camera:")
print("   python3 test_gesture.py")
print("="*70)
