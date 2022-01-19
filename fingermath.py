import cv2
import mediapipe as mp
import math
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)   
detector = htm.HandDetector()    


def detectGesture(fingersUp):

    if fingersUp==[0,0,0,0,0]:
        return 0
    elif fingersUp==[0,1,0,0,0]:
        return 1
    elif fingersUp==[0,1,1,0,0]:
        return 2
    elif fingersUp==[0,1,1,1,0]:
        return 3
    elif fingersUp==[0,1,1,1,1]:
        return 4
    elif fingersUp==[1,1,1,1,1]:
        return 5

    #thumb out for *
    elif fingersUp==[1,0,0,0,0]:
        return "*"
    #thumb and index for /
    elif fingersUp==[1,1,0,0,0]:
        return "/"
    #3 for +
    elif fingersUp==[1,1,1,0,0]:
        return "+"
    #4 for -
    elif fingersUp==[1,1,1,1,0]:
        return "-"
    else:
        return " "
     
equation=''
answer=''
display=''

while True:
    success, img = cap.read() 
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    
    cv2.rectangle(img, (20, 350), (120, 450), (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img, (140, 375), (500, 450), (0, 255, 0), cv2.FILLED)

    if len(lmList) !=0:
        fingersUp = detector.checkFingers(img)

        if (math.sqrt(pow(lmList[8][2]-lmList[12][2],2)+pow(lmList[8][1]-lmList[12][1],2))<30 and fingersUp[2]==1 and fingersUp[1]==1):
            gesture = ("=")
            cv2.line(img,(lmList[12][1],lmList[12][2]),(lmList[8][1],lmList[8][2]),(0,0,255),4)
        else:
            gesture = str(detectGesture(fingersUp))

        cv2.putText(img,gesture,(50,420),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),5)

    cv2.putText(img,display,(170,420),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    cv2.imshow("Image",img)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # if 'q' is pressed then quit
        break 

    if cv2.waitKey(33) == ord(' '):  #record number when space pressed
        if gesture != "=":
            equation+=gesture
            display=equation
        else:
            answer = equation + "=" + str(eval(equation))
            display = answer
            equation = '' 
        print(equation)

