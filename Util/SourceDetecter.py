import os
import cv2
import time

class SourseDetecter(object):
    def __init__(self):
        pass

    @staticmethod
    def GetUiImgs(path):
        if(os.path.exists(path)):
            imgs = os.listdir(path)
            imgFiles = []
            for img in imgs:

                imgFile = cv2.imread(f"{path}/{img}")

                imgFiles.append(imgFile)

            return imgFiles

        else:
            raise FileNotFoundError("Not is File")
    def SaveImg(self,img):
        cv2.imwrite(f"image/input.jpg",img)        


if __name__=="__main__":

    root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+"\\"
    img2 = SourseDetecter.GetUiImgs(root_path+"Media")[0]