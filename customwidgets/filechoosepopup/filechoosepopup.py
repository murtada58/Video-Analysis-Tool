from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.lang import Builder


Builder.load_file("customwidgets/filechoosepopup/filechoosepopup.kv")

class FileChoosePopup(Popup):
    load = ObjectProperty()


