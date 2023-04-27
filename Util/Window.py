import cv2
import os
from Util.SourceDetecter import SourseDetecter
class Window(object):
    def __init__(self,sourse=0,width = 640,height = 480):

        self.cv = cv2
        self.cap = self.cv.VideoCapture(sourse)
        self.cap.set(3,width)
        self.cap.set(4,height)
        self.SourseUi=[]
        root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "\\"
        try:
            self.SourseUi = SourseDetecter.GetUiImgs(root_path+"Media")
        except Exception as e:
            self.SourseUi = []
            print(e)


    # def PrintUi(self,img,ID):
    #     if (self.SourseUi):
    #         hui, wui, cui = self.SourseUi[ID].shape

    #         img[0:hui,0:wui] = self.SourseUi[ID]
    #         return img
    #     else:
    #         return None

    def show(self,name,img):

        self.cv.imshow(name,img)


    def addImg(self,img1,img2):
        #合并两个图片,img2为需要被合并的图片
        imgGray = self.cv.cvtColor(img2,self.cv.COLOR_BGR2GRAY) #对画布图片进行灰度处理，降低合并后的差异
        _,imgInv = self.cv.threshold(imgGray,50,255,self.cv.THRESH_BINARY_INV)
        imgInv = self.cv.cvtColor(imgInv,self.cv.COLOR_GRAY2BGR) # 处理后重新转换会彩色图片

        img1 = self.cv.bitwise_and(img1,imgInv)
        img1 = self.cv.bitwise_or(img1,img2)



        return img1

    def release(self):
        self.cap.release()
        self.cv.destroyAllWindows()

    def __str__(self):
        print("For Show img")