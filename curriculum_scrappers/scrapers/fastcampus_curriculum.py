from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from curriculum_scrappers.scrapers.site import Site
from curriculum_scrappers.utils.clicker import ElementClicker
from curriculum_scrappers.utils.time_utils import TimeUtils
from curriculum_scrappers.utils.driver import Driver
from bs4 import BeautifulSoup
import time

class FastCampusCurriculum(Site) : 
  __login_url = 'https://fastcampus.co.kr/account/sign-in?client_id=fc%3Aclient%3Awww&response_type=token&redirect_uri=https%3A%2F%2Ffastcampus.co.kr%2F&scope=www&x-fingerprint=038e1764567f279c2d27008dfc37f905'
  __parts_class_name = 'classroom-sidebar-clip__chapter__part'
  __clips_class_name = 'classroom-sidebar-clip__chapter__clip'
  __cpt_elements = []
  __last_chapter = 0
  
  def __init__(self, driver):
      self.__target_url = input("수강 중인 강의의 URL을 입력하세요: ")
      self.__user_id = input("아이디를 입력하세요: ")
      self.__user_pw = input("비밀번호를 입력하세요: ")
      self.__driver = driver.get_driver()
      self.__wait = driver.get_wait()

  def scraping(self): 
    driver = Driver()
    self.__driver = driver.get_driver()
    self.__wait = driver.get_wait()
    self.__fc_login()
    self.__load_scraping_page()
    self.__click_all_cpt()
    parts = self.__get_all_parts()
    self.__click_parts(parts=parts)
    parts = self.__soup_parsing_with_parts()
    self.__make_result_file(parts)
  
  def __fc_login(self) :
    # 로그인 페이지를 로드
    self.__driver.get(self.__login_url)

    # 로그인 폼에 사용자 이름과 비밀번호 입력
    self.__driver.find_element(By.ID, 'user-email').send_keys(self.__user_id)  # 'username'은 실제 웹페이지에서 확인해야 합니다.
    self.__driver.find_element(By.ID, 'user-password').send_keys(self.__user_pw)  # 'username'은 실제 웹페이지에서 확인해야 합니다.

    # 로그인 버튼 클릭
    button = self.__driver.find_element(By.CSS_SELECTOR, '.btn.btn--md.btn--wide.btn--primary')
    button.click()
    element = self.__wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'header-new')))
    
  def   __load_scraping_page(self) :
    self.__driver.get(self.__target_url)
    try : 
      dialog = self.__wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="classroom-modal__backdrop"]')))
      self.__close_confirm_modal(dialog)
    except Exception as e:
      print("There is no confirm modal")
      pass
      
  def __click_all_cpt(self) :
    self.__cpt_elements = self.__driver.find_elements(By.CLASS_NAME, 'classroom-sidebar-clip__chapter')
    self.__last_chapter = len(self.__cpt_elements)
    cpt_clicker = ElementClicker(self.__driver, self.__cpt_elements)
    cpt_clicker.click()
  
  def __get_all_parts(self) :
    parts = []
    for cpt in self.__cpt_elements:
      parts += self.__get_parts_of_cpt(cpt)
    return parts

  def __click_parts(self, parts) :
    part_clicker = ElementClicker(self.__driver, parts)
    part_clicker.click()
    
  def __soup_parsing_with_parts(self) :
    html = self.__driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all('div', {'class': 'classroom-sidebar-clip__chapter__part'})

  def __make_result_file(self, parts) :
    with open('result_fc.txt', 'w') as fc:
      for part in parts:
        part_title = part.find('p', {'class': 'classroom-sidebar-clip__chapter__part__title'}).text.strip()
        fc.write(f'Part: {part_title}\n')

        # 각 clip마다 정보를 가져와서 출력
        clips = part.find_all('div', {'class': 'classroom-sidebar-clip__chapter__clip'})
        total = 0
        for clip in clips:
          clip_title = clip.find('span', {'class': 'classroom-sidebar-clip__chapter__clip__title'}).text.strip()
          clip_time = clip.find('span', {'class': 'classroom-sidebar-clip__chapter__clip__time'}).text.strip()
          fc.write(f'{clip_title} {clip_time}\n')
          total += TimeUtils.convert_to_seconds(clip_time) 
        fc.write(f'Total: {TimeUtils.convert_to_hms(total)}\n\n')
    
        
  def __get_parts_of_cpt(self, cpt):
    parts = cpt.find_elements(By.CLASS_NAME, 'classroom-sidebar-clip__chapter__part')
    return parts
          
  def __close_confirm_modal(self, dialog):
    try:
        element = dialog.find_element(By.CSS_SELECTOR, 'svg[data-e2e="classroom-confirm-modal-close"]')
        element.click()
    except Exception as e:
      print("There is no confirm modal")


