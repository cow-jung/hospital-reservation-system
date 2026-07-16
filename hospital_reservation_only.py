import csv
import calendar
import datetime
import os # 운영체제와 상호작용을 하게 해주는 모듈이다. 파일이 존재하는지 확인하기 위해 사용

def show_login_menu(): # 로그인 첫 메뉴
    print('======== 🏥 병원 예약 관리 시스템 로그인 ========')
    print('1. 로그인')
    print('2. 회원가입')
    print('3. 프로그램 종료\n')

current_user = None  # 현재 로그인한 사용자 정보를 저장

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

def user_menu(current_user): # 사용자 로그인 시 메뉴
    print('======== 병원 예약 관리 ========')
    print(f"현재 사용자 : {current_user['이름']} / {current_user['환자번호']}")
    print('1. 진료과 조회')
    print('2. 예약하기')
    print('3. 내 예약 관리')
    print('4. 진료 이력 조회')
    print('5. 로그아웃')
    print('=============================\n')

def admin_menu(current_user): # 관리자 로그인 시 메뉴
    print('======== 병원 예약 관리 ========')
    print(f"현재 사용자 : {current_user['이름']} / {current_user['환자번호']}")
    print('1. 회원 관리')
    print('2. 예약 관리')
    print('3. 진료과/의료진 관리')
    print('4. 진료비/매출 조회')
    print('5. 로그아웃')
    print('=============================\n')

def signup(): # 회원가입 메뉴
    print("회원가입")

# 로그아웃 기능
def logout(current_user):
    # 로그인 상태가 아니면 종료
    if current_user is None:
        print('로그인 상태가 아닙니다.')
        return None
    # 로그아웃하면 현재 사용자를 None으로 반환
    print(current_user['이름'], '님 로그아웃')
    return None

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

# 선택한 진료과의 의료진 전체 출력
def show_doctors_by_department(department):
    print(department)
    pass

# 입력한 아이디/비밀번호가 일치하는 사용자 찾기
def find_user(user_id, password):
    with open('user.csv','r',encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for user in reader:
            if user['아이디'] == user_id and user['비밀번호'] == password:
                return user
    # 일치하는 사용자가 없으면 None 반환
    return None

'''============= 예약 ============='''
# 예약 방법 메뉴 출력
def reservation_menu():
    print('\n========= 예약하기 =========')
    print('1. 진료과로 예약')
    print('2. 과거 진료 이력으로 예약')
    print('\n0. 이전 메뉴')
    print('==========================\n')

# 예약 전체 흐름
def reservation(current_user):
    while True:
        reservation_menu() # 예약 방법 메뉴

        choice = input('예약 방법을 선택하세요 > ')

        if choice == '1':
            is_success = reserve_by_department(current_user) # 진료과로 예약
            if is_success: # 예약이 성공(True)했다면 예약 메뉴를 완전히 빠져나감
                return

        elif choice == '2':
            is_success = reserve_by_history(current_user) # 과거 진료 이력으로 예약
            if is_success: # 예약이 성공(True)했다면 예약 메뉴를 완전히 빠져나감
                return


        elif choice == '0':
            print('이전 메뉴로 돌아갑니다.')
            break

        else:
            print('올바른 메뉴 번호를 입력하세요.\n')

def reserve_by_department(current_user):
    # 1. 데이터 불러오기
    doctors = load_doctors()  # load_doctors(): 의료진 정보를 불러오기 위한 함수
    reservations = load_reservations()  # load_reservations : 전체 예약 정보를 불러오기 위한 함수

    # 2. 진료과 선택
    department = select_department(doctors)  # select_department : 진료과를 선택하기 위한 함수
    if department is None:
        return

    # 3. 의료진 선택
    doctor = select_doctor(doctors, department) # select_doctor : 의료진을 선택하기 위한 함수
    if doctor is None:  # 의료진이 없어서 None이 반환되었다면
        return  # 함수를 즉시 종료하고 예약 메뉴로 돌아감

    while True:
        # 4. 날짜 선택
        date_str = select_date(doctor, reservations) # select_date : 날짜를 선택하기 위한 함수
        if date_str is None:  # '취소'을 눌러서 None이 반환되었다면
            return  # 예약 메뉴로 돌아감

        # 5. 시간 선택
        time_str = select_time(doctor, date_str, reservations)
        if time_str is None:
            print("\n시간 선택을 취소했습니다. 다시 날짜를 선택해주세요.")
            continue

        # 날짜와 시간을 모두 정상적으로 선택했다면 루프 탈출
        break

    print(f"\n ========== [예약 상세] ==========")
    print(f"예약날짜: {date_str}")
    print(f"예약시간: {time_str}")
    print(f"진료과 및 의료진 이름: {doctor['진료과']} {doctor['이름']}")
    print(f"================================")

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

    print(f"\n======== [{current_user['이름']}]님의 진료 이력 ========")

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
    print(f"\n ======== [예약 상세] ========")
    print(f"예약날짜: {date_str}")
    print(f"예약시간: {time_str}")
    print(f"진료과 및 의료진 이름: {selected_doctor['진료과']} {selected_doctor['이름']}")
    print(f"================================")

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

    while True:
        try:
            # .strip(): 사용자가 실수로 스페이스바를 누르거나 엔터를 친 '공백'을 양끝에서 깔끔하게 잘라내는 기능
            value = input("\n 진료과 번호를 선택하세요: ").strip()
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
    available_doctors = [doctor_info for doctor_info in doctors if doctor_info['진료과'] == department and doctor_info['근무상태'] == '진료중']

    if not available_doctors:
        print("현재 해당 진료과에 예약 가능한 의료진이 없습니다.")
        return None

    print(f"\n==================== {department} 의료진 선택 ====================")
    for index, doctor_info in enumerate(available_doctors, 1):
        print(f"{index}. {doctor_info['이름']} (진료요일: {doctor_info['진료요일']} / 진료시간: {doctor_info['진료시작시간']} ~ {doctor_info['진료종료시간']})")
    print("\n0. 이전 메뉴")

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

    print(f"\n ======== [예약 완료] ========")
    print(f"예약이 아래와 같이 완료되었습니다.")
    print(f"발급된 예약번호: {new_reservation_id}")
    print(f"=============================")
    print()
    print()


def user_manage(current_user):
    while True:
        # 메뉴 출력
        user_menu(current_user)

        # 사용자 입력 대기
        choice = input('메뉴를 선택하세요 > ')

        if choice == '1':
            department_doctor_view()
        elif choice == '2':
            reservation(current_user)
        elif choice == '3':
            my_reservation(current_user)
        elif choice == '4':
            medical_history(current_user)
        elif choice == '5':
            # 로그아웃 후 상태 반환
            current_user = logout(current_user)
            return current_user
        else:
            print('올바른 메뉴 번호를 입력하세요.\n')

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
            current_user = user_manage(current_user)