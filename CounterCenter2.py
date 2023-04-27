from Util.HandDetecter import HandDetected
from Util.SourceDetecter import SourseDetecter
from Util.Window import Window
import numpy
import cv2

class Controller(object):
    def __init__(self):
        self.HandDetected = HandDetected()
        self.window_w = 1300
        self.window_h = 720
        self.Window = Window(width=self.window_w,height=self.window_h)
        self.SourseDetecter = SourseDetecter()
        self.ID = 0
        self.PenColor = (0, 0, 255) #默认颜色
        self.PenPostion = (0,0)
        self.Canvas = numpy.zeros((self.window_h,self.window_w,3),numpy.uint8)
        self.PenSize = 15

    def saveCanvas(self):
        # 保存Canvas为PNG图片
        cv2.imwrite("canvas.png", self.Canvas)
        print("Canvas saved as canvas.png")

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

                #开始具体的功能模块
                if(0<=center_y and center_y<=125):
                    if(center_x>=125 and center_x<=260):
                        self.ID = 1
                        self.PenSize = 15
                        self.PenColor=(0,0,255)
                    if(center_x>=365 and center_x<=505):
                        self.ID = 2
                        self.PenSize = 15
                        self.PenColor = (255,0,0)
                    if(center_x>=615 and center_x<=755):
                        self.ID = 3
                        self.PenSize=15
                        self.PenColor=(0,255,0)
                    if(center_x>=1065 and center_x<=1205):
                        self.ID = 4
                        self.PenSize= 30
                        self.PenColor=(0,0,0)
                    if(center_x>=905 and center_x<=1045):
                        self.ID = 5
                        self.saveCanvas()

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
                if (self.PenPostion == (0, 0)):
                    self.PenPostion = (indexFinger_x, indexFinger_y)

                if (self.ID == 1):
                    self.Window.cv.line(img, self.PenPostion, (indexFinger_x, indexFinger_y), self.PenColor, self.PenSize)
                    self.Window.cv.circle(img, (indexFinger_x, indexFinger_y), self.PenSize, self.PenColor, self.Window.cv.FILLED)
                elif (self.ID == 2):
                    self.Canvas = numpy.zeros((self.window_h, self.window_w, 3), numpy.uint8)
                elif (self.ID == 3):
                    self.Window.cv.circle(self.Canvas, (indexFinger_x, indexFinger_y), self.PenSize, self.PenColor, self.Window.cv.FILLED)
                elif (self.ID == 4):
                    self.Window.cv.circle(img, (indexFinger_x, indexFinger_y), self.PenSize, self.PenColor, self.Window.cv.FILLED)
                self.PenPostion = (indexFinger_x, indexFinger_y)
        return img


    def Run(self):
        # 开始运行主程序
        cap = self.SourseDetecter.OpenCamera(0,640,480,30)
        while True:
            success,img = cap.read()
            img = self.HandDetected.FindHand(img)
            img = cv2.flip(img, 1)
            img = self.Window.Show(img)
            result = self.HandDetected.FindPosition(img)
            if(self.ID == 0):
                img = self.ControllerFingerTrack(result,img)
            else:
                img = self.DrawPenController(result,img)
            cv2.imshow("Image", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    controller = Controller()
    controller.Run()