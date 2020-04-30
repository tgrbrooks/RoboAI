import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while True:
    # Capture frame by frame
    ret, frame = cap.read()

    # Perform operations on the frame
    rotate = cv2.rotate(frame, cv2.ROTATE_180)

    cv2.imshow('frame', rotate)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()
