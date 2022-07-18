# find colors, implement webcam and then place the color at different points where that particular color was detected
import cv2
import numpy as np
#using webcam

cap=cv2.VideoCapture(0)  #for webcam default is 0
cap.set(3,640)  #frame width id no=3
cap.set(4,10)  #frame height id no=4
cap.set(10,100) #brightness id no=10

myColors=[[5,107,0,19,255,255], #orange
          [57,76,0,100,255,255]] #green

myColorValues=[[51,153,255],
               [0,255,0]]

myPoints=[] #to draw  [x,y,colorIndex]


def findColor(img,myColors,myColorValues):
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count=0
    newPoints=[]
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x,y = getContours(mask)
        # draw a circle around x,y
        cv2.circle(imgResult,(x,y),20,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count+=1
        # cv2.imshow(str(color[0]),mask)
    return newPoints


# for each of the color that we detect, we have to identify its position
def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)  # RETR_EXTERNAL retrieves the outer contours
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            # calculate the curve length to find the corners of the shapes
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
            x, y, w, h = cv2.boundingRect(approx)
            #we have to draw from the tip rather than the center
    return x+w//2,y  #tip point

def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult,(point[0],point[1]),20,myColorValues[point[2]],cv2.FILLED)



while True:
    success,img=cap.read()
    imgResult = img.copy()

    newPoints = findColor(img,myColors,myColorValues)
    if len(newPoints)!=0:
        #getting the color
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)
    cv2.imshow("video",imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break