import numpy as np
import cv2

# Minimal example of capturing and modifying video with openCV
# Start the capture
cap = cv2.VideoCapture(0)

# Infinite loop
while True:
    # Capture frame by frame
    ret, frame = cap.read()

    # Perform operations on the frame
    rotate = cv2.rotate(frame, cv2.ROTATE_180)

    # Show the frame on openCVs native gui
    cv2.imshow('frame', rotate)

    # Quit on press of 'q'
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
