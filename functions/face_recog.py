import face_recognition as fr
import cv2
import sqlite3
import time
import json
import numpy as np

conn = sqlite3.connect('app.db')

c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON")

def face_recog(frame, comparison_encoding, name, frame_number, project_id, person_id, total_frames):
    #print("doing something in this process")
    #time.sleep(1)
    #print("finished and will call proccess again")
    #face_recog()
    face_locations = fr.face_locations(frame)
    face_encodings = fr.face_encodings(frame, face_locations)
    #print(f"face locations: {face_locations}\n face encodings: {face_encodings}")
    if not face_locations:
        c.execute(f"INSERT INTO Face_Recog_Data(project_id, person_id, frame_number, analysed, face_distance, x1, y1, x2, y2) VALUES ({project_id}, {person_id}, {frame_number}, {0}, {0}, {0}, {0}, {0}, {0})")
        conn.commit()
        # self.all_face_locations[str(self.frame_num)] = None
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        face_distance = fr.face_distance(np.array(json.loads(comparison_encoding)), face_encoding)[0]
        #print(face_distance)
        
        # Draw box
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 0), 2)

        # Draw label
        cv2.rectangle(frame, (left, bottom), (right, bottom + 42), (0, 0, 0), -1)
        cv2.putText(frame, name, (left + 4, bottom + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        #print(top, right, bottom, left)
        #print(person_id)
        c.execute(f"INSERT INTO Face_Recog_Data(project_id, person_id, frame_number, analysed, face_distance, x1, y1, x2, y2) VALUES ({project_id}, {person_id}, {frame_number}, {1}, {face_distance}, {top}, {right}, {bottom}, {left})")
        conn.commit()
        
        color_bar_index = int(frame_number * (511 / total_frames))
        print("\n\n\n ids below")
        print(person_id)
        print(project_id)
        c.execute(f"SELECT face_distance FROM Color_Bar WHERE number = {color_bar_index} AND image_id = '{person_id}' AND project_id = '{project_id}'")
        color_bar_fd = c.fetchone()
        #print("the colorbar fd:")
        #print(color_bar_fd)
        if color_bar_fd == None:
            c.execute(f"INSERT INTO Color_Bar(project_id, image_id, number, face_distance) VALUES ({project_id}, {person_id}, {color_bar_index}, {face_distance})")
            conn.commit()
        elif color_bar_fd[0] > face_distance:
            c.execute(f"UPDATE Color_Bar SET face_distance  = {face_distance} WHERE number = {color_bar_index} AND image_id = '{person_id}' AND project_id = '{project_id}'")
            conn.commit()
        