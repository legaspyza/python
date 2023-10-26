import cv2
import qrcode
from pyzbar.pyzbar import decode
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

class Wow:
    def __init__(self, window):
        self.window = window
        self.window.title("QR Code Scanner")

        self.camera = cv2.VideoCapture(0)
        self.canvas = tk.Canvas(window, width=640, height=480)
        self.canvas.pack()
        
        self.results_label = Label(window, text="Scanning QR codes...")
        self.results_label.pack()

        self.update()

    def update(self):
        ret, frame = self.camera.read()
        if ret:
            decoded_objects = decode(frame)
            self.show_frame(frame, decoded_objects)
        self.window.after(30, self.update)

    def show_frame(self, frame, decoded_objects):
        for obj in decoded_objects:
            x, y, w, h = obj.rect
            qr_data = obj.data.decode('utf-8')
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        if decoded_objects:
            self.results_label.config(text="\n".join([obj.data.decode('utf-8') for obj in decoded_objects]))
        else:
            self.results_label.config(text="Scanning QR codes...")

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        self.canvas.photo = photo

if __name__ == '__main__':
    root = tk.Tk()
    app = Wow(root)
    root.mainloop()
