#테스트 메시지
'''
완료: ✅
진행중: 🔥
오류/수정: 🚫
[첫 화면]
✅ 1. 로그인   (아이디로 일반 회원/관리자 자동 구분)
2. 회원가입
✅ 3. 프로그램 종료

[로그인 후 - 일반 회원]
🔥 1. 진료과/의료진 조회
🔥 2. 예약 (진료과로 예약 / 과거 이력으로 예약) - 캘린더
🔥 3. 내 예약 조회/변경/취소
4. 진료 이력 조회 (진료비 확인)
✅ 5. 로그아웃 (→ 첫 화면으로 이동)

[로그인 후 - 관리자] (관리자 계정 1개, 별도 메뉴 없이 로그인 시 자동 구분)
1. 회원 조회 (수정/삭제 포함)
2. 예약 조회 (수정/취소 포함)
3. 진료과/의료진 조회 (수정/삭제 포함)
4. 진료비/매출 조회
✅ 4. 로그아웃 (→ 첫 화면으로 이동)

소정 : 1+4+관4
고은 : 2
유진 : 3+관1
민정 : 관2+관3

'''
import csv
import pprint
import re
from getpass import getpass
from tabnanny import check

from tabulate import tabulate
from wcwidth import wcswidth
import calendar
import datetime
import os
os.system("") # cmd에서 색을 나타내기 위한 새로고침 기능

def show_login_menu(): # 로그인 첫 메뉴
    print('======== 🏥 병원 예약 관리 시스템 로그인 ========')
    print('1. 로그인')
    print('2. 회원가입')
    print('3. 프로그램 종료\n')

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
    with open('user.csv','r',encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for user in reader:
            if user['아이디'] == user_id and user['비밀번호'] == password:
                return user
    # 일치하는 사용자가 없으면 None 반환
    return None

'''============= 회원가입 ============='''
# 아이디 중복 확인
def is_duplicate_user_id(user_id):
    with open('user.csv','r',encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        for user in reader:
            if user['아이디'] == user_id:
                return True
        return False

# 연락처 중복 확인
def is_duplicate_phone(phone_number):
    with open('user.csv','r',encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        for user in reader:
            if user['연락처'] == phone_number:
                return True
        return False

# 환자번호 생성
def generate_user_number():
    max_number = 0
    with open('user.csv','r',encoding='utf-8-sig') as file:
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
    with open('user.csv', 'a', encoding='utf-8-sig', newline='') as file:
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


'''============= 사용자 메뉴 ============='''
# 사용자 메뉴 전체 흐름
def user_view(current_user):
    while True:
        user_menu(current_user)
        choice = input('메뉴를 선택하세요 : ')

        if choice == '1':
            department_doctor_view()

        elif choice == '2':
            reservation(current_user)

        elif choice == '3':
            my_reservation(current_user)

        elif choice == '4':
            medical_history(current_user)

        elif choice == '5':
            current_user = logout(current_user)
            return current_user

        else:
            print('올바른 메뉴 번호를 입력하세요.\n')

def user_menu(current_user): # 사용자 로그인 시 메뉴
    print('\n======== 병원 예약 관리 ========')
    print(f"현재 사용자 : {current_user['이름']} / {current_user['환자번호']}")
    print('1. 진료과 조회')
    print('2. 예약하기')
    print('3. 내 예약 관리')
    print('4. 진료 이력 조회')
    print('5. 로그아웃')
    print('=============================\n')


'''============= 진료과/의료진 조회 ============='''
# 진료과/의료진 조회 전체 흐름
def department_doctor_view():
    while True:
        show_departments()
        choice = input('진료과를 선택하세요 > ')

        if choice == '1':
            show_doctors_by_department('내과')

        elif choice == '2':
            show_doctors_by_department('외과')

        elif choice == '3':
            show_doctors_by_department('정형외과')

        elif choice == '4':
            show_doctors_by_department('소아청소년과')

        elif choice == '5':
            show_doctors_by_department('피부과')

        elif choice == '0':
            break

        else:
            print('올바른 메뉴 번호를 입력하세요.\n')

# 진료과 전체 목록 출력
def show_departments():
    print('======== 진료과 ========')
    print('1. 내과')
    print('2. 외과')
    print('3. 정형외과')
    print('4. 소아과')
    print('5. 피부과')
    print('0. 이전')
    print('=============================\n')

# wcswidth 기준으로 가운데 정렬해주는 함수 (새로 추가)
def center_by_width(text, width):
    text_width = wcswidth(text)
    total_padding = width - text_width
    left = total_padding // 2
    right = total_padding - left
    return ' ' * left + text + ' ' * right

# 선택한 진료과의 의료진 전체 출력
def show_doctors_by_department(department):
    doctor_list = []
    phone_number = ''

    with open('doctors.csv', 'r', encoding='utf-8-sig',newline='') as file:
        reader = csv.DictReader(file)

        num = 1

        for doctor in reader:
            if doctor['진료과'] == department:
                phone_number = doctor['진료과전화번호']

                doctor_list.append([
                    num,
                    doctor['이름'],
                    doctor['진료요일'].replace('월,화,수,목,금', '월~금'),
                    f"{doctor['진료시작시간']} ~ "
                    f"{doctor['진료종료시간']}"
                ])
                num += 1

    if doctor_list:
        table = (tabulate(
            doctor_list,
            headers=[
                '번호',
                '의료진',
                '진료 요일',
                '진료 시간'
                ],
            tablefmt='grid',
            disable_numparse=True,
            colalign=(
                'center',  # 번호
                'center',  # 의료진
                'center',  # 진료요일
                'center'  # 진료시간
            )))

        first_line = table.splitlines()[0]
        table_width = wcswidth(first_line)
        title = f'🩺 [{department}] 의료진'

        print('=' * table_width)
        print(center_by_width(title, table_width))
        print('=' * table_width)
        print()
        print(table)
        print()
        print(f'📞 진료과 대표번호 : {phone_number}')
        print('=' * table_width)
        print('\n')

    else:
        print('등록된 의료진이 없습니다.')

'''============= 예약 ============='''
# 예약 전체 흐름
def reservation(current_user):
    while True:
        reservation_menu() # 예약 방법 메뉴

        choice = input('예약 방법을 선택하세요 > ')

        if choice == '1':
            is_success = reserve_by_department(current_user)  # 진료과로 예약
            if is_success:  # 예약이 성공(True)했다면 예약 메뉴를 완전히 빠져나감
                return

        elif choice == '2':
            is_success = reserve_by_history(current_user)  # 과거 진료 이력으로 예약
            if is_success:  # 예약이 성공(True)했다면 예약 메뉴를 완전히 빠져나감
                return

        elif choice == '0':
            print('이전 메뉴로 돌아갑니다.')
            break

        else:
            print('올바른 메뉴 번호를 입력하세요.\n')

# 예약 방법 메뉴 출력
def reservation_menu():
    print('\n========== 예약하기 ==========')
    print('1. 진료과로 예약')
    print('2. 과거 진료 이력으로 예약')
    print('\n0. 이전 메뉴')
    print('============================\n')

# 진료과로 예약
def reserve_by_department(current_user):
    # 1. 데이터 불러오기
    doctors = load_doctors()  # load_doctors(): 의료진 정보를 불러오기 위한 함수
    reservations = load_reservations()  # load_reservations : 전체 예약 정보를 불러오기 위한 함수

    # 2. 진료과 선택
    department = select_department(doctors)  # select_department : 진료과를 선택하기 위한 함수
    if department is None:
        return

    # 3. 의료진 선택
    doctor = select_doctor(doctors, department)  # select_doctor : 의료진을 선택하기 위한 함수
    if doctor is None:  # 의료진이 없어서 None이 반환되었다면
        return  # 함수를 즉시 종료하고 예약 메뉴로 돌아감

    while True:
        # 4. 날짜 선택
        date_str = select_date(doctor, reservations)  # select_date : 날짜를 선택하기 위한 함수
        if date_str is None:  # '취소'을 눌러서 None이 반환되었다면
            return  # 예약 메뉴로 돌아감

        # 5. 시간 선택
        time_str = select_time(doctor, date_str, reservations)
        if time_str is None:
            print("\n시간 선택을 취소했습니다. 다시 날짜를 선택해주세요.")
            continue

        # 날짜와 시간을 모두 정상적으로 선택했다면 루프 탈출
        break

    print(f"\n========================= [예약 상세] =======================")
    print(f"예약날짜: {date_str}")
    print(f"예약시간: {time_str}")
    print(f"진료과 및 의료진 이름: {doctor['진료과']} {doctor['이름']}")
    print(f"===========================================================")

    while True:
        confirm = input("\n예약을 확정하시겠습니까? (Y/N) > ").strip().upper()

        if confirm == 'Y':
            # 6. 예약 정보 저장
            patient_id = current_user['환자번호']
            save_reservation(patient_id, doctor, date_str, time_str, reservations)
            return True  # True를 반환하여 성공했음을 알림

        elif confirm == 'N':
            # 예약하지 않고 메뉴로 돌아가기
            print("\n진행 중인 예약이 취소되었습니다. 예약 초기 메뉴로 돌아갑니다.")
            return False  # 취소 시 False 반환

        else:
            print("올바른 입력이 아닙니다. Y 또는 N을 입력해주세요.")

    # 과거 진료 이력으로 예약
def reserve_by_history(current_user):
    # 1. 예약 데이터 및 의료진 데이터 불러오기
    reservations = load_reservations()
    doctors = load_doctors()

    patient_id = current_user['환자번호']

    # 2. 해당 환자의 '진료완료' 기록만 필터링
    history_records = [record for record in reservations if record['환자번호'] == patient_id and record['상태'] == '진료완료']

    # 3. 기록이 없을 경우 처리
    if not history_records:
        print("\n과거 진료 완료 기록이 없습니다. 예약 초기 메뉴로 돌아갑니다.")
        return

    # 의료진 번호로 의료진 정보를 쉽게 찾기 위해 딕셔너리 생성
    doctor_dict = {doctor_info['의료진번호']: doctor_info for doctor_info in doctors}

    print(f"\n===================== [{current_user['이름']}]님의 진료 이력 =====================")

    # 출력 및 선택을 위해 리스트에 저장
    display_list = []
    for index, record in enumerate(history_records, 1):
        doctor_info_id = record['의료진번호']
        doctor_info = doctor_dict.get(doctor_info_id)

        # 만약 의료진 정보가 있다면 내역에 추가
        if doctor_info:
            date = record['예약날짜']
            department_name = doctor_info['진료과']
            doctor_info_name = doctor_info['이름']

            display_list.append(doctor_info)
            print(f"{index}. 진료과: {department_name} / 의료진: {doctor_info_name} / 진료 날짜: {date}")

    print("\n0. 이전 메뉴")
    print("==============================================================")

    # 4. 예약할 항목 선택
    while True:
        try:
            value = input("\n다시 예약할 진료 항목의 번호를 선택하세요 > ").strip()

            if value == '0':
                return

            if not value:
                raise ValueError("공백 입력은 불가합니다.")

            choice = int(value)
            if not (1 <= choice <= len(display_list)):
                raise ValueError("범위를 벗어난 번호입니다.")

            selected_doctor = display_list[choice - 1]
            break

        except ValueError as error:
            if "invalid literal" in str(error):
                print("오류: 문자 입력은 불가합니다. 숫자로만 입력해주세요.")
            else:
                print(f"오류: {error}")

    # 5. 기존 방식과 동일하게 예약 진행 (선택한 의료진 정보 사용)
    print(f"\n[{selected_doctor['진료과']} {selected_doctor['이름']} 원장] 예약 단계로 넘어갑니다.")

    while True:
        date_str = select_date(selected_doctor, reservations)
        if date_str is None:  # 과거 이력으로 예약 중 날짜 선택 취소
            return

        time_str = select_time(selected_doctor, date_str, reservations)
        if time_str is None:  # 과거 이력으로 예약 중 시간 선택 취소
            print("\n시간 선택을 취소했습니다. 다시 날짜를 선택해주세요.")
            continue

        break

    # 예약 상세 확인 및 저장 로직
    print(f"\n========================= [예약 상세] =======================")
    print(f"예약날짜: {date_str}")
    print(f"예약시간: {time_str}")
    print(f"진료과 및 의료진 이름: {selected_doctor['진료과']} {selected_doctor['이름']}")
    print(f"===========================================================")

    while True:
        confirm = input("\n예약을 확정하시겠습니까? (Y/N) > ").strip().upper()

        if confirm == 'Y':
            save_reservation(patient_id, selected_doctor, date_str, time_str, reservations)
            return True
        elif confirm == 'N':
            print("\n진행 중인 예약이 취소되었습니다. 예약 초기 메뉴로 돌아갑니다.")
            return False
        else:
            print("올바른 입력이 아닙니다. Y 또는 N을 입력해주세요.")

def load_doctors():
    # 의료진 정보를 CSV에서 불러옴
    doctors = []
    try:
        with open('doctors.csv', 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # .append(): 리스트(doctors)의 맨 마지막에 새로운 데이터(row)를 하나씩 추가
                doctors.append(row)
    except FileNotFoundError:
        print(f"오류: {'doctors.csv'} 파일이 존재하지 않습니다.")
        return None
    return doctors

def load_reservations():
    # 전체 예약 정보를 CSV에서 불러옴
    reservations = []
    try:
        with open('reservations_total_only.csv', 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                reservations.append(row)
    except FileNotFoundError:
        pass
    return reservations

def select_department(doctors):
    # 진료과를 선택하기 위한 함수 정의
    # set(): 중복된 데이터를 제거
    # sorted(): 데이터를 가나다순(또는 오름차순)으로 정렬
    departments = sorted(list(set(doctor_info['진료과'] for doctor_info in doctors)))

    print("\n======== 진료과 선택 =========")
    # enumerate(리스트, 1): 리스트의 내용물을 꺼낼 때 1부터 시작하는 순서 번호(index)도 같이 꺼냄
    for index, department_name in enumerate(departments, 1):
        print(f"{index}. {department_name}")
    print("\n0. 이전 메뉴")
    print("===========================")

    while True:
        try:
            # .strip(): 사용자가 실수로 스페이스바를 누르거나 엔터를 친 '공백'을 양끝에서 깔끔하게 잘라내는 기능
            value = input("\n예약할 진료과 번호를 선택하세요: ").strip()
            if value == '0':
                return None
            if not value:
                raise ValueError("공백 입력은 불가합니다.")
            choice = int(value)
            if not (1 <= choice <= len(departments)):
                raise ValueError("범위를 벗어난 번호입니다.")
            return departments[choice - 1]
        except ValueError as error:
            if "invalid literal" in str(error):
                print("오류: 문자 입력은 불가합니다. 숫자로만 입력해주세요.")
            else:
                print(f"오류: {error}")

def select_doctor(doctors, department):
    # 근무상태가 '진료중'인 해당 진료과 의사만 필터링
    available_doctors = [doctor_info for doctor_info in doctors if
                         doctor_info['진료과'] == department and doctor_info['근무상태'] == '진료중']

    if not available_doctors:
        print("현재 해당 진료과에 예약 가능한 의료진이 없습니다.")
        return None

    print(f"\n======================= {department} 의료진 선택 ========================")
    for index, doctor_info in enumerate(available_doctors, 1):
        print(
            f"{index}. {doctor_info['이름']} (진료요일: {doctor_info['진료요일']} / 진료시간: {doctor_info['진료시작시간']} ~ {doctor_info['진료종료시간']})")
    print("\n0. 이전 메뉴")
    print(f"==============================================================")

    while True:
        try:
            value = input("\n예약을 원하는 의료진 번호를 숫자로 입력하세요: ").strip()
            if value == '0':
                return None
            if not value:
                raise ValueError("공백 입력은 불가합니다.")
            choice = int(value)
            if not (1 <= choice <= len(available_doctors)):
                raise ValueError("범위를 벗어난 번호입니다.")
            return available_doctors[choice - 1]
        except ValueError as error:
            if "invalid literal" in str(error):
                print("오류: 문자 입력은 불가합니다. 숫자로만 입력해주세요.")
            else:
                print(f"오류: {error}")

def create_time_slots(start_time, end_time):
    # 시작 시간부터 종료 시간까지 30분 단위의 시간 슬롯을 생성
    slots = []
    # map(int, 리스트): 리스트 안의 모든 데이터를 정수(int)로 한 번에 변환
    start_hour, start_minute = map(int, start_time.split(':'))
    end_hour, end_minute = map(int, end_time.split(':'))

    current_hour, current_minute = start_hour, start_minute
    while current_hour < end_hour or (current_hour == end_hour and current_minute < end_minute):
        slots.append(f"{current_hour:02d}:{current_minute:02d}")
        current_minute += 30
        if current_minute >= 60:
            current_hour += 1
            current_minute -= 60
    return slots

def get_available_times(doctor, date_str, reservations):
    # 특정 날짜의 예약 가능한 시간 목록을 반환
    # 주말(토, 일)은 예약 불가
    year, month, day = map(int, date_str.split('-'))
    target_date = datetime.date(year, month, day)

    # target_date.weekday(): 월요일은 0, 일요일은 6과 같이 요일을 숫자로 안내
    if target_date.weekday() >= 5:  # 5(토요일), 6(일요일)이면 빈 리스트 반환
        return []

    weekday_map = {0: '월', 1: '화', 2: '수', 3: '목', 4: '금', 5: '토', 6: '일'}
    target_weekday_str = weekday_map[target_date.weekday()]

    working_days = doctor.get('진료요일', '월,화,수,목,금')

    if target_weekday_str not in working_days:
        return []

    if target_date < datetime.date.today():
        return []

    slots = create_time_slots(doctor['진료시작시간'], doctor['진료종료시간'])

    for reservation_record in reservations:
        if reservation_record['의료진번호'] == doctor['의료진번호'] and reservation_record['예약날짜'] == date_str:
            if reservation_record['상태'] in ['예약완료', '진료완료']:
                if reservation_record['예약시간'] in slots:
                    # .remove(): 리스트 안에서 해당하는 특정 데이터 하나를 찾아 삭제
                    slots.remove(reservation_record['예약시간'])

    return slots

def print_calendar(year, month, doctor, reservations):
    # 해당 월의 달력을 출력하고 예약 마감 날짜를 표시
    # calendar.monthcalendar(): 해당 월의 달력을 1주 단위로 묶어서 리스트 형태로 반환
    month_calendar = calendar.monthcalendar(year, month)
    print(f"\n===================== {year}년 {month}월 예약 달력 =====================")
    print("                    월    화    수   목   금")

    fully_booked_dates = []
    RED = '\033[91m'  # 밝은 빨간색 시작
    RESET = '\033[0m'  # 색상 초기화 (원래 색으로 되돌림)

    for week in month_calendar:
        week_string = ""
        # week[:5]: 리스트를 처음부터 5번째 항목(월~금)까지만 잘라서 사용 (슬라이싱)
        for _, day in enumerate(week[:5]):
            if day == 0:
                week_string += "     "
            else:
                date_str = f"{year}-{month:02d}-{day:02d}"
                available_times = get_available_times(doctor, date_str, reservations)

                if len(available_times) == 0:
                    week_string += f" {RED}{day:2d}{RESET}  "
                    fully_booked_dates.append(date_str)
                else:
                    week_string += f" {day:2d}  "

        if week_string.strip():
            print(f'                   {week_string}')

    print(f"\n                 * {RED}빨간색 숫자{RESET}: 예약 불가능한 날짜")
    print(f"=============================================================")

def select_date(doctor, reservations):
    # 예약할 날짜를 달력에서 선택
    now = datetime.date.today()
    current_year = now.year
    current_month = now.month

    while True:
        print_calendar(current_year, current_month, doctor, reservations)

        print()
        print("(이전달: 이전 /  다음달: 다음  /  예약 취소: 취소) >> 해당 메뉴 이용 시 아래에 입력")
        print()

        try:
            value = input("예약할 날짜(일)를 숫자로 입력하세요: ").strip()

            # .lower(): 입력된 영어 문자열을 모두 소문자로 변환 (대소문자 상관없이 인식하기 위함)
            if value.lower() == '취소':
                print("\n진행 중인 예약이 취소되었습니다. 예약 초기 메뉴로 돌아갑니다.")
                return None
            elif value.lower() == '다음':
                current_month += 1
                if current_month > 12:
                    current_year += 1
                    current_month = 1
                continue
            elif value.lower() == '이전':
                current_month -= 1
                if current_month < 1:
                    current_year -= 1
                    current_month = 12
                continue

            if not value:
                raise ValueError("공백 입력은 불가합니다.")

            day = int(value)
            # calendar.monthrange()[1]: 해당 연도, 월이 며칠까지 있는지 마지막 날짜를 안내
            last_day = calendar.monthrange(current_year, current_month)[1]

            if not (1 <= day <= last_day):
                raise ValueError("존재하지 않는 날짜입니다.")

            date_str = f"{current_year}-{current_month:02d}-{day:02d}"

            available_times = get_available_times(doctor, date_str, reservations)
            if not available_times:
                raise ValueError("해당 날짜는 예약 가능한 시간이 없습니다(주말, 과거 날짜, 또는 마감).")

            return date_str

        except ValueError as error:
            if "invalid literal" in str(error):
                print("오류: 문자 입력이 감지되었습니다. 숫자로만 입력해주세요.")
            else:
                print(f"오류: {error}")

def select_time(doctor, date_str, reservations):
    # 해당 날짜에 예약 가능한 시간대를 선택
    available_times = get_available_times(doctor, date_str, reservations)

    print(f"\n================== {date_str} 예약 가능 시간 ==================")
    for index, t in enumerate(available_times, 1):
        print(f"                         {index}. {t}")
    print("\n                         0. 이전 메뉴")
    print(f"============================================================")

    while True:
        try:
            value = input("\n예약을 원하는 시간의 번호를 숫자로 입력하세요: ").strip()
            if value == "0":
                return None
            if not value:
                raise ValueError("공백 입력은 불가합니다.")
            choice = int(value)
            if not (1 <= choice <= len(available_times)):
                raise ValueError("잘못된 시간 선택(범위를 벗어난 번호)입니다.")
            return available_times[choice - 1]
        except ValueError as error:
            if "invalid literal" in str(error):
                print("오류: 문자 입력이 감지되었습니다. 숫자로만 입력해주세요.")
            else:
                print(f"오류: {error}")

def save_reservation(patient_id, doctor, date_str, time_str, reservations):
    # 1. 예약번호 생성 및 딕셔너리 구성
    # 예약을 완료하고 예약번호를 생성하여 CSV에 저장
    # .replace("-", ""): 문자열에서 "-" 기호를 찾아서 ""(빈 문자열)로 대체
    date_prefix = date_str.replace("-", "")
    max_sequence_number = 0
    total_fare = 0

    for reservation_record in reservations:
        if reservation_record.get('예약날짜') == date_str:
            # .get('키', '기본값'): 딕셔너리에서 값을 찾을 때 사용. 키가 없으면 에러가 나는 대신 '기본값'을 안전하게 반환
            reservation_id = reservation_record.get('예약번호', '')

            # .startswith(): 문자열이 괄호 안의 글자(date_prefix)로 시작하는지 확인하여 참(True)/거짓(False)을 안내
            if reservation_id.startswith(date_prefix):
                try:
                    # .split("-"): 문자열을 "-" 기준으로 쪼개서 리스트로 생성 (예: ["20260701", "001"])
                    sequence_number = int(reservation_id.split("-")[1])
                    if sequence_number > max_sequence_number:
                        max_sequence_number = sequence_number
                except (IndexError, ValueError):
                    pass

    new_reservation_id = f"{date_prefix}-{max_sequence_number + 1:03d}"

    new_reservation = {
        '예약번호': new_reservation_id,
        '환자번호': patient_id,
        '의료진번호': doctor['의료진번호'],
        '예약날짜': date_str,
        '예약시간': time_str,
        '총금액': total_fare,
        '상태': '예약완료'
    }

    # os.path.isfile(): 해당 경로에 파일이 실제로 존재하는지 확인
    file_path = 'reservations_total_only.csv'
    file_exists = os.path.isfile(file_path)

    # 2. 파일이 이미 존재하면 파일의 첫 줄을 읽어와서 순서를 맞춤
    if file_exists:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            # next()를 사용해 첫 번째 줄(헤더)만 쏙 뽑아옵니다.
            fieldnames = next(reader)
    else:
        # 파일이 없을 때만 기본 순서 사용 (CSV 파일의 실제 순서와 맞춤)
        fieldnames = ['예약번호', '환자번호', '의료진번호', '예약날짜', '예약시간', '총금액', '상태']

    # 3. 데이터 추가 (동기화된 fieldnames 사용)
    with open(file_path, 'a', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(new_reservation)

    print(f"\n========================= [예약 완료] =======================")
    print(f"예약이 아래와 같이 완료되었습니다.")
    print(f"발급된 예약번호: {new_reservation_id}")
    print(f"===========================================================")
    print()

'''============= 내 예약 관리 ============='''
# 내 예약 관리 메뉴 흐름
def my_reservation(current_user):
    while True:
        my_reservation_menu()

        choice = input('메뉴를 선택하세요 > ')

        if choice == '1':
            show_my_reservations(current_user)

        elif choice == '2':
            modify_reservation(current_user) # 수정 전 변수명: update_reservation(current_user)

        elif choice == '3':
            cancel_my_reservation(current_user)

        elif choice == '0':
            break

        else:
            print('올바른 메뉴 번호를 입력하세요.\n')

# 내 예약관리 메뉴 표출
def my_reservation_menu():
    print('======== 내 예약 관리 ========')
    print('1. 예약 조회')
    print('2. 예약 변경')
    print('3. 예약 취소')
    print('0. 이전 메뉴')
    print('============================\n')

# 내 예약 조회
def show_my_reservations(current_user):
    print('\n======== 예약 조회 ========')

    with (open('reservations_total_only.csv', 'r', encoding='utf-8-sig') as file):
        reader = csv.DictReader(file)
        next(reader)


        print(current_user['이름'], '님의 예약을 조회합니다.')

        for reservation in reader:
            if reservation['환자번호'] == current_user['환자번호'] and reservation['상태'] == '예약완료':
                print('예약번호 :', reservation['예약번호'])
                print('환자번호 :', reservation['환자번호'])
                print('의료진번호 :', reservation['의료진번호'])
                print('예약날짜 :', reservation['예약날짜'])
                print('예약시간 :', reservation['예약시간'])
                print('총금액 :', reservation['총금액'])
                print('상태 :', reservation['상태'])
                print()

# 내 예약 변경
def update_reservations_csv(reservations):
    """수정된 전체 예약 목록을 CSV 파일에 덮어씁니다."""
    import os
    import csv

    file_path = 'reservations_total_only.csv'

    if reservations:
        # .keys(): 딕셔너리에서 값(value)을 제외하고 이름표(key)들만 쏙 뽑아옵니다.
        # list(): 뽑아온 키들을 리스트 형태로 변환합니다. (예: ['예약번호', '환자번호', ...])
        fieldnames = list(reservations[0].keys())
    else:
        fieldnames = ['예약번호', '환자번호', '의료진번호', '예약날짜', '예약시간', '총금액', '상태']

    # 'w' 모드(Write): 파일의 기존 내용을 싹 지우고 처음부터 새로 씁니다. (덮어쓰기)
    with open(file_path, 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        # .writerows(): writerow(단수)와 달리, 리스트 안에 있는 여러 줄의 데이터를 한 번에 파일에 씁니다.
        writer.writerows(reservations)


def modify_reservation(current_user):
    """내 예약 정보를 확인하고 날짜와 시간을 수정합니다."""
    reservations = load_reservations()
    doctors = load_doctors()
    patient_id = current_user['환자번호']

    # 1. 내 예약 중 '예약완료' 상태인 것만 걸러내기 (리스트 컴프리헨션)
    active_reservations = [record for record in reservations if record['환자번호'] == patient_id and record['상태'] == '예약완료']

    if not active_reservations:
        print("\n수정할 수 있는 예약 내역이 없습니다.")
        return

    # 의사 정보를 쉽게 찾기 위해 딕셔너리 생성
    doctor_dict = {doctor_info['의료진번호']: doctor_info for doctor_info in doctors}

    print(f"\n======== [{current_user['이름']}]님의 예약 수정 ========")
    for index, record in enumerate(active_reservations, 1):
        doctor_info = doctor_dict.get(record['의료진번호'])
        if doctor_info:
            print(
                f"{index}. [예약번호: {record['예약번호']}] {doctor_info['진료과']} {doctor_info['이름']} 원장 / 기존 예약: {record['예약날짜']} {record['예약시간']}")
    print("0. 이전 메뉴로 돌아가기")

    # 2. 수정할 예약 선택
    while True:
        try:
            input_value = input("\n수정할 예약 번호를 선택하세요: ").strip()
            if input_value == '0':
                return None
            if not input_value:
                raise ValueError("공백 입력은 불가합니다.")

            choice = int(input_value)
            if not (1 <= choice <= len(active_reservations)):
                raise ValueError("범위를 벗어난 번호입니다.")

            # 사용자가 선택한 수정 대상 예약 정보
            target_reservation = active_reservations[choice - 1]
            break
        except ValueError as error:
            if "invalid literal" in str(error):
                print("오류: 숫자로만 입력해주세요.")
            else:
                print(f"오류: {error}")

    # 3. 선택한 예약의 의료진 정보 추출
    doctor = doctor_dict.get(target_reservation['의료진번호'])
    print(f"\n[{doctor['진료과']} {doctor['이름']} 원장] 예약 변경을 시작합니다.")

    # 4. 새로운 날짜와 시간 선택 (기존 블록 재사용)
    while True:
        new_date = select_date(doctor, reservations)
        if new_date is None:
            return

        new_time = select_time(doctor, new_date, reservations)
        if new_time is None:
            print("\n▶ 시간 선택을 취소했습니다. 다시 날짜를 선택해주세요.")
            continue

        break

    # 5. 변경 상세 확인 및 덮어쓰기
    print(f"\n ======== [예약 수정 상세] ========")
    print(f"기존 예약: {target_reservation['예약날짜']} {target_reservation['예약시간']}")
    print(f"변경 예약: {new_date} {new_time}")
    print(f"================================")

    while True:
        confirm = input("\n위 일정으로 예약을 수정하시겠습니까? (Y/N) > ").strip().upper()

        if confirm == 'Y':
            # 전체 reservations 리스트 안에 있는 타겟 예약의 데이터만 새롭게 바꿉니다.
            target_reservation['예약날짜'] = new_date
            target_reservation['예약시간'] = new_time

            # 변경된 전체 리스트를 CSV에 덮어씁니다.
            update_reservations_csv(reservations)

            print("\n예약 수정이 정상적으로 완료되었습니다. 이전 메뉴로 돌아갑니다.")
            return True

        elif confirm == 'N':
            print("\n예약 수정이 취소되었습니다. 이전 메뉴로 돌아갑니다.")
            return False

        else:
            print("올바른 입력이 아닙니다. Y 또는 N을 입력해주세요.")

# 내 예약 취소
def cancel_my_reservation(current_user):
    print('\n======== 예약 취소 ========')

    reservations = []

    # 1. 파일에서 데이터 읽어오기
    with open('reservations_with_fee_breakdown.csv', 'r', encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        for reservation in reader:
            reservations.append(reservation)


        reservation_number = input('취소할 예약번호 : ')
        is_found = False

        for reservation in reservations:
            if reservation['예약번호'] == reservation_number and reservation['환자번호']==current_user['환자번호']:
                reservation['상태'] ='예약취소'
                print(current_user['이름'], '님의 예약을 취소합니다.')
                is_found = True

    if is_found:
        with open('reservations_with_fee_breakdown.csv', 'w', encoding='utf-8-sig', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()  # 맨 첫 줄에 컬럼명(헤더) 작성
            writer.writerows(reservations)  # '취소'로 바뀐 데이터 전체 작성
    else:
        print("일치하는 예약 정보를 찾을 수 없습니다.")

    print()

'''============= 진료 이력 조회 ============='''
# 진료 이력 조회 전체 흐름
def medical_history(current_user):
    while True:
        medical_history_menu()

        choice = input('메뉴를 선택하세요 > ')

        if choice == '1':
            show_medical_history(current_user)

        #elif choice == '2':
        #    show_medical_history_detail(current_user)

        #elif choice == '3':
        #    show_medical_fee(current_user)

        elif choice == '0':
            break

        else:
            print('올바른 메뉴 번호를 입력하세요.\n')

# 진료 이력 조회 메뉴
def medical_history_menu():
    print('\n======== 진료 이력 조회 ========')
    print('1. 전체 진료 이력 조회')
    #print('2. 진료 이력 상세 조회')
    #print('3. 진료비 확인')
    print('0. 이전 메뉴')
    print('===============================\n')

# 전체 진료 이력 조회
def show_medical_history(current_user):
    # 로그인한 사용자의 환자번호 확인
    # 해당 환자의 진료 이력 전체 조회
    # 진료일자 / 진료과 / 의료진 / 진료상태 출력

    # 상세 조회에 사용할 원본 딕셔너리 목록
    medical_history_data = []
    # tabulate 출력에 사용할 목록
    medical_history_table = []

    with open('reservations_with_fee_breakdown.csv', 'r', encoding='utf-8-sig',newline='') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row['환자번호'] == current_user['환자번호'] and row['상태']=='진료완료':
                doctor_info = find_doctor_by_number(row['의료진번호'])
                if doctor_info is not None:
                    doctor_name = doctor_info['이름']
                    department = doctor_info['진료과']
                else:
                    doctor_name = '정보없음'
                    department = '정보없음'

                # 상세 조회에서 사용하기 위해 필요한 정보 추가
                history = {
                    '예약번호': row['예약번호'],
                    '진료과': department,
                    '의료진': doctor_name,
                    '진료날짜': row['예약날짜'],
                    '진료시간': row['예약시간'],
                    '진단명': row['진단명'],
                    '급여': row['급여'],
                    '비급여': row['비급여'],
                    '총금액': row['총금액'],
                    '상태': row['상태']
                }
                medical_history_data.append(history)

                medical_history_table.append([
                    len(medical_history_table)+1,
                    row['예약번호'],
                    department,
                    doctor_name,
                    row['예약날짜'],
                    row['예약시간'],
                    f"{int(row['총금액']):,}원",
                    row['상태']
                ])
        if not medical_history_data:
            print('\n진료 이력이 없습니다.\n')
            return
        while True:

            table = tabulate(
                medical_history_table,
                headers=[
                    '번호',
                    '진료과',
                    '의료진',
                    '진료날짜',
                    '진료시간',
                    '총금액',
                    '상태'
                ],
                tablefmt='grid',
                stralign='center',
                numalign='center',
                disable_numparse=True
            )
            first_line = table.splitlines()[0]
            table_width = wcswidth(first_line)
            title = '🩺 전체 진료 이력'

            print('=' * table_width)
            print(center_by_width(title, table_width))
            print('=' * table_width)
            print()
            print(table)
            print('=' * table_width)

            history_menu = input('조회할 번호를 입력하세요 (0. 이전) : ')

            if history_menu == '0':
                return

            # 빈 값 또는 숫자가 아닌 값 검사
            if not history_menu.isdigit():
                print('목록에 있는 숫자를 입력하세요.\n')
                continue

            history_index = int(history_menu) - 1

            if not 0 <= history_index < len(medical_history_data):
                print('목록에 있는 번호를 입력하세요. \n')
                continue

            selected_history = medical_history_data[history_index]
            insured_fee = int(selected_history['급여'])
            uninsured_fee = int(selected_history['비급여'])
            total_fee = int(selected_history['총금액'])

            print('\n====== 진료 이력 상세 ======')
            print(f'예약번호 : {selected_history['예약번호']}')
            print(f'진료일자 : {selected_history['진료날짜']}')
            print(f'진료시간 : {selected_history['진료시간']}')
            print(f'진료과 : {selected_history['진료과']}')
            print(f'의료진 : {selected_history['의료진']}')
            print(f'진단명 : {selected_history['진단명']}')
            print(f'진단상태 : {selected_history['상태']}')
            print('-' * 34)
            print(f'급여 : {insured_fee:,}원')
            print(f'비급여 : {uninsured_fee:,}원')
            print('-' * 34)
            print(f'총금액 : {total_fee:,}원')
            print('================================\n')

# 의료진 찾기
def find_doctor_by_number(doctor_number):
    with open('doctors.csv', 'r', encoding='utf-8-sig',newline='') as file:
        reader = csv.DictReader(file)

        for doctor in reader:
            if doctor['의료진번호'] == doctor_number:
                return doctor
    return None

# 진료 이력 상세 조회
def show_medical_history_detail(current_user):
    print('\n======== 진료 이력 상세 조회 ========')

    # 진료 이력 목록 출력
    # 조회할 진료 이력 선택
    # 진료일자 / 진료과 / 의료진 / 진단명 / 처방내역 출력

# 진료비 확인
def show_medical_fee(current_user):
    print('\n======== 진료비 확인 ========')

    # 진료 이력 목록 출력
    # 확인할 진료 이력 선택
    # 급여 금액 확인
    # 비급여 금액 확인
    # 총 진료비 확인
    # 수납 상태 확인

'''============= 관리자 메뉴 ============='''
# 관리자 메뉴 전체 흐름
def admin_manage(current_user):
    while True:
        admin_menu(current_user)

        choice = input('메뉴를 선택하세요 > ')

        if choice == '1':
            member_manage(current_user)

        elif choice == '2':
            reservation_manage(current_user)

        elif choice == '3':
            department_doctor_manage(current_user)

        elif choice == '4':
            payment_sales_manage(current_user)

        elif choice == '5':
            current_user = logout(current_user)
            return current_user

        else:
            print('올바른 메뉴 번호를 입력하세요.\n')

# 관리자 메뉴 출력
def admin_menu(current_user):
    print('\n======== 관리자 메뉴 ========')
    print(f"현재 관리자 : {current_user['이름']} / {current_user['아이디']}")
    print('1. 회원 조회')
    print('2. 예약 조회')
    print('3. 진료과/의료진 조회')
    print('4. 진료비/매출 조회')
    print('5. 로그아웃')
    print('============================\n')

'''============= 회원 조회 ============='''
# 회원 관리 전체 흐름
def member_manage(current_user):
    while True:
        member_manage_menu()

        choice = input('메뉴를 선택하세요 > ')

        if choice == '1':
            show_all_members()

        elif choice == '2':
            search_member_by_patient_number()

        elif choice == '3':
            search_member_by_name()

        elif choice == '4':
            update_member()

        elif choice == '5':
            delete_member()

        elif choice == '0':
            break

        else:
            print('올바른 메뉴 번호를 입력하세요.\n')

# 회원 관리 메뉴 출력
def member_manage_menu():
    print('\n======== 회원 관리 ========')
    print('1. 전체 회원 조회')
    print('2. 환자번호로 조회')
    print('3. 이름으로 조회')
    print('4. 회원 정보 수정')
    print('5. 회원 삭제')
    print('0. 이전 메뉴')
    print('==========================\n')

def show_all_members():
    print('\n======== 전체 회원 조회 ========')



    # user.csv 전체 회원 조회


def search_member_by_patient_number():
    print('\n======== 환자번호 조회 ========')

    # 환자번호 입력
    # 일치하는 회원 조회


def search_member_by_name():
    print('\n======== 이름 조회 ========')

    # 환자 이름 입력
    # 일치하는 회원 조회


def update_member():
    print('\n======== 회원 정보 수정 ========')

    # 수정할 회원 검색
    # 수정할 정보 선택
    # 회원 정보 수정
    # user.csv 저장


def delete_member():
    print('\n======== 회원 삭제 ========')

    # 삭제할 회원 검색
    # 삭제 여부 확인
    # 회원상태 변경 또는 회원 삭제
    # user.csv 저장

'''============= 예약 조회 ============='''
# 예약 관리 전체 흐름
def reservation_manage(current_user):
    while True:
        reservation_manage_menu()

        choice = input('메뉴를 선택하세요 > ')

        if choice == '1':
            show_all_reservations()

        elif choice == '2':
            search_reservation_by_patient()

        elif choice == '3':
            update_reservation()

        elif choice == '4':
            cancel_reservation()

        elif choice == '0':
            break

        else:
            print('올바른 메뉴 번호를 입력하세요.\n')

# 예약 관리 메뉴 출력
def reservation_manage_menu():
    print('\n======== 예약 관리 ========')
    print('1. 전체 예약 조회')
    print('2. 환자별 예약 조회')
    print('3. 예약 수정')
    print('4. 예약 취소')
    print('0. 이전 메뉴')
    print('==========================\n')


# 전체 조회
def show_all_reservations():
    import csv
    from tabulate import tabulate
    # CSV 파일 읽기
    try:
        with open("reservations_with_fee_breakdown.csv", "r", encoding="utf-8-sig") as file:
            reader = list(csv.DictReader(file))
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        return

    # 1. 헤더 정의
    headers = ["예약번호", "환자번호", "의료진번호", "예약날짜", "예약시간", "급여", "비급여", "총금액", "상태"]

    # 2. 표에 들어갈 데이터 행(Row) 구축
    table_data = []
    for row in reader:
        # 금액 데이터 천 단위 콤마(,) 포맷팅
        salary_paid = f"{int(row['급여']):,}"
        non_salary_paid = f"{int(row['비급여']):,}"
        total_paid = f"{int(row['총금액']):,}"

        table_data.append([
            row["예약번호"],
            row["환자번호"],
            row["의료진번호"],
            row["예약날짜"],
            row["예약시간"],
            salary_paid,
            non_salary_paid,
            total_paid,
            row["상태"]
        ])

    # 3. 각 열의 정렬 방식 지정 (가운데 정렬 5개, 오른쪽 정렬 3개, 가운데 정렬 1개)
    col_align = ["center", "center", "center", "center", "center", "right", "right", "right", "center"]

    # 4. 표 출력 (딱 한 번만 출력되도록 정리!)
    print("=" * 112)
    print("전체 예약 조회".center(112))
    print("=" * 112)

    # grid 옵션 적용하여 출력
    print(tabulate(
        table_data,
        headers=headers,
        tablefmt="grid",  # 원하셨던 2번 스타일!
        colalign=col_align
    ))


# 환자별 조회
def search_reservation_by_patient():
    import csv
    from tabulate import tabulate

    # 조회할 환자번호 입력
    patient_no = input("\n환자번호를 입력하세요 : ").strip()

    # CSV 파일 읽기
    try:
        with open("reservations_with_fee_breakdown.csv", "r", encoding="utf-8-sig") as file:
            reader = list(csv.reader(file))
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        return

    # 1. 헤더 정의 (reader[0] 대신 보기 좋은 한글 헤더 지정)
    headers = ["예약번호", "환자번호", "의료진번호", "예약날짜", "예약시간", "급여", "비급여", "총금액", "상태"]

    # 2. 일치하는 데이터 필터링 및 구축
    table_data = []

    # 첫 번째 행(헤더)을 제외하고 데이터 순회 (index 1번부터)
    for row in reader[1:]:
        # row[1]은 '환자번호' 열입니다.
        if row[1].strip() == patient_no:
            # 금액 데이터 천 단위 콤마(,) 포맷팅
            salary_paid = f"{int(row[5]):,}"
            non_salary_paid = f"{int(row[6]):,}"
            total_paid = f"{int(row[7]):,}"

            table_data.append([
                row[0],  # 예약번호
                row[1],  # 환자번호
                row[2],  # 의료진번호
                row[3],  # 예약날짜
                row[4],  # 예약시간
                salary_paid,
                non_salary_paid,
                total_paid,
                row[8]  # 상태
            ])

    # 3. 정렬 방식 설정
    col_align = ["center", "center", "center", "center", "center", "right", "right", "right", "center"]

    # 4. 표 출력
    print()
    print("=" * 112)
    print("환자별 예약 조회".center(112))
    print("=" * 112)

    # 일치하는 데이터가 하나도 없을 때
    if not table_data:
        print("조회된 예약이 없습니다.")
        print("=" * 112)
    else:
        # 데이터가 있으면 2번 grid 스타일로 출력
        print(tabulate(
            table_data,
            headers=headers,
            tablefmt="grid",
            colalign=col_align
        ))


# 예약 수정
def update_reservation():
    import csv

    print("\n============================= 예약 수정 =============================")

    # 수정할 예약번호 입력
    reservation_no = input("수정할 예약번호를 입력하세요 : ")

    # CSV 파일 읽기
    with open("reservations_with_fee_breakdown.csv", "r", encoding="utf-8-sig") as file:
        reader = list(csv.reader(file))

    # 1. 수정할 예약 데이터 행(Row) 찾기
    target_row = None
    for row in reader[1:]:
        if row[0].strip() == reservation_no.strip():  # 공백 제거 후 비교
            target_row = row
            break

    # 예약번호를 찾지 못한 경우 함수 종료
    if target_row is None:
        print("\n예약번호가 존재하지 않습니다.")
        return

    # 현재 예약 정보 출력
    print("\n================ 현재 예약 정보 ================")
    print(f"예약번호   : {target_row[0]}")
    print(f"환자번호   : {target_row[1]}")
    print(f"의료진번호 : {target_row[2]}")
    print(f"예약날짜   : {target_row[3]}")
    print(f"예약시간   : {target_row[4]}")
    print("==============================================")

    # 새로운 예약 날짜와 시간 입력
    new_date = input("새 예약날짜를 입력하세요 (YYYY-MM-DD) : ").strip()
    new_time = input("새 예약시간을 입력하세요 (HH:MM) : ").strip()

    # 수정 여부 확인
    check = input("\n정말 수정하시겠습니까? (Y/N) : ").upper().strip()

    if check == "Y":
        # 하이픈(-) 제거하여 YYYYMMDD 형태 만들기 (예: 2026-07-02 -> 20260702)
        date_prefix = new_date.replace("-", "")

        max_sequence = 0
        # 전체 리스트를 돌며 새 날짜로 시작하는 예약번호 중 가장 큰 순번 찾기
        for row in reader[1:]:
            if row[0] and "-" in row[0]:
                parts = row[0].strip().split("-")
                if parts[0] == date_prefix:
                    try:
                        seq = int(parts[1])
                        if seq > max_sequence:
                            max_sequence = seq
                    except ValueError:
                        pass

        # 무조건 새 예약번호 생성 (최대 순번 + 1)
        new_sequence = max_sequence + 1
        new_reservation_no = f"{date_prefix}-{new_sequence:03d}"

        print(f"\n[안내] 예약번호가 '{target_row[0]}'에서 '{new_reservation_no}'로 변경됩니다.")

        # 데이터 최종 적용 (예약번호, 날짜, 시간 모두 무조건 갱신)
        target_row[0] = new_reservation_no
        target_row[3] = new_date
        target_row[4] = new_time

        # 3. 수정된 전체 데이터를 CSV 파일에 덮어쓰기
        with open("reservations_with_fee_breakdown.csv", "w", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(reader)

        print("\n예약이 수정되었습니다.")

    else:
        print("\n예약 수정을 취소했습니다.")

# 예약 취소
def cancel_reservation():
    import csv
    print("\n============================= 예약 취소 =============================")

    reservation_cancel = input('취소할 예약번호를 입력하세요 : ').strip()

    # 파일읽기
    try:
        with open("reservations_with_fee_breakdown.csv", "r", encoding="utf-8-sig") as file:
            reader = list(csv.reader(file))
    except FileNotFoundError:
        print("\n[오류] reservations_with_fee_breakdown.csv 파일이 존재하지 않습니다.")
        return

    # 1. 취소할 예약 데이터의 '행 인덱스(위치)' 찾기
    target_index = -1
    for i in range(1, len(reader)):
        if reader[i][0] == reservation_cancel:
            target_index = i
            break

    # 예약번호를 찾지 못한 경우 함수 종료
    if target_index == -1:
        print("\n예약번호가 존재하지 않습니다.")
        return

    # 2. 현재 상태 검증 및 정보 출력 (9번째 컬럼 = 인덱스 8)
    current_status = reader[target_index][8].strip()

    if current_status == "예약취소":
        print("\n[안내] 이미 취소된 예약입니다.")
        return
    elif current_status == "진료완료":
        print("\n[안내] 이미 진료가 완료된 예약은 취소할 수 없습니다.")
        return

    print("\n================ 취소할 예약 정보 ================")
    print(f"예약번호   : {reader[target_index][0]}")
    print(f"환자번호   : {reader[target_index][1]}")
    print(f"의료진번호 : {reader[target_index][2]}")
    print(f"예약날짜   : {reader[target_index][3]}")
    print(f"예약시간   : {reader[target_index][4]}")
    print(f"현재상태   : {current_status}")
    print("=================================================")

    # 3. 최종 취소 확인 여부 질문
    check = input("\n정말 예약을 취소하시겠습니까? (Y/N) : ").upper().strip()

    if check == "Y":
        # 원본 데이터의 '상태' 컬럼을 '예약취소'로 변경
        reader[target_index][8] = "예약취소"

        # 변경된 내용을 csv 파일에 덮어쓰기
        with open("reservations_with_fee_breakdown.csv", "w", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(reader)

        print("\n예약이 성공적으로 취소되었습니다.")
    else:
        print("\n예약 취소를 취소했습니다.")


'''============= 진료과/의료진 조회 ============='''
# 진료과/의료진 관리 전체 흐름
def department_doctor_manage(current_user):
    while True:
        department_doctor_manage_menu()

        choice = input('메뉴를 선택하세요 > ')

        if choice == '1':
            show_all_doctors()

        elif choice == '2':
            show_doctors_by_department_admin()

        elif choice == '3':
            update_doctor()

        elif choice == '4':
            delete_doctor()

        elif choice == '0':
            break

        else:
            print('올바른 메뉴 번호를 입력하세요.\n')

# 진료과/의료진 관리 메뉴 출력
def department_doctor_manage_menu():
    print('\n======== 진료과/의료진 관리 ========')
    print('1. 전체 진료과/의료진 조회')
    print('2. 진료과별 의료진 조회')
    print('3. 의료진 정보 수정')
    print('4. 의료진 삭제')
    print('0. 이전 메뉴')
    print('==================================\n')


# 전체 진료과/의료진 조회
def show_all_doctors():
    import csv
    from tabulate import tabulate

    # CSV 파일 읽기
    try:
        with open("doctors.csv", "r", encoding="utf-8-sig") as file:
            reader = list(csv.reader(file))
    except FileNotFoundError:
        print("\n[오류] doctors.csv 파일이 존재하지 않습니다.")
        return

    # 1. 헤더 정의
    headers = [
        "의료진번호", "이름", "진료과", "진료실번호",
        "진료과전화번호", "진료요일", "진료시작시간", "진료종료시간", "근무상태"
    ]

    # 2. 데이터 행(Row) 구축 (공백 제거 적용)
    table_data = []
    for row in reader[1:]:
        table_data.append([item.strip() for item in row])

    # 3. 정렬 방식 설정 (모든 열 가운데 정렬)
    # 총 9개 열의 정렬 방식을 지정합니다.
    col_align = ["center"] * 9

    # 4. grid 표 생성 (너비 계산을 위해 먼저 표를 텍스트로 생성)
    table_string = tabulate(
        table_data,
        headers=headers,
        tablefmt="grid",  # 2번 스타일 적용!
        colalign=col_align
    )

    # 5. 표의 실제 가로 길이에 맞추어 타이틀 출력
    # table_string의 첫 번째 줄(가로 테두리 선)의 길이를 기준으로 계산합니다.
    actual_width = len(table_string.split('\n')[0])

    print("\n" + "=" * actual_width)
    print("전체 진료과/의료진 조회".center(actual_width))
    print("=" * actual_width)
    print(table_string)


# 진료과별 의료진 조회
def show_doctors_by_department_admin():
    import csv
    from tabulate import tabulate

    # 조회할 진료과 입력
    dept_name = input("\n조회할 진료과를 입력하세요 : ").strip()

    # CSV 파일 읽기
    try:
        with open("doctors.csv", "r", encoding="utf-8-sig") as file:
            reader = list(csv.reader(file))
    except FileNotFoundError:
        print("\n[오류] doctors.cvs 파일을 찾을 수 없습니다.")
        return

    # 1. 헤더 정의
    headers = ["의료진번호", "이름", "진료과", "진료실번호",
               "진료과전화번호", "진료요일", "진료시작시간", "진료종료시간", "근무상태"
               ]

    # 2. 입력받은 진료과와 일치하는 데이터 필터링
    table_data = []

    for row in reader[1:]:
        # row[2]는 '진료과' 열입니다. 공백을 제거한 후 입력값과 비교한다
        if row[2].strip() == dept_name:
            table_data.append([item.strip() for item in row])

    # 3. 정렬 방식 설정 (모든 열 가운데 정렬)
    col_align = ["center"] * 9

    # 4. 조회 결과 처리 및 출력
    if not table_data:
        # 일치하는 진료과가 없을 때
        print("\n" + "=" * 50)
        print(f"[{dept_name}] 의료진 정보가 없습니다.".center(50))
        print("=" * 50)
    else:
        # 표 생성 및 테두리 길이에 맞춰 타이틀 출력
        table_string = tabulate(
            table_data,
            headers=headers,
            tablefmt="grid",
            colalign=col_align
        )

        actual_width = len(table_string.split('\n')[0])

        print("\n" + "=" * actual_width)
        print(f"[{dept_name}] 의료진 조회".center(actual_width))
        print("=" * actual_width)
        print(table_string)


# 의료진 정보 수정
def update_doctor():
    import csv
    from tabulate import tabulate

    # 1. 수정할 의료진 번호 입력받기
    doctor_id = input("\n수정할 의료진번호를 입력하세요 (예: D01001) : ").strip()

    # CSV 파일 전체 읽기
    try:
        with open("doctors.csv", "r", encoding="utf-8-sig") as file:
            reader = list(csv.reader(file))
    except FileNotFoundError:
        print("\n[오류] doctors.csv 파일이 존재하지 않습니다.")
        return

    # 헤더와 데이터 분리
    headers = [h.strip() for h in reader[0]]
    rows = reader[1:]

    # 수정할 의료진 찾기
    target_index = -1
    for i, row in enumerate(rows):
        # 행이 비어있거나 데이터가 제대로 안 채워진 경우 건너뜀
        if not row:
            continue
        if row[0].strip() == doctor_id:
            target_index = i
            break

    # 해당 의료진이 없는 경우
    if target_index == -1:
        print(f"\n[오류] 의료진번호 '{doctor_id}'에 해당하는 정보가 없습니다.")
        return

    # 기존 데이터 복사 (글자 쪼개짐 현상 완벽 방지)
    target_row = rows[target_index]

    # 만약 리스트가 아닌 단일 문자열로 읽혔다면 처리
    if isinstance(target_row, str):
        original_row = [item.strip() for item in target_row.split(',')]
    else:
        original_row = [str(item).strip() for item in target_row]

    updated_row = list(original_row)  # 실제 '값'이 수정될 리스트

    # 현재 정보 먼저 표로 보여주기
    col_align = ["center"] * len(headers)
    print("\n[현재 의료진 정보]")
    print(tabulate([original_row], headers=headers, tablefmt="grid", colalign=col_align))

    # 2. 수정할 데이터 항목 선택받기
    print("\n[수정 가능 항목]")
    print("1. 이름,  2. 진료과,  3. 진료실번호,  4. 진료과전화번호,  5. 진료요일,  6. 진료시작시간,  7. 진료종료시간,  8. 근무상태")

    try:
        choice = int(input("\n수정할 항목의 번호를 입력하세요 (1~8) : "))
        if choice < 1 or choice > 8:
            print("[오류] 1부터 8 사이의 번호를 입력해야 합니다.")
            return
    except ValueError:
        print("[오류] 숫자만 입력 가능합니다.")
        return

    # 선택한 번호에 해당하는 열(Column) 이름과 현재 '값' 가져오기
    field_name = headers[choice]
    current_value = original_row[choice]

    # 3. 새로운 데이터 '값' 입력받기
    new_value = input(f"\n새로운 [{field_name}] 값 입력 (기존: {current_value}) -> ").strip()

    if not new_value:
        print("[취소] 입력된 값이 없어 수정을 취소합니다.")
        return

    # 기존 데이터 행의 해당 열 위치에 새로운 '값' 대입
    updated_row[choice] = new_value

    # 4. 최종 저장 여부 확인
    print("\n" + "=" * 50)
    print(" 변경 예정 정보 확인 ".center(50))
    print("=" * 50)
    print(f" 수정 항목 : {field_name}")
    print(f" 기존 데이터: {current_value}  --->  변경 데이터: {new_value}")
    print("=" * 50)

    confirm = input("이대로 정보를 수정하여 저장하시겠습니까? (Y/N) : ").strip().upper()

    if confirm == "Y":
        # 원본 리스트 데이터 변경
        rows[target_index] = updated_row

        # CSV 파일 덮어쓰기
        try:
            with open("doctors.csv", "w", encoding="utf-8-sig", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(rows)
            print("\n[성공] 수정 사항이 파일에 정상적으로 반영되었습니다.")

            # 최종 수정 완료된 표 출력
            print("\n[최종 수정 완료 정보]")
            print(tabulate([updated_row], headers=headers, tablefmt="grid", colalign=col_align))
        except Exception as e:
            print(f"\n[오류] 파일 저장 중 문제가 발생했습니다: {e}")
    else:
        print("\n[취소] 수정이 취소되었습니다. 파일은 변경되지 않았습니다.")


# 의료진 삭제
def delete_doctor():
    import csv
    from tabulate import tabulate

    # 1. 삭제할 의료진 번호 입력받기
    doctor_id = input("\n삭제할 의료진번호를 입력하세요 (예: D01001) : ").strip()

    # CSV 파일 전체 읽기
    try:
        with open("doctors.csv", "r", encoding="utf-8-sig") as file:
            reader = list(csv.reader(file))
    except FileNotFoundError:
        print("\n[오류] doctors.csv 파일이 존재하지 않습니다.")
        return

    if not reader:
        print("\n[오류] 파일에 데이터가 없습니다.")
        return

    # [원천 차단] 읽어온 전체 데이터를 시작하자마자 깨끗한 리스트 형태로 파싱합니다.
    cleaned_data = []
    for row in reader:
        if not row:
            continue
        # 한 줄이 통째로 문자열로 읽혔을 때 쉼표로 쪼갭니다.
        if isinstance(row, str):
            cleaned_data.append([item.strip() for item in row.split(',')])
        elif len(row) == 1 and ',' in row[0]:
            cleaned_data.append([item.strip() for item in row[0].split(',')])
        else:
            cleaned_data.append([str(item).strip() for item in row])

    # 파싱된 데이터에서 헤더와 데이터 행 분리
    headers = cleaned_data[0]
    rows = cleaned_data[1:]

    # 삭제할 의료진 찾기
    target_index = -1
    for i, row in enumerate(rows):
        if row[0] == doctor_id:
            target_index = i
            break

    # 해당 의료진이 없는 경우
    if target_index == -1:
        print(f"\n[오류] 의료진번호 '{doctor_id}'에 해당하는 정보가 없습니다.")
        return

    # 삭제 대상 데이터 확보
    target_row = rows[target_index]

    # 2. 삭제 대상 정보 표로 보여주기
    col_align = ["center"] * len(headers)
    print("\n[삭제 예정 의료진 정보]")
    print(tabulate([target_row], headers=headers, tablefmt="grid", colalign=col_align))

    # 3. 삭제 최종 확인
    print("\n" + "!" * 100)
    print("경고: 삭제된 데이터는 복구할 수 없습니다! ".center(90))
    print("!" * 100)
    confirm = input(f"정말 [{doctor_id}] 의료진 정보를 완전히 삭제하시겠습니까? (Y/N) : ").strip().upper()

    if confirm == "Y":
        # 데이터 리스트에서 제거
        rows.pop(target_index)

        # 4. CSV 파일 덮어쓰기 (깨끗하게 파싱된 리스트 형태를 그대로 저장하므로 파일이 망가지지 않음)
        try:
            with open("doctors.csv", "w", encoding="utf-8-sig", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(headers)  # 깨끗한 헤더 저장
                writer.writerows(rows)  # 깨끗한 데이터 행들 저장
            print(f"\n[성공] 의료진 [{doctor_id}] 정보가 정상적으로 삭제되었습니다.")
        except Exception as e:
            print(f"\n[오류] 파일 저장 중 문제가 발생했습니다: {e}")
    else:
        print("\n[취소] 삭제가 취소되었습니다. 파일은 변경되지 않았습니다.")


'''============= 진료비/매출 조회 ============='''
# 진료비/매출 조회 전체 흐름
def payment_sales_manage(current_user):
    while True:
        payment_sales_manage_menu()

        choice = input('메뉴를 선택하세요 > ')

        if choice == '1':
            show_all_payments()

        elif choice == '2':
            search_payment_by_patient()

        elif choice == '3':
            show_department_sales()

        elif choice == '4':
            show_payment_by_type()

        elif choice == '5':
            show_monthly_sales()

        elif choice == '0':
            break

        else:
            print('올바른 메뉴 번호를 입력하세요.\n')

# 진료비/매출 관리 메뉴 출력
def payment_sales_manage_menu():
    print('\n======== 진료비/매출 조회 ========')
    print('1. 전체 진료비 조회')
    print('2. 환자별 진료비 조회')
    print('3. 진료과별 진료비 조회')
    print('4. 급여/비급여별 진료비 조회')
    print('5. 월별 매출 조회')
    print('0. 이전 메뉴')
    print('================================\n')

# 전체 진료비 조회
def show_all_payments():
    # 전체 진료비 내역을 관리자에게 출력
    payment_list = []

    insured_total = 0   # 급여 전체 합계
    uninsured_total = 0 # 비급여 전체 합계
    total_sales = 0     # 총 매출
    completed_count = 0 # 진료완료 건수

    # 환자번호와 환자 이름 연결
    patient_dict = {}

    with open('user_500_added.csv','r', encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for user in reader:
            patient_dict[user['환자번호']] = user['이름']

    # 의료진번호와 의료진 정보 연결
    doctor_dict = {}
    with open('doctors.csv','r', encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for doctor in reader:
            doctor_dict[doctor['의료진번호']] = {
                '진료과': doctor['진료과'],
                '이름': doctor['이름']
            }
    # 진료완료 내역 조회
    with open('reservations_500_added.csv','r', encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        for reservation in reader:
            # 매출은 실제 진료를 마친 데이터만 포함
            if reservation['상태'] != '진료완료':
                continue

            patient_number = reservation['환자번호']
            doctor_number = reservation['의료진번호']

            patient_name = patient_dict.get(
                patient_number,
                '정보 없음'
            )

            doctor_info = doctor_dict.get(
                doctor_number,
                {
                    '진료과': '정보 없음',
                    '이름' : '정보 없음'
                }
            )

            doctor_name = doctor_info['이름']
            department = doctor_info['진료과']

            #csv파일에서 읽은 금액은 문자열이라서 int로 변환
            insured_fee = int(reservation['급여'])
            uninsured_fee = int(reservation['비급여'])
            total_fee = int(reservation['총금액'])

            #합계 계산
            insured_total += insured_fee
            uninsured_total += uninsured_fee
            total_sales += total_fee
            completed_count += 1

            payment_list.append({
                '번호': completed_count,
                '진료일자': reservation['예약날짜'],
                '환자번호': patient_number,
                '환자명': patient_name,
                '진료과' : department,
                '의료진' : doctor_name,
                '진단명' : reservation['진단명'],
                '급여' : insured_fee,
                '비급여' : uninsured_fee,
                '총금액' : total_fee
            })
    # 조회 결과가 없는 경우
    if not payment_list:
        console.print(
            Panel(
                '[bold red]조회할 진료비 내역이 없습니다.[/bold red]',
                title='💰 전체 진료비 조회',
                border_style='red'
            )
        )
        return

    # 최신 진료일 순으로 정렬
    payment_list.sort(
        key=lambda payment: (
            payment['진료일자'],
            payment['번호']
        ),
        reverse=True
    )

    # 매출 요약 카드
    summary_table = Table.grid(
        padding=(0, 2)
    )

    summary_table.add_column(
        justify='left',
        style='bold'
    )

    summary_table.add_column(
        justify='right'
    )

    summary_table.add_row(
        '🏥 진료 건수',
        f'[bold cyan]{completed_count}건[/bold cyan]'
    )

    summary_table.add_row(
        '🩺 급여 매출',
        f'[green]{insured_total:,}원[/green]'
    )

    summary_table.add_row(
        '💊 비급여 매출',
        f'[yellow]{uninsured_total:,}원[/yellow]'
    )

    summary_table.add_row(
        '💰 전체 매출',
        f'[bold magenta]{total_sales:,}원[/bold magenta]'
    )

    # 페이지 설정
    page_size = 10
    current_page = 1

    total_count = len(payment_list)

    total_pages = (
                          total_count + page_size - 1
                  ) // page_size

    while True:
        # 현재 페이지에서 보여줄 데이터 범위
        start_index = (current_page - 1) * page_size
        end_index = start_index + page_size

        page_data = payment_list[start_index:end_index]

        # 현재 페이지 표 생성
        payment_table = Table(
            title=(
                f'🧾 전체 진료비 내역 '
                f'({current_page}/{total_pages} 페이지)'
            ),
            box=box.ROUNDED,
            header_style='bold white',
            border_style='bright_white',
            show_lines=True,
            padding=(0, 1),
            expand=False
        )

        payment_table.add_column(
            '번호',
            justify='center',
            style='cyan',
            no_wrap=True,
            width=4
        )

        payment_table.add_column(
            '진료일',
            justify='center',
            no_wrap=True,
            width=12
        )

        payment_table.add_column(
            '환자 정보',
            justify='center',
            width=14
        )

        payment_table.add_column(
            '진료 정보',
            justify='center',
            width=15
        )

        payment_table.add_column(
            '진단명',
            justify='center',
            width=16
        )

        payment_table.add_column(
            '급여',
            justify='center',
            style='green',
            no_wrap=True,
            width=11
        )

        payment_table.add_column(
            '비급여',
            justify='center',
            style='yellow',
            no_wrap=True,
            width=11
        )

        payment_table.add_column(
            '총금액',
            justify='center',
            style='bold magenta',
            no_wrap=True,
            width=12
        )

        # 현재 페이지 데이터만 표에 추가
        for index, payment in enumerate(
                page_data,
                start=start_index + 1
        ):
            patient_text = (
                f"[bold]{payment['환자명']}[/bold]\n"
                f"[dim]{payment['환자번호']}[/dim]"
            )

            medical_text = (
                f"[bold]{payment['진료과']}[/bold]\n"
                f"[dim]{payment['의료진']}[/dim]"
            )

            payment_table.add_row(
                str(index),
                payment['진료일자'],
                patient_text,
                medical_text,
                payment['진단명'],
                f"{payment['급여']:,}원",
                f"{payment['비급여']:,}원",
                f"{payment['총금액']:,}원"
            )

        console.print()

        console.print(
            Panel(
                summary_table,
                title='[bold cyan]💰 전체 매출 요약[/bold cyan]',
                border_style='cyan',
                expand=False
            )
        )

        console.print(payment_table)

        first_number = start_index + 1
        last_number = min(end_index, total_count)

        console.print(
            f'\n[cyan]전체 {total_count}건 중 '
            f'{first_number}~{last_number}건을 표시합니다.[/cyan]'
        )

        console.print(
            '[bold]N[/bold]. 다음 페이지  '
            '[bold]P[/bold]. 이전 페이지  '
            '[bold]F[/bold]. 첫 페이지  '
            '[bold]L[/bold]. 마지막 페이지  '
            '[bold]0[/bold]. 이전 메뉴'
        )

        page_choice = input(
            '메뉴를 선택하세요 > '
        ).strip().upper()

        if page_choice == '0':
            return

        elif page_choice == 'N':
            if current_page < total_pages:
                current_page += 1
            else:
                console.print(
                    '[yellow]마지막 페이지입니다.[/yellow]'
                )

        elif page_choice == 'P':
            if current_page > 1:
                current_page -= 1
            else:
                console.print(
                    '[yellow]첫 페이지입니다.[/yellow]'
                )

        elif page_choice == 'F':
            current_page = 1

        elif page_choice == 'L':
            current_page = total_pages

        else:
            console.print(
                '[bold red]'
                'N, P, F, L, 0 중 하나를 입력하세요.'
                '[/bold red]'
            )

# 환자별 진료비 조회
def search_payment_by_patient():
    while True:
        console.print(
            '\n[bold cyan]======== 환자별 진료비 조회 ========[/bold cyan]'
        )

        search_value = input(
            '환자 이름 또는 환자번호 일부를 입력하세요 '
            '(0. 이전) : '
        ).strip()

        if search_value == '0':
            return

        if search_value == '':
            console.print(
                '[bold red]검색어를 입력하세요.[/bold red]\n'
            )
            continue

        # 검색된 환자 목록
        matched_patients = []

        with open(
            'user_500_added.csv',
            'r',
            encoding='utf-8-sig',
            newline=''
        ) as file:
            reader = csv.DictReader(file)

            for user in reader:
                # 일반 사용자만 검색
                if user['권한'] != 'user':
                    continue

                # 탈퇴 회원 제외
                if user['회원상태'] != '정상':
                    continue

                patient_number = user['환자번호']
                patient_name = user['이름']

                # 이름 또는 환자번호 부분 검색
                if (
                    search_value in patient_name
                    or search_value.upper() in patient_number.upper()
                ):
                    matched_patients.append(user)

        if not matched_patients:
            console.print(
                '[bold red]일치하는 환자를 찾을 수 없습니다.[/bold red]\n'
            )
            continue

        # 검색 결과가 너무 많으면 다시 검색
        if len(matched_patients) > 20:
            console.print(
                f'[yellow]검색 결과가 {len(matched_patients)}명입니다.\n'
                '이름이나 환자번호를 더 자세히 입력하세요.[/yellow]\n'
            )
            continue

        # 환자 검색 결과 표
        patient_table = Table(
            title=f'👤 환자 검색 결과 ({len(matched_patients)}명)',
            box=box.ROUNDED,
            header_style='bold white',
            border_style='bright_white',
            show_lines=True,
            expand=False
        )

        patient_table.add_column(
            '번호',
            justify='center',
            style='cyan',
            no_wrap=True
        )

        patient_table.add_column(
            '환자번호',
            justify='center',
            no_wrap=True
        )

        patient_table.add_column(
            '이름',
            justify='center',
            no_wrap=True
        )

        patient_table.add_column(
            '생년월일',
            justify='center',
            no_wrap=True
        )

        patient_table.add_column(
            '성별',
            justify='center',
            no_wrap=True
        )

        patient_table.add_column(
            '연락처',
            justify='center',
            no_wrap=True
        )

        for index, patient in enumerate(
            matched_patients,
            start=1
        ):
            phone_number = patient['연락처']
            phone_parts = phone_number.split('-')

            if len(phone_parts) == 3:
                masked_phone = (
                    f'{phone_parts[0]}-****-{phone_parts[2]}'
                )
            else:
                masked_phone = phone_number

            patient_table.add_row(
                str(index),
                patient['환자번호'],
                patient['이름'],
                patient['생년월일'],
                patient['성별'],
                masked_phone
            )

        console.print(patient_table)

        while True:
            patient_choice = input(
                '조회할 환자 번호를 선택하세요 '
                '(0. 다시 검색) : '
            ).strip()

            if patient_choice == '0':
                break

            if not patient_choice.isdigit():
                console.print(
                    '[bold red]목록에 있는 숫자를 입력하세요.[/bold red]'
                )
                continue

            patient_index = int(patient_choice) - 1

            if not 0 <= patient_index < len(matched_patients):
                console.print(
                    '[bold red]목록에 있는 번호를 입력하세요.[/bold red]'
                )
                continue

            selected_patient = matched_patients[patient_index]

            show_selected_patient_payments(selected_patient)
            return

# 선택한 환자의 진료비 함수
def show_selected_patient_payments(selected_patient):
    patient_number = selected_patient['환자번호']
    patient_name = selected_patient['이름']

    # 의료진번호와 의료진 정보 연결
    doctor_dict = {}

    with open(
        'doctors.csv',
        'r',
        encoding='utf-8-sig',
        newline=''
    ) as file:
        reader = csv.DictReader(file)

        for doctor in reader:
            doctor_dict[doctor['의료진번호']] = {
                '이름': doctor['이름'],
                '진료과': doctor['진료과']
            }

    payment_list = []

    insured_total = 0
    uninsured_total = 0
    total_sales = 0

    with open(
        'reservations_500_added.csv',
        'r',
        encoding='utf-8-sig',
        newline=''
    ) as file:
        reader = csv.DictReader(file)

        for reservation in reader:
            if reservation['상태'] != '진료완료':
                continue

            if reservation['환자번호'] != patient_number:
                continue

            doctor_info = doctor_dict.get(
                reservation['의료진번호'],
                {
                    '이름': '정보 없음',
                    '진료과': '정보 없음'
                }
            )

            insured_fee = int(reservation['급여'])
            uninsured_fee = int(reservation['비급여'])
            total_fee = int(reservation['총금액'])

            insured_total += insured_fee
            uninsured_total += uninsured_fee
            total_sales += total_fee

            payment_list.append({
                '진료일자': reservation['예약날짜'],
                '진료과': doctor_info['진료과'],
                '의료진': doctor_info['이름'],
                '진단명': reservation['진단명'],
                '급여': insured_fee,
                '비급여': uninsured_fee,
                '총금액': total_fee
            })

    if not payment_list:
        console.print(
            Panel(
                f'[bold red]{patient_name}님의 '
                '진료완료 내역이 없습니다.[/bold red]',
                title='👤 환자별 진료비 조회',
                border_style='red'
            )
        )
        return

    # 최신 진료일부터 정렬
    payment_list.sort(
        key=lambda payment: payment['진료일자'],
        reverse=True
    )

    summary_table = Table.grid(padding=(0, 2))
    summary_table.add_column(style='bold')
    summary_table.add_column(justify='right')

    summary_table.add_row('환자명', patient_name)
    summary_table.add_row('환자번호', patient_number)
    summary_table.add_row(
        '진료 건수',
        f'{len(payment_list)}건'
    )
    summary_table.add_row(
        '급여 합계',
        f'[green]{insured_total:,}원[/green]'
    )
    summary_table.add_row(
        '비급여 합계',
        f'[yellow]{uninsured_total:,}원[/yellow]'
    )
    summary_table.add_row(
        '총 진료비',
        f'[bold magenta]{total_sales:,}원[/bold magenta]'
    )

    console.print(
        Panel(
            summary_table,
            title='[bold cyan]👤 환자 진료비 요약[/bold cyan]',
            border_style='cyan',
            expand=False
        )
    )

    payment_table = Table(
        title='🧾 환자별 진료비 내역',
        box=box.ROUNDED,
        header_style='bold white',
        border_style='bright_white',
        show_lines=True,
        expand=False
    )

    payment_table.add_column(
        '번호',
        justify='center',
        style='cyan',
        no_wrap=True
    )

    payment_table.add_column(
        '진료일',
        justify='center',
        no_wrap=True
    )

    payment_table.add_column(
        '진료 정보',
        justify='center'
    )

    payment_table.add_column(
        '진단명',
        justify='center'
    )

    payment_table.add_column(
        '급여',
        justify='right',
        style='green',
        no_wrap=True
    )

    payment_table.add_column(
        '비급여',
        justify='right',
        style='yellow',
        no_wrap=True
    )

    payment_table.add_column(
        '총금액',
        justify='right',
        style='bold magenta',
        no_wrap=True
    )

    for index, payment in enumerate(payment_list, start=1):
        medical_text = (
            f"[bold]{payment['진료과']}[/bold]\n"
            f"[dim]{payment['의료진']}[/dim]"
        )

        payment_table.add_row(
            str(index),
            payment['진료일자'],
            medical_text,
            payment['진단명'],
            f"{payment['급여']:,}원",
            f"{payment['비급여']:,}원",
            f"{payment['총금액']:,}원"
        )

    console.print(payment_table)

    input('\nEnter를 누르면 이전 메뉴로 돌아갑니다.')

# 진료과별 매출 조회
def show_department_sales():
    console.print(
        '\n[bold cyan]======== 진료과별 매출 조회 ========[/bold cyan]'
    )

    # 의료진번호와 진료과 연결
    doctor_dict = {}

    with open(
        'doctors.csv',
        'r',
        encoding='utf-8-sig',
        newline=''
    ) as file:
        reader = csv.DictReader(file)

        for doctor in reader:
            doctor_dict[doctor['의료진번호']] = doctor['진료과']

    # 진료과별 매출을 저장할 딕셔너리
    department_sales = {}

    total_insured = 0
    total_uninsured = 0
    total_sales = 0
    total_count = 0

    with open('reservations_500_added.csv', 'r', encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file)

        for reservation in reader:
            # 진료완료인 데이터만 매출에 포함
            if reservation['상태'] != '진료완료':
                continue

            doctor_number = reservation['의료진번호']

            department = doctor_dict.get(
                doctor_number,
                '정보 없음'
            )

            insured_fee = int(reservation['급여'])
            uninsured_fee = int(reservation['비급여'])
            total_fee = int(reservation['총금액'])

            # 해당 진료과가 처음 나오면 초기값 생성
            if department not in department_sales:
                department_sales[department] = {
                    '진료건수': 0,
                    '급여': 0,
                    '비급여': 0,
                    '총매출': 0
                }

            # 진료과별 합계
            department_sales[department]['진료건수'] += 1
            department_sales[department]['급여'] += insured_fee
            department_sales[department]['비급여'] += uninsured_fee
            department_sales[department]['총매출'] += total_fee

            # 전체 합계
            total_count += 1
            total_insured += insured_fee
            total_uninsured += uninsured_fee
            total_sales += total_fee

    if not department_sales:
        console.print(
            Panel(
                '[bold red]조회할 진료과별 매출 내역이 없습니다.[/bold red]',
                title='🏥 진료과별 매출 조회',
                border_style='red'
            )
        )
        return

    # 총매출이 높은 진료과부터 정렬
    sorted_departments = sorted(
        department_sales.items(),
        key=lambda item: item[1]['총매출'],
        reverse=True
    )

    department_table = Table(
        title='🏥 진료과별 매출 현황',
        box=box.ROUNDED,
        header_style='bold white',
        border_style='bright_white',
        show_lines=True,
        padding=(0, 1),
        expand=False
    )

    department_table.add_column(
        '순위',
        justify='center',
        style='cyan',
        no_wrap=True
    )

    department_table.add_column(
        '진료과',
        justify='center',
        no_wrap=True
    )

    department_table.add_column(
        '진료 건수',
        justify='center',
        no_wrap=True
    )

    department_table.add_column(
        '급여 매출',
        justify='right',
        style='green',
        no_wrap=True
    )

    department_table.add_column(
        '비급여 매출',
        justify='right',
        style='yellow',
        no_wrap=True
    )

    department_table.add_column(
        '총매출',
        justify='right',
        style='bold magenta',
        no_wrap=True
    )

    for rank, (department, sales) in enumerate(
        sorted_departments,
        start=1
    ):
        department_table.add_row(
            str(rank),
            department,
            f"{sales['진료건수']}건",
            f"{sales['급여']:,}원",
            f"{sales['비급여']:,}원",
            f"{sales['총매출']:,}원"
        )

    summary_table = Table.grid(padding=(0, 2))

    summary_table.add_column(
        justify='left',
        style='bold'
    )

    summary_table.add_column(
        justify='right'
    )

    summary_table.add_row(
        '🏥 전체 진료 건수',
        f'[bold cyan]{total_count}건[/bold cyan]'
    )

    summary_table.add_row(
        '🩺 전체 급여 매출',
        f'[green]{total_insured:,}원[/green]'
    )

    summary_table.add_row(
        '💊 전체 비급여 매출',
        f'[yellow]{total_uninsured:,}원[/yellow]'
    )

    summary_table.add_row(
        '💰 전체 매출',
        f'[bold magenta]{total_sales:,}원[/bold magenta]'
    )

    console.print()

    console.print(
        Panel(
            summary_table,
            title='[bold cyan]💰 진료과 매출 요약[/bold cyan]',
            border_style='cyan',
            expand=False
        )
    )

    console.print(department_table)

    input('\nEnter를 누르면 이전 메뉴로 돌아갑니다.')

# 급여/비급여별 조회
def show_payment_by_type():
    console.print('\n[bold cyan]======== 급여/비급여별 조회 ========[/bold cyan]')

    insured_total = 0
    uninsured_total = 0

    insured_count = 0
    uninsured_count = 0
    completed_count = 0

    with open('reservations_500_added.csv', 'r', encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file)

        for reservation in reader:
            if reservation['상태'] != '진료완료':
                continue

            insured_fee = int(reservation['급여'])
            uninsured_fee = int(reservation['비급여'])

            insured_total += insured_fee
            uninsured_total += uninsured_fee
            completed_count += 1

            if insured_fee > 0:
                insured_count += 1

            if uninsured_fee > 0:
                uninsured_count += 1

    if completed_count == 0:
        console.print('[bold red]조회할 매출 내역이 없습니다.[/bold red]\n')
        return

    total_sales = insured_total + uninsured_total

    payment_table = Table(
        title='💰 급여·비급여 매출 현황',
        box=box.ROUNDED,
        header_style='bold white on blue',
        border_style='bright_blue'
    )

    payment_table.add_column('구분', justify='center')
    payment_table.add_column('포함 건수', justify='center')
    payment_table.add_column('매출 금액', justify='right')

    payment_table.add_row(
        '급여',
        f'{insured_count}건',
        f'[green]{insured_total:,}원[/green]'
    )

    payment_table.add_row(
        '비급여',
        f'{uninsured_count}건',
        f'[yellow]{uninsured_total:,}원[/yellow]'
    )

    payment_table.add_row(
        '전체',
        f'{completed_count}건',
        f'[bold magenta]{total_sales:,}원[/bold magenta]'
    )

    console.print(payment_table)

    summary = (
        f'급여 매출 비율   : '
        f'{insured_total / total_sales * 100:.1f}%\n'
        f'비급여 매출 비율 : '
        f'{uninsured_total / total_sales * 100:.1f}%'
    )

    console.print(
        Panel(
            summary,
            title='📊 매출 비율',
            border_style='cyan',
            expand=False
        )
    )

    input('\nEnter를 누르면 이전 메뉴로 돌아갑니다.')

# 월별 매출 조회
def show_monthly_sales():
    console.print('\n[bold cyan]======== 월별 매출 조회 ========[/bold cyan]')

    search_year = input('조회할 연도를 입력하세요 (YYYY / 0. 이전) : ').strip()

    if search_year == '0':
        return

    search_month = input(
        '조회할 월을 입력하세요 (1~12) : '
    ).strip()

    if (
        not search_year.isdigit()
        or len(search_year) != 4
        or not search_month.isdigit()
        or not 1 <= int(search_month) <= 12
    ):
        console.print(
            '[bold red]연도와 월을 올바르게 입력하세요.[/bold red]\n'
        )
        return

    search_month = search_month.zfill(2)
    search_year_month = f'{search_year}-{search_month}'

    # 날짜별 매출 저장
    daily_sales_dict = {}

    monthly_insured_total = 0
    monthly_uninsured_total = 0
    monthly_total_sales = 0
    monthly_count = 0

    with open('reservations_with_fee_breakdown.csv', 'r', encoding='utf-8-sig', newline='')as file:
        reader = csv.DictReader(file)

        for reservation in reader:
            if reservation['상태'] != '진료완료':
                continue

            if not reservation['예약날짜'].startswith(search_year_month):
                continue

            reservation_date = reservation['예약날짜']

            insured_fee = int(reservation['급여'])
            uninsured_fee = int(reservation['비급여'])
            total_fee = int(reservation['총금액'])

            monthly_insured_total += insured_fee
            monthly_uninsured_total += uninsured_fee
            monthly_total_sales += total_fee
            monthly_count += 1

            if reservation_date not in daily_sales_dict:
                daily_sales_dict[reservation_date] = {
                    '건수': 0,
                    '급여': 0,
                    '비급여': 0,
                    '총금액': 0
                }

            daily_sales_dict[reservation_date]['건수'] += 1
            daily_sales_dict[reservation_date]['급여'] += insured_fee
            daily_sales_dict[reservation_date]['비급여'] += uninsured_fee
            daily_sales_dict[reservation_date]['총금액'] += total_fee

    if monthly_count == 0:
        console.print('[bold red]해당 월의 매출 내역이 없습니다.[/bold red]\n')
        return

    monthly_table = Table(
        title=f'📆 {search_year}년 {search_month}월 매출',
        box=box.ROUNDED,
        header_style='bold white on blue',
        border_style='bright_blue',
        show_lines=True
    )

    monthly_table.add_column('날짜', justify='center')
    monthly_table.add_column('진료 건수', justify='center')
    monthly_table.add_column('급여', justify='right', style='green')
    monthly_table.add_column('비급여', justify='right', style='yellow')
    monthly_table.add_column(
        '총매출',
        justify='right',
        style='bold magenta'
    )

    for date in sorted(daily_sales_dict):
        daily_data = daily_sales_dict[date]

        monthly_table.add_row(
            date,
            f"{daily_data['건수']}건",
            f"{daily_data['급여']:,}원",
            f"{daily_data['비급여']:,}원",
            f"{daily_data['총금액']:,}원"
        )

    console.print(monthly_table)

    summary_table = Table.grid(padding=(0, 2))
    summary_table.add_column(style='bold')
    summary_table.add_column(justify='right')

    summary_table.add_row(
        '월 진료 건수',
        f'{monthly_count}건'
    )
    summary_table.add_row(
        '급여 합계',
        f'[green]{monthly_insured_total:,}원[/green]'
    )
    summary_table.add_row(
        '비급여 합계',
        f'[yellow]{monthly_uninsured_total:,}원[/yellow]'
    )
    summary_table.add_row(
        '월 총매출',
        f'[bold magenta]{monthly_total_sales:,}원[/bold magenta]'
    )

    console.print(
        Panel(
            summary_table,
            title='💰 월별 매출 요약',
            border_style='cyan',
            expand=False
        )
    )
    input('\nEnter를 누르면 이전 메뉴로 돌아갑니다.')


# 일별 매출 조회
'''def show_daily_sales():
    console.print('\n[bold cyan]======== 일별 매출 조회 ========[/bold cyan]')

    search_date = input(
        '조회할 날짜를 입력하세요 (YYYY-MM-DD / 0. 이전) : '
    ).strip()

    if search_date == '0':
        return

    try:
        datetime.datetime.strptime(
            search_date,
            '%Y-%m-%d'
        )

    except ValueError:
        console.print(
            '[bold red]날짜 형식은 YYYY-MM-DD로 입력하세요.[/bold red]\n'
        )
        return

    patient_dict = {}

    with open(
        'user.csv',
        'r',
        encoding='utf-8-sig',
        newline=''
    ) as file:
        reader = csv.DictReader(file)

        for user in reader:
            patient_dict[user['환자번호']] = user['이름']

    daily_list = []

    insured_total = 0
    uninsured_total = 0
    total_sales = 0

    with open(
        'reservations_with_fee_breakdown.csv',
        'r',
        encoding='utf-8-sig',
        newline=''
    ) as file:
        reader = csv.DictReader(file)

        for reservation in reader:
            if (
                reservation['상태'] != '진료완료'
                or reservation['예약날짜'] != search_date
            ):
                continue

            insured_fee = int(reservation['급여'])
            uninsured_fee = int(reservation['비급여'])
            total_fee = int(reservation['총금액'])

            insured_total += insured_fee
            uninsured_total += uninsured_fee
            total_sales += total_fee

            daily_list.append({
                '환자번호': reservation['환자번호'],
                '환자명': patient_dict.get(
                    reservation['환자번호'],
                    '정보 없음'
                ),
                '진단명': reservation['진단명'],
                '급여': insured_fee,
                '비급여': uninsured_fee,
                '총금액': total_fee
            })

    if not daily_list:
        console.print(
            '[bold red]해당 날짜의 매출 내역이 없습니다.[/bold red]\n'
        )
        return

    daily_table = Table(
        title=f'📅 {search_date} 일별 매출',
        box=box.ROUNDED,
        header_style='bold white on blue',
        border_style='bright_blue',
        show_lines=True
    )

    daily_table.add_column('번호', justify='center')
    daily_table.add_column('환자번호', justify='center')
    daily_table.add_column('환자명', justify='center')
    daily_table.add_column('진단명', justify='center')
    daily_table.add_column('급여', justify='right', style='green')
    daily_table.add_column('비급여', justify='right', style='yellow')
    daily_table.add_column(
        '총금액',
        justify='right',
        style='bold magenta'
    )

    for index, payment in enumerate(daily_list, start=1):
        daily_table.add_row(
            str(index),
            payment['환자번호'],
            payment['환자명'],
            payment['진단명'],
            f"{payment['급여']:,}원",
            f"{payment['비급여']:,}원",
            f"{payment['총금액']:,}원"
        )

    console.print(daily_table)

    summary_table = Table.grid(padding=(0, 2))
    summary_table.add_column(style='bold')
    summary_table.add_column(justify='right')

    summary_table.add_row('진료 건수', f'{len(daily_list)}건')
    summary_table.add_row(
        '급여 매출',
        f'[green]{insured_total:,}원[/green]'
    )
    summary_table.add_row(
        '비급여 매출',
        f'[yellow]{uninsured_total:,}원[/yellow]'
    )
    summary_table.add_row(
        '일일 총매출',
        f'[bold magenta]{total_sales:,}원[/bold magenta]'
    )

    console.print(
        Panel(
            summary_table,
            title='💰 일별 매출 요약',
            border_style='cyan',
            expand=False
        )
    )

    input('\nEnter를 누르면 이전 메뉴로 돌아갑니다.')'''




# ==============================================================
while True:
    # 로그인하지 않은 상태
    if current_user is None:
        show_login_menu()
        choice = input('메뉴를 선택하세요 > ')

        if choice == '1':
            current_user = login(current_user)

        elif choice == '2':
            signup()

        elif choice == '3':
            print('프로그램을 종료합니다.')
            break

        else:
            print('올바른 메뉴 번호가 아닙니다.\n')

    else:
        # 관리자
        if current_user['권한'] == 'admin':
            current_user = admin_manage(current_user)

        # 일반 회원
        else:
            current_user = user_view(current_user)




