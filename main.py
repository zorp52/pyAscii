import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Text, Label, Entry, Scale, Button, Frame
from PIL import Image, ImageTk, ImageEnhance, ImageOps

ASCII_CHARS = "⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿⡀⡁⡂⡃⡄⡅⡆⡇⡈⡉⡊⡋⡌⡍⡎⡏⡐⡑⡒⡓⡔⡕⡖⡗⡘⡙⡚⡛⡜⡝⡞⡟⡠⡡⡢⡣⡤⡥⡦⡧⡨⡩⡪⡫⡬⡭⡮⡯⡰⡱⡲⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿⢀⢁⢂⢃⢄⢅⢆⢇⢈⢉⢊⢋⢌⢍⢎⢏⢐⢑⢒⢓⢔⢕⢖⢗⢘⢙⢚⢛⢜⢝⢞⢟⢠⢡⢢⢣⢤⢥⢦⢧⢨⢩⢪⢫⢬⢭⢮⢯⢰⢱⢲⢳⢴⢵⢶⢷⢸⢹⢺⢻⢼⢽⢾⢿⣀⣁⣂⣃⣄⣅⣆⣇⣈⣉⣊⣋⣌⣍⣎⣏⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟⣠⣡⣢⣣⣤⣥⣦⣧⣨⣩⣪⣫⣬⣭⣮⣯⣰⣱⣲⣳⣴⣵⣶⣷⣸⣹⣺⣻⣼⣽⣾⣿"

def imgResize(image, newWidth, newHeight):
    return cv2.resize(image, (newWidth, newHeight))

def imgAdjust(image):
    if grayscaleSlider.get() == 1:
        image = ImageOps.grayscale(image)
    
    image = image.convert("RGB")
    
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightnessSlider.get() / 100)
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(sharpnessSlider.get() / 100)
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(saturationSlider.get() / 100)
    
    if sepiaSlider.get() == 1:
        sepiaImage = np.array(image)
        sepiaFilter = np.array([[0.393, 0.769, 0.189],
                               [0.349, 0.686, 0.168],
                               [0.272, 0.534, 0.131]])
        sepiaImage = sepiaImage.dot(sepiaFilter.T)
        sepiaImage = np.clip(sepiaImage, 0, 255).astype(np.uint8)
        image = Image.fromarray(sepiaImage)
    if invertSlider.get() == 1:
        image = ImageOps.invert(image)
    return image

def imgConvert(image, newWidth, newHeight):
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resizedImage = imgResize(grayImage, newWidth, newHeight)
    asciiStr = ""
    for row in resizedImage:
        for pixel in row:
            asciiStr += ASCII_CHARS[pixel // (256 // len(ASCII_CHARS))]
        asciiStr += "\n"
    return asciiStr

def fileOpen():
    global image
    filePath = filedialog.askopenfilename()
    if filePath:
        image = cv2.imread(filePath)
        refreshImage()

def refreshImage():
    if image is not None:
        adjustedImage = imgAdjust(Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))
        asciiArt = imgConvert(np.array(adjustedImage), int(widthEntry.get()), int(heightEntry.get()))
        textWidget.delete(1.0, tk.END)
        textWidget.insert(tk.END, asciiArt)
        displayPreview(adjustedImage)

def displayPreview(image):
    image.thumbnail((200, 200))
    photo = ImageTk.PhotoImage(image)
    previewLabel.config(image=photo)
    previewLabel.image = photo

root = tk.Tk()
root.title("ASCII Image Converter")
root.geometry("1280x720")

controlFrame = Frame(root)
controlFrame.pack(fill=tk.X, padx=10, pady=10)

widthLabel = Label(controlFrame, text="Width:")
widthLabel.pack(side=tk.LEFT)
widthEntry = Entry(controlFrame, width=5)
widthEntry.pack(side=tk.LEFT, padx=5)
widthEntry.insert(0, "20")

heightLabel = Label(controlFrame, text="Height:")
heightLabel.pack(side=tk.LEFT)
heightEntry = Entry(controlFrame, width=5)
heightEntry.pack(side=tk.LEFT, padx=5)
heightEntry.insert(0, "20")

brightnessSlider = Scale(controlFrame, from_=50, to=150, orient=tk.HORIZONTAL, label="Brightness")
brightnessSlider.set(100)
brightnessSlider.pack(side=tk.LEFT, padx=10)

sharpnessSlider = Scale(controlFrame, from_=50, to=150, orient=tk.HORIZONTAL, label="Sharpness")
sharpnessSlider.set(100)
sharpnessSlider.pack(side=tk.LEFT, padx=10)

saturationSlider = Scale(controlFrame, from_=50, to=150, orient=tk.HORIZONTAL, label="Saturation")
saturationSlider.set(100)
saturationSlider.pack(side=tk.LEFT, padx=10)

grayscaleSlider = tk.IntVar()
tk.Checkbutton(controlFrame, text="Grayscale", variable=grayscaleSlider).pack(side=tk.LEFT, padx=10)

sepiaSlider = tk.IntVar()
tk.Checkbutton(controlFrame, text="Sepia", variable=sepiaSlider).pack(side=tk.LEFT, padx=10)

invertSlider = tk.IntVar()
tk.Checkbutton(controlFrame, text="Invert Colors", variable=invertSlider).pack(side=tk.LEFT, padx=10)

openButton = Button(controlFrame, text="Open Image", command=fileOpen)
openButton.pack(side=tk.LEFT, padx=10)

refreshButton = Button(controlFrame, text="Refresh Image", command=refreshImage)
refreshButton.pack(side=tk.LEFT, padx=10)

previewFrame = Frame(root)
previewFrame.pack(fill=tk.X, padx=10, pady=10)

previewLabel = tk.Label(previewFrame)
previewLabel.pack()

textFrame = Frame(root)
textFrame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

textWidget = Text(textFrame, wrap=tk.WORD, font=("Courier", 8))
textWidget.pack(expand=True, fill=tk.BOTH)

root.mainloop()
