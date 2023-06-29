from curriculum_scrappers.scrapers.fastcampus_curriculum import FastCampusCurriculum
import os 

def clear():
  if os.name == 'nt':
    os.system('cls')
    os.system('pause')
  else :
    os.system('clear')
    os.system('read -n1 -r -p "Press any key to continue..." key')

if __name__ == '__main__': 
  fc = FastCampusCurriculum()
  fc.get_session()
