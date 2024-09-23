import cv2
import numpy as np

cap = cv2.VideoCapture(0)
targetlocked = False

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    low_red = np.array([161, 155, 84]) # Remember to change these colour values to suit classroom environment (blue carpet, white walls etc)
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red) # This should create a colour mask so red is white and everything else is black
    _, contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # Basically finds objects (OpenCV is magic)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True) # Sorts objects/contours from big to small

    for a in contours:
        (x, y, w, h) = cv2.boundingRect(a) # Finds a bounding box for object
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (245, 169, 184), 2) # Draws the bounding box
        x_midpoint = (x+x+w)/2
        y_midpoint = (y+y+h)/2
        break # So only the biggest one gets considered

    cv2.line(frame, (x_midpoint, 0), (x_midpoint, 480), (245, 169, 184), 2) # Draws a midpoint line for the object


    cv2.imshow("Frame", frame) # These create visual windows, will use for debugging but probably remove for final version
    cv2.imshow("Mask", red_mask)

    if targetlocked == True:
        break

print("Yo I am looking right at it")
cap.release()
cv2.destroyAllWindows()
exit()