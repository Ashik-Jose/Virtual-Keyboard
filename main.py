import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller
import numpy as np
import cvzone
from time import sleep

cap = cv2.VideoCapture(0)
cap.set(3,1000)
cap.set(4,980)

detector = HandDetector(detectionCon=0.8)
keyboard = Controller()
keyboard_keys = [
    ['Q','W','E','R','T','Y','U','I','O','P','<-'],
    ['A','S','D','F','G','H','J','K','L'],
    ['Z','X','C','V','B','N','M',',','.','/']
]

class keyButton():
    def __init__(self,p1,p2,text):
        self.text = text
        self.p1 = p1
        self.p2 = p2

keyList=[]

for k in range(len(keyboard_keys)):
    for x,key in enumerate(keyboard_keys[k]):
        keyList.append(keyButton([x*50+90,k*90+86],[x*50+130,k*90+127],key))

colorR = (140, 7, 3)
strline=""
while True:
    success,img = cap.read()
    img = cv2.flip(img,1)
    if success:
        hands,img = detector.findHands(img)
        cv2.rectangle(img,(90,330),(650,365),(255,255,255),cv2.FILLED)
        cv2.putText(img,strline,(93,355),cv2.FONT_HERSHEY_PLAIN,2,(0, 0, 0),2)
        imgNew = np.zeros_like(img,np.uint8)          
        
        # for k in range(len(keyboard_keys)):
        #     for x,key in enumerate(keyboard_keys[k]):
        #         cv2.rectangle(imgNew,(x*50+90,k*90+86),(x*50+130,k*90+127),colorR,cv2.FILLED)
        #         cvzone.cornerRect(imgNew,(x*50+90,k*90+86,38,39),10,rt=0)
        #         cv2.putText(imgNew,key,(x*50+99,k*90+115),cv2.FONT_HERSHEY_PLAIN,2,(16, 36, 148),2)

        for k in keyList:
            x1,y1=k.p1
            x2,y2=k.p2
            key = k.text
            cv2.rectangle(imgNew,(x1,y1),(x2,y2),colorR,cv2.FILLED)
            cvzone.cornerRect(imgNew,(x1,y1,x2-x1,y2-y1),10,rt=0)
            cv2.putText(imgNew,key,(x1+9,y1+29),cv2.FONT_HERSHEY_PLAIN,2,(255, 255, 255),3)
                
        out = img.copy()
        alpha = 0.3
        mask = imgNew.astype(bool)
        out[mask] = cv2.addWeighted(img,alpha,imgNew,1-alpha,0)[mask]
        img = out.copy()

        if hands:
            hand1 = hands[0]
            lmList1 = hand1["lmList"]
            l1,_ = detector.findDistance((lmList1[8][0],lmList1[8][1]),(lmList1[12][0],lmList1[12][1]),img=None)
            # print(lmList1[8][2])
            # sleep(1)
            cursor = lmList1[8]

            for k in keyList:
                x1,y1=k.p1
                x2,y2=k.p2
                key = k.text

                
                if x1<cursor[0]<x2 and y1<cursor[1]<y2:
                    cv2.rectangle(img,(x1,y1),(x2,y2),colorR,cv2.FILLED)
                    cvzone.cornerRect(img,(x1,y1,x2-x1,y2-y1),10,rt=0)
                    cv2.putText(img,key,(x1+9,y1+29),cv2.FONT_HERSHEY_PLAIN,2,(0, 0, 255),3)
                    if l1<17:
                        if key=='<-':
                            strline=strline[:-1]
                            sleep(0.5)
                        else:
                            keyboard.press(key)
                            strline+=key
                            sleep(0.5)
                    
            if len(hands)==2:
                hand2 = hands[0]
                lmList2 = hand2["lmList"]
                l2,_ = detector.findDistance((lmList2[4][0],lmList2[4][1]),(lmList2[14][0],lmList2[14][1]),img=None)

                if l2<45:
                    strline=""

                
                

        # print(cursor[2])

            # 
            #     colorR = (100,240,0)
            #     strline+='a'
            #     print(strline)
            # else:
            #     colorR = (0,250,125)
            # if 300<cursor[0]<400 and 300<cursor[1]<400 and cursor[2]<-41:
            #     colorR = (100,240,0)
            #     strline+='b'
            #     print(strline)
            # else:
            #     colorR = (0,250,125)

        # cv2.rectangle(img,(100,100),(200,200),colorR,cv2.FILLED)
        # cv2.rectangle(img,(300,300),(400,400),colorR,cv2.FILLED)

    cv2.imshow("Image",img)
    cv2.waitKey(1)