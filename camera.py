import cv2
import mediapipe as mp
import math
import HandTrackingModule as htm

detector = htm.HandDetector()
equation=''

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

class Video(object):
    def __init__(self):
        self.video=cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret,img = self.video.read()
        gesture=' '

        img = detector.findHands(img)
        lmList = detector.findPosition(img)
    
        cv2.rectangle(img, (20, 350), (120, 450), (0, 255, 0), cv2.FILLED)

        if len(lmList) !=0:
            fingersUp = detector.checkFingers(img)

            if (math.sqrt(pow(lmList[8][0]-lmList[12][0],2)+pow(lmList[8][1]-lmList[12][1],2))<30 and fingersUp[2]==1 and fingersUp[1]==1):
                gesture = ("=")
                #print("equals")
            else:
                gesture = str(detectGesture(fingersUp))

            cv2.putText(img,gesture,(50,420),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),5)

        ret,jpg = cv2.imencode('.jpg',img)
        return jpg.tobytes(),gesture

    
