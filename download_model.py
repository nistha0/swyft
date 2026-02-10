#!/usr/bin/env python3
"""
Download and verify MediaPipe hand tracking model
"""
import os
import urllib.request
import hashlib

MODEL_URL = 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task'
MODEL_PATH = os.path.expanduser('~/.mediapipe/hand_landmarker.task')

def download_model():
    """Download the hand tracking model"""
    
    # Create directory if it doesn't exist
    model_dir = os.path.dirname(MODEL_PATH)
    os.makedirs(model_dir, exist_ok=True)
    
    print("="*70)
    print("MEDIAPIPE MODEL DOWNLOADER")
    print("="*70)
    
    # Check if model already exists
    if os.path.exists(MODEL_PATH):
        size = os.path.getsize(MODEL_PATH)
        print(f"\n→ Model already exists at: {MODEL_PATH}")
        print(f"  Size: {size:,} bytes")
        
        # Verify it's not corrupt
        if size < 1000000:  # Should be ~13MB
            print("⚠ File seems too small, re-downloading...")
            os.remove(MODEL_PATH)
        else:
            print("✓ Model file exists and looks valid")
            return MODEL_PATH
    
    print(f"\n→ Downloading model from:")
    print(f"  {MODEL_URL}")
    print(f"\n→ Saving to:")
    print(f"  {MODEL_PATH}")
    print("\nThis is a one-time download (~13MB)...")
    
    try:
        # Download with progress
        def reporthook(blocknum, blocksize, totalsize):
            downloaded = blocknum * blocksize
            if totalsize > 0:
                percent = min(downloaded * 100 / totalsize, 100)
                print(f"\r  Progress: {percent:.1f}% ({downloaded:,} / {totalsize:,} bytes)", end='')
        
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH, reporthook)
        print()  # New line after progress
        
        # Verify download
        size = os.path.getsize(MODEL_PATH)
        print(f"\n✓ Download complete!")
        print(f"  File size: {size:,} bytes")
        
        if size < 1000000:
            print("✗ Downloaded file seems corrupted (too small)")
            os.remove(MODEL_PATH)
            return None
        
        print(f"✓ Model saved successfully!")
        return MODEL_PATH
        
    except Exception as e:
        print(f"\n✗ Download failed: {e}")
        if os.path.exists(MODEL_PATH):
            os.remove(MODEL_PATH)
        return None

if __name__ == "__main__":
    result = download_model()
    
    print("\n" + "="*70)
    if result:
        print("SUCCESS!")
        print("="*70)
        print(f"\nModel is ready at: {result}")
        print("\nYou can now run:")
        print("  python3 test_gesture.py")
        print("  python3 main.py")
    else:
        print("FAILED!")
        print("="*70)
        print("\nTry manual download:")
        print(f"  wget {MODEL_URL} -O {MODEL_PATH}")
    print("="*70)
