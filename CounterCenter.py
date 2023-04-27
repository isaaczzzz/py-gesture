from Util.HandDetecter import HandDetected
from Util.SourceDetecter import SourseDetecter
from Util.Window import Window
import numpy
class Controller(object):
    def __init__(self):
        self.HandDetected = HandDetected()
        self.window_w = 1300
        self.window_h = 720
        self.Window = Window(width=self.window_w,height=self.window_h)
        self.SourseDetecter = SourseDetecter()
        self.ID = 0
        self.PenColor = (255, 255, 255) #画笔颜色
        self.PenPostion = (0,0)
        self.Canvas = numpy.zeros((self.window_h,self.window_w,3),numpy.uint8)
        self.PenSize = 30

    def ControllerFingerTrack(self,result,img):
        # 负责跟踪食指和中指
        postions = self.HandDetected.CheckHandUp(result)
        if(postions):
            indexFinger = postions[self.HandDetected.INDEXFINGER]
            middleFinger = postions[self.HandDetected.MIDDLEFINGER]

            if(indexFinger.get('flag') and middleFinger.get('flag') ):
                #食指，中指立起来了开始检测是否选择功能
                indexFinger_x ,indexFinger_y =int( indexFinger.get("x")*self.window_w),int (indexFinger.get("y")*self.window_h )
                middleFinger_x,middleFinger_y = int( middleFinger.get("x")*self.window_w),int(middleFinger.get("y")*self.window_h )

                center_x = int((indexFinger_x+middleFinger_x)/2)
                center_y = int((indexFinger_y+middleFinger_y)/2)

                self.Window.cv.circle(img, (center_x,center_y), 35, self.PenColor, self.Window.cv.FILLED)

                # #开始具体的功能模块
                # if(0<=center_y and center_y<=125):
                #     if(center_x>=125 and center_x<=260):
                #         self.ID = 1
                #         self.PenSize = 15
                #         self.PenColor=(0,0,255)
                #     if(center_x>=365 and center_x<=505):
                #         self.ID = 2
                #         self.PenSize = 15
                #         self.PenColor = (255,0,0)
                #     if(center_x>=615 and center_x<=755):
                #         self.ID = 3
                #         self.PenSize=15
                #         self.PenColor=(0,255,0)
                #     if(center_x>=1065 and center_x<=1205):
                #         self.ID = 4
                #         self.PenSize= 30
                #         self.PenColor=(0,0,0)

        return img


    def DrawPenController(self,result,img):
        # 开始绘制图形
        postions = self.HandDetected.CheckHandUp(result)
        h, w, c = img.shape
        if (postions):
            indexFinger = postions[self.HandDetected.INDEXFINGER]
            middleFinger = postions[self.HandDetected.MIDDLEFINGER]


            if (indexFinger.get('flag') and not middleFinger.get('flag')):
                indexFinger_x, indexFinger_y = int(indexFinger.get("x") * self.window_w), int(
                    indexFinger.get("y") * self.window_h)
                self.Window.cv.circle(img, (indexFinger_x, indexFinger_y), self.PenSize, self.PenColor, self.Window.cv.FILLED)

                if (self.PenPostion == (0,0)):
                    self.PenPostion = (indexFinger_x,indexFinger_y)

                self.Window.cv.line(self.Canvas,self.PenPostion,(indexFinger_x,indexFinger_y),self.PenColor,self.PenSize)
                self.PenPostion = (indexFinger_x,indexFinger_y)

            else:
                self.PenPostion = (0, 0)

        return img


    def ShowDrawWay(self,img):
        h, w, c = img.shape
        self.Canvas = self.Window.cv.resize(self.Canvas, (w, h))
        img = self.Window.addImg(img, self.Canvas)
       
        return img

    def Main(self):

        while True:

            flag,img =  self.Window.cap.read()
            img = self.Window.cv.flip(img, 1)
            result,img = self.HandDetected.findHands(img,True)


            img = self.ControllerFingerTrack(result,img)

            img = self.DrawPenController(result,img)
            img = self.ShowDrawWay(img)

            self.Window.show("Canvas",img)
            if(self.Window.cv.waitKey(1)==ord("s")):
                # 保存图片
                self.SourseDetecter.SaveImg(self.Canvas)
            if(self.Window.cv.waitKey(1)==ord("q")):
                return


if __name__=="__main__":
    Controller = Controller()
    Controller.Main()
