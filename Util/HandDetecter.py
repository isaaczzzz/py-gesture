import mediapipe as mp
import cv2
import os
from Util.SourceDetecter import SourseDetecter
class HandDetected(object):
    def __init__(self):
        self.mpHand = mp.solutions.hands
        self.Hand = self.mpHand.Hands()
        self.mphanddraw = mp.solutions.drawing_utils
        self.THUMB = 0
        self.INDEXFINGER=1
        self.MIDDLEFINGER=2
        self.RIGHTFINGER=3
        self.PINKY=4


    def findHands(self,img,flag=False,name="Hands"):
        #将从摄像头获取的图片传入这个函数
        rgbimg = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        result = self.Hand.process(rgbimg)
        if(flag):
            self.MarkHands(result,img,name)
        return result,img

    def GetHandPoints(self,result):
        pass

    def FindUPFings(self,result,ID):
        #改方法适合一次性查看一个手指的状况，不适合同时跟踪多个手指
        if(result.multi_hand_landmarks):
            fingers = self.CheckHandUp(result)
            if(fingers[ID].get('flag')):
                return fingers[ID]

    def CheckHandUp(self,result):

        TipsId = [4, 8, 12, 16, 20]  # 定点的坐标
        hands_data = result.multi_hand_landmarks
        if (hands_data):
            for handlist in hands_data:
                fingers = []
                #判断大拇指的开关
                if(handlist.landmark[TipsId[0]-2].x < handlist.landmark[TipsId[0]+1].x):
                    if handlist.landmark[TipsId[0]].x >  handlist.landmark[TipsId[0]-1].x:
                        data = {"flag":0,"x":int(handlist.landmark[TipsId[0]].x),"y":handlist.landmark[TipsId[0]].y}
                        fingers.append(data)
                    else:
                        data = {"flag": 1, "x": int(handlist.landmark[TipsId[0]].x), "y": handlist.landmark[TipsId[0]].y}
                        fingers.append(data)
                else:
                    if handlist.landmark[TipsId[0]].x < handlist.landmark[TipsId[0] - 1].x:
                        data = {"flag": 0, "x": handlist.landmark[TipsId[0]].x, "y": handlist.landmark[TipsId[0]].y}
                        fingers.append(data)
                    else:
                        data = {"flag": 1, "x": handlist.landmark[TipsId[0]].x, "y": handlist.landmark[TipsId[0]].y}
                        fingers.append(data)
                # 判断其他手指
                for id in range(1,5):
                    if(handlist.landmark[TipsId[id]].y > handlist.landmark[TipsId[id]-2].y):
                        data = {"flag": 0, "x": handlist.landmark[TipsId[id]].x, "y": handlist.landmark[TipsId[id]].y}
                        fingers.append(data)
                    else:
                        data = {"flag": 1, "x": handlist.landmark[TipsId[id]].x,
                                "y": handlist.landmark[TipsId[id]].y}
                        fingers.append(data)


                return fingers
        else:
            return None


    def MarkHands(self,result,img,name):
        #是否对检测到的手部进行标注，之后返回标注好的图片
        hands_data = result.multi_hand_landmarks
        if (hands_data):

            for handlm in hands_data:
                h, w, c = img.shape
                self.mphanddraw.draw_landmarks(img, handlm, self.mpHand.HAND_CONNECTIONS, )



    def __str__(self):
        print("HandDetected for Identify Hands")

if __name__=="__main__":
    pass