# main.py is the main python file of ForecastSend2.0 application
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.clock import Clock


# used to store text inputted in text boxes
class SaveText:
  # for saving text inputted in the "medium-range update" box
  def UpdateSave(self, updateText):
    self.textSave = updateText

# prompts user to select between "one-day precipitation" or "medium-range update" forecasts
class HomeWindow(Screen):
  # when user clicks "one-day precipitation" button
  def one_day_precip(self):
    sm.current = "one_day_main" # switch to one-day precipitation screen

  # when user clicks "medium-range update" button
  def medium_range(self):
    sm.current = "medium_range" # switch to medium-range update screen

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
  update = ObjectProperty(None)
  character_count = ObjectProperty(None)

  def on_enter(self):
    event = Clock.schedule_interval(self.start_count, 1)
  
  def start_count(self, dt):
    print(self.update.text)
    text = self.update.text
    self.character_count.bind(text = lambda instance, text: setattr(update, "text", str(len(text))))

  # when user clicks the "BACK" button
  def back(self):
    sm.current = "home" # go back to home screen

  # when user clicks the "GO" button
  def go(self):
    event.cancel()
    sv.UpdateSave(self.update.text) # save the text written in the text box
    sm.current = "preview" # switch to preview screen

# preview window for both types of forecasts
class PreviewWindow(Screen):
  previewText = ObjectProperty(None)

  def on_enter(self, *args):
    self.previewText.text = sv.textSave

class WindowManager(ScreenManager):
  pass

kv = Builder.load_file("main.kv") # load main.kv file
sm = WindowManager() # load WindowManager upon running
sv = SaveText() # access to functions for storing text

# create screens dictionary that assigns name (ID) to each class
screens = [HomeWindow(name = "home"), OneDayParameterWindow(name = "one_day_main"), MediumRangeWindow(name = "medium_range"), PreviewWindow(name = "preview")]
for screen in screens:
  sm.add_widget(screen)

sm.current = "home" # by default, current screen goes to HomeWindow

# builds the kivy application
class ForecastSendApp(App):
  def build(self):
    return sm

if __name__ == "__main__":
  ForecastSendApp().run()

# Stuck on figuring out how to get bind function to work!!!
