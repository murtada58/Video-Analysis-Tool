from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from customwidgets.analysiscard.analysiscard import AnalysisCard
from functions.face_recog import face_recog
from functions.analyse import analyse
from functions.draw_faces import draw_faces
import face_recognition as fr
import cv2
import multiprocessing
import sqlite3


conn = sqlite3.connect('app.db')

c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON")

Builder.load_file("./pages/analysispage/analysispage.kv")

class AnalysisWindow(Screen):
    image_add = ObjectProperty(None)
    current_image = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.entered = False
        self.play = False

    def on_enter(self):
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._keydown)
        c.execute("SELECT value FROM Flags WHERE flag_name = 'current_project'")
        project_name = c.fetchone()[0]
        c.execute(f"UPDATE Flags SET value  = 'false' WHERE flag_name = 'analysing'")
        conn.commit()
        c.execute(f"SELECT video_path FROM Projects WHERE project_name = '{project_name}'")
        video_path = c.fetchone()[0]
        self.cap = cv2.VideoCapture(video_path)
        Clock.schedule_once(self.play_video, 1/60)
    
        while(self.image_add.children):
            self.image_add.remove_widget(self.image_add.children[0])
     
        c.execute("SELECT value FROM Flags WHERE flag_name = 'current_project'")
        self.project_name = c.fetchone()[0]
        c.execute(f"SELECT id FROM Projects WHERE project_name = '{project_name}'")
        self.project_id = c.fetchone()[0]

        self.analyse = multiprocessing.Process(target=analyse)
        
        for image_name, path, person_id in c.execute(f"SELECT image_name, image_path, id FROM Comparison_Images WHERE project_id = '{self.project_id}'"):
            print("test")
            self.person_id = person_id
            self.comaprison_image_name = image_name
            self.ids["current_image"].values.append(image_name)
            #self.comparison_encoding = fr.face_encodings(fr.load_image_file(path))
            temp = AnalysisCard(100, image_name, path)
            self.image_add.add_widget(temp)

        self.ids["current_image"].text = self.comaprison_image_name

        c.execute(f"SELECT fps, total_frames, analysed_frames FROM Projects WHERE project_name = '{project_name}'")
        self.fps, self.total_number_of_frames, self.analysed_frames = c.fetchone()   
        self.ids["fps"].text = str(self.fps)
        self.ids["frame_seeker"].max = self.total_number_of_frames


        self.color_bar = []
        divisions = 255
        for i in range(divisions + 1):
            button = Button(
                            background_color=(1, ((i/divisions)), ((i/divisions)), 1),
                            disabled=True,
                            background_disabled_normal=""
                        )
            self.color_bar.append(button)
            self.ids["color_bar"].add_widget(self.color_bar[i])
        for i in range(divisions + 1):
            button = Button(
                            background_color=(1 - ((i/divisions)), 1, 1 - ((i/divisions)), 1),
                            disabled=True,
                            background_disabled_normal=""
                        )
            self.color_bar.append(button)
            self.ids["color_bar"].add_widget(self.color_bar[i + 256])
        self.color_bar[400].background_color = (0, 0, 0, 1)

        for i in range(len(self.color_bar)):
            self.color_bar[i].background_color = (0, 0, 0, 1)
        
        self.update_color_bar(0)
        Clock.schedule_interval(self.update_color_bar, 5)

        self.entered = True

    def update_color_bar(self, time):
        c.execute(f"SELECT number, face_distance FROM Color_Bar WHERE project_id = '{self.project_id}' AND image_id = '{self.person_id}'")
        all_data = c.fetchall()
        all_data.sort()
        for i in range(512):
            self.color_bar[i].background_color = (0, 0, 0 ,1)
        if all_data:
            data_index = 0
            for i in range(512):
                if i == all_data[data_index][0]:
                    if all_data[data_index][1] < 0.5:
                        self.color_bar[i].background_color = (1, all_data[data_index][1] * 2, all_data[data_index][1] * 2, 1)
                    else:
                        self.color_bar[i].background_color = ((1 - all_data[data_index][1]) * 2, 1, (1 - all_data[data_index][1]) * 2, 1)
                    data_index = min(data_index + 1, len(all_data) - 1)
                

    def control_buttons(self, button):
        if button == "play":
            self.play = not self.play
            self.play_video(0)
        elif button == "speed_up":
            self.fps *= 2
            c.execute(f"UPDATE Projects SET fps  = '{self.fps}' WHERE project_name = '{self.project_name}'")
            self.ids["fps"].text = str(self.fps)
            conn.commit()
        elif button == "slow_down":
            self.fps /= 2
            c.execute(f"UPDATE Projects SET fps  = '{self.fps}' WHERE project_name = '{self.project_name}'")
            self.ids["fps"].text = str(self.fps)
            conn.commit()
        else:
            # replay
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            #self.ids["current_frame"].text = str(int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)))
            ret, frame = self.cap.read()
            if ret:
                buf1 = cv2.flip(frame, 0)
                buf = buf1.tostring()
                image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.ids["video_player"].texture = image_texture
            self.ids["current_frame"].text = str(int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)))
            self.ids["frame_seeker"].value = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))

    def play_video(self, time):
        
        #print(time)
        if self.play:
            Clock.schedule_once(self.play_video, (1/self.fps))
        ret, frame = self.cap.read()
        if ret:
            #face_recog(frame, self.comparison_encoding, self.comaprison_image_name)
            draw_faces(self.project_id, self.person_id, int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)), frame)

            # self.ids["face_distance"].text = str(face_distance)
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.ids["video_player"].texture = image_texture
        else:
            if self.play:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        self.ids["current_frame"].text = str(int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)))
        self.ids["frame_seeker"].value = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))


    def analysis(self, button):
        
        if button.text == "Start analysis":
            button.text = "Stop analysis"
            #p1 = multiprocessing.Process(target=face_recog)
            #p1.start()
            c.execute(f"UPDATE Flags SET value  = 'true' WHERE flag_name = 'analysing'")
            conn.commit()
            self.analyse.start()
        else:
            #p1.join()
            c.execute(f"UPDATE Flags SET value  = 'false' WHERE flag_name = 'analysing'")
            conn.commit()
            self.analyse.join()
            self.analyse = multiprocessing.Process(target=analyse)
            button.text = "Start analysis"



    def on_slider_val_change(self, value):
        if self.cap.get(cv2.CAP_PROP_POS_FRAMES) != value:
            self.play = False
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, value)
            self.play_video(0)

    def change_current_image(self, image_name):
        print(image_name)
        c.execute(f"SELECT id FROM Comparison_Images WHERE project_id = '{self.project_id}' AND image_name = '{image_name}'")
        self.person_id = c.fetchone()[0]
        self.comparison_image_name = image_name
        if self.entered:
            self.update_color_bar(0)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._keydown)
        self._keyboard = None
            
    def _keydown(self, window, keycode, text, modifiers):
        print("pressed key")
        if keycode[1] == 'd' or keycode[1] == 'right':
            self.play = False
            print("right")
            self.play_video(0)
        elif keycode[1] == 'a' or keycode[1] == 'left':
            self.play = False
            print("left")
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)) - 2)
            self.play_video(0)
        elif keycode[1] == 'spacebar':
            print("space")
            self.play = not self.play
            self.play_video(0)
            
