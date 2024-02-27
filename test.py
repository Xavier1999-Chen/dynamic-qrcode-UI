import tkinter as tk
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, image_path):
        self.root = tk.Tk()
        self.root.title("Image Viewer")

        # 加载图片
        self.image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(self.image)

        # 创建显示图片的标签
        self.label = tk.Label(self.root, image=self.photo)
        self.label.pack(expand=True)

        # 监听窗口大小改变事件
        self.root.bind("<Configure>", self.resize_image)

    def resize_image(self, event):
        # 获取当前窗口大小
        width = event.width
        height = event.height

        # 仅在窗口大小实际改变时调整图片大小和更新UI
        if self.root.winfo_width() != width or self.root.winfo_height() != height:
            # 根据窗口大小调整图片大小
            resized_image = self.image.resize((width, height))
            self.photo = ImageTk.PhotoImage(resized_image)

            # 更新图片
            self.label.config(image=self.photo)

    def run(self):
        self.root.mainloop()

# 创建ImageViewer对象，传入图片路径
viewer = ImageViewer("qr_code.png")
# 启动应用
viewer.run()