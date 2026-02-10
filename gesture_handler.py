"""
SWYFT - Gesture Handler for MediaPipe 0.10.30+
Hand gesture recognition with camera window
"""
import threading
import time
import cv2
import numpy as np
import os

class GestureHandler:
    def __init__(self):
        self.available = False
        self.running = False
        self.accelerating = False
        self.braking = False
        self.gesture_active = False
        self.current_frame = None
        self.frame_lock = threading.Lock()
        self.window_created = False
        self.camera_working = False
        self.speed_level = 1  # Speed level based on finger count (1=slow, 2=medium, 3=fast)
        
        # Try to import and initialize MediaPipe
        try:
            import mediapipe as mp
            self.mp = mp
            
            print("→ Initializing MediaPipe (new API)...")
            
            from mediapipe.tasks import python
            from mediapipe.tasks.python import vision
            
            # Get model path
            model_path = self._get_model_path()
            if not model_path:
                raise Exception("Could not download model")
            
            # Create hand landmarker
            base_options = python.BaseOptions(model_asset_path=model_path)
            options = vision.HandLandmarkerOptions(
                base_options=base_options,
                num_hands=1,
                min_hand_detection_confidence=0.7,
                min_hand_presence_confidence=0.7,
                min_tracking_confidence=0.5
            )
            
            self.detector = vision.HandLandmarker.create_from_options(options)
            self.available = True
            print("✓ MediaPipe hand tracking initialized (v0.10.30+)")
            
        except Exception as e:
            print(f"✗ Gesture control unavailable: {e}")
            print("  Run: python3 download_model.py")
            self.available = False
    
    def _get_model_path(self):
        """Get or download the hand landmarker model"""
        # Try multiple locations
        possible_paths = [
            os.path.expanduser('~/.mediapipe/hand_landmarker.task'),
            '/tmp/hand_landmarker.task',
            'hand_landmarker.task'  # Current directory
        ]
        
        # Check if model exists in any location
        for path in possible_paths:
            if os.path.exists(path):
                size = os.path.getsize(path)
                if size > 1000000:  # Should be ~13MB
                    print(f"✓ Using model from: {path}")
                    return path
                else:
                    print(f"⚠ Model at {path} seems corrupted, removing...")
                    try:
                        os.remove(path)
                    except:
                        pass
        
        # Download model
        print("→ Model not found, downloading...")
        return self._download_model()
    
    def _download_model(self):
        """Download hand landmarker model"""
        import urllib.request
        
        model_path = os.path.expanduser('~/.mediapipe/hand_landmarker.task')
        model_dir = os.path.dirname(model_path)
        
        try:
            os.makedirs(model_dir, exist_ok=True)
        except:
            model_path = '/tmp/hand_landmarker.task'
            print(f"  Using /tmp instead...")
        
        url = 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task'
        
        print(f"→ Downloading model to: {model_path}")
        print("  This may take a minute (~13MB)...")
        
        try:
            urllib.request.urlretrieve(url, model_path)
            
            # Verify download
            size = os.path.getsize(model_path)
            if size > 1000000:
                print(f"✓ Model downloaded successfully ({size:,} bytes)")
                return model_path
            else:
                print("✗ Download failed (file too small)")
                os.remove(model_path)
                return None
                
        except Exception as e:
            print(f"✗ Download failed: {e}")
            print("\nManual fix:")
            print(f"  wget {url} -O {model_path}")
            print("  Or run: python3 download_model.py")
            return None
    
    def start(self):
        """Start camera and gesture detection"""
        if not self.available:
            print("✗ Cannot start gesture control - MediaPipe not available")
            return False
        
        try:
            print("\n" + "="*60)
            print("STARTING CAMERA FOR GESTURE CONTROL")
            print("="*60)
            print("→ Opening camera...")
            
            self.cap = cv2.VideoCapture(0)
            time.sleep(0.5)
            
            if not self.cap.isOpened():
                print("✗ Failed to open camera")
                print("  Possible issues:")
                print("  - Camera is being used by another application")
                print("  - No camera detected")
                print("  - Camera permissions not granted")
                print("\n  Fix:")
                print("    sudo usermod -a -G video $USER")
                print("    Then LOG OUT and LOG BACK IN")
                return False
            
            # Test read
            ret, test_frame = self.cap.read()
            if not ret or test_frame is None:
                print("✗ Camera opened but cannot read frames")
                self.cap.release()
                return False
            
            print("✓ Camera opened successfully")
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            # Note: No separate OpenCV window - display is handled by pygame
            self.window_created = False
            print("✓ Camera ready (display in-game)")
            
            # Start processing thread
            self.running = True
            self.camera_working = True
            self.thread = threading.Thread(target=self._process, daemon=True)
            self.thread.start()
            
            print("\n" + "✓"*30)
            print("GESTURE CONTROL ACTIVE!")
            print("✓"*30)
            print("\nControls:")
            print("  🖐️  Open hand (3+ fingers) = ACCELERATE")
            print("  ✊  Closed fist = BRAKE")
            print("\nCamera feed will appear in-game (bottom-right corner)")
            print("="*60 + "\n")
            
            return True
            
        except Exception as e:
            print(f"✗ Failed to start gesture control: {e}")
            if hasattr(self, 'cap'):
                try:
                    self.cap.release()
                except:
                    pass
            return False
    
    def stop(self):
        """Stop camera and gesture detection"""
        print("→ Stopping gesture control...")
        self.running = False
        self.camera_working = False
        
        if hasattr(self, 'thread'):
            self.thread.join(timeout=1.0)
        
        if hasattr(self, 'cap'):
            try:
                self.cap.release()
            except:
                pass
        
        # No OpenCV windows to destroy anymore
        
        print("✓ Gesture control stopped")
    
    def _process(self):
        """Main processing loop"""
        print("→ Camera processing started")
        
        frame_count = 0
        last_fps_time = time.time()
        fps = 0
        
        while self.running:
            try:
                success, frame = self.cap.read()
                if not success or frame is None:
                    time.sleep(0.1)
                    continue
                
                # FPS calculation
                frame_count += 1
                if time.time() - last_fps_time > 1.0:
                    fps = frame_count
                    frame_count = 0
                    last_fps_time = time.time()
                
                # Flip for mirror effect
                frame = cv2.flip(frame, 1)
                h, w, _ = frame.shape
                
                # Convert to RGB for MediaPipe
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = self.mp.Image(image_format=self.mp.ImageFormat.SRGB, data=rgb_frame)
                
                # Detect hands
                detection_result = self.detector.detect(mp_image)
                
                # Reset gestures
                self.accelerating = False
                self.braking = False
                
                # Process results
                if detection_result.hand_landmarks:
                    self.gesture_active = True
                    
                    # Draw hand landmarks
                    for hand_landmarks in detection_result.hand_landmarks:
                        # Draw connections
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
                                start_point = hand_landmarks[start_idx]
                                end_point = hand_landmarks[end_idx]
                                
                                start_x = int(start_point.x * w)
                                start_y = int(start_point.y * h)
                                end_x = int(end_point.x * w)
                                end_y = int(end_point.y * h)
                                
                                cv2.line(frame, (start_x, start_y), (end_x, end_y), (0, 255, 255), 2)
                        
                        # Draw landmarks
                        for landmark in hand_landmarks:
                            x = int(landmark.x * w)
                            y = int(landmark.y * h)
                            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
                        
                        # Detect gesture
                        self._detect_gesture(hand_landmarks)
                else:
                    self.gesture_active = False
                
                # Add UI overlay
                overlay = frame.copy()
                cv2.rectangle(overlay, (0, 0), (w, 120), (0, 0, 0), -1)
                cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
                
                # Status text
                status_color = (0, 255, 0) if self.gesture_active else (0, 0, 255)
                status_text = "✓ Hand Detected" if self.gesture_active else "✗ No Hand"
                cv2.putText(frame, status_text, (10, 40), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, status_color, 2)
                
                # Gesture indicator
                if self.accelerating:
                    speed_text = ["SLOW", "MEDIUM", "FULL"][self.speed_level - 1]
                    cv2.putText(frame, f">>> ACCELERATE ({speed_text}) >>>", (10, 80), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                elif self.braking:
                    cv2.putText(frame, "<<< BRAKE <<<", (10, 80), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 165, 255), 2)
                else:
                    cv2.putText(frame, "NEUTRAL", (10, 80), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.9, (150, 150, 150), 2)
                
                # FPS
                cv2.putText(frame, f"FPS: {fps}", (w - 120, 40), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Instructions
                cv2.putText(frame, "3 fingers=SLOW  4=MED  5=FAST", 
                           (10, h - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(frame, "Closed fist = BRAKE", 
                           (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                # Store frame for pygame (no separate OpenCV window to prevent freezing)
                with self.frame_lock:
                    self.current_frame = frame.copy()
                    
            except Exception as e:
                print(f"⚠ Processing error: {e}")
                time.sleep(0.1)
        
        print("→ Camera processing stopped")
    
    def _detect_gesture(self, landmarks):
        """Detect gesture from hand landmarks with 3 speed levels"""
        try:
            tips = [landmarks[i] for i in [8, 12, 16, 20]]
            bases = [landmarks[i] for i in [5, 9, 13, 17]]
            
            extended = [tip.y < base.y for tip, base in zip(tips, bases)]
            finger_count = sum(extended)
            
            # Reset states
            self.accelerating = False
            self.braking = False
            self.speed_level = 1  # Default speed
            
            if finger_count == 0:
                # Closed fist = BRAKE
                self.braking = True
            elif finger_count >= 3:
                # Open hand = ACCELERATE with speed levels
                self.accelerating = True
                if finger_count == 3:
                    self.speed_level = 1  # Slow speed (60%)
                elif finger_count == 4:
                    self.speed_level = 2  # Medium speed (80%)
                else:  # 5 fingers
                    self.speed_level = 3  # Full speed (100%)
            elif extended[0] and extended[1]:
                # Peace sign fallback
                self.accelerating = True
                self.speed_level = 1
                
        except Exception as e:
            pass
    
    def get_speed_multiplier(self):
        """Get speed multiplier based on finger count"""
        speed_map = {
            1: 0.6,   # 3 fingers = 60% speed
            2: 0.8,   # 4 fingers = 80% speed
            3: 1.0    # 5 fingers = 100% speed
        }
        return speed_map.get(self.speed_level, 1.0)
    
    def is_accelerating(self):
        return self.accelerating and self.gesture_active and self.camera_working
    
    def has_hand_detected(self):
        """Check if hand is currently detected"""
        return self.gesture_active and self.camera_working
    
    def is_braking(self):
        return self.braking and self.gesture_active and self.camera_working
    
    def get_frame(self):
        try:
            with self.frame_lock:
                if self.current_frame is not None:
                    return self.current_frame.copy()
        except:
            pass
        return None
    
    def is_active(self):
        return self.running and self.camera_working
