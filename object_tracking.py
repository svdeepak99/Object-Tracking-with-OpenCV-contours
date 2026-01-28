import cv2
import numpy as np

cam = cv2.VideoCapture(0)

# ll = np.array([25,80,1])                       # for ball
# ul = np.array([42,255 ,137])
ll = np.array([0,0,0])                       # for ball
ul = np.array([255,255,255])

def nothing(x):
    pass

cv2.namedWindow('Isolated Contour')

cv2.createTrackbar('lh', 'Isolated Contour', ll[0], 180, nothing)
cv2.createTrackbar('uh', 'Isolated Contour', ul[0], 180, nothing)
cv2.createTrackbar('ls', 'Isolated Contour', ll[1], 255, nothing)
cv2.createTrackbar('us', 'Isolated Contour', ul[1], 255, nothing)
cv2.createTrackbar('lv', 'Isolated Contour', ll[2], 255, nothing)
cv2.createTrackbar('uv', 'Isolated Contour', ul[2], 255, nothing)

background = np.zeros((480,640,3), np.uint8)

kernel = np.ones((3,3))

draw = False
lift = 1

while True:
    _, frame = cam.read()

    lh = cv2.getTrackbarPos('lh', 'Isolated Contour')
    uh = cv2.getTrackbarPos('uh', 'Isolated Contour')
    ls = cv2.getTrackbarPos('ls', 'Isolated Contour')
    us = cv2.getTrackbarPos('us', 'Isolated Contour')
    lv = cv2.getTrackbarPos('lv', 'Isolated Contour')
    uv = cv2.getTrackbarPos('uv', 'Isolated Contour')

    ll = np.array([lh, ls, lv])
    ul = np.array([uh, us, uv])

    frame = cv2.flip(frame, 1)
    blur = cv2.GaussianBlur(frame, (15,15) , 0)
    frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, ll, ul)
    res = cv2.bitwise_or(frame,frame, mask=mask)

    contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    maxarea = 0

    try:
        c = max(contours, key = cv2.contourArea)
        if cv2.contourArea(c) > 150:
            
            (xcirc , ycirc) , radius = cv2.minEnclosingCircle(c)
            center = (int(xcirc) , int(ycirc))
            radius = int(radius)

            xdraw = int(xcirc)
            ydraw = int(ycirc)

            print(xdraw , ydraw)
            
            cv2.circle(res , center , radius , (255 , 0 ,0) , 3)
            cv2.circle(res , center , 1 , (0,255,0) , 4)

            cv2.circle(frame, center, radius, (255, 0, 0), 3)
            cv2.circle(frame, center, 1, (0, 255, 0), 4)
                     
            s= str(ydraw) + '\t' + str(xdraw) + '\t' + str(lift) +'\n'
            print(s)
            
            if draw == True:
                cv2.line(background ,(xdraw,ydraw),(xdraw+1,ydraw+1),(0,255,0),8)

    except:
        pass

    cv2.imshow('Live Feed',frame)
    cv2.imshow('Isolated Contour' , res)
    cv2.imshow('black ' , background)  

    key = cv2.waitKey(1)
    if key == ord('u') & 0xFF:
        print('pen lifted')
        lift = 1
        draw = False
        
    if key == ord('d') & 0xFF:
        print('pen dropped')
        lift = 0
        draw = True
            
    if key == ord('q') & 0xFF or key == 27:
        break
    if key == ord('c') & 0xFF:
        background = np.zeros((480,640,3), np.uint8)
        print('screen cleared')

cam.release()
cv2.destroyAllWindows()
