import cv2
import numpy as np
import os
import time


t0 = time.time()
groups = [f for f in os.listdir("./Reverse_image_search_dataset/images")]
HISTs = []
number_of_videos = 0
number_of_images = 0
all_images = []
for group in groups:
    _, _, group_number = group.partition('_')
    group_number = int(group_number)
    print(number_of_videos)
    images = [f for f in os.listdir(f"./Reverse_image_search_dataset/images/{group}")]
    group_EDs = []
    for image in images:
        img = cv2.imread(f'./Reverse_image_search_dataset/images/{group}/{image}')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (960, 540), interpolation = cv2.INTER_LINEAR)
        all_images.append((img, group_number))
        number_of_images += 1
    number_of_videos += 1

EDs = []
i = 0
for img, group_number in all_images:
    group_EDs = []
    print(f"analysed images {i}")
    for img2, group_number2 in all_images:
        ED = float(np.sqrt(np.sum(cv2.absdiff(img, img2)**2))) # subtract rounds to 0 yielding much worse results, absdiff gets the absolute difference which yeields better results
        if ED != 0.0:
            group_EDs.append((ED, group_number2))
    EDs.append((group_EDs, group_number))    
    i += 1

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
print(f"This script took {total_run_time}s to run")
print(f"Total number of analysed videos: {number_of_videos}")
print(f"Total nuber of analysed images: {number_of_images}")
print(f"Number of correct matches: {correct}")
print(f"Number of incorrect matches: {incorrect}")