import face_recognition as fr
import cv2
from functions.face_recog import face_recog
import sqlite3


conn = sqlite3.connect('app.db')

c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON")
def analyse():
    c.execute("SELECT value FROM Flags WHERE flag_name = 'current_project'")
    current_project = c.fetchone()[0]
    c.execute(f"SELECT id FROM Projects WHERE project_name = '{current_project}'")
    project_id = c.fetchone()[0]
    # for image_name, path, comnparison_id in c.execute(f"SELECT image_name, image_path, id FROM Comparison_Images WHERE project_id = '{project_id}'"):
    #     comparison_image_id = comnparison_id
    #     name = image_name
    #     comparison_encoding = fr.face_encodings(fr.load_image_file(path))


    c.execute(f"SELECT video_path FROM Projects WHERE project_name = '{current_project}'")
    video_path = c.fetchone()[0]
    print(video_path)
    cap = cv2.VideoCapture(video_path)

    c.execute(f"SELECT total_frames FROM Projects WHERE project_name = '{current_project}'")
    total_frames = c.fetchone()[0]
    frame_num_index = 0
    frame_gap = total_frames - 1
    while(True):
        print(frame_num_index)
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(frame_num_index))
        print(frame_num_index)
        ret, frame = cap.read()
        if ret:
            all_data = []
            for data in c.execute(f"SELECT image_name, image_path, id, encoding FROM Comparison_Images WHERE project_id = '{project_id}'"):
                all_data.append(data)
            for data in all_data:
                image_name, path, comparison_image_id, comparison_encoding = data

                c.execute(f"SELECT frame_number FROM face_recog_data WHERE project_id = '{project_id}' AND person_id = '{comparison_image_id}' AND frame_number = {int(cap.get(cv2.CAP_PROP_POS_FRAMES))}")
                frame_num = c.fetchone()
                print(frame_num)
                if frame_num == None:
                    face_recog(frame, comparison_encoding, image_name, int(cap.get(cv2.CAP_PROP_POS_FRAMES)), project_id, comparison_image_id, total_frames)
                print("next image")


        frame_num_index += frame_gap
        if frame_num_index >= total_frames:
            frame_gap /= 2
            frame_num_index = 0

        c.execute("SELECT value FROM Flags WHERE flag_name = 'analysing'")
        still_analysing = c.fetchone()[0]
        if still_analysing == "false":
            break