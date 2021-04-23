import cv2
import numpy as np
import os
import time

# img = cv2.imread('./Reverse_image_search_dataset/images/group_0/group_0_0.jpg')
# img1 = cv2.imread('./Reverse_image_search_dataset/images/group_1/group_1_0.jpg')


# R1 = cv2.calcHist([img],[2],None,[256],[0,256])
# R2 = cv2.calcHist([img1],[2],None,[256],[0,256])
# G1 = cv2.calcHist([img],[1],None,[256],[0,256])
# G2 = cv2.calcHist([img1],[1],None,[256],[0,256])
# B1 = cv2.calcHist([img],[0],None,[256],[0,256])
# B2 = cv2.calcHist([img1],[0],None,[256],[0,256])

# DR = sum(((R1 - R2)**2))
# DG = sum(((G1 - G2)**2))
# DB = sum(((B1 - B2)**2))

# ED = (DR**2) + (DG**2) + (DB**2)
# print(ED)


t0 = time.time()
groups = [f for f in os.listdir("./Reverse_image_search_dataset/images")]
HISTs = []
number_of_videos = 0
number_of_images = 0
for group in groups:
    _, _, group_number = group.partition('_')
    group_number = int(group_number)
    print(number_of_videos)
    images = [f for f in os.listdir(f"./Reverse_image_search_dataset/images/{group}")]
    for image in images:
        img = cv2.imread(f'./Reverse_image_search_dataset/images/{group}/{image}')
        img = cv2.resize(img, (1920, 1080), interpolation = cv2.INTER_LINEAR)
        B = cv2.calcHist([img],[0],None,[256],[0,256])
        G = cv2.calcHist([img],[1],None,[256],[0,256])
        R = cv2.calcHist([img],[2],None,[256],[0,256])
        HISTs.append(((R, G, B), group_number))
        number_of_images += 1
    number_of_videos += 1

EDs = []
t2 = time.time()
histogram_run_time = t2-t0
print(f"histogram took {histogram_run_time}s to run")
j = 0
for histogram in HISTs:
    hist, group_number = histogram
    R, G, B = hist
    group_EDs = []
    print(f"analysed images: {j}")
    for comparison_histogram in HISTs:
        comparison_hist, comparison_group_number = comparison_histogram
        R2, G2, B2 = comparison_hist
        ED = float(np.sqrt(np.sum(((R - R2)**2) + ((G - G2)**2) + ((B - B2)**2))))
        if ED != 0.0:
            group_EDs.append((ED, comparison_group_number))

    EDs.append((group_EDs, group_number))
    j += 1

correct = 0
incorrect  = 0
for ED in EDs:
    ED, group_number = ED
    ED.sort()
    i = 0
    for comparison_ED in ED:
        comparison_ED, comparison_group_number = comparison_ED
        if comparison_group_number == group_number:
            correct += 1
        else:
            incorrect += 1
        i += 1
        if i >= 5:
            break
t1 = time.time()
total_run_time = t1-t0
print(f"histogram took {histogram_run_time}s to run")
print(f"This script took {total_run_time}s to run")
print(f"Total number of analysed videos: {number_of_videos}")
print(f"Total nuber of analysed images: {number_of_images}")
print(f"Number of correct matches: {correct}")
print(f"Number of incorrect matches: {incorrect}")
        