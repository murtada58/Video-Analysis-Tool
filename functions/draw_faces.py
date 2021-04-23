import face_recognition as fr
import cv2
import sqlite3
import time


conn = sqlite3.connect('app.db')

c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON")

def draw_faces(project_id, person_id, frame_number, frame):
    c.execute(f"SELECT x1, y1, x2, y2, face_distance, person_id, analysed FROM face_recog_data WHERE project_id = '{project_id}' AND person_id = '{person_id}' AND frame_number = '{frame_number}'")
    all_data = c.fetchall()
    for data in all_data:
        print(data)
        if data != None:
            top, right, bottom, left, face_distance, person_id, analysed = data

            if analysed == 1:
                c.execute(f"SELECT image_name FROM Comparison_Images WHERE project_id = '{project_id}' AND ID = '{person_id}'")
                
                person_name = c.fetchone()[0]

                # Draw box
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 0), 2)

                # Draw label
                cv2.rectangle(frame, (left, bottom), (right, bottom + 42), (0, 0, 0), -1)
                cv2.putText(frame, person_name, (left + 4, bottom + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                # Draw face distance label
                cv2.rectangle(frame, (left, bottom + 32), (right, bottom + 42 + 32), (0, 0, 0), -1)
                cv2.putText(frame, "FD: {:.5f}".format(face_distance), (left + 4, bottom + 30 + 32), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    return frame