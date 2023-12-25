from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pyautogui
import pyperclip

# 크롬 드라이버 실행
driver = webdriver.Chrome()

# url 입력 및 실행
url = 'https://www.bigkinds.or.kr/'
driver.get(url)
time.sleep(2)

#로그인 버튼 클릭
driver.find_element(By.CLASS_NAME, 'btn-login.login-modal-btn.login-area-before').click()
time.sleep(1)

#Big Kinds id/pw 입력 및 로그인
driver.find_element(By.ID, 'login-user-id').send_keys('빅카인즈 아이디')
driver.find_element(By.ID, 'login-user-password').send_keys('비밀번호')
driver.find_element(By.CLASS_NAME, 'btn.btn-lg.btn-primary.btn-login.login-btn').click()
time.sleep(1)

#워드 클라우드 다운로드 버튼이 보이도록 Page down
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
time.sleep(0.5)

#워드 클라우드 png 다운로드
driver.find_element(By.CLASS_NAME, 'btn.btn-dark.btn-sm.btn-round02').click()
time.sleep(0.5)
driver.find_element(By.CLASS_NAME, 'network-download.mobile-excel-download.btn_keyword_down').click()
time.sleep(3)

#크롬 드라이버 종료
driver.close()

#카카오톡 실행 (로그인 되어 있는 상태여야함)
position_kakao_app = pyautogui.locateOnScreen('kakao_icon.PNG' ,confidence=0.7)
clickPosition = pyautogui.center(position_kakao_app)
pyautogui.doubleClick(clickPosition)
time.sleep(5.0)

#내프로필 클릭 (나에게 보내기)
position_profile = pyautogui.locateOnScreen('kakao_profile.PNG' ,confidence=0.93)
clickPosition = pyautogui.center(position_profile)
pyautogui.click(clickPosition, button='right') #우클릭
pyautogui.move(20,20)
pyautogui.click()
time.sleep(1.0)

#첨부 파일 보내기
pyautogui.hotkey("ctrl", "t")
time.sleep(2.0)

#다운로드 폴더로 이동
position_png = pyautogui.locateOnScreen('path_download.PNG' ,confidence=0.93)
clickPosition = pyautogui.center(position_png)
pyautogui.moveTo(clickPosition)
pyautogui.click()
time.sleep(0.5)

#파일 선택 및 전송
position_png = pyautogui.locateOnScreen('kakao_today.PNG' ,confidence=0.7)
clickPosition = pyautogui.center(position_png)
pyautogui.moveTo(clickPosition)
pyautogui.move(0,40)
pyautogui.doubleClick()
pyautogui.press('enter')

#이미지 설명 텍스트 전송
pyperclip.copy("오늘의 뉴스 WordCloud") 
pyautogui.hotkey("ctrl", "v")
time.sleep(0.5)
pyautogui.press('enter')
time.sleep(0.5)

#채팅방 나가기
pyautogui.press('escape')
time.sleep(0.5)

#카카오톡 종료
pyautogui.press('escape')
