from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from curriculum_scrappers.utils.clicker import ElementClicker
from curriculum_scrappers.utils.time_utils import TimeUtils
from bs4 import BeautifulSoup
import time

class FastCampusCurriculum: 
  login_url = 'https://fastcampus.co.kr/account/sign-in?client_id=fc%3Aclient%3Awww&response_type=token&redirect_uri=https%3A%2F%2Ffastcampus.co.kr%2F&scope=www&x-fingerprint=038e1764567f279c2d27008dfc37f905'
  driver_path = '/opt/homebrew/Caskroom/chromedriver/114.0.5735.90/chromedriver'
  parts_class_name = 'classroom-sidebar-clip__chapter__part'
  clips_class_name = 'classroom-sidebar-clip__chapter__clip'
  
  def __init__(self):
      self.target_url = input("수강 중인 강의의 URL을 입력하세요: ")
      self.user_id = input("아이디를 입력하세요: ")
      self.user_pw = input("비밀번호를 입력하세요: ")
      self.last_chapter = int(input("마지막 챕터를 입력하세요: "))

  def get_session(self): 
    # 웹 드라이버를 실행
    s = Service(self.driver_path)
    driver = webdriver.Chrome(service=s)

    # 로그인 페이지를 로드
    driver.get(self.login_url)

    # 로그인 폼에 사용자 이름과 비밀번호 입력
    driver.find_element(By.ID, 'user-email').send_keys(self.user_id)  # 'username'은 실제 웹페이지에서 확인해야 합니다.
    driver.find_element(By.ID, 'user-password').send_keys(self.user_pw)  # 'username'은 실제 웹페이지에서 확인해야 합니다.

    # 로그인 버튼 클릭
    button = driver.find_element(By.CSS_SELECTOR, '.btn.btn--md.btn--wide.btn--primary')
    button.click()
    wait = WebDriverWait(driver, 10)  # 최대 10초까지 기다림
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'header-new')))

    # 스크래핑 대상 페이지를 로드
    driver.get(self.target_url)
    try : 
      dialog = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="classroom-modal__backdrop"]')))
      self.__close_confirm_modal(dialog)
    except Exception as e:
      print("There is no confirm modal")
    
    cpt_elements = driver.find_elements(By.CLASS_NAME, 'classroom-sidebar-clip__chapter')
    cpt_clicker = ElementClicker(driver, cpt_elements)
    cpt_clicker.click()
    
    parts = []
    for cpt in cpt_elements:
      parts += self.__get_parts(cpt)
    
    part_clicker = ElementClicker(driver, parts)
    part_clicker.click()
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    parts = soup.find_all('div', {'class': 'classroom-sidebar-clip__chapter__part'})
    
    with open('result.txt', 'w') as fc:
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
        
  def __get_parts(self, cpt):
    parts = cpt.find_elements(By.CLASS_NAME, 'classroom-sidebar-clip__chapter__part')
    return parts
          
  def __close_confirm_modal(self, dialog):
    try:
        element = dialog.find_element(By.CSS_SELECTOR, 'svg[data-e2e="classroom-confirm-modal-close"]')
        element.click()
    except Exception as e:
      print("There is no confirm modal")


