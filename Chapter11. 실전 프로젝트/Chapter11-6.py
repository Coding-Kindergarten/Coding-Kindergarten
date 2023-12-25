# 파일, 폴더 자동 분류하기
# Step1. File Move를 위한 각 라이브러리 import
import os #파일명, 폴더명 정보를 읽어오기 위한 모듈
import shutil #파일 이동을 위한 모듈

# Step2. 정해진 경로의 파일명들을 리스트로 저장하여 반환한다.
path_before = r"./원본" #원본 파일들이 있는 폴더 경로
file_list = os.listdir(path_before) #폴더의 파일명을 리스트화
category = [] # 분류 데이터 저장을 위해 빈 리스트 생성

for file in file_list: # 위에서 저장한 list
    temp_list = file.split("_") #파일명중 "_"로 분리하여 리스트화
    category.append(temp_list[-2]) #리스트의 -2 인덱싱 데이터를 category에 추가
print("최종 category : ", category)

# Step3. 저장한 category 리스트의 중복제거
temp_set = set(category) #중복을 제거하기 위해 set 사용
folder_name_list = list(temp_set) #중복 제거 후 다시 리스트화

print("\n")
print("최종결과 :", folder_name_list)



#Step4. 앞 리스트 결과를 받아와서 명칭에 대한 폴더를 새로 생성한다.
try: os.makedirs("결과")
except: pass

path_after = r"./결과"
for folder_name in folder_name_list:
    try: #폴더가 이미 생성되어있을 경우를 위한 예외처리
        os.makedirs(path_after+"/"+folder_name)
    except: #에러가 발생하면 pass한다.
        pass
    

# Step5. 원본 파일 리스트 통해 폴더명 매칭 정보 딕셔너리 생성
filelist = os.listdir(path_before)
print("원본 파일 리스트 : ", filelist)

tmp_dict = {} # {'파일명' : '폴더명'} 매칭을 위한 빈 딕셔너리 정의
for file_name in file_list:
    tmp_list = file_name.split('_') #파일명을 "_" 기준으로 분리하여 리스트화
    #print("파일명 분리 리스트화 : ", tmp_list)
    #print("필요한 문자열 : ", tmp_list[-2])
    tmp_dict[file_name] = tmp_list[-2]
print('최종 결과 딕셔너리')
print(tmp_dict) #최종 결과 딕셔너리 출력
    
    
# Step 6. 딕셔너리 정보 활용하여 파일들을 각 분류 폴더로 이동
for file_name, folder_name in tmp_dict.items():
    shutil.move(path_before+"/"+file_name, path_after+"/"+folder_name)