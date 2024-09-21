import cv2
import numpy as np

cap = cv2.VideoCapture(0)
targetlocked = False

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    low_red = np.array([161, 155, 84])
    

    cv2.imshow("Frame", frame)

    if targetlocked == True:
        break

cap.release()
cv2.destroyAllWindows()