import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk
import struct
import redis
import pickle
import numpy as np


r = redis.Redis(host='localhost', port=6379, db=0)

root = tk.Tk()
root.bind('<Escape>', lambda e: root.quit())
lmain = tk.Label(root)
lmain.pack()
last_frame = np.zeros(shape=(5, 2))

width_window, height_window = root.winfo_screenwidth(), root.winfo_screenheight()

button = tk.Button(root, text="QUIT", fg="red", command=quit)
button.place(x=20, y=100)


def from_redis_webcam(r, n):
    """Retrieve Numpy array from Redis key 'n'"""
    encoded = r.get(n)
    h, w = struct.unpack('>II',encoded[:8])
    a = np.frombuffer(encoded, dtype=np.uint8, offset=8).reshape(h,w,3)
    return a


def ultra_receive():
    read = r.get("ultrasonic")
    ultrasonic = pickle.loads(read)

    return ultrasonic


def show_frame():
    # ---------------------------------------------------Text
    frame = from_redis_webcam(r, 'webcam')
    ultrasonic_encoded = ultra_receive()
    print(ultrasonic_encoded)

    back_dist = ultrasonic_encoded['back_dist']
    front_dist = ultrasonic_encoded['front_dist']

    print(front_dist)
    print(back_dist)

    front_dist_label = Label(root, text="Front Distance: {}mm".format(front_dist))
    front_dist_label.place(x=20, y=20)

    back_dist_label = Label(root, text="Back Distance: {}mm".format(back_dist))
    back_dist_label.place(x=20, y=50)

    # ------------------------------------------------------Frame
    scale_percent = 100  # percent of original size

    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    cv2image = cv2.cvtColor(resized, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)


show_frame()
root.mainloop()
