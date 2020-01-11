# main.py is the main python file of ForecastSend2.0 application
import math
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty


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
  
  # when user clicks the "BACK" button
  def back(self):
    sm.current = "home" # go back to home screen

  # when user clicks the "GO" button
  def go(self):
    sv.UpdateSave(self.update.text) # save the text written in the text box
    sm.current = "preview" # switch to preview screen

# preview window for both types of forecasts
class PreviewWindow(Screen):
  previewText = ObjectProperty(None)

  def on_enter(self, *args):
    self.previewText.text = sv.textSave

  # Create dynamically sized label for preview text
  def fontsize(self, text, height, width):
    dimAvg = (height + width) / 2 # calculate an average dimension size (between width and height)
    sp = math.ceil(dimAvg * 0.02) # two percent of the screen's dimensions

    # For messages larger than 320 characters
    if len(text) > 320:
      lenAdjust = len(text) - 160 # offset character count by 160
      spDrop = math.floor(lenAdjust / 160) # calculate "drop in sp" based on character count
      sp -= spDrop # initiate "drop in sp"

    # print #sp on font_size
    return "{}sp".format(sp) 

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

# Left off at dynamic labels
