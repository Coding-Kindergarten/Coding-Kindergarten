import smtplib

# smtplib.SMTP('사용할 SMTP 서버의 URL', PORT)
smtp = smtplib.SMTP('smtp.gmail.com', 587) # Google
# smtp = smtplib.SMTP('smtp.naver.com', 587) # Naver

# TLS 암호화 (TLS 사용할 때에만 해당코드 입력_gmail, naver는 TLS 사용)
smtp.starttls()

# gmail - smtp.login('메일 주소', '비밀번호')
smtp.login('xxxxx@gmail.com', '지난 시간 받았던 16자리 앱 비밀번호')

# naver - smtp.login('메일 주소', '비밀번호')
# smtp.login('xxxxx@naver.com', '비밀번호')

# 수신 메일, 발신 메일, 제목, 내용 입력
from_addr = 'sender@example.com'
to_addrs = ['recipient1@example.com', 'recipient2@example.com']
subject = '메일 자동화 테스트용 발신'
body = '''
원하는 메세지를 입력하세요.


여러줄 메일을 보내려면 이렇게 보내시면 됩니다.


감사합니다.
'''

# email 모듈의 MIMEText 클래스 import
from email.mime.text import MIMEText


# MIMEText에 입력
msg = MIMEText(body)
msg['Subject'] = subject
msg['From'] = from_addr
msg['To'] = ', '.join(to_addrs)

# 메세지 보내기
smtp.sendmail(msg['From'], msg['To'], msg.as_string())

# smtp 종료
smtp.quit()