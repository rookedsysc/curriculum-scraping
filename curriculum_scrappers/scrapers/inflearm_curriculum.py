from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from curriculum_scrappers.scrapers.site import Site
from curriculum_scrappers.utils.driver import Driver
from selenium.webdriver.common.by import By

from curriculum_scrappers.utils.time_utils import TimeUtils

class InflearnCurriculum(Site) :
  def __init__(self, driver) :
    self.__target_url = input("수강 중인 강의의 URL을 입력하세요: ")
    self.__driver = driver.get_driver()
    
  def __load_scraping_page(self)  :
    self.__driver.get(self.__target_url)
    return self.__driver.page_source
    
  
  def crawling(self) :
    html = self.__load_scraping_page()
    soup = BeautifulSoup(html, 'html.parser')
    chapters = soup.find_all('li', {'class' : 'css-1nvk6w3'})
    
    total = 0
    with open('result_inf.txt', 'w') as f :
      for chapter in chapters : 
        cpt_total = 0
        cpt = BeautifulSoup(str(chapter), 'html.parser')
        f.write(self.__cpt_number_with_title(cpt) + '\n')
        sections = chapter.find_all('li', attrs={'data-testid': 'sectionUnit'})
        for section in sections :
          title, time = self.__section_title_with_time(section)
          f.write(title + " " + TimeUtils.convert_to_hms(time) + '\n')
          cpt_total += time
          total += time
        f.write(f'total : {TimeUtils.convert_to_hms(cpt_total)}\n\n')
        cpt_total = 0 
        
      f.write(f'총 수강시간 : {TimeUtils.convert_to_hms(total)}')
        
  def __cpt_number_with_title(self, cpt) :
    chapter_number = cpt.find('p', {'class' : 'mantine-Text-root mantine-xvbjl0'}).text
    chapter_title = cpt.find('p', {'class' : 'mantine-Text-root mantine-1i0nnuq'}).text
    return "{} : {}".format(chapter_number, chapter_title)
  
  def __section_title_with_time(self, section) :
    soup = BeautifulSoup(str(section), 'html.parser')
    try : 
      title = soup.find('p').text
    except Exception as e : 
      title = "null"
      pass
    
    try : 
      time = soup.find_all('span')
      time.reverse()
      time = time[0]
    except Exception as e :
      time = None
      pass
    if(time != None) : 
      time = time.text
    else : 
      time = "0"
      
    return title, self.__convert_txt_to_seconds(time)
    
  def __convert_txt_to_seconds(self, txt) :
    hour = txt.split('시간')
    try :
      minute = hour[1].split('분')
    except IndexError as e :
      minute = txt.split('분')[0]
    except : 
      minute = '0'
      
    hour = hour[0]
    if('분' in hour) :
      hour = '0'

    
    return int(hour[0]) * 3600 + int(minute[0]) * 60
    