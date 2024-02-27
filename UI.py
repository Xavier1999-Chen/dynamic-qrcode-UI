import tkinter as tk
import threading
import time
from datetime import datetime
import qrcode
from PIL import Image, ImageTk
import os

class QRCodeGenerator:
    def __init__(self):      
        self.window = tk.Tk()
        self.window.geometry("1600x1200")
        self.window.configure(bg='white')
        self.window.title("Dynamic QR Code Attendance")
        self.window.bind("<Configure>", self.resize_win)
        self.last_update_time = 0
        self.img_temp = None

        # 创建UI控件
        self.time_label = tk.Label(self.window , font=("Helvetica", 24),bg='white')
        self.time_label.pack()

        self.qrcode_canvas = tk.Canvas(self.window , bg="white")
        self.qrcode_canvas.pack(fill="both", expand=True)

        # 创建一个定时器线程，每分钟更新二维码并刷新UI
        self.timer_thread = threading.Thread(target=self.timer_loop)
        self.timer_thread.daemon = True  # 在主线程退出时自动结束
        self.timer_thread.start()

    def update_time(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)

    def generate_qr_code(self,url):
        current_time = time.time()
        if current_time - self.last_update_time < 5:
            # self.resize_win()
            return
        timestamp = datetime.now().timestamp()
        # print(timestamp)

        data = f"{url}?timestamp={timestamp}"

        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        # qr_image.save("qr_code.png")

        # 保存二维码为临时文件
        qr_img_temp_file = "qrcode_temp.png"
        qr_image.save(qr_img_temp_file)


        x = self.window.winfo_width()  // 4
        w = self.window.winfo_width() // 2
        h = self.window.winfo_width() // 2

        # 使用PIL库打开临时文件并转换为tk.PhotoImage对象
        pil_img = Image.open(qr_img_temp_file).resize((w,h))
        self.img_temp = pil_img
        self.qrcode_image = ImageTk.PhotoImage(pil_img)

        # 删除临时文件
        os.remove(qr_img_temp_file)

        # 在Canvas中显示二维码
        self.qrcode_canvas.delete("all")
        self.qrcode_canvas.config(width=self.qrcode_image.width(), height=self.qrcode_image.height())
        self.qrcode_image_id = self.qrcode_canvas.create_image(x, 50, anchor=tk.NW, image=self.qrcode_image)

        # 更新最后更新时间
        self.last_update_time = current_time
    
    def resize_win(self, event):
        width = event.width
        height = event.height
        pil_img = self.img_temp

        # 获取窗口和图片的尺寸
        window_width = self.window.winfo_width()
        
        # 计算图片的位置
        x = window_width  // 4
        w = window_width // 2
        h = window_width // 2

        # 仅在窗口大小实际改变时调整图片大小和更新UI
        if self.window.winfo_width() != width or self.window.winfo_height() != height:
            # 设置Label控件的位置
            pil_img = pil_img.resize((w, h))
            self.qrcode_image = ImageTk.PhotoImage(pil_img)
            self.qrcode_canvas.delete("all")
            self.qrcode_canvas.config(width=self.qrcode_image.width(), height=self.qrcode_image.height())
            self.qrcode_image_id = self.qrcode_canvas.create_image(x, 50, anchor=tk.NW, image=self.qrcode_image)



    def timer_loop(self):
        url = "https://xavier1999-chen.github.io/dynamic-qrcode/"
        while True:
            self.generate_qr_code(url)
            self.update_time()
            time.sleep(1)  # 每1秒更新一次

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    
    app = QRCodeGenerator()
    app.run()
    