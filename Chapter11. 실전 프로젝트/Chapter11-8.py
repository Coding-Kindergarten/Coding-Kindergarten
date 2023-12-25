from datetime import datetime
import csv

# 웹 로그 파일의 각 행을 리스트로 저장
def read_log_file(fpath:str)->list:
    logs = [] #로그를 한줄식 리스트로 저장하는 코드
    with open(fpath, 'r') as file:
        for line in file:
            logs.append(line.strip())
    return logs

def convert_day(str_data:str):
    date_obj = datetime.strptime(str_data, "%d/%b/%Y:%H:%M:%S")
    formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date #2023-07-16 15:30:21 형태로 변환

# 웹 로그 parser , 필요한 정보만을 추출하여 리스트로 저장
def log_parser(log_list:list):
    parser_list=[] # 최종 결과 저장을 위한 빈 리스트 생성
    for one_line in log_list:
        line_info = [None] * 7 # 필요 한 정보 저장을 위한 배열 생성(size=7)
        split_data = one_line.split(' ') # 공백을 기준으로 split
        
        if len(split_data) == 1: continue #빈 줄일 경우 루프 건너뛰기
        
        # 필요한 정보 추출
        ip = split_data[0].replace(' ',"") #공백 제거
        
        date = split_data[3].replace("[","") #괄호 [ 제거
        date_obj = datetime.strptime(date,"%d/%b/%Y:%H:%M:%S") # 웹 로그의 날짜 형태
        date = date_obj.strftime("%Y-%m-%d %H:%M:%S") # 2023-07-16 15:30:21 형태로 변환
        
        get_post = split_data[5].replace('"',"") # 쌍따옴표" 제거
        request = split_data[6] #요청 메서드
        status_code = split_data[8].replace('"',"") # 쌍따옴표" 제거
        referring = split_data[10].replace('"',"") #참조 페이지
        user_agent = ' '.join(split_data[11:]).replace('"',"") #각 리스트를 공백으로 구분하여 join
        line_info = [ip, date, get_post, request, status_code, referring, user_agent] # 한줄 리스트로 저장
        
        parser_list.append(line_info) #각 라인을 결고 리스트에 추가
    return parser_list

# 웹 로그 저장 배열에서 날짜 정보를 읽어옴(중복이 없는 날짜 배열)
def return_day_info(log_parse_data:list):
    day_list = [x[1] for x in log_parse_data] # 날짜,시간 부분만 리스트 컴프리헨션
    day_list = [x.split(' ')[0] for x in day_list] # 날짜만 분리
    day_list = list(set(day_list)) # 중복제거
    return day_list

# 날짜 문자열 정보를 입력으로 받아서 필요한 데이터만 분류하여 반환 함.
def return_one_day_log(day:str, log_parse_data:list):
    one_day_log=[]  # 날짜별 정보를 저장하기 위한 빈 리스트 생성
    for one in log_parse_data: # 웹 로그 배열을 1개씩 반복
        if one[1].find(day) != -1: # 날짜가 같은 경우에만 실행 (-1: 날짜가 같음)
            one_day_log.append(one) # 결과 배열에 추가
    one_day_log.insert(0, ['IP','날짜','요청 메서드','요청 리소스',
                           '상태 코드','참조 페이지','사용자 에이전트']) # 제목행 추가
    return one_day_log
    
# 날짜별로 분리하여 csv 파일 생성
def write_csv_file(save_path:str, log_parse_data:list):
    day_info = return_day_info(log_parse_data) # 날짜 정보 반환(csv 생성 대상)
    for one_day in day_info: # 날짜별 반복 ex) 2023-07-17, 2023-07-18
        one_day_log = return_one_day_log(one_day, log_parse_data) # 날짜별 데이터 필터링
        save_fpath = save_path+'/'+one_day +'.csv' #저장 경로 및 파일명 설정
        with open(save_fpath, 'w', newline='') as file: # csv 파일 쓰기 및 저장
            writer = csv.writer(file) #
            writer.writerows(one_day_log)

if __name__ == '__main__':
    fpath = r"./웹로그 파일/log.txt" # 웹 로그 경로
    logs = read_log_file(fpath) #함수 실행
    parser = log_parser(logs)
    write_csv_file(fpath, parser)