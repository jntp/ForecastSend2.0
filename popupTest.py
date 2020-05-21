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
  errorIntLabel = ObjectProperty(None)

  def validate(self, input, value, min_value = 0, max_value = 3):
    try:
      print(min_value, max_value) # test
      status = float(min_value) <= float(value) <= float(max_value)
    except Exception as e:
      print("OOPS!") 
      self.errorIntLabel.text = "WTF"

  def testLol(self,  min_value, max_value):
    print("TESTING WORKED!!!")

    if self.errorIntLabel.text == "":
      self.errorIntLabel.text = "Enter a value between " + str(min_value) + " and " + str(max_value) + "." 
      firstTime = False
    else:
      print("LOLITA!")

class WindowManager(ScreenManager):
  pass


## Popup Windows

# def excessChar()
  # excessChar = Popup(title = "ERROR", content = Label(text = "Error! No more than 2 characters allowed."), size_hint = (None, None), size = (400, 400))
  # excessChar.open() 

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

# Getting somewhere... finish testLol function 
