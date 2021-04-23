from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.app import App
import sqlite3


conn = sqlite3.connect('app.db')

c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON")

Builder.load_file("customwidgets/projectcard/projectcard.kv")

class ProjectCard(GridLayout):
    def __init__(self, height, name, texture):
        super().__init__()
        self.app = App.get_running_app()
        self.initialised = False
        self.size_hint_y = None
        self.height = height
        self.name = name
        self.ids["name"].text = name
        self.ids["image"].texture = texture


    def name_change(self, focused):
        if not focused:
            tmp_name = self.ids["name"].text
            c.execute(f"SELECT project_name FROM Projects WHERE project_name  = '{tmp_name}'")
            if not c.fetchone() and tmp_name != "None":
                c.execute(f"UPDATE Projects SET project_name  = '{tmp_name}' WHERE project_name = '{self.name}'")
                self.name = self.ids["name"].text
                if self.ids["name_label"].background_color == [0.25, 0.5, 0.75, 1]:
                    c.execute(f"UPDATE Flags SET value  = '{tmp_name}' WHERE flag_name = 'current_project'")
            else:
                self.ids["name"].text = self.name
            conn.commit()


    #def on_text(self):
    #    print(self.ids["name"].text)
    #    if self.initialised:
    #        self.name_change()
    #
    #    self.initialised = True

    def remove(self):
        print(f"\n\n\n{self.name}\n\n\n")
        if self.ids["name_label"].background_color == [0.25, 0.5, 0.75, 1]:
            c.execute(f"UPDATE Flags SET value  = 'None' WHERE flag_name = 'current_project'")
        c.execute(f"DELETE FROM Projects WHERE project_name = '{self.name}'")
        conn.commit()
        self.parent.remove_widget(self)
    
    def selected(self):
        #self.app.project_window.test()
        c.execute(f"UPDATE Flags SET value  = '{self.name}' WHERE flag_name = 'current_project'")
        conn.commit()

        for child in self.parent.children:
            child.ids["name_label"].background_color = (0.45, 0.45, 0.45, 1)
        
        self.ids["name_label"].background_color = (0.25, 0.5, 0.75, 1)
        

