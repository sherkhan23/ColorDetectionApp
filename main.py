import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from matplotlib import colors, pyplot as plt
from PIL import Image, ImageTk
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color  # Import the convert_color function
import webcolors

# Set the Matplotlib backend
import matplotlib
matplotlib.use('TkAgg')

# Rest of your code...

def closest_color(requested_color):
    min_colors = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        color_rgb = webcolors.hex_to_rgb(key)
        delta = sum((abs(c1 - c2) for c1, c2 in zip(requested_color, color_rgb)))
        min_colors[delta] = name

    return min_colors[min(min_colors.keys())]


def detect_colors(image_path):
    # Load the image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Reshape the image to a list of pixels
    pixels = image.reshape((-1, 3))

    # Perform K-Means clustering to find dominant colors
    k = 5  # You can adjust the number of dominant colors to find
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.2)
    _, labels, centers = cv2.kmeans(pixels.astype(np.float32), k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)

    # Convert centers to RGB format
    rgb_centers = [tuple(center) for center in centers]

    # Map RGB values to color names using webcolors
    color_names = [closest_color(rgb) for rgb in rgb_centers]

    return rgb_centers, color_names

def browse_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        rgb_colors, color_names = detect_colors(file_path)
        show_detected_colors(rgb_colors, color_names)
        show_image(file_path)


def show_detected_colors(rgb_colors, color_names):
    plt.figure(figsize=(5, 5))
    for rgb_color, color_name in zip(rgb_colors, color_names):
        plt.subplot(1, len(rgb_colors), rgb_colors.index(rgb_color) + 1)
        plt.imshow([[rgb_color]])
        plt.axis('off')
        plt.title(f'{color_name}\n#{rgb_color[0]:02x}{rgb_color[1]:02x}{rgb_color[2]:02x}')
    plt.show()



def show_image(image_path):
    img = Image.open(image_path)
    img.thumbnail((400, 400))
    img = ImageTk.PhotoImage(img)
    panel = tk.Label(root, image=img)
    panel.image = img
    panel.pack()


root = tk.Tk()
root.title("Image Color Detection")

browse_button = tk.Button(root, text="Browse Image", command=browse_image)
browse_button.pack()

root.mainloop()
