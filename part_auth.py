"""
part_auth.py — 로그인 / 회원가입 담당
"""
import csv
import re

from part_common import USER_CSV, clear_screen, print_box


def show_login_menu(): # 로그인 첫 메뉴
    clear_screen()
    lines = [
        '1. 로그인',
        '2. 회원가입',
        '3. 프로그램 종료'
    ]
    print_box(lines, title='🏥 병원 예약 관리 시스템 로그인')
    print()

current_user = None  # 현재 로그인한 사용자 정보를 저장


'''============= 로그인 ============='''
def login(current_user): # 로그인 진행
    # 이미 로그인되어 있으면 다시 로그인하지 않음
    if current_user is not None:
        print('이미 로그인되어 있습니다.')
        return current_user

    user_id = input("아이디를 입력하세요 : ")
    password = input("비밀번호를 입력하세요 : ")

    # 입력한 아이디/비밀번호가 일치하는 사용자 찾기
    user = find_user(user_id, password)

    # 사용자가 없으면 로그인 실패
    if user is None:
        print('아이디 또는 비밀번호가 올바르지 않습니다.\n')
        return current_user
    # 로그인한 사용자 정보를 반환
    print(user['이름'], '님 로그인 성공\n')
    return user

# 입력한 아이디/비밀번호가 일치하는 사용자 찾기

def find_user(user_id, password):
    try:
        with open(USER_CSV, 'r', encoding='utf-8-sig', newline='') as file:
            reader = csv.DictReader(file)

            for user in reader:
                if (user['아이디'] == user_id and user['비밀번호'] == password and user['회원상태'] == '정상'):
                    return user

    except FileNotFoundError:
        print(f'{USER_CSV} 파일을 찾을 수 없습니다.')

    return None


'''============= 회원가입 ============='''
def is_duplicate_user_id(user_id):
    with open(USER_CSV,'r',encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        for user in reader:
            if user['아이디'] == user_id:
                return True
        return False

# 연락처 중복 확인

def is_duplicate_phone(phone_number):
    with open(USER_CSV,'r',encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        for user in reader:
            if user['연락처'] == phone_number:
                return True
        return False

# 환자번호 생성

def generate_user_number():
    max_number = 0
    with open(USER_CSV,'r',encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        for user in reader:
            user_number = user['환자번호']

            if user_number.startswith('P'):
                number = int(user_number[1:])

                if number > max_number:
                    max_number = number
    next_number = max_number + 1
    return f'P{next_number:06d}'

# 주민등록번호 형식 확인

def validate_resident_number(resident_number):
    pattern = r'^\d{6}-\d{7}$'

    if re.match(pattern, resident_number):
        return True
    return False

# 주민등록번호에서 생년월일과 이름 추출

def parse_resident_number(resident_number):
    birth_date = resident_number[:6]
    gender_number = resident_number[7]

    if gender_number in ['1', '3']:
        gender = '남'

    elif gender_number in ['2', '4']:
        gender = '여'

    else:
        return None, None

    return birth_date, gender

# 연락처 형식 확인

def validate_phone_number(phone_number):
    pattern = r'^010-\d{4}-\d{4}$'

    if re.match(pattern, phone_number):
        return True

    return False

# 새로운 회원 csv 저장

def save_user(new_user):
    fieldnames = [
        '환자번호',
        '아이디',
        '비밀번호',
        '이름',
        '생년월일',
        '성별',
        '연락처',
        '비밀번호초기화',
        '회원상태',
        '권한'
    ]
    with open(USER_CSV, 'a', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(new_user)

# 회원가입

def signup():
    print('\n======== 병원 예약 관리 ========')
    print('회원가입을 취소하려면 취소를 입력하세요.\n')

    # 아이디 입력
    while True:
        new_user_id = input('아이디를 입력하세요 : ')

        if new_user_id == '취소':
            print('회원가입을 취소합니다.\n')
            return

        if new_user_id == '':
            print('아이디를 입력하세요\n')
            continue

        if not new_user_id.isalnum():
            print('아이디는 영문과 숫자만 입력할 수 있습니다.\n')
            continue

        if is_duplicate_user_id(new_user_id):
            print('이미 사용 중인 아이디입니다.\n')
            continue
        break

    while True:
        new_password = input('비밀번호를 입력하세요 : ').strip()

        if new_password == '취소':
            print('회원가입을 취소합니다.\n')
            return

        if len(new_password) < 8:
            print('비밀번호는 8자 이상 입력하세요\n')
            continue

        confirm_password = input('비밀번호를 다시 입력하세요 : ').strip()

        if new_password != confirm_password :
            print('비밀번호가 일치하지 않습니다.\n')
            continue

        break

    # 이름 입력
    while True:
        user_name = input('이름을 입력하세요 : ').strip()

        if user_name == '취소':
            print('회원가입을 취소합니다.\n')
            return

        if user_name == '':
            print('이름을 입력하세요 ; \n')
            continue
        break

    # 주민등록번호 입력
    while True:
        resident_number = input('주민등록번호를 입력하세요(000000-0000000) : ').strip()

        if resident_number == '취소':
            print('회원가입을 취소합니다.\n')
            return

        if not validate_resident_number(resident_number) :
            print('주민등록번호 형식이 올바르지 않습니다.\n')
            continue

        birth_date, gender = parse_resident_number(resident_number)

        if birth_date is None:
            print('주민등록번호의 성별 구분 번호가 올바르지 않습니다.\n')
            continue

        break

    # 연락처 입력
    while True:
        phone_number = input('연락처를 입력하세요(010-0000-0000) : ').strip()

        if phone_number == '취소':
            print('회원가입을 취소합니다.\n')
            return

        if not validate_phone_number(phone_number) :
            print('연락처 형식이 올바르지 않습니다.\n')
            continue

        if is_duplicate_phone(phone_number):
            print('이미 가입한 연락처 입니다.\n')
            continue
        break

    # 환자번호 자동 생성
    patient_number = generate_user_number()

    # 저장할 회원 정보
    new_user = {
        '환자번호': patient_number,
        '아이디': new_user_id,
        '비밀번호': new_password,
        '이름': user_name,
        '생년월일': birth_date,
        '성별': gender,
        '연락처': phone_number,
        '비밀번호초기화': 'N',
        '회원상태': '정상',
        '권한': 'user'
    }

    #최종 확인
    print('\n======== 회원가입 정보 확인 ========')
    print(f'환자번호 : {patient_number}')
    print(f'아이디   : {new_user_id}')
    print(f'이름     : {user_name}')
    print(f'생년월일 : {birth_date}')
    print(f'성별     : {gender}')
    print(f'연락처   : {phone_number}')
    print('==================================\n')

    while True:
        save_choice = input('회원가입 정보를 저장하시겠습니까? (Y/N) : ')
        save_choice = save_choice.strip().upper()

        if save_choice == 'Y':
            save_user(new_user)

            print('\n회원가입이 완료되었습니다.')
            print('발급된 환자번호 : ', patient_number)
            print('로그인 화면으로 이동합니다.\n')
            return

        elif save_choice == 'N':
            print('회원가입을 취소합니다.\n')
            return

        else:
            print('Y 또는 N을 입력하세요.\n')

# 로그아웃 기능

def logout(current_user):
    # 로그인 상태가 아니면 종료
    if current_user is None:
        print('로그인 상태가 아닙니다.')
        return None
    # 로그아웃하면 현재 사용자를 None으로 반환
    print(current_user['이름'], '님 로그아웃')
    return None