import csv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


with open('HSV_LCH_bad_matches.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        image_name = row[0]
        image_name2 = row[1]
        number_of_underscores = 0
        group = ""
        for letter in row[0]:
            if letter == "_":
                number_of_underscores += 1
                if number_of_underscores >= 2:
                    break
            group += letter

        number_of_underscores = 0
        group2 = ""
        for letter in row[1]:
            if letter == "_":
                number_of_underscores += 1
                if number_of_underscores >= 2:
                    break
            group2 += letter

        fig = plt.figure()
        plt.subplot(2, 1, 1)
        img = mpimg.imread(f"./Reverse_image_search_dataset/images/{group}/{image_name}")
        plt.title(image_name)
        imgplot = plt.imshow(img)
        plt.subplot(2, 1, 2)
        img2 = mpimg.imread(f"./Reverse_image_search_dataset/images/{group2}/{image_name2}")
        plt.title(image_name2)
        imgplot = plt.imshow(img2)

        fig.tight_layout(pad=1.0)
        plt.show()
   