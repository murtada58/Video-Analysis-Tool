from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from pages.comparisonpage.comparisonpage import ComparisonWindow
from pages.analysispage.analysispage import AnalysisWindow
from pages.projectpage.projectpage import ProjectWindow
import sqlite3


conn = sqlite3.connect('app.db')

c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON")

Builder.load_file("./pages/analysispage/analysispage.kv")
class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("layout.kv")

class MainApp(App):
    project_window = ProjectWindow()
    comparison_window = ComparisonWindow()
    analysis_window = AnalysisWindow()
    def build(self):
        self.icon = "./images/icon4.webp"
        return kv
    
    def on_stop(self):
        c.execute(f"UPDATE Flags SET value  = 'false' WHERE flag_name = 'analysing'")
        c.execute(f"UPDATE Flags SET value  = 'None' WHERE flag_name = 'current_project'")
        conn.commit()


if __name__ == "__main__":
    TC2_app = MainApp()
    TC2_app.run()