import cv2
import numpy as np
import os
import time
import csv

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
    for image_name in images:
        img = cv2.imread(f'./Reverse_image_search_dataset/images/{group}/{image_name}')
        img = cv2.resize(img, (1920, 1080), interpolation = cv2.INTER_LINEAR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        H = cv2.calcHist([img],[0],None,[256],[0,256])
        S = cv2.calcHist([img],[1],None,[256],[0,256])
        V = cv2.calcHist([img],[2],None,[256],[0,256])
        HISTs.append(((H, S, V), group_number, image_name))
        number_of_images += 1
    number_of_videos += 1

EDs = []
t2 = time.time()
histogram_run_time = t2-t0
print(f"histogram took {histogram_run_time}s to run")
j = 0
for hist, group_number, image_name in HISTs:
    H, S, V = hist
    group_EDs = []
    print(f"analysed images: {j}")
    for comparison_hist, comparison_group_number, comparison_image_name in HISTs:
        H2, S2, V2 = comparison_hist
        ED = float(np.sqrt(np.sum(((H - H2)**2) + ((S - S2)**2) + ((V - V2)**2))))
        if ED != 0.0:
            group_EDs.append((ED, comparison_group_number, comparison_image_name))

    EDs.append((group_EDs, group_number, image_name))
    j += 1

correct = 0
incorrect  = 0
for ED, group_number, image_name in EDs:
    ED.sort()
    i = 0
    for comparison_ED, comparison_group_number, comparison_image_name in ED:
        if comparison_group_number == group_number:
            correct += 1
        else:
            with open('HSV_histogram_bad_matches.csv','a', newline='') as bad_matches:
                bad_matches_writer = csv.writer(bad_matches, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                bad_matches_writer.writerow([image_name, comparison_image_name])
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
        