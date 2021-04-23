import cv2
import os

files = [f for f in os.listdir("./Reverse_image_search_dataset/videos")]

group_number = 0
for filename in files:
    os.mkdir(f"./Reverse_image_search_dataset/images/group_{group_number}")
    cap = cv2.VideoCapture(f"./Reverse_image_search_dataset/videos/{filename}")
    total_number_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = total_number_of_frames // 10
    frame_number = 0
    while True:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        success, img = cap.read()
        if not success:
            break
        cv2.imwrite(f"./Reverse_image_search_dataset/images/group_{group_number}/group_{group_number}_{frame_number}.jpg", img)
        frame_number += interval

    group_number += 1
    print(f"moving on to next video ({group_number})")