# libraries
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from collections import Counter


#  function to get the most frequent colors:
def get_colors(image, number_of_colors):
    # Resize image to reduce the number of pixels
    modified_image = cv2.resize(image, (600, 400), interpolation=cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0] * modified_image.shape[1], 3)

    clf = KMeans(n_clusters=number_of_colors)
    labels = clf.fit_predict(modified_image)

    counts = Counter(labels)
    center_colors = clf.cluster_centers_
    ordered_colors = [center_colors[i] for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]

    return rgb_colors, counts

# function to match the colors to their names
def getColorName(R, G, B):
    minimum = 10000
    csv = pd.read_csv('colors.csv', names=["color", "color_name", "hex", "R", "G", "B"], header=None)
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if(d <= minimum):
            minimum = d
            cname = csv.loc[i, "color_name"]

    return cname

# main part of the script that uses the functions defined above. This part of the code loads the image,
# gets the most frequent colors, and then displays the results:
def main():
    # Load an image
    image_path = 'path_to_your_image.jpg'  # Change this to your image path
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB

    # Get colors
    number_of_colors = 8  # You can change this value
    colors, counts = get_colors(image, number_of_colors)

    # Show image
    plt.figure(figsize=(14, 8))
    plt.subplot(1, 2, 1)
    plt.imshow(image)
    plt.title('Image')

    # Show pie chart
    plt.subplot(1, 2, 2)
    plt.pie(counts.values(), labels=[getColorName(*colors[i]) for i in counts.keys()],
            colors=[colors[i] / 255 for i in counts.keys()])
    plt.title('Color Distribution')
    plt.show()


if __name__ == "__main__":
    main()
