#!/usr/bin/env python3
"""
Test gesture control with MediaPipe 0.10.30+
"""
import cv2
import time
import os

print("="*60)
print("GESTURE CONTROL TEST")
print("="*60)
print("\nTesting camera and hand detection...")
print("\nControls:")
print("  🖐️  Open hand (3+ fingers extended) = ACCELERATE")
print("  ✊  Closed fist (no fingers) = BRAKE")
print("\nPress ESC to exit\n")
print("="*60)

def get_model_path():
    """Get or download model"""
    import urllib.request
    
    # Try multiple locations
    possible_paths = [
        os.path.expanduser('~/.mediapipe/hand_landmarker.task'),
        '/tmp/hand_landmarker.task',
        'hand_landmarker.task'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            size = os.path.getsize(path)
            if size > 1000000:
                print(f"✓ Using model from: {path}")
                return path
            else:
                print(f"⚠ Removing corrupted model at {path}")
                try:
                    os.remove(path)
                except:
                    pass
    
    # Download
    model_path = os.path.expanduser('~/.mediapipe/hand_landmarker.task')
    model_dir = os.path.dirname(model_path)
    
    try:
        os.makedirs(model_dir, exist_ok=True)
    except:
        model_path = '/tmp/hand_landmarker.task'
    
    url = 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task'
    
    print(f"\n→ Downloading model (one-time, ~13MB)...")
    print(f"  To: {model_path}")
    
    try:
        urllib.request.urlretrieve(url, model_path)
        size = os.path.getsize(model_path)
        
        if size > 1000000:
            print(f"✓ Download complete ({size:,} bytes)")
            return model_path
        else:
            print("✗ Download failed (file too small)")
            os.remove(model_path)
            return None
    except Exception as e:
        print(f"✗ Download failed: {e}")
        print("\nManual download:")
        print(f"  python3 download_model.py")
        return None

try:
    # Import MediaPipe
    import mediapipe as mp
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
    
    print("\n→ Initializing MediaPipe...")
    
    # Get model
    model_path = get_model_path()
    if not model_path:
        print("\n✗ Could not get model")
        print("  Run: python3 download_model.py")
        exit(1)
    
    # Create hand detector
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=1,
        min_hand_detection_confidence=0.7
    )
    detector = vision.HandLandmarker.create_from_options(options)
    print("✓ Hand detector created")
    
    # Open camera
    print("→ Opening camera...")
    cap = cv2.VideoCapture(0)
    time.sleep(0.5)
    
    if not cap.isOpened():
        print("✗ Failed to open camera!")
        print("\nFix:")
        print("  sudo usermod -a -G video $USER")
        print("  Then LOG OUT and LOG BACK IN")
        exit(1)
    
    print("✓ Camera opened")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Create window
    cv2.namedWindow('Gesture Test', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Gesture Test', 640, 480)
    print("✓ Window created")
    
    print("\n" + "="*60)
    print("CAMERA FEED ACTIVE - Look for the window!")
    print("="*60)
    print("Try these gestures:")
    print("  1. Show open hand → Should say ACCELERATE")
    print("  2. Make a fist → Should say BRAKE")
    print("  3. Press ESC to quit")
    print("="*60 + "\n")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        
        # Flip for mirror effect
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        
        # Convert to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        
        # Detect
        result = detector.detect(mp_image)
        
        # Check if hand detected
        gesture = "No Hand"
        color = (0, 0, 255)
        
        if result.hand_landmarks:
            landmarks = result.hand_landmarks[0]
            
            # Draw hand skeleton
            for hand_landmarks in result.hand_landmarks:
                connections = [
                    (0, 1), (1, 2), (2, 3), (3, 4),
                    (0, 5), (5, 6), (6, 7), (7, 8),
                    (5, 9), (9, 10), (10, 11), (11, 12),
                    (9, 13), (13, 14), (14, 15), (15, 16),
                    (13, 17), (17, 18), (18, 19), (19, 20),
                    (0, 17)
                ]
                
                for connection in connections:
                    start_idx, end_idx = connection
                    if start_idx < len(hand_landmarks) and end_idx < len(hand_landmarks):
                        start = hand_landmarks[start_idx]
                        end = hand_landmarks[end_idx]
                        cv2.line(frame, 
                                (int(start.x * w), int(start.y * h)),
                                (int(end.x * w), int(end.y * h)),
                                (0, 255, 255), 2)
                
                for landmark in hand_landmarks:
                    cv2.circle(frame, 
                              (int(landmark.x * w), int(landmark.y * h)),
                              5, (0, 255, 0), -1)
            
            # Count fingers
            tips = [landmarks[i] for i in [8, 12, 16, 20]]
            bases = [landmarks[i] for i in [5, 9, 13, 17]]
            extended = [tip.y < base.y for tip, base in zip(tips, bases)]
            finger_count = sum(extended)
            
            if finger_count >= 3:
                gesture = "ACCELERATE (Open Hand)"
                color = (0, 255, 0)
            elif finger_count == 0:
                gesture = "BRAKE (Fist)"
                color = (0, 165, 255)
            else:
                gesture = f"Neutral ({finger_count} fingers)"
                color = (200, 200, 200)
        
        # Draw UI
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, 100), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        cv2.putText(frame, gesture, (10, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
        
        cv2.putText(frame, "Press ESC to exit", (10, h - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Show
        cv2.imshow('Gesture Test', frame)
        
        if cv2.waitKey(1) & 0xFF == 27:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("\n✓ Test complete!")
    print("If gestures worked here, they'll work in the game!")
    
except ImportError as e:
    print(f"\n✗ Import error: {e}")
    print("\nInstall dependencies:")
    print("  pip install opencv-python mediapipe")
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    print("\nIf model download failed, run:")
    print("  python3 download_model.py")
