from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.app import App
import sqlite3


conn = sqlite3.connect('app.db')

c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON")

Builder.load_file("customwidgets/comparisoncard/comparisoncard.kv")

class ComparisonCard(GridLayout):
    def __init__(self, height, name, image):
        super().__init__()
        self.app = App.get_running_app()
        self.initialised = False
        self.size_hint_y = None
        self.height = height
        self.name = name
        self.ids["name"].text = name
        self.ids["image"].source = image


    def name_change(self, focused):
        if not focused:
            tmp_name = self.ids["name"].text
            old_name = self.name
            new_name = tmp_name
            c.execute(f"SELECT image_name FROM Comparison_Images WHERE image_name  = '{tmp_name}'")
            if not c.fetchone():
                c.execute(f"UPDATE Comparison_Images SET image_name  = '{tmp_name}' WHERE image_name = '{self.name}'")
                conn.commit()
                self.name = self.ids["name"].text
            else:
                self.ids["name"].text = self.name


    def remove(self):
        print(f"\n\n\n{self.name}\n\n\n")
        c.execute(f"DELETE FROM Comparison_Images WHERE image_name = '{self.name}'")
        conn.commit()
        self.parent.remove_widget(self)
