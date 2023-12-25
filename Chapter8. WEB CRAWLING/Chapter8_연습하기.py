# step1.프로젝트에 필요한 패키지 불러오기
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
import math

# step2.로그인 정보 및 검색할 회사 미리 정의
USR = "잡플래닛 ID (e-mail address)"
PWD = "비밀번호"
QUERY = "네이버랩스"

# step3.크롬드라이버 실행 및 잡플래닛 로그인 함수
def login(driver, usr, pwd):
    driver.get("https://www.jobplanet.co.kr/users/sign_in?_nav=gb")
    time.sleep(5)
    
    # 아이디 입력
    login_id = driver.find_element(By.ID, "user_email")
    login_id.send_keys(usr)

    # 비밀번호 입력
    login_pwd = driver.find_element(By.ID, "user_password")
    login_pwd.send_keys(pwd)

    # 로그인 버튼 클릭
    login_id.send_keys(Keys.RETURN)
    time.sleep(5)

# step4.원하는 회사의 리뷰 페이지까지 이동 함수
def go_to_review_page(driver, query):
    
    # 검색창에 회사명 입력
    search_query = driver.find_element(By.ID, "search_bar_search_query")
    search_query.send_keys(query)
    search_query.send_keys(Keys.RETURN)
    time.sleep(3)

    # 회사명 클릭
    driver.find_element(By.CLASS_NAME, "tit").click()
    time.sleep(5)

    # 팝업창 제거
    driver.find_element(By.CLASS_NAME, "btn_close_x_ty1").click()
    time.sleep(3)

# step5. 별점 변환 함수
def parse_star_rating(style_attribute):
    if len(style_attribute) == 11:
        rating_value = int(style_attribute[7:9])
        return f"{rating_value // 20}점"
    else:
        return "5점"

# step6.데이터 크롤링 함수 (직무/근속여부/일시/요약/평점/장점/단점/경영진에게 바라는 점)
def scrape_data(driver):
    list_div = []
    list_cur = []
    list_date = []
    list_stars = []
    list_summery = []
    list_merit = []
    list_disadvantages = []
    list_opinions = []
    
    # 크롤링 할 리뷰 갯수 파악
    review_count = driver.find_element(By.ID, "viewReviewsTitle")
    review_count = review_count.find_element(By.CLASS_NAME, "num").text
    
    # 크롤링 할 페이지수 파악
    page = math.ceil(int(review_count)/5)
    
    for _ in range(page):
        
        review_box = driver.find_elements(By.CLASS_NAME, "content_wrap")
        
        # 페이지당 최대 5개의 리뷰 박스 존재
        for i in review_box:
            
            user_info = i.find_elements(By.CLASS_NAME, "txt1")

            # 직무
            division = user_info[0].text
            list_div.append(division)
            
            # 재직여부
            current = user_info[1].text
            list_cur.append(current)
            
            # 날짜
            try:
                date = user_info[3].text
                list_date.append(date)
                
            except: #날짜 없는 경우 예외처리
                date = "날짜 없음"
                list_date.append(date)
                
            # 리뷰 요약
            try:
                summary = i.find_element(By.CLASS_NAME, "us_label ")
                list_summery.append(summary.text)
                
            except: #신고로 인해 리뷰 요약 없는 경우 예외처리
                summery_ban = i.find_element(By.CLASS_NAME, "cont_discontinu.discontinu_category")
                list_summery.append(summery_ban.text)
                list_merit.append(summery_ban.text)
                list_disadvantages.append(summery_ban.text)
                list_opinions.append(summery_ban.text)

            # 장점, 단점, 경영진에게 바라는 점
            try:
                contents = i.find_elements(By.CLASS_NAME, "df1")
                
                merit = contents[0].text
                list_merit.append(merit)
                
                disadvantage = contents[1].text
                list_disadvantages.append(disadvantage)

                opinion = contents[2].text
                list_opinions.append(opinion)
                
            except:
                pass

            try:
                stars = i.find_elements(By.CLASS_NAME, "star_score")
                for star in stars:
                    list_stars.append(parse_star_rating(star.get_attribute('style')))
            except:
                list_stars.append("별점 없음")

        try:
            driver.find_element(By.CLASS_NAME, "btn_pgnext").click()
            time.sleep(5)
        except:
            pass

    total_data = pd.DataFrame({
        '날짜': list_date,
        '직무': list_div,
        '고용 현황': list_cur,
        '별점': list_stars,
        '요약': list_summery,
        '장점': list_merit,
        '단점': list_disadvantages,
        '경영진에게 바라는 점': list_opinions
    })

    return total_data

def main():
    # 크롬 드라이버 실행
    driver = webdriver.Chrome()
    login(driver, USR, PWD)
    go_to_review_page(driver, QUERY)
    total_data = scrape_data(driver)
    total_data.to_excel(f"잡플래닛 리뷰 총정리_{QUERY}.xlsx", index=True)
    driver.close()

if __name__ == "__main__":
    main()