import tkinter as tk
import cv2
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from collections import Counter
import webcolors
from tkinter import filedialog, messagebox, Label


class ColorDetectionApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Color Detection App")
        self.root.geometry('800x600')  # Set starting size of window

        # Style configurations
        self.bg_color = "#000000"
        self.button_color = "#FFFFFF"
        self.root.configure(bg=self.bg_color)

        # Status Label
        self.status_label = Label(self.root, text="Select an image to process.", bg=self.bg_color)
        self.status_label.pack(pady=10)

        # Create a button to open an image with custom font and flat style
        self.btn_open = tk.Button(self.root, text='Select Image', command=self.open_image, bg="white", fg="black",
                                  font=("Helvetica", 12), relief=tk.FLAT)
        self.btn_open.pack(pady=10)

        # Create a button to process the image and show colors with custom font and flat style
        self.btn_process = tk.Button(self.root, text='Find Colors', command=self.process_image, bg="white", fg="black",
                                     font=("Helvetica", 12), relief=tk.FLAT, state=tk.DISABLED)
        self.btn_process.pack(pady=10)

        # Create a label to display the image
        self.image_label = tk.Label(self.root, bg=self.bg_color)
        self.image_label.pack(pady=10)

    def open_image(self):
        # Update status label
        self.status_label.config(text="Loading image...")
        self.root.update()

        # Open file dialog to select an image
        file_path = filedialog.askopenfilename()
        if not file_path:
            self.status_label.config(text="Image loading cancelled.")
            return

        # Load and display the image
        self.image = cv2.imread(file_path)
        # imread - read image into a numpy array using opencv library
        if self.image is None:
            messagebox.showerror("Error", "Failed to load the image.")
            self.status_label.config(text="Failed to load the image.")
            return

        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        # cv2.cvtColor() method is used to convert an image from one color space to another.
        self.show_image(self.image)

        # Enable the 'Find Colors' button after the image is loaded
        self.btn_process['state'] = tk.NORMAL
        self.status_label.config(text="Image loaded successfully. Click 'Find Colors' to process.")

    def show_image(self, image):
        # Convert the image to a format that Tkinter can use
        image = Image.fromarray(image)
        image.thumbnail((350, 350))
        image = ImageTk.PhotoImage(image)

        # Update the label with the new image
        self.image_label.configure(image=image)
        self.image_label.image = image  # Keep a reference!


    def process_image(self):
        # Check if the image is loaded
        if not hasattr(self, 'image'):
            messagebox.showerror("Error", "No image loaded. Please select an image first.")
            return

        # Update status label
        self.status_label.config(text="Processing image...")
        self.root.update()

        # Get colors
        number_of_colors = 10
        colors, counts = get_colors(self.image, number_of_colors)

        # Create and display a pie chart
        plt.figure(figsize=(8, 6))
        labels = [closest_color((int(color[0]), int(color[1]), int(color[2]))) for color in colors]
        plt.pie(counts.values(), labels=labels, colors=[color / 255 for color in colors])
        plt.title('Color Distribution')
        plt.show()

        self.status_label.config(text="Done!")


def get_colors(image, number_of_colors):
    # Resize image to reduce the number of pixels
    # Working with smaller images speeds up the process - resize
    modified_image = cv2.resize(image, (600, 400), interpolation=cv2.INTER_AREA)
    #  prepare the image data for the KMeans algorithm. - image array into a 2D array - represents a pixel and each
    #  column represents one of the RGB
    modified_image = modified_image.reshape(modified_image.shape[0] * modified_image.shape[1], 3)

    #  To perform color quantization, effectively reducing the number of colors in the image.
    clf = KMeans(n_clusters=number_of_colors, n_init=10)
    labels = clf.fit_predict(modified_image)

    # count how many pixels are in each cluster/color.
    counts = Counter(labels)
    center_colors = clf.cluster_centers_
    # To sort the colors by their frequency in the image and convert their values from floats to integers.
    ordered_colors = [center_colors[i] for i in counts.keys()]
    rgb_colors = [ordered_colors[i].astype(int) for i in counts.keys()]

    return rgb_colors, counts


def closest_color(requested_color):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_color)
    except ValueError:
        min_colors = {}
        for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_color[0]) ** 2
            gd = (g_c - requested_color[1]) ** 2
            bd = (b_c - requested_color[2]) ** 2
            min_colors[(rd + gd + bd)] = name
        closest_name = min_colors[min(min_colors.keys())]
    return closest_name


# Create the Tkinter window
root = tk.Tk()
app = ColorDetectionApp(root)
root.mainloop()
