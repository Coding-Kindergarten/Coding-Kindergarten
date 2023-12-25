import imaplib
import email
from email.header import decode_header, make_header
import os

# 첨부 파일 저장 경로
save_directory = r'C:\Users\NAME\Desktop\VSCODE BASIC\메일 첨부파일 저장소'

# IMAP 서버 세부 정보 
# google의 IMAP_SERVER는 ‘imap.gmail.com이며, PASSWORD는 ‘앱 비밀번호’ 입력 필요
IMAP_SERVER = 'imap.naver.com'
USERNAME = '메일 주소'
PASSWORD = '비밀번호'

# IMAP 서버에 연결
imap = imaplib.IMAP4_SSL(IMAP_SERVER, timeout=600)

# 계정에 로그인
imap.login(USERNAME, PASSWORD)

# 액세스하려는 이메일이 있는 메일박스(폴더) 선택
imap.select('inbox')  # 예: 'inbox', 'spam', 'sent' 등

# 이메일 검색
status, messages = imap.search(None, 'ALL')  # 다른 검색 기준을 사용할 수 있습니다

# 이메일 메시지 가져오기
for num in reversed(messages[0].split()):
    # fetch 메소드를 사용하여 이메일 메시지 가져오기
    status, msg_data = imap.fetch(num, '(RFC822)')
    # byte string을 이메일 객체로 변환
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)


    # 이메일의 발신자와 제목 출력
    fr = make_header(decode_header(msg.get('From')))
    subject = make_header(decode_header(msg.get('Subject')))

    print('Sent mail address:', fr)
    print('Email Subject:', subject)

    # 이메일 본문을 읽기 쉬운 형태로 변환
    body = None

    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)
                break
    else:
        body = msg.get_payload(decode=True)

    # 본문을 읽기 쉬운 형태로 변환
    if body is not None:
        try:
            body = body.decode('utf-8')
        except:
            body = body.decode('euc-kr')
    else:
        pass
    print('Mail body:', body)

    # 이메일 파트를 순회하며 첨부 파일 추출
    for part in msg.walk():
        
        # 일반적으로 첨부파일은 ‘multipart’에 포함되지 않으므로 multipart면 다음루프로 넘어감. 
        if part.get_content_maintype() == 'multipart':
            continue

        # 'Content-Disposition' 헤더가 있는지 확인 후, 없으면 다음루프로 넘어갑니다.
        if part.get('Content-Disposition') is None:
            continue

        # 'Content-Disposition' 헤더에서 파일 이름을 가져옵니다. 
        #만약 파일이름이 없으면 for문의 다음루프로 넘어갑니다.
        filename = part.get_filename()
        if not filename:
            continue     

        # 인코딩된 파일 이름을 디코딩하여 원래 파일 이름을 가져옵니다.
        filename = decode_header(filename)[0][0]

        # 디코딩한 filename이 바이트 문자열이라면	
        if isinstance(filename, bytes):
            try:
                # utf-8로 디코딩합니다.
                filename = filename.decode('utf-8')

            except UnicodeDecodeError:
                # utf-8로 디코딩 중 오류가 발생하면 euc-kr로 디코딩합니다.
                filename = filename.decode('euc-kr', errors='ignore')

        # 첨부 파일을 읽습니다.
        payload = part.get_payload(decode=True)

        # 지정된 디렉토리에 첨부 파일을 저장합니다.
        file_path = os.path.join(save_directory, filename)
        with open(file_path, 'wb') as f:
            f.write(payload)

# IMAP 서버 로그아웃 및 종료
imap.logout()
