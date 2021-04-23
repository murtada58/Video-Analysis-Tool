from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from customwidgets.filechoosepopup.filechoosepopup import FileChoosePopup
from customwidgets.comparisoncard.comparisoncard import ComparisonCard
from kivy.clock import Clock
import json
import face_recognition as fr
import cv2
import sqlite3
import numpy as np

conn = sqlite3.connect('app.db')

c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON")

Builder.load_file("./pages/comparisonpage/comparisonpage.kv")

class ComparisonWindow(Screen):
    image_add = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.entered = False

    def start(self):
        c.execute("SELECT value FROM Flags WHERE flag_name = 'current_project'")
        project_name = c.fetchone()[0]
        print(project_name)
        c.execute(f"SELECT id FROM Projects WHERE project_name = '{project_name}'")
        project_id = c.fetchone()[0]
        for image, path in c.execute(f"SELECT image_name, image_path FROM Comparison_Images WHERE project_id = '{project_id}'"):
            print(path)
            temp = ComparisonCard(100, image, path)
            self.image_add.add_widget(temp)


    def on_enter(self):
        if not self.entered:
            self.entered = True
            # self.remove_widget(self.children)
            #c.execute("SELECT project_name FROM Projects")
            #print(c.fetchall())
            #c.execute("SELECT image_name FROM Comparison_Images")
            #print(c.fetchall())
            #c.execute("SELECT x1 FROM Face_Recog_Data")
            #print(c.fetchall())
        
        c.execute("SELECT value FROM Flags WHERE flag_name = 'current_project'")
        project_name = c.fetchone()[0]
        self.ids["current_project"].text = project_name
        while(self.image_add.children):
            self.image_add.remove_widget(self.image_add.children[0])

        c.execute(f"SELECT fps, total_frames, analysed_frames FROM Projects WHERE project_name = '{project_name}'")
        fps, total_number_of_frames, analysed_frames = c.fetchone()
        print(fps)
        print(total_number_of_frames)
        print(analysed_frames)
        self.ids["total_frames"].text = str(total_number_of_frames)
        self.ids["analysed_frames"].text = str(analysed_frames)
        self.ids["fps"].text = str(fps)
        self.start()


    def add_image(self, selection):
        print(selection)
        c.execute("SELECT value FROM Flags WHERE flag_name = 'current_project'")
        project_name = c.fetchone()[0]
        c.execute(f"SELECT id FROM Projects WHERE project_name = '{project_name}'")
        project_id = c.fetchone()[0]
        c.execute(f"SELECT image_name FROM Comparison_Images")
        names = []
        for name in c.fetchall():
            names.append(name[0])

        i = 0
        while (f"image{i}" in names):
            i += 1

        comparison_encoding = json.dumps(np.array(fr.face_encodings(fr.load_image_file(selection[0]))).tolist())

        c.execute(f"INSERT INTO Comparison_images(project_id, image_name, image_path, encoding) VALUES ({project_id}, 'image{i}', '{selection[0]}', '{comparison_encoding}')")
        conn.commit()
        temp = ComparisonCard(100, f"image{i}", selection[0])
        self.image_add.add_widget(temp)
        self.the_popup.dismiss()
    

    def open_popup(self):
        self.popup_id = id
        self.the_popup = FileChoosePopup(load=self.add_image, title="Choose an image")
        self.the_popup.open()