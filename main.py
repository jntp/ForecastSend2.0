# main.py is the main python file of ForecastSend2.0 application
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

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

kv = Builder.load_file("main.kv") # load main.kv file
sm = WindowManager() # load WindowManager upon running

# create screens dictionary that assigns name (ID) to each class
screens = [HomeWindow(name = "home"), MediumRangeWindow(name = "medium_range")]
for screen in screens:
  sm.add_widget(screen)

sm.current = "home" # by default, current screen goes to HomeWindow

# builds the kivy application
class ForecastSendApp(App):
  def build(self):
    return sm

if __name__ == "__main__":
  ForecastSendApp().run()


