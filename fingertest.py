import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    success, img = cap.read()
    RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(RGBimg)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                #print(id,lm)
                h,w,c = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h) #prints pixel coordinates
                print (id, cx, cy)

            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)


    cv2.imshow("Image",img)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # if 'q' is pressed then quit
        break
cap.release()
cv2.destroyAllWindows()