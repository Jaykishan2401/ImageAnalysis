import tkinter as tk
import PIL
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
from tkinter import Frame, Label, CENTER
import google.generativeai as genai


GOOGLE_API_KEY = "XXX"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')


window = tk.Tk()
window.geometry('800x600')
window.title("Image Analysis")
b1 = tk.Button(window, text="Upload Files",
               width=20, command=lambda: upload_file())
b1.grid(row=2, columnspan=3)
l1 = tk.Label(window, text="Image Analysis", width=30)
l1.grid(row=3, column=0)
l2 = tk.Label(window, text="Text Extraction", width=30)
l2.grid(row=3, column=1)
l3 = tk.Label(window, text="Visual Element Segmentation", width=30)
l3.grid(row=3, column=2)
def upload_file():
    f_types = [('Jpg Files', '*.jpg'),
               ('PNG Files', '*.png')]
    filename = tk.filedialog.askopenfilename(filetypes=f_types)
    img = Image.open(filename)
    img = img.resize((300, 300))
    img = ImageTk.PhotoImage(img)
    l_img = tk.Label(window, image=img)
    l_img.grid(row=1, columnspan=3)
    l_img.image = img

    response = model.generate_content(["Analyze the image.", Image.open(filename)], stream=True)
    response.resolve()
    t1 = Message(window, text=response.text)
    t1.grid(row=4, column=0)

    response = model.generate_content(["Extract text from the image. Provide output as a json file", Image.open(filename)],
                                      stream=True)
    response.resolve()
    t2 = Message(window, text=response.text)
    t2.grid(row=4, column=1)

    img2 = Image.open(filename)
    grayscale_image = img2.convert("L")
    # Apply thresholding (simple example)
    threshold = 128
    image_segmented = grayscale_image.point(lambda p: p > threshold and 255)
    # Display the segmented image
    image_segmented = image_segmented.resize((100, 100))
    image_segmented = ImageTk.PhotoImage(image_segmented)
    l_img2 = tk.Label(window, image=image_segmented)
    l_img2.place(x=550, y=400)
    l_img2.image = image_segmented



window.mainloop()

