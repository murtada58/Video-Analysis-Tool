from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from customwidgets.filechoosepopup.filechoosepopup import FileChoosePopup
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
#from customwidgets.card.card import Card
from customwidgets.projectcard.projectcard import ProjectCard
import sqlite3
import cv2


conn = sqlite3.connect('app.db')

c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON")

Builder.load_file("./pages/projectpage/projectpage.kv")

class ProjectWindow(Screen):
    project_add = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.entered = False
        Clock.schedule_once(self.start)

    def start(self, time):
        for project, path in c.execute("SELECT project_name, video_path FROM Projects"):
            print(f"Loading project from {path}")
            cap = cv2.VideoCapture(path)
            ret, frame = cap.read()
            if ret:
                buf1 = cv2.flip(frame, 0)
                buf = buf1.tostring()
                image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            else:
                image_texture =''
            temp = ProjectCard(100, project, image_texture)
            self.project_add.add_widget(temp)

    def on_start_button(self):
        c.execute(f"SELECT value FROM Flags WHERE flag_name = 'current_project'")
        if c.fetchone()[0] != "None":
            return True
        else:
            popup = Popup(title='Select a project',
                content=Label(text='Please Select a project to continue\n(Press on a project "Name:" label to select)'),
                size_hint=(None, None), size=(350, 150))
            popup.open()
            return False

    def on_enter(self):
        if not self.entered:
            self.entered = True
            #c.execute("SELECT project_name FROM Projects")
            #print(c.fetchall())
            #c.execute("SELECT image_name FROM Comparison_Images")
            #print(c.fetchall())
            #c.execute("SELECT x1 FROM Face_Recog_Data")
            #print(c.fetchall())
    
    def test(self):
        print("this is a test")

    def add_project(self, selection):
        print(f"added project at {selection}")
        c.execute("SELECT project_name FROM Projects")
        names = []
        for name in c.fetchall():
            names.append(name[0])

        i = 0
        while (f"video{i}" in names):
            i += 1

        cap = cv2.VideoCapture(selection[0])
        total_number_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        ret, frame = cap.read()
        if ret:
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        #print(image_texture)
        c.execute(f"INSERT INTO Projects(project_name, video_path, total_frames, fps) VALUES ('video{i}', '{selection[0]}', '{total_number_of_frames}', '{fps}')")
        conn.commit()
        temp = ProjectCard(100, f"video{i}", image_texture)
        self.project_add.add_widget(temp)
        self.the_popup.dismiss()
    

    def open_popup(self):
        self.popup_id = id
        self.the_popup = FileChoosePopup(load=self.add_project, title="Choose a video")
        self.the_popup.open()