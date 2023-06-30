from curriculum_scrappers.scrapers.fastcampus_curriculum import FastCampusCurriculum
import os

from curriculum_scrappers.scrapers.inflearm_curriculum import InflearnCurriculum
from curriculum_scrappers.utils.driver import Driver 

def fast_campus(driver) :
  fc = FastCampusCurriculum(driver)
  fc.scraping()

def inflearn(driver) :
  inf = InflearnCurriculum(driver)
  inf.crawling()

def clear():
  if os.name == 'nt':
    os.system('pause')
    os.system('cls')
  else :
    os.system('read -n1 -r -p "Press any key to continue..." key')
    os.system('clear')

def choose_lecture() : 
  driver = Driver()
  while True :
    print("1. FastCampus")
    print("2. Inflearn")
    print("q. Exit")
    select = input("Select Site : ")
    if(select == "1") :
      fast_campus(driver)
      clear()
    elif(select == "2") :
      inflearn(driver)
      clear()
    elif(select == "q" or select == "Q") :
      clear()
      break
    else : 
      print("Wrong input. Please try again.")
      clear()

if __name__ == '__main__': 
  choose_lecture()

