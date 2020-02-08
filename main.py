# main.py is the main python file of ForecastSend2.0 application
import math
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

# used to store text inputted in text boxes
class SaveText:
  # for saving text selected in the "city window" drop down menu 
  def citySelect(self, cityText):
    self.citySave = cityText

  # for saving text inputted in the "medium-range update" box
  def UpdateSave(self, updateText):
    self.textSave = updateText

# class for drop down menu
class CustomDropDown(DropDown):
  pass

# holds contents of pop up windows
class PopUps(FloatLayout):
  def error_popup(self):
    errorPopup = Popup(title = "ERROR", content = pop, size_hint = (None, None), size = (400, 400))
    errorPopup.open() # show the popup

# prompts user to select between "one-day precipitation" or "medium-range update" forecasts
class HomeWindow(Screen):
  # when user clicks "one-day precipitation" button
  def one_day_precip(self):
    sm.current = "city" # switch to one-day precipitation screen

  # when user clicks "medium-range update" button
  def medium_range(self):
    sm.current = "city" # then switch to medium-range update screen

# prompts user to choose which city or region to send the forecast
class CityWindow(Screen):  
  dropDownList = ObjectProperty(None)
  cityString = "Select city/region"

  def __init__(self, *args, **kwargs):
    super(CityWindow, self).__init__(*args, **kwargs)
    self.drop_down = CustomDropDown()

    # create drop down menu of select cities
    dropdown = DropDown() 
    cities = ["San Francisco/Oakland", "Davis/Sacramento", "Santa Clara Valley", "Los Angeles/Orange County", "San Diego", "New York City"]
    for city in cities:
      # create button individually for each city
      btn = Button(text = '%r' % city, size_hint_y = None, height = 30, pos = (25, 25), on_release = lambda btn : sv.citySelect(btn.text))
      btn.bind(on_release = lambda btn : dropdown.select(btn.text)) # attach a callback which will pass the text selected as data
      dropdown.add_widget(btn)

    # create the main or default button
    mainbutton = Button(text = 'Select city/region', size_hint = (0.5, 0.5))
    mainbutton.bind(on_release = dropdown.open) # show drop down menu when released
    dropdown.bind(on_select = lambda instance, x : setattr(mainbutton, 'text', x)) # assign data to button text
    self.dropDownList.add_widget(mainbutton)

  # when user clicks the "BACK" button
  def back(self):
    sm.current = "home" # go back to home screen

  # when user clicks the "GO" button
  def go(self):
    if hasattr(sv,'citySave'):
      print(sv.citySave)
      sm.current = "medium_range" # switch to medium-range update main screen
    else:
      pop.error_popup()

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
    sm.current = "city" # go back to select city screen

  # when user clicks the "GO" button
  def go(self):
    sv.UpdateSave(self.update.text) # save the text written in the text box
    sm.current = "preview" # switch to preview screen

# preview window for both types of forecasts
class PreviewWindow(Screen):
  previewText = ObjectProperty(None)
  characterCount = ObjectProperty(None)

  def on_enter(self, *args):
    self.previewText.text = sv.textSave

    text_length = len(self.previewText.text)
    sms_count = math.ceil(text_length / 160)
    info_string = "[b]" + "Character Count: " + str(text_length) + "\n" + "Number of Messages: " + str(sms_count) + "[/b]"

    self.characterCount.text = info_string

  # Create dynamically sized label for preview text
  def fontsize(self, text, height, width):
    dimAvg = (height + width) / 2 # calculate an average dimension size (between width and height)
    sp = math.ceil(dimAvg * 0.02) # two percent of the screen's dimensions

    # For messages larger than 320 characters
    if len(text) > 320:
      lenAdjust = len(text) - 160 # offset character count by 160
      spDrop = math.floor(lenAdjust / 160) # calculate "drop in sp" based on character count
      sp -= spDrop # initiate "drop in sp"

      # calculate greater "drop in sp" for large messages and large windows (will overlap with the character counter)
      if spDrop >= 3 and dimAvg > 970:
        sp -= 1 # drop the font size by another 1 sp if conditions are met

    # print #sp on font_size
    return "{}sp".format(sp)    

class WindowManager(ScreenManager):
  pass

kv = Builder.load_file("main.kv") # load main.kv file
sm = WindowManager() # load WindowManager upon running
sv = SaveText() # access to functions for storing text
pop = PopUps()

# create screens dictionary that assigns name (ID) to each class
screens = [HomeWindow(name = "home"), CityWindow(name = "city"), OneDayParameterWindow(name = "one_day_main"), MediumRangeWindow(name = "medium_range"), PreviewWindow(name = "preview")]
for screen in screens:
  sm.add_widget(screen)

sm.current = "home" # by default, current screen goes to HomeWindow

# builds the kivy application
class ForecastSendApp(App):
  def build(self):
    return sm

if __name__ == "__main__":
  ForecastSendApp().run()

# In process of adding error pop up windows (you need to get the OK button to work)
# Don't forget to add pop up windows for error messages
