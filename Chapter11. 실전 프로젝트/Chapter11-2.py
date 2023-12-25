#엑셀 데이터를 PDF 파일로 자동 변환하기
# Step1. Import 및 Excel 파일이 있는 경로 설정
import win32com.client 
import os
path = "./견적서" # 견적서 폴더 경로

# Step2. OS 라이브러리 통해 설정한 경로에 있는 파일명 경로 출력해보기
for one in os.walk(path):
    print('해당 경로 : {}'.format(one[0]))
    print("해당 경로의 폴더 : {}".format(one[1]))
    print('파일 리스트 : {}'.format(one[2]))

# Step3. 위 결과 활용하여 모든 파일의 절대경로를 리스트로 반환
file_path_list = [] # 경로 저장을 위한 빈 리스트 생성
for path, folder_list, file_list in os.walk(path): # os.walk 함수
    for file_name in file_list: # 파일리스트를 for 반복문 진행
        file_all_path =  path+"/"+file_name # 설정 경로 + "/" + 파일이름 형태 (절대 경로)
        file_path_list.append(file_all_path)  # 리스트에 추가
    
# Step4. 엑셀 Application 객체 생성
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = False 
print("win32com Excel Application 객체 생성 : ", excel)


# Step5. 각 엑셀 파일에 대한 시트이름 반환
excel_sht_info={} # 빈 딕셔너리 생성
for file_path in file_path_list: # file_path 반복문
    try:
        wb = excel.Workbooks.Open(file_path) #엑셀 Workbook 열기
        sheet_names = [sheet.Name for sheet in wb.Sheets] #시트 이름 리스트화
        excel_sht_info[file_path] = sheet_names #딕셔너리 저장
    except: 
        pass
    
for key, value in excel_sht_info.items(): # 딕셔너리 출력
    print("key : ", key) # key는 엑셀파일의 경로
    print("Value : ", value) # value는 엑셀파일 시트 리스트

# Step6. 각 파일 pdf 변환
idx = 1 #파일명 중복 방지를 위한 인덱스 부여
for file_path, sheet_list in excel_sht_info.items():
    wb = excel.Workbooks.Open(file_path) # Workbook 객체 생성
    for sht_name in sheet_list: # 시트 리스트 반복
        ws_sht = wb.Worksheets(sht_name) # Worksheet 객체 생성
        save_file_path = path+ '/' + '{}_{}.pdf'.format(idx, sht_name) # 파일명, 저장경로 설정
        ws_sht.Select() #해당 시트 선택(활성화)
        wb.ActiveSheet.ExportAsFixedFormat(0, save_file_path) # pdf 파일 변환
        print("{} 시트 pdf 파일 생성 완료".format(sht_name)) # 완료 메시지
        idx+=1 # 중복 방지 인덱스 증가

# Step7. 엑셀 종료
wb.Close(False)
excel.Quit()