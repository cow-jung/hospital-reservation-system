#테스트 메세지
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
import re
from getpass import getpass
from tabnanny import check

from tabulate import tabulate
from wcwidth import wcswidth
import calendar
import datetime
import os

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
    print('\n======== 예약하기 ========')
    print('1. 진료과로 예약')
    print('2. 과거 진료 이력으로 예약')
    print('\n0. 이전 메뉴')
    print('==========================\n')

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

    print(f"\n ============ [예약 상세] ============")
    print(f"예약날짜: {date_str}")
    print(f"예약시간: {time_str}")
    print(f"진료과 및 의료진 이름: {doctor['진료과']} {doctor['이름']}")
    print(f"====================================")

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

    print(f"\n================ [{current_user['이름']}]님의 진료 이력 ================")

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
    print("=====================================================")

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
    print(f"\n ============ [예약 상세] ============")
    print(f"예약날짜: {date_str}")
    print(f"예약시간: {time_str}")
    print(f"진료과 및 의료진 이름: {selected_doctor['진료과']} {selected_doctor['이름']}")
    print(f"====================================")

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

    print("\n======== 진료과 선택 ========")
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

    print(f"\n==================== {department} 의료진 선택 ====================")
    for index, doctor_info in enumerate(available_doctors, 1):
        print(
            f"{index}. {doctor_info['이름']} (진료요일: {doctor_info['진료요일']} / 진료시간: {doctor_info['진료시작시간']} ~ {doctor_info['진료종료시간']})")
    print("\n0. 이전 메뉴")
    print(f"========================================================")

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
    print(f"\n======== {year}년 {month}월 예약 달력 ========")
    print("월    화    수    목   금")

    fully_booked_dates = []

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
                    week_string += f"[{day:2d}] "
                    fully_booked_dates.append(date_str)
                else:
                    week_string += f" {day:2d}  "

        if week_string.strip():
            print(week_string)

    print("\n * [ ]: 예약 불가능한 날짜")
    print(f"===================================")

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

    print(f"\n=========== {date_str} 예약 가능 시간 ===========")
    for index, t in enumerate(available_times, 1):
        print(f"{index}. {t}")
    print("\n0. 이전 메뉴")
    print(f"==============================================")

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

    fieldnames = ['예약번호', '환자번호', '의료진번호', '예약날짜', '예약시간', '총금액', '상태']

    # os.path.isfile(): 해당 경로에 파일이 실제로 존재하는지 확인
    file_exists = os.path.isfile('reservations_total_only.csv')

    with open('reservations_total_only.csv', 'a', encoding='utf-8-sig', newline='') as file:
        # csv.DictWriter(): 딕셔너리 형태의 데이터를 CSV 파일에 쓸 수 있게 하는 기능
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()  # 파일이 없어서 새로 만들었다면 맨 윗줄(헤더)을 작성
        writer.writerow(new_reservation)  # 실제 데이터를 한 줄 작성

    print(f"\n ============ [예약 완료] ============")
    print(f"예약이 아래와 같이 완료되었습니다.")
    print(f"발급된 예약번호: {new_reservation_id}")
    print(f"====================================")
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
            update_my_reservation(current_user)

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
def update_my_reservation(current_user):
    print('\n======== 예약 변경 ========')
    print(current_user['이름'], '님의 예약을 변경합니다.')
    print()

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


# 한글을 포함한 문자열의 출력 너비를 맞춰주는 함수
def pad(text, width, align="left"):
    text = str(text)
    space = width - wcswidth(text)

    if align == "right":
        return " " * space + text
    else:
        return text + " " * space

# 전체 조회
def show_all_reservations():
    import csv
    from wcwidth import wcswidth

    # CSV 파일 읽기
    with open("reservations_with_fee_breakdown.csv", "r", encoding="utf-8-sig") as file:
        reader = list(csv.DictReader(file))

    # 표의 가로 구분선
    line = "=" * 125

    # 제목 출력
    print(line)
    print("전체 예약 조회".center(len(line)))
    print(line)

    # 헤더 출력
    print(
        pad("   예약번호", 21),
        pad("환자번호", 14),
        pad("의료진번호", 17),
        pad("예약날짜", 16),
        pad("예약시간", 15),
        pad("급여", 12),
        pad("비급여", 14),
        pad("총금액", 14),
        pad("상태", 10)
    )

    print(line)

    # 예약 정보 출력
    for row in reader:
        print(
            pad(row["예약번호"], 18),
            pad(row["환자번호"], 13),
            pad(row["의료진번호"], 12),
            pad(row["예약날짜"], 16),
            pad(row["예약시간"], 6),
            pad(f"{int(row['급여']):,}", 11, 'right') + ' ',
            pad(f"{int(row['비급여']):,}", 11, 'right') + ' ',
            pad(f"{int(row['총금액']):,}", 11, 'right') + '      ',
            pad(row["상태"], 5)
        )

    # 표의 마지막 구분선
    print(line)

# 환자별 조회
def search_reservation_by_patient():
    import csv

    # 조회할 환자번호 입력
    patient_no = input("\n환자번호를 입력하세요 : ")

    # CSV 파일 읽기
    with open("reservations_with_fee_breakdown.csv", "r", encoding="utf-8-sig") as file:
        reader = list(csv.reader(file))

    # 표의 가로 구분선
    line = "=" * 125

    print()
    print(line)
    print("환자별 예약 조회".center(len(line)))
    print(line)

    # 헤더 출력
    print(
        pad("   예약번호", 21),
        pad("환자번호", 14),
        pad("의료진번호", 17),
        pad("예약날짜", 16),
        pad("예약시간", 15),
        pad("급여", 12),
        pad("비급여", 14),
        pad("총금액", 14),
        pad("상태", 10)
    )

    print(line)

    # 조회 결과 확인 변수
    found = False

    # 입력한 환자번호와 일치하는 예약 조회
    for row in reader[1:]:
        if row[1] == patient_no:
            found = True

            print(
                pad(row[0], 18),
                pad(row[1], 13),
                pad(row[2], 12),
                pad(row[3], 16),
                pad(row[4], 6),
                pad(f"{int(row[5]):,}", 11, 'right') + ' ',
                pad(f"{int(row[6]):,}", 11, 'right') + ' ',
                pad(f"{int(row[7]):,}", 11, 'right') + '      ',
                pad(row[8], 5)
            )

    print(line)

    # 조회 결과가 없는 경우
    if not found:
        print("조회된 예약이 없습니다.")


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

def show_all_doctors():
    print('\n======== 전체 의료진 조회 ========')

    # doctors.csv 전체 의료진 조회


def show_doctors_by_department_admin():
    print('\n======== 진료과별 의료진 조회 ========')

    # 진료과 선택
    # 해당 진료과 의료진 조회


def update_doctor():
    print('\n======== 의료진 정보 수정 ========')

    # 수정할 의료진 검색
    # 수정할 정보 선택
    # doctors.csv 저장


def delete_doctor():
    print('\n======== 의료진 삭제 ========')

    # 삭제할 의료진 검색
    # 삭제 여부 확인
    # 근무상태 변경 또는 의료진 삭제
    # doctors.csv 저장

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
            show_payment_by_type()

        elif choice == '4':
            show_daily_sales()

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
    print('3. 급여/비급여별 조회')
    print('4. 일별 매출 조회')
    print('5. 월별 매출 조회')
    print('0. 이전 메뉴')
    print('================================\n')

def show_all_payments():
    print('\n======== 전체 진료비 조회 ========')
    # 전체 진료비와 수납 상태 조회


def search_payment_by_patient():
    print('\n======== 환자별 진료비 조회 ========')

    # 환자 검색
    # 해당 환자의 진료비 조회


def show_payment_by_type():
    print('\n======== 급여/비급여별 조회 ========')

    # 급여 항목 조회
    # 비급여 항목 조회


def show_daily_sales():
    print('\n======== 일별 매출 조회 ========')

    # 조회 날짜 입력
    # 해당 날짜의 수납 완료 금액 합계 조회


def show_monthly_sales():
    print('\n======== 월별 매출 조회 ========')

    # 조회 연도와 월 입력
    # 해당 월의 수납 완료 금액 합계 조회



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




