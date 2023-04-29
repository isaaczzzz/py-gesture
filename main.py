from CounterCenter import Controller
from window import make_window
from PIL import Image
import numpy
import cv2
import Run

if __name__ == '__main__':
    Controller = Controller()
    Controller.Main()
    im = Image.open('./image/output.jpg')
    # 压缩图片
    new_size = (370, 250)
    im = im.resize(new_size)
    img = cv2.cvtColor(numpy.asarray(im), cv2.COLOR_RGB2BGR)  # 以灰度保存所截图像至img
    tr = Run.Run(img)  # 调用Run中方法对所截图img进行处理，返回一个列表tr，里面每个元素都是对应字符 eg.['3', '2', '6']
    # print(tr) # 查看tr内容
    re = ''.join(str(s) for s in tr)
    print('识别到的数字: '+re)
    make_window(re)
    