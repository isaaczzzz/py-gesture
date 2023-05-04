# 第一步，导入相关模块，增加了几个调用
import tensorflow as tf
from PIL import Image
import numpy as np
import os

# 第二步，根据输入特征和标签，自制数据集
# 2.1 导入数据集，添加数据集特征和标签路径，以及保存的路径
train_path = './mnist_image_label/mnist_train_jpg_60000/'    # 训练集输入特征路径
train_txt = './mnist_image_label/mnist_train_jpg_60000.txt'  # 训练集标签txt文件
x_train_savepath = './mnist_image_label/mnist_x_train.npy'   # 训练集输入特征存储文件
y_train_savepath = './mnist_image_label/mnist_y_train.npy'   # 训练集标签存储文件

test_path = './mnist_image_label/mnist_test_jpg_10000/'      # 测试集输入特征路径
test_txt = './mnist_image_label/mnist_test_jpg_10000.txt'    # 测试集标签文件
x_test_savepath = './mnist_image_label/mnist_x_test.npy'     # 测试集输入特征存储文件
y_test_savepath = './mnist_image_label/mnist_y_test.npy'     # 测试集标签存储文件

# 2.2 自制数据集函数
def generateds(path, txt):      # 通过函数导入数据路径和
    f = open(txt, 'r')          # 以只读形式打开txt文件
    contents = f.readlines()    # 读取文件中所有行
    f.close()                   # 关闭txt文件
    x, y_ = [], []              # 建立空列表
    for content in contents:    # 逐行取出
        value = content.split()           # 以空格分开保存到value中，图片路径为value[0] , 标签为value[1] , 存入列表
        img_path = path + value[0]        # 拼接图片路径和文件名
        img = Image.open(img_path)        # 读入图片
        img = np.array(img.convert('L'))  # 图片变为8位宽灰度值的np.array格式
        img = img / 255.                  # 数据归一化（实现预处理）
        x.append(img)                     # 归一化后的数据，贴到列表x
        y_.append(value[1])               # 标签贴到列表y_
        print('loading : ' + content)     # 打印状态提示

    x = np.array(x)           # x变为np.array格式
    y_ = np.array(y_)         # y变为np.array格式
    y_ = y_.astype(np.int64)  # y变为64位整型
    return x, y_              # 返回输入特征x，返回标签y_

# 2.3 判断数据集是否存在，是则直接导入，否则调用函数创造数据集
if os.path.exists(x_train_savepath) and os.path.exists(y_train_savepath) and os.path.exists(
        x_test_savepath) and os.path.exists(y_test_savepath):  # 判断训练集和测试集是否存在，是则直接读取
    print('-------------Load Datasets-----------------')
    x_train_save = np.load(x_train_savepath)
    y_train = np.load(y_train_savepath)
    x_test_save = np.load(x_test_savepath)
    y_test = np.load(y_test_savepath)
    x_train = np.reshape(x_train_save, (len(x_train_save), 28, 28))  # 将输入特征转换为28*28的形式
    x_test = np.reshape(x_test_save, (len(x_test_save), 28, 28))     # 同上
else:  # 若数据集不存在，调用函数进行制作
    print('-------------Generate Datasets-----------------')
    x_train, y_train = generateds(train_path, train_txt)
    x_test, y_test = generateds(test_path, test_txt)
    print('-------------Save Datasets-----------------')
    x_train_save = np.reshape(x_train, (len(x_train), -1))
    x_test_save = np.reshape(x_test, (len(x_test), -1))
    np.save(x_train_savepath, x_train_save)
    np.save(y_train_savepath, y_train)
    np.save(x_test_savepath, x_test_save)
    np.save(y_test_savepath, y_test)

# 第三步，搭建网络结构
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])
# 第四步，配置训练方法
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
              metrics=['sparse_categorical_accuracy'])
# 第五步，执行训练，依次为训练集样本，训练集标签，小批量大小32，训练轮次5，测试集，训练集循环1轮次进行一次测试
model.fit(x_train, y_train, batch_size=32, epochs=5, validation_data=(x_test, y_test), validation_freq=1)
# 第六步，打印网络结构和参数统计
model.summary()