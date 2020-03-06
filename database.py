# database.py loads and handles databases for ForecastSend2.0
import datetime

class DataBase:
  def __init__(self, filename):
    self.filename = filename
    self.subscribers = None
    self.file = None
    self.load()

  # Loads the database
  def load(self):
    self.file = open(self.filename, "r")
    self.subscribers = {} # create dictionary out of users

    # parse each line of the database
    for line in self.file:
      name, city, phone_number = line.strip().split(", ")
      self.subscribers[name] = (city, phone_number) # create a dictionary containing information of each subscriber

    self.file.close()

  # Retrieves subscribers based on the selected city or region
  def get_subscribers(self, cityRegion):
    self.cityRegion = cityRegion
    self.cityCode = ""
    self.selectedNames = []
    self.selectedNumbers = []

    # Find the respective "city code" for the cityRegion string
    if "All" in cityRegion: 
      self.cityCode = "ALL"
    elif "San Francisco/Oakland" in cityRegion:
      self.cityCode = "SF"
    elif "Davis/Sacramento" in cityRegion:
      self.cityCode = "SAC"
    elif "Santa Clara Valley" in cityRegion:
      self.cityCode = "SJ" # SJ for San Jose
    elif "Los Angeles/Orange County" in cityRegion:
      self.cityCode = "LA"
    elif "San Diego" in cityRegion:
      self.cityCode = "SD"
    elif "New York City" in cityRegion:
      self.cityCode = "NYC" 
    elif "Baltimore" in cityRegion:
      self.cityCode = "BALT"

    # Search through the database and retrieve subscribers based on selected city/region
    for name in self.subscribers:
      # Check if user selected the "All" button
      if self.cityCode == "ALL":
        # Retreive the name and number
        self.selectedNames.append(name)
        self.selectedNumbers.append(self.subscribers[name][1])
      else: # if user selected an actual city or region
        if self.subscribers[name][0] == self.cityCode: # check if subscriber has matching cityCode
          print(self.subscribers[name])
          # Retrieve the name and number
          self.selectedNames.append(name)
          self.selectedNumbers.append(self.subscribers[name][1])

    self.cityCode = "" # clear the cityCode string in case user presses the back button (avoids appending multiple city codes)
        






