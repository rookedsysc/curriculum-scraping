from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

class Driver :
  __driver_path = '/opt/homebrew/Caskroom/chromedriver/114.0.5735.90/chromedriver'
  def __init__(self) :
    s = Service(self.__driver_path)
    self.__driver = webdriver.Chrome(service=s)
    self.__wait = WebDriverWait(self.__driver, 15)
    
  def get_driver(self) :
    return self.__driver
  
  def get_wait(self) :
    return self.__wait