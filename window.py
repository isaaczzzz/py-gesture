import tkinter as tk
import sys

def make_window(num):
    # 创建主窗口对象
    root = tk.Tk()
    # 隐藏主窗口
    root.withdraw()

    # 创建弹窗对象
    popup = tk.Toplevel()

    # 设置弹窗标题
    popup.title("提示")

    # 设置弹窗大小
    popup.geometry("200x100")

    # 设置弹窗的提示内容
    message = "识别到的数字为: {}".format(num)
    label = tk.Label(popup, text=message)
    label.pack(pady=20)

    def on_ok_button_click():
        popup.destroy()
        sys.exit()
        
    # 创建关闭按钮
    button = tk.Button(popup, text="确定", command=on_ok_button_click)
    button.pack()

    # 让弹窗保持在屏幕中央
    windowWidth = popup.winfo_reqwidth()
    windowHeight = popup.winfo_reqheight()
    positionRight = int(popup.winfo_screenwidth() / 2 - windowWidth / 2)
    positionDown = int(popup.winfo_screenheight() / 2 - windowHeight / 2)
    popup.geometry("+{}+{}".format(positionRight, positionDown))

    # 运行弹窗程序
    popup.mainloop()

if __name__ == '__main__':
    make_window(113)