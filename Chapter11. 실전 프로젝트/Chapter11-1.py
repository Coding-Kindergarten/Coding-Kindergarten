from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
import time # 시간 delay를 위한 모듈
import pandas as pd # 리스트를 엑셀로 넘겨주기 위한 패키지
import math # 페이지 수 올림 계산을 위한 모듈

# 크롬 드라이버 실행
driver = webdriver.Chrome()

# url 입력 및 실행
url = '스마트 스토어 상품 페이지 url 입력'
driver.get(url)
time.sleep(2)

# 리뷰 탭 클릭
driver.find_element(By.CLASS_NAME, "_2pgHN-ntx6").click()
time.sleep(1)

# 크롤링 할 리뷰 갯수 파악
review_count = driver.find_element(By.CLASS_NAME, "UlkDgu9gWI")
page_count = math.ceil(int(review_count.text)/20)

# 정보를 담을 빈 리스트 정의
all_list_star = []
all_list_id = []
all_list_date = []
all_list_option = []
all_list_comment = []

print("리뷰를 수집합니다.")

for i in range(page_count):
    # 리뷰 상자
    list_review_div = driver.find_elements(By.CLASS_NAME, "_1yIGHygFbx")

    # 리뷰 상자 안의 정보들을 리스트로 형태로 가공
    list_star = [review.find_element(By.CLASS_NAME, "_15NU42F3kT").text for review in list_review_div]
    list_id = [review.find_elements(By.CLASS_NAME, "_3QDEeS6NLn")[0].text for review in list_review_div]
    list_date = [review.find_elements(By.CLASS_NAME, "_3QDEeS6NLn")[1].text for review in list_review_div]

    # 옵션 (선택옵션 정보가 없는 경우를 대응하기 위함)
    list_option = [ ]
    options = driver.find_elements(By.CLASS_NAME, "_14FigHP3K8")

    for i in options:
        option = i.text.split("\n")

        if len(option) == 1:
            option = "옵션 없음"
        else:
            option = option[0]

        list_option.append(option)
    
    # 리뷰 내용 저장
    list_review_comment = driver.find_elements(By.CLASS_NAME, "YEtwtZFLDz")   
    list_comment = [comment.text for comment in list_review_comment]

    # 리스트들을 전체 리스트에 추가
    all_list_star.extend(list_star)
    all_list_id.extend(list_id)
    all_list_date.extend(list_date)
    all_list_option.extend(list_option)
    all_list_comment.extend(list_comment)

# 다음 페이지 이동
    try:
        driver.find_element(By.CLASS_NAME, "fAUKm1ewwo._2Ar8-aEUTq").click()
        time.sleep(2)
    except:
        print("마지막 페이지입니다.")
        pass

# 크롬 드라이버 종료
driver.close()

# 전체 리스트를 묶음
list_sum = list(zip(all_list_id, all_list_date, all_list_option, all_list_star, all_list_comment))

# DataFrame 생성
col = ['아이디', '날짜', '구매옵션', '별점', '리뷰']
df = pd.DataFrame(list_sum, columns=col)

# 엑셀에 저장
df.to_excel('./스마트 스토어 상품 리뷰.xlsx')