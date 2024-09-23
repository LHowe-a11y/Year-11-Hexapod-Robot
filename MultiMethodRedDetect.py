import cv2
import numpy as np
from picamera2 import Picamera2 # type: ignore
from Control import * # type: ignore
from Ultrasonic import * # type: ignore

ultrasonic = Ultrasonic() # type: ignore
c=Control() # type: ignore
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280,720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

foundred = False # Has a red object been seen yet?
leniency = int(10) # How close to the centre something has to be to count as centred

im= picam2.capture_array() # To get inital frame to calculate middle
rows, columns, _ = im.shape
x_midpoint = int(columns/2) # Sets default to middle
x_centre = x_midpoint # Sets middle

while True:
    im= picam2.capture_array()
    hsv_frame = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    x_midpoint = 0 # Temporary to resolve issues

    low_red = np.array([161, 155, 84]) # Remember to change these colour values to suit classroom environment (blue carpet, white walls etc)
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red) # This should create a colour mask so red is white and everything else is black
    _, contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # Basically finds objects (OpenCV is magic)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    
    if contours != None:
        foundred = True

    for a in contours:
        (x, y, w, h) = cv2.boundingRect(a) # Finds a bounding box for object
        x_midpoint = (x+x+w)/2
        break # So only the biggest one gets considered

    #cv2.line(im, (x_midpoint, 0), (x_midpoint, 480), (245, 169, 184), 2) # Draws a midpoint line for the object

    cv2.imshow("Camera", im)
    cv2.imshow("Mask", red_mask)

    if (x_midpoint - leniency) > x_centre:
        data=['CMD_MOVE', '1', '-35', '0', '8', '10']
        c.run(data)
    elif (x_midpoint + leniency) < x_centre:
        data=['CMD_MOVE', '1', '35', '0', '8', '-10']
        c.run(data)
    elif foundred == True:
        break

    if cv2.waitKey(1)==ord('q'):
        break

# Move forwards
data=['CMD_MOVE', '1', '0', '35', '10', '0']
i=0
while True:
    for a in range(3):
        x = ultrasonic.getDistance()
        if x <= 20 and x != 0:
            i += 1
    if i >= 3:
        break # And stop
    else:
        i = 0
    c.run(data)
print('Stopped in front of object')
cv2.destroyAllWindows()
exit()