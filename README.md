# ColorDetectionApp

How to run app? 

python color_detection_app.py



Libraries:
    1. tkinter: A standard Python interface to the Tk GUI toolkit. Used for creating the graphical user interface.
    2. cv2 (OpenCV): Open-source computer vision and machine learning software library. Used for image processing tasks.
    3. PIL (Pillow): Python Imaging Library, adds image processing capabilities to your Python interpreter. Used for opening, manipulating, and saving many different image file formats.
    4. matplotlib: A plotting library for Python and its numerical mathematics extension NumPy. Used for creating the pie chart for color distribution.
    5. sklearn (Scikit-learn): A machine learning library for Python. It provides simple and efficient tools for predictive data analysis. Used for KMeans clustering to identify dominant colors.
    6. collections (Counter): A built-in Python library. Counter is a dict subclass for counting hashable objects. It's used to count the occurrences of each color.
    7. webcolors: A Python library for working with color names and color value formats defined by the HTML and CSS specifications for use in documents on the Web.

Istall using pip:

pip install opencv-python-headless matplotlib pandas
pip install tk
pip install webcolors


How It Works:

When you run the script, a window opens with two buttons ('Select Image' and 'Find Colors') and a status label.
Clicking 'Select Image' allows you to select an image file. The selected image is displayed in the window, and the 'Find Colors' button is enabled.
When you click 'Find Colors', the application processes the image. It uses K Means clustering to find the dominant colors and then matches these colors to the closest named colors using the webcolors library.
The results are displayed as a pie chart showing the distribution of the dominant colors in the image, and each slice of the pie is labeled with the name of the color and its RGB value.
Throughout the process, the status label updates to inform you of the current action (loading image, processing image, etc.)

Problems: 

why we hve exact number of colors ? 

Automatically determining the exact number of distinct colors in an image is quite complex and subjective, especially since digital images are composed of pixels with potentially slight color variations due to lighting, shadows, and noise.

However, if you want to dynamically estimate the number of significant color clusters in the image, you can use methods such as the Elbow Method, which is often used to determine the optimal number of clusters in KMeans clustering. Keep in mind that this method provides an estimation and might not always match the exact number of perceived distinct colors.
