#!/bin/bash
# Camera Permission Fix for Fedora

echo "======================================================================"
echo "CAMERA PERMISSION FIX FOR FEDORA"
echo "======================================================================"
echo ""

# Check if camera exists
if ls /dev/video* 1> /dev/null 2>&1; then
    echo "✓ Camera device found:"
    ls -l /dev/video*
else
    echo "✗ No camera device found!"
    echo "  Your system may not have a camera or drivers aren't loaded"
    exit 1
fi

echo ""
echo "Current user: $USER"
echo ""

# Check if user is in video group
if groups $USER | grep -q '\bvideo\b'; then
    echo "✓ You are already in the 'video' group"
else
    echo "✗ You are NOT in the 'video' group"
    echo ""
    echo "Adding you to the video group..."
    sudo usermod -a -G video $USER
    
    if [ $? -eq 0 ]; then
        echo "✓ Successfully added to video group"
        echo ""
        echo "⚠ IMPORTANT: You must LOG OUT and LOG BACK IN for this to take effect!"
        echo ""
        echo "After logging back in, run this script again to verify."
    else
        echo "✗ Failed to add to video group"
        echo "  Make sure you have sudo privileges"
        exit 1
    fi
fi

echo ""
echo "======================================================================"
echo "CAMERA DIAGNOSTICS"
echo "======================================================================"
echo ""

# Check what's using the camera
echo "Checking if camera is in use..."
if command -v lsof &> /dev/null; then
    if sudo lsof /dev/video0 2>/dev/null | grep -v COMMAND; then
        echo ""
        echo "⚠ Camera is being used by another application!"
        echo "  Close the application(s) above before running the game"
    else
        echo "✓ Camera is not in use"
    fi
else
    echo "  (lsof not available, skipping)"
fi

echo ""
echo "======================================================================"
echo "NEXT STEPS"
echo "======================================================================"
echo ""
echo "1. If you just added yourself to the video group:"
echo "   → LOG OUT and LOG BACK IN (this is required!)"
echo ""
echo "2. Close any apps using the camera:"
echo "   - Cheese"
echo "   - Zoom"
echo "   - Teams"
echo "   - Discord"
echo "   - Firefox (if camera is open in a tab)"
echo ""
echo "3. Install Python dependencies:"
echo "   pip install opencv-python mediapipe"
echo ""
echo "4. Test the camera:"
echo "   python3 test_gesture.py"
echo ""
echo "5. Run the game:"
echo "   python3 main.py"
echo ""
echo "======================================================================"
