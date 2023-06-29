from selenium.webdriver.common.action_chains import ActionChains

class ElementClicker :
  def __init__(self, driver, elements):
    self.driver = driver
    self.elements = elements 
  
  def click(self) :
    for element in self.elements :
      try :
        action = ActionChains(self.driver)
        action.move_to_element(element).click().perform()
      except Exception as e:
        print(e)
        print("Elemeent Not Found : {}".format(element))
