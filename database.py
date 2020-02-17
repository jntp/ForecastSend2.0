# database.py loads and handles databases for ForecastSend2.0
import datetime

class DataBase:
  def __init__(self, filename):
    self.filename = filename
    self.subscribers = None
    self.file = None
    self.load()

  def load(self):
    self.file = open(self.filename, "r")
    self.subscribers = {} # create dictionary out of users

    for line in self.file:
      name, city, phone_number = line.strip().split(", ")
      self.subscribers[name] = (city, phone_number)

    print(self.subscribers)
    self.file.close()

  def get_subscribers(self, cityRegion):
    self.cityRegion = cityRegion
    self.selectedLines = []
    index = 0

    if cityRegion == "San Francisco/Oakland":
      cityCode = "SF"

    for name in self.subscribers:
      if self.subscribers[name][0] == "SF":
        print(self.subscribers[name])
        self.selectedLines.append(name + ", " + self.subscribers[name][1] + "\n")

    print(self.selectedLines)
        






