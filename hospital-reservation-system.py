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
from tabulate import tabulate
from wcwidth import wcswidth

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
        resident_number = input('주민등록번호를 입력하세요(000000-0) : ').strip()

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
        reservation_menu()

        choice = input('예약 방법을 선택하세요 > ')

        if choice == '1':
            reserve_by_department(current_user)

        elif choice == '2':
            reserve_by_history(current_user)

        elif choice == '0':
            break

        else:
            print('올바른 메뉴 번호를 입력하세요.\n')

# 예약 방법 메뉴 출력
def reservation_menu():
    print('\n======== 예약하기 ========')
    print('1. 진료과로 예약')
    print('2. 과거 진료 이력으로 예약')
    print('0. 이전 메뉴')
    print('==========================\n')

# 진료과로 예약
def reserve_by_department(current_user):
    print('\n======== 진료과로 예약 ========')
    # 진료과 선택
    # 의료진 선택
    # 예약 날짜 선택
    # 예약 시간 선택
    # 예약 메모 입력
    # 예약 내용 확인
    # 예약 저장

# 과거 진료 이력으로 예약
def reserve_by_history(current_user):
    print('\n======== 과거 진료 이력으로 예약 ========')
    # 과거 진료 이력 조회
    # 진료 이력 선택
    # 의료진 선택
    # 예약 날짜 선택
    # 예약 시간 선택
    # 예약 내용 확인
    # 예약 저장

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

        elif choice == '2':
            show_medical_history_detail(current_user)

        elif choice == '3':
            show_medical_fee(current_user)

        elif choice == '0':
            break

        else:
            print('올바른 메뉴 번호를 입력하세요.\n')

# 진료 이력 조회 메뉴
def medical_history_menu():
    print('\n======== 진료 이력 조회 ========')
    print('1. 전체 진료 이력 조회')
    print('2. 진료 이력 상세 조회')
    print('3. 진료비 확인')
    print('0. 이전 메뉴')
    print('===============================\n')

# 전체 진료 이력 조회
def show_medical_history(current_user):
    # 로그인한 사용자의 환자번호 확인
    # 해당 환자의 진료 이력 전체 조회
    # 진료일자 / 진료과 / 의료진 / 진료상태 출력

    medical_history_list = []
    with open('reservations_total_only.csv', 'r', encoding='utf-8-sig',newline='') as file:
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

                medical_history_list.append([
                    len(medical_history_list)+1,
                    row['예약번호'],
                    department,
                    doctor_name,
                    row['예약날짜'],
                    row['예약시간'],
                    f"{int(row['총금액']):,}원",
                    row['상태']
                ])

        if medical_history_list:
            table = tabulate(
                medical_history_list,
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

        else:
            print('진료 이력이 없습니다.\n')

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

def show_all_reservations():
    import csv
    from wcwidth import wcswidth

    # CSV 파일 읽기
    with open("reservations_with_fee_breakdown.csv", "r", encoding="utf-8-sig") as file:
        reader = list(csv.reader(file))

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
    for row in reader[1:]:
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

    # 표의 마지막 구분선
    print(line)


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



def update_reservation():
    print('\n======== 예약 수정 ========')

    # 수정할 예약번호 입력
    reservation_no = input("수정할 예약번호를 입력하세요 : ")

    # 파일읽기
    with open("reservations_with_fee_breakdown.csv", "r", encoding="utf-8-sig") as file:
        reader = list(csv.reader(file))

        # 예약번호를 찾았는지 확인하는 변수
        found = False

        # 헤더를 제외한 예약 데이터 검색
        for row in reader[1:]:

            # 예약번호가 일치하면
            if row[0] == reservation_no:
                found = True

                # 현재 예약 정보 출력
                print("\n================ 현재 예약 정보 ================")
                print(f"예약번호   : {row[0]}")
                print(f"환자번호   : {row[1]}")
                print(f"의료진번호 : {row[2]}")
                print(f"예약날짜   : {row[3]}")
                print(f"예약시간   : {row[4]}")
                print("==============================================")

                # 새로운 예약 날짜와 시간 입력
                new_date = input("새 예약날짜를 입력하세요 (YYYY-MM-DD) : ")
                new_time = input("새 예약시간을 입력하세요 (HH:MM) : ")

                # 수정 여부 확인
                check = input("\n정말 수정하시겠습니까? (Y/N) : ").upper()

                if check == "Y":
                    # 날짜와 시간 수정
                    row[3] = new_date
                    row[4] = new_time

                    print("\n예약이 수정되었습니다.")

                else:
                    print("\n예약 수정을 취소했습니다.")

                break

        # 예약번호를 찾지 못한 경우
        if not found:
            print("\n예약번호가 존재하지 않습니다.")
            return

        # 수정된 내용을 csv파일에 저장
        with open("reservations_with_fee_breakdown.csv", "w", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(reader)



def cancel_reservation():
    print('\n======== 예약 취소 ========')

    # 취소할 예약 검색
    # 취소 여부 확인
    # 예약상태를 취소로 변경
    # reservation.csv 저장

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
            urrent_user = user_view(current_user)




