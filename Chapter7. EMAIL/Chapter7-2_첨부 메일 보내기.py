#step1.관련 모듈, 클래스 불러오기
import os
import smtplib
from email.header import Header
from email.mime.base import MIMEBase # 메일 내용과 첨부파일을 담는 포맷 클래스
from email.mime.text import MIMEText # 메일 내용 작성 관련 클래스
from email.mime.application import MIMEApplication # 파일 첨부 관련 클래스

#step2.각 메일의 SMTP 서버를 dictionary로 정의
smtp_info = {
    'gmail.com': ('smtp.gmail.com', 587),
    'naver.com': ('smtp.naver.com', 587),
    'outlook.com': ('smtp-mail.outlook.com', 587),
    'hotmail.com': ('smtp-mail.outlook.com', 587),
    'yahoo.com': ('smtp.mail.yahoo.com', 587),
    'nate.com': ('smtp.mail.nate.com', 465),
    'daum.net': ('smtp.daum.net', 465),
    'hanmail.net': ('smtp.daum.net',465)
}

#step3.메일 보내는 함수 정의 (발신 메일, 수신 메일(여러개 가능), 제목, 본문, 첨부파일 경로, 비밀번호)
def send_email(sender_email, receiver_emails, subject, message, attachments=(), password='', subtype='plain'):

    # Step 4: 멀티 파트 포맷을 객체화
    mail_format = MIMEBase('multipart', 'mixed')

    # Step 5: 입력한 이메일 주소, 제목, 본문 등을 암호화하여 메일 형식으로 입력
    mail_format['From'] = sender_email #발신 메일을 포맷에 입력
    mail_format['To'] = ', '.join(receiver_emails) #리스트로 된 수신 메일 목록을 문자열로 변환
    mail_format['Subject'] = Header(subject.encode('utf-8'), 'utf-8') #utf-8로 인코딩 후, Header 모듈로 메일 제목 입력
    message = MIMEText(message.encode('utf-8'), _subtype=subtype, _charset='utf-8') #메일 본문 인코딩
    mail_format.attach(message) #인코딩한 본문 mail_format에 입력

    #step6.여러개의 파일을 하나씩 첨부
    for file_path in attachments:
        folder, file = os.path.split(file_path)
        
        with open(file_path, 'rb') as file_obj: # 첨부 파일 열기
            attachment_contents = file_obj.read()
    
        attachment = MIMEApplication(attachment_contents, _subtype=subtype)
        attachment.add_header('Content-Disposition', 'attachment', filename=(Header(file, 'utf-8').encode()))
        mail_format.attach(attachment)


    #step7.SMTP 서버 로그인 및 작성된 메일 보내기
    username, host = sender_email.rsplit("@",1) #발신인 메일 주소의 @를 기준으로 username과 host로 나눔

    smtp_server, port = smtp_info[host] #step2의 dict를 이용해서 host와 port 정보들을 받아옴

    # SMTP 서버 접속 여부 확인
    if port == 587:
        smtp = smtplib.SMTP(smtp_server, port)
        rcode1, _ = smtp.ehlo()
        rcode2, _ = smtp.starttls()

    else:
        smtp = smtplib.SMTP_SSL(smtp_server, port)
        rcode1, _ = smtp.ehlo()
        rcode2 = 220
    
    if rcode1 != 250 or rcode2 != 220:
        smtp.quit()
        return '연결에 실패하였습니다.'

    smtp.login(sender_email, password)
    smtp.sendmail(sender_email, receiver_emails, mail_format.as_string())
    smtp.quit()

#step8.실제 함수 실행 부분
sender_address = '보내는 메일 주소'
password = '보내는 메일 비밀번호'
receiver_addresses = ['받는 메일 주소 1', '받는 메일 주소 2']


subject = '파이썬으로 메일 보내기 테스트'


message = """
안녕하세요, 파이썬 코드로 제작된 '메일 전송 봇'입니다.


첨부드리는 파일 참고 부탁드립니다.


감사합니다.
"""

attachment_files = ['첨부파일1.PNG', '첨부파일2.xlsx','첨부파일3.py']
send_email(sender_address, receiver_addresses, subject, message, attachment_files, password=password)
