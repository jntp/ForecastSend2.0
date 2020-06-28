# main.py is the main python file of ForecastSend2.0 application
import math
import numpy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from database import DataBase
from send_SMS import MakeCalls
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty

# used to store text inputted in text boxes
class SaveText:
  # for saving text selected in the "city window" drop down menu 
  def citySelect(self, cityText):
    self.citySave = cityText

  # for saving text inputted in the "medium-range update" box
  def UpdateSave(self, updateText):
    self.textSave = updateText

  # for saving event type inputted in the "one day" drop down menu
  def eventSave(self, eventText):
    self.eventType = eventText

# used to store "global variables and functions"
class Globals:
  # "recalls" if user wanted to send a one-day forecast
  def oneDay(self, checkIt):
    if checkIt:
      self.oneDayBool = True
    else:
      self.oneDayBool = False

  # keeps track of all the "good responses" in the one-day window 
  def oneGoodResponses(self):
    self.oneTracker = numpy.zeros(5, dtype = bool) 

# class for drop down menu
class CustomDropDown(DropDown):
  pass

# prompts user to select between "one-day precipitation" or "medium-range update" forecasts
class HomeWindow(Screen):
  # when user clicks "one-day precipitation" button
  def one_day_precip(self):
    sm.current = "city" # switch to city selection screen
    gb.oneDay(True) # set oneDayBool equal to True

  # when user clicks "medium-range update" button
  def medium_range(self):
    sm.current = "city" # then switch to city selection screen
    gb.oneDay(False) # set oneDayBool equal to False

# prompts user to choose which city or region to send the forecast
class CityWindow(Screen):  
  dropDownList = ObjectProperty(None)
  backButton = ObjectProperty(None)
  goButton = ObjectProperty(None) 
  cityString = "Select city/region"

  def __init__(self, *args, **kwargs):
    super(CityWindow, self).__init__(*args, **kwargs)
    self.drop_down = CustomDropDown()

    # create drop down menu of select cities
    dropdown = DropDown() 
    cities = ["All", "San Francisco/Oakland", "Davis/Sacramento", "Santa Clara Valley", "Los Angeles/Orange County", "San Diego", "New York City", \
        "Baltimore"]
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
    # clear the selectedNames and selectedNumbers lists to prevent names/numbers from stacking up
    db.selectedNames = []
    db.selectedNumbers = []    

    sm.current = "home" # go back to home screen

  # when user clicks the "GO" button
  def go(self):
    # check if user actually selected a city/region
    if hasattr(sv,'citySave'): # if user selected anything (if object has attribute)
      db.get_subscribers(sv.citySave) # call database function to retrieve subscribers with matching city

      # Check if user selected a one-day or medium-range forecast 
      if gb.oneDayBool is True: 
        # check if user selected "all"; this would output an error
        if "All" in sv.citySave:
          errorAll() # display pop up error message
        else: # success
          sm.current = "one_day_main" # switch one-day main screen
      else:
        sm.current = "medium_range" # switch to medium-range update main screen

    else:
      errorCity() # display error pop up window

# one-day precipitation: main screen for user entering parameters
class OneDayParameterWindow(Screen):
  dropDownList = ObjectProperty(None)
  pop = ObjectProperty(None)
  popMessage = ObjectProperty(None) 
  placeOne = ObjectProperty(None)
  placeTwo = ObjectProperty(None) 
  tempOne = ObjectProperty(None)
  tempTwo = ObjectProperty(None)
  tempThree = ObjectProperty(None) 
  tempFour = ObjectProperty(None) 
  boxOne = ObjectProperty(None)
  boxTwo = ObjectProperty(None)
  boxThree = ObjectProperty(None) 
  boxFour = ObjectProperty(None)  
  unitOne = ObjectProperty(None)
  unitTwo = ObjectProperty(None)
  unitThree = ObjectProperty(None)
  unitFour = ObjectProperty(None)
  tempMessageOne = ObjectProperty(None) 

  def __init__(self, *args, **kwargs):
    super(OneDayParameterWindow, self).__init__(*args, **kwargs)
    self.drop_down = CustomDropDown()

    # create drop down menu of select cities
    dropdown = DropDown() 
    events = ["Light Rain", "Moderate Rain", "Heavy Rain", "Thunderstorm", "Wintry Mix", "Sleet", "Freezing Rain", "Flurries", "Snow Showers", \
        "Snow", "Heavy Snow"]
    for event in events:
      # create button individually for each city
      btn = Button(text = '%r' % event, size_hint_y = None, height = 30, pos = (25, 25), on_release = lambda btn : sv.eventSave(btn.text))
      btn.bind(on_release = lambda btn : dropdown.select(btn.text)) # attach a callback which will pass the text selected as data
      dropdown.add_widget(btn)

    # create the main or default button
    mainbutton = Button(text = 'Event Type', size_hint = (0.5, 0.5))
    mainbutton.bind(on_release = dropdown.open) # show drop down menu when released
    dropdown.bind(on_select = lambda instance, x : setattr(mainbutton, 'text', x)) # assign data to button text
    self.dropDownList.add_widget(mainbutton)

  def on_pre_enter(self, *args):
    gb.oneGoodResponses()
    cityInPrint = db.cityRegion[1:-1] # cut the quotations off the beginning and end of the string 

    # Display the temperature labels and boxes according to the scenario 
    if "single-city" in db.cityType:
      self.placeOne.text = "[i]" + cityInPrint + "[/i]"
      self.tempOne.text = "High:"
      self.tempTwo.text = "Low:" 
    elif "double-city" in db.cityType:
      # Partition the cityInPrint string into two cities
      cityOne, cityTwo = cityInPrint.split("/")

      # Bring boxThree and boxFour to life
      self.boxThree.pos_hint["x"] = 0.44
      self.boxFour.pos_hint["x"] = 0.74

      # Customize display of cities
      self.placeOne.text = "[i]" + cityOne + "[i]"
      self.placeTwo.text = "[i]" + cityTwo + "[i]"

      # Add labels for the 2nd line
      self.tempThree.text = "High:"
      self.tempFour.text = "Low:" 
      self.unitThree.text = "F"
      self.unitFour.text = "F"
    elif "region" in db.cityType:
      # Only display boxOne and boxThree 
      self.boxTwo.pos_hint["x"] = -0.74 # hide boxTwo
      self.boxThree.pos_hint["x"] = 0.44 # show boxThree 

      # Change box sizes to accomodate extra text
      self.boxOne.size_hint_x = 0.15
      self.boxThree.size_hint_x = 0.15

      # Change the text accordingly 
      self.tempOne.text = "High/Low:"
      self.tempThree.text = "High/Low:"
      self.tempTwo.text = "" # remove tempTwo
      self.unitTwo.text = "" # remove unitTwo
      self.unitThree.text = "F" # display unitThree 
      
      # Change positions of "unit" text (fahrenheit, celsius)
      self.unitOne.pos_hint["x"] = 0.6
      self.unitThree.pos_hint["x"] = 0.6

      # City display will look different per region
      if "Los Angeles/Orange County" or "San Diego" in cityInPrint:
        self.placeOne.text = "[i]Coast[/i]"
        self.placeTwo.text = "[i]Valley[/i]" 

  def back(self):
    ## Note you may need to write a function for the "restoration of default"
    # restore or ensure attributes are at "default" 
    self.boxOne.size_hint_x = 0.08

  def popMessages(self, min_value, max_value):
    value = self.pop.text
    gb.oneTracker[0] = False # automatically assume false and thus "bad" response 

    # check if user is focusing on textinput for the first time
    if self.pop.text == "":
      self.popMessage.color = (0, 0.9, 0.5, 0.9) # initiate green text
      self.popMessage.text = "Please enter an integer between " + str(min_value) + " and " + str(max_value) + "."
    else: 
      # check if user entered an integer
      try:
        status = int(min_value) <= int(value) <= int(max_value)
      except:
        # display error message
        self.popMessage.color = (1, 0.1, 0.1, 0.9) # change label color to red
        self.popMessage.text = "Error! Please enter an integer."
      else:
        remainder = int(value) % 10 # check if input is divisible by 10
        self.popMessage.color = (1, 0.1, 0.1, 0.9) # change label color to red

        # check if input is "correct"
        if remainder is 0 and status is True: # correct input
          self.popMessage.text = "" # "erase" label
          gb.oneTracker[0] = True # set response to "good" 
          print("True?", gb.oneTracker) 
        elif status is False: # check if number is within bounds FIRST before checking divisibility
          self.popMessage.text = "Error! Integer must be between 30 and 100."
        elif remainder is not 0 and status is True: # for input not divisible by 10
          self.popMessage.text = "Error! Please enter an integer divisible by 10."

  def tempMessages(self, orderRank):
    gb.oneTracker[orderRank] = False 
    value = ""  
    tempType = self.convertTempType(orderRank) 
    
    if orderRank == 1:
      value = self.boxOne.text
    elif orderRank == 2:
      value = self.boxTwo.text
      tempType = "Low" 
    elif orderRank == 3:
      value = self.boxThree.text
    elif orderRank == 4:
      value = self.boxFour.text

    # check if user is focusing on textinput for the first time
    if value == "":
      self.popMessage.color = (0, 0.9, 0.5, 0.9) # initiate green text
      self.popMessage.text = "Please enter an appropriate " + tempType + " temperature."
    # YOU LEFT OFF HERE! 

  def convertTempType(self, orderRank):
    if orderRank == 1 or orderRank == 3:
      if "region" in db.cityType:
        finalString = "High/Low"
      else:
        finalString = "High"
    elif orderRank == 2 or orderRank == 4:
      finalString = "Low" 

    return finalString 

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
    # check if text box is blank
    if self.update.text == "":
      errorMedium() # display error pop up window
    else:
      sv.UpdateSave(self.update.text) # save the text written in the text box
      sm.current = "preview" # switch to preview screen

# preview window for both types of forecasts
class PreviewWindow(Screen):
  previewText = ObjectProperty(None)
  characterCount = ObjectProperty(None)
  selectedNames = ObjectProperty(None)
  selectedNumbers = ObjectProperty(None)
  selectedNames2 = ObjectProperty(None) # 3rd column of recipients text
  selectedNumbers2 = ObjectProperty(None) # 4th column of recipients text

  def on_enter(self, *args):
    self.previewText.text = sv.textSave

    text_length = len(self.previewText.text)
    sms_count = math.ceil(text_length / 160)
    info_string = "[b]" + "Character Count: " + str(text_length) + "\n" + "Number of Messages: " + str(sms_count) + "[/b]"

    self.characterCount.text = info_string

    # Loop through selectedNames and selectedNumbers of the database
    columnSplit = math.floor((len(db.selectedNames) - 1) / 2) # list "splits" halfway, allowing recipients to "overflow" to next 2 columns

    for index, name in enumerate(db.selectedNames):
      # check if index less than or equal to half the length of selectedNames and selectedNumbers
      if index <= columnSplit:
        # onto left 2 columns
        self.selectedNames.text = self.selectedNames.text + "\n" + db.selectedNames[index] # show in recipient box
        self.selectedNumbers.text = self.selectedNumbers.text + "\n" + db.selectedNumbers[index]
      # overflow to the next two columns if number of recipients exceeds 9
      elif index > columnSplit:
        self.selectedNames2.text = self.selectedNames2.text + "\n" + db.selectedNames[index]
        self.selectedNumbers2.text = self.selectedNumbers2.text + "\n" + db.selectedNumbers[index]

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

  # Create dynamically sized label for recipients' text
  def recipientFont(self, text, height, width):
    dimAvg = (height + width) / 2
    sp = math.ceil(dimAvg * 0.02)
    count = text.count("\n") # intend to do an sp drop for count >= 7 where dimAvg == 800

    if count >= 7:
      countAdjust = count - 7
      spDrop = math.floor(countAdjust / 2) + 1 # for every two lines, drop the font size by 1 sp
      sp -= spDrop

      # drop by another sp if there are 10 or more recipients in one column
      if count >= 10:
        sp -= 1 

    # calculate greater "drop in sp" for 9 lines or more and larger windows
    if count >= 9 and dimAvg >= 750:
      sp -= 1

      # drop sp again if window is even larger
      if dimAvg >= 900:
        sp -= 1
        
        # keep dropping the sp
        if dimAvg >= 1000:
          sp -= 1

          # drop sp again for larger columns
          if count >= 10:
            sp -= 1

    return "{}sp".format(sp)

  # when user presses the "BACK" button
  def back(self):
    sm.current = "medium_range"

    # Clear the recipients columns to prevent names from stacking onto each other
    self.selectedNames.text = ""
    self.selectedNumbers.text = ""
    self.selectedNames2.text = ""
    self.selectedNumbers2.text = ""

  # when user presses the "SEND" button
  def send(self):
    self.warnSend()

  # warning message for sending the forecast
  def warnSend(self):
    # Create box layout to accomodate two buttons and label
    box = BoxLayout(orientation = 'vertical', padding = (17))
    box.add_widget(Label(text = "You are about to send the forecast.\n This action cannot be undone.\n SMS charges will apply.\n Continue?"))
    noButton = Button(text = "NO", pos_hint = {"x": 0.30}, size_hint = (0.4, 0.15))
    yesButton = Button(text = "YES", pos_hint = {"x": 0.30}, size_hint = (0.4, 0.15))
    box.add_widget(yesButton)
    box.add_widget(noButton)
  
    # Create pop up
    warnPopup = Popup(title = "WARNING!", content = box, size_hint = (None, None), size = (400, 400), auto_dismiss = True)
    yesButton.bind(on_press = self.go) # will send you to the "sent" screen
    yesButton.bind(on_press = warnPopup.dismiss)
    noButton.bind(on_press = warnPopup.dismiss) # stay on the preview window
    warnPopup.open()

  # when user confirms submission of forecast
  def go(self, instance):
    mc.makeCall(sv.textSave, db.selectedNumbers, db.selectedNames) # make API Call
    sm.current = "sent" # switch to sent screen

    # Clear the recipients text box to prevent names from stacking if user decides to send another forecast
    self.selectedNames.text = ""
    self.selectedNumbers.text = ""
    self.selectedNames2.text = ""
    self.selectedNumbers2.text = ""

# screen for when user sends the forecast
class SentWindow(Screen):
  # when user presses the "YES" button
  def yes(self):
    # clear the selectedNames and selectedNumbers lists
    db.selectedNames = []
    db.selectedNumbers = []    

    sm.current = "home" # go back to home screen 

  # when user presses the "NO" button
  def no(self):
    App.get_running_app().stop() # exit the application

class WindowManager(ScreenManager):
  pass

## Popup Windows for Errors

# for unselected city/region in city window
def errorCity():
  errorPopup = Popup(title = "ERROR", content = Label(text = "Error! Please select a city/region."), size_hint = (None, None), size = (400, 400))
  errorPopup.open() # show the popup

# for blank input box in medium-range update window
def errorMedium():
  errorPopup = Popup(title = "ERROR", content = Label(text = "Error! Text box cannot be blank."), size_hint = (None, None), size = (400, 400))
  errorPopup.open()

# for selecting "ALL" in city window when user specifies "one-day" forecast
def errorAll():
  errorPopup = Popup(title = "ERROR", content = Label(text = "Error! One cannot select *All* when \nsending a one-day precipitation forecast."), \
      size_hint = (None, None), size = (400, 400))
  errorPopup.open()

## Class instances
kv = Builder.load_file("main.kv") # load main.kv file
sm = WindowManager() # load WindowManager upon running
sv = SaveText() # access to functions for storing text
gb = Globals() # access to "global variables and functions" 
db = DataBase("data.txt") # load database
mc = MakeCalls() # allow access to Twilio

# create screens list that assigns name (ID) to each class
screens = [HomeWindow(name = "home"), CityWindow(name = "city"), OneDayParameterWindow(name = "one_day_main"), MediumRangeWindow(name = "medium_range"), \
    PreviewWindow(name = "preview"), SentWindow(name = "sent")]
for screen in screens:
  sm.add_widget(screen)

sm.current = "home" # by default, current screen goes to HomeWindow

# builds the kivy application
class ForecastSendApp(App):
  def build(self):
    return sm

if __name__ == "__main__":
  ForecastSendApp().run()

# You left off at temperature messages.  
# Don't forget later when you add the back button to the one-day screen, you will need to "reset" the positions of the attributes!!!
# You left off at High/Low Temps, and the different scenarios to display it
# Also don't forget to put an error message IF the forecast does not send
# Don't forget to add pop up windows for error messages
