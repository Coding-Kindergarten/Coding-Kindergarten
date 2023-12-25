import pyautogui
import pyperclip
import time
import schedule

def send_mesaage():
    position_img = pyautogui.locateOnScreen('kakao_profile.PNG' ,confidence=0.93)


    clickPosition = pyautogui.center(position_img)
    pyautogui.doubleClick(clickPosition)


    pyperclip.copy("이 메시지는 파이썬 코드로 보내는 자동메시지 입니다.")
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)


    pyautogui.write(["enter"])
    time.sleep(1)


    pyautogui.write(["escape"])
    time.sleep(1)


# 10초마다 함수를 실행 (Chapter 10에서 더 자세히 다룰 예정)
schedule.every(10).seconds.do(send_mesaage)

while True:
    schedule.run_pending()
    time.sleep(1)


