from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty 

KV = """

<ValidateLabel>:
  size_hint: (None, None)
  size: (60, 20)
  Label:
    id: Label
    text: "Must be a whole number divisible by 10."

<MyInput>:
  foreground_color: (0,1,0,1) if root.validated else (1,0,0,1)
  size_hint: 0.05, 0.12

FloatInput: 

"""

class HomeWindow(Screen):
  intLabel = ObjectProperty(None)

  def __init__(self, **kwargs):
    self.intLabel.bind(text = self.validate)

  def validate


class WindowManager(ScreenManager):
  pass

sm = WindowManager()
kv = Builder.load_file("popupTest.kv")

screens = [HomeWindow(name = "home")]
for screen in screens:
  sm.add_widget(screen)

sm.current = "home" 

class TestApp(App):
  def build(self):
    return sm
  
if __name__ == "__main__":
  TestApp().run() 

# You left off writing validate function? How will the popups appear? 
