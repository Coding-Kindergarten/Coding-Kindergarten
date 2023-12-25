import imaplib
import email
from email.header import decode_header, make_header

imap = imaplib.IMAP4_SSL('imap.gmail.com')

# imap.login('메일 주소', '비밀번호')
sender_adress = 'your_email@gmail.com'
password = '지난 시간 받았던 16자리 앱 비밀번호'
imap.login(sender_adress, password)

# 사서함 선택 ("받은 메일함")
imap.select("INBOX")

# 사서함의 모든 메일의 UID (고유식별자) 정보 가져오기 (만약 특정 발신 메일만 선택하고 싶다면 'ALL' 대신에 '(FROM "xxxxx@naver.com")' 입력
status, messages = imap.search(None, 'ALL')

# b’숫자’ 형태의 UID(고유식별자)를 요소로 하는 리스트
messages = messages[0].split()

# 0이 가장 마지막 메일, -1이 가장 최신 메일
recent_email = messages[-1]

# fetch 함수로 메일 가져오기
status, message = imap.fetch(recent_email, "(RFC822)")

# 바이트 문자열
raw = message[0][1]

# 바이트 문자열을 유니코드 문자열로 디코딩
raw_readable = message[0][1].decode('utf-8')

# raw_readable에서 원하는 부분만 파싱하기 위해 email 모듈을 이용해 변환
email_message = email.message_from_string(raw_readable)

# 보낸 메일 주소
fr = make_header(decode_header(email_message.get('From')))

# 메일 제목
subject = make_header(decode_header(email_message.get('Subject')))

# 메일 내용
if email_message.is_multipart():
    for part in email_message.walk():
        ctype = part.get_content_type()
        cdispo = str(part.get('Content-Disposition'))
        if ctype == 'text/plain' and 'attachment' not in cdispo:
            body = part.get_payload(decode=True)  # decode
            break
else:
    body = email_message.get_payload(decode=True)

# 사람이 읽을 수 있는 형태로 메일 본문을 변경
body = body.decode('utf-8')

print('보낸 메일 주소:', fr)
print('메일 제목:',subject)
print('메일 본문:', body)

# 메일함을 닫고 imap 서버에서 로그아웃
imap.close()
imap.logout()
