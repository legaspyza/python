import cv2
from pyzbar.pyzbar import decode
import requests  # Import the requests module
import tkinter as tk
from tkinter import Label, Button, ttk  # Import ttk for the combo box
from PIL import Image, ImageTk

class QRCodeScanner:
    def __init__(self, parent_window):
        self.window = tk.Toplevel(parent_window)
        self.window.title("QR Code Scanner")

        self.camera = cv2.VideoCapture(0)
        self.canvas = tk.Canvas(self.window, width=640, height=480)
        self.canvas.pack()

        self.results_label = Label(self.window, text="Scanning QR codes...")
        self.results_label.pack()

        self.stop_button = Button(self.window, text="Stop Camera", command=self.close_window)
        self.stop_button.pack()

        self.qr_values = self.retrieve_data()  # Fetch the QR code data from the API
        self.camera_running = True
        self.update()

    def retrieve_data(self):
        try:
            response = requests.get("http://127.0.0.1:5000/api/qr_data")
            print("API RESPONSE:", response.json())
            if response.status_code == 200:
                qr_values = response.json()
                return set(qr_values)
            else:
                print("Error fetching data from API:", response.text)
                return set()
        except Exception as e:
            print("Error fetching data from API:", str(e))
            return set()

    def update(self):
        ret, frame = self.camera.read()
        if ret:
            decoded_objects = decode(frame)
            self.show_frame(frame, decoded_objects)
        self.window.after(30, self.update)

    def close_window(self):
        self.camera_running = False
        if self.camera.isOpened():
            self.camera.release()
        self.window.destroy()

    def show_frame(self, frame, decoded_objects):
        for obj in decoded_objects:
            x, y, w, h = obj.rect
            qr_data = obj.data.decode('utf-8')

            if qr_data in self.qr_values:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        self.canvas.photo = photo

class FirstWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("First Window")

        # Set the initial size of the first window (width x height)
        self.root.geometry("400x300")
        self.select_label = Label(self.root, text="Please select the the method you want")
        self.select_label.pack()

        self.open_second_window_button = Button(self.root, text="Scan", command=self.open_second_window)
        self.open_second_window_button.pack()
        
        self.open_pers_window_button = Button(self.root, text="Borrow and Return", command=self.open_pers_window)
        self.open_pers_window_button.pack()

    def open_second_window(self):
        MainApplication(self.root)
    
    def open_pers_window(self):
        QRCodeScanner(self.root)

class MainApplication:
    def __init__(self):
        self.window = tk.Tk()
        self.root.title("Main Application")

        # Set the initial size of the main application window (width x height)
        self.root.geometry("800x600")

        # Create a label with the text "Please select the shelves"
        self.select_label = Label(self.root, text="Please select the shelves")
        self.select_label.pack()

        # Create a combo box widget
        self.combo_box = ttk.Combobox(self.root, values=["Option 1", "Option 2", "Option 3"])
        self.combo_box.pack()

        self.open_scanner_button = Button(self.root, text="Open QR Code Scanner", command=self.open_scanner)
        self.open_scanner_button.pack()

    def open_scanner(self):
        QRCodeScanner(self.root)

if __name__ == '__main__':
    root = tk.Tk()
    first_window = FirstWindow(root)
    root.mainloop()
