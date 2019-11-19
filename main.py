# main.py is the main python file of ForecastSend2.0 application
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# prompts user to select between "one-day precipitation" or "medium-range update" forecasts
class HomeWindow(Screen):
  pass

# prompts user to choose which city or region to send the forecast
class CityWindow(Screen):
  pass

# one-day precipitation: main screen for user entering parameters
class OneDayParameterWindow(Screen):
  pass

# one-day precipitation: for editing the forecast
class OneDayEditWindow(Screen):
  pass

# medium-range update: main window 
class MediumRangeWindow(Screen):
  pass

# preview window for both types of forecasts
class PreviewWindow(Screen):
  pass

class WindowManager(ScreenManager):
  pass

kv = Builder.load_file("main.kv") # DON'T FORGET TO CREATE THIS FILE!!!

# builds the kivy application
class MyMainApp(App):
  def build(self):
    return kv

if __name__ == "__main__":
  MyMainApp().run()


