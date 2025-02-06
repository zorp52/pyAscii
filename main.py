import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Text, Label, Entry, Scale, Button
from PIL import Image, ImageTk, ImageEnhance

# The entirety of braile unicode characters
ASCII_CHARS = "⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿⡀⡁⡂⡃⡄⡅⡆⡇⡈⡉⡊⡋⡌⡍⡎⡏⡐⡑⡒⡓⡔⡕⡖⡗⡘⡙⡚⡛⡜⡝⡞⡟⡠⡡⡢⡣⡤⡥⡦⡧⡨⡩⡪⡫⡬⡭⡮⡯⡰⡱⡲⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿⢀⢁⢂⢃⢄⢅⢆⢇⢈⢉⢊⢋⢌⢍⢎⢏⢐⢑⢒⢓⢔⢕⢖⢗⢘⢙⢚⢛⢜⢝⢞⢟⢠⢡⢢⢣⢤⢥⢦⢧⢨⢩⢪⢫⢬⢭⢮⢯⢰⢱⢲⢳⢴⢵⢶⢷⢸⢹⢺⢻⢼⢽⢾⢿⣀⣁⣂⣃⣄⣅⣆⣇⣈⣉⣊⣋⣌⣍⣎⣏⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟⣠⣡⣢⣣⣤⣥⣦⣧⣨⣩⣪⣫⣬⣭⣮⣯⣰⣱⣲⣳⣴⣵⣶⣷⣸⣹⣺⣻⣼⣽⣾⣿"

def imgResize(image, new_width, new_height):
    return cv2.resize(image, (new_width, new_height))

def adjustImg(image):
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness_slider.get() / 100)
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(sharpness_slider.get() / 100)
    return image

def imgConvert(image, new_width, new_height):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized_image = imgResize(gray_image, new_width, new_height)
    ascii_str = ""
    for row in resized_image:
        for pixel in row:
            ascii_str += ASCII_CHARS[pixel // (256 // len(ASCII_CHARS))]
        ascii_str += "\n"
    return ascii_str

def fileOpen():
    global image
    file_path = filedialog.askopenfilename()
    if file_path:
        image = cv2.imread(file_path)
        imgRefresh()

def imgRefresh():
    if image is not None:
        adjusted_image = adjustImg(Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))
        ascii_art = imgConvert(np.array(adjusted_image), int(width_entry.get()), int(height_entry.get()))
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, ascii_art)
        imgPreview(adjusted_image)

def imgPreview(image):
    image.thumbnail((200, 200))
    photo = ImageTk.PhotoImage(image)
    preview_label.config(image=photo)
    preview_label.image = photo

root = tk.Tk()
root.title("ASCII Image Converter")
root.geometry("1280x720")

frame = tk.Frame(root)
frame.pack()

width_label = Label(frame, text="Width:")
width_label.pack(side=tk.LEFT)
width_entry = Entry(frame)
width_entry.pack(side=tk.LEFT)
width_entry.insert(0, "20")

height_label = Label(frame, text="Height:")
height_label.pack(side=tk.LEFT)
height_entry = Entry(frame)
height_entry.pack(side=tk.LEFT)
height_entry.insert(0, "20")

brightness_slider = Scale(frame, from_=50, to=150, orient=tk.HORIZONTAL, label="Brightness")
brightness_slider.set(100)
brightness_slider.pack()

sharpness_slider = Scale(frame, from_=50, to=150, orient=tk.HORIZONTAL, label="Sharpness")
sharpness_slider.set(100)
sharpness_slider.pack()

open_button = Button(frame, text="Open Image", command=fileOpen)
open_button.pack()

refresh_button = Button(frame, text="Refresh Image", command=imgRefresh)
refresh_button.pack()

text_widget = Text(root, wrap=tk.WORD, font=("Courier", 8))
text_widget.pack(expand=True, fill=tk.BOTH)

preview_label = tk.Label(root)
preview_label.pack()

root.mainloop()
