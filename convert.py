from PIL import Image

# 读取图片文件
img = Image.open("Media/input.jpg")

# 压缩图片到指定大小
new_size = (370, 250)
img = img.resize(new_size)

# 获取图片的像素矩阵
pixels = img.load()

# 遍历所有像素点，将每个像素点的RGB值进行反色处理
for i in range(img.size[0]):
    for j in range(img.size[1]):
        # 获取当前像素点的RGB值
        r, g, b = pixels[i, j]
        # 反色处理
        pixels[i, j] = (255 - r, 255 - g, 255 - b)

# 保存修改后的图片
img.save("output.png")