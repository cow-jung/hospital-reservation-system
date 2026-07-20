"""
part_reservation.py — 예약 담당 (신규 예약 흐름 + 내 예약 조회/변경/취소)
"""
import csv
import calendar
import datetime
import os

from tabulate import tabulate

from part_common import (
    USER_CSV, DOCTOR_CSV, RESERVATION_CSV,
    clear_screen, pause, print_box, safe_width, center_by_width,
)


'''============= 예약 ============='''
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
    clear_screen()
    print()
    lines = [
        '1. 진료과로 예약',
        '2. 과거 진료 이력으로 예약',
        '',
        '0. 이전 메뉴'
    ]
    print_box(lines, title='예약하기')
    print()

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

    if reservations is None:
        reservations = []

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

    # 출력 및 선택을 위해 리스트에 저장
    display_list = []
    table_data = []
    # enumerate 대신 직접 번호를 세는 변수(display_index)를 만듭니다.
    display_index = 1

    for record in history_records:
        doctor_info_id = record['의료진번호']
        doctor_info = doctor_dict.get(doctor_info_id)

        # 만약 의료진 정보가 '정상적으로 존재하는 경우'에만 번호표를 부여하고 출력합니다!
        if doctor_info:
            date = record['예약날짜']
            department_name = doctor_info['진료과']
            doctor_info_name = doctor_info['이름']

            display_list.append(doctor_info)
            table_data.append([
                display_index,
                department_name,
                doctor_info_name,
                date
            ])
            display_index += 1
            # 출력이 성공했을 때만 다음 번호표로 숫자를 1 올립니다.

        # tabulate를 활용한 표 출력 로직
    if table_data:
        table = tabulate(
            table_data,
            headers=['번호', '진료과', '의료진', '진료 날짜'],
            tablefmt='grid',
            disable_numparse=True,
            colalign=('center', 'center', 'center', 'center')
        )
        first_line = table.splitlines()[0]
        table_width = safe_width(first_line)
        title = f"🗓️ [{current_user['이름']}]님의 진료 이력"

        print()
        print('=' * table_width)
        print(center_by_width(title, table_width))
        print('=' * table_width)
        print(table)
        print(center_by_width("0. 이전 메뉴", table_width))
        print('=' * table_width)
    else:
        print("\n표시할 진료 이력이 없습니다.")
        return

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
        with open(DOCTOR_CSV, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # .append(): 리스트(doctors)의 맨 마지막에 새로운 데이터(row)를 하나씩 추가
                doctors.append(row)
    except FileNotFoundError:
        print(f"오류: {DOCTOR_CSV} 파일이 존재하지 않습니다.")
        return None
    return doctors

def load_reservations():
    # 전체 예약 정보를 CSV에서 불러옴
    reservations = []

    # RESERVATION_CSV가 상대 경로라면 현재 파이썬 파일이 있는 폴더를 기준으로 찾습니다.
    if os.path.isabs(RESERVATION_CSV):
        file_path = RESERVATION_CSV
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, RESERVATION_CSV)

    try:
        with open(file_path, 'r', encoding='utf-8-sig', newline='') as file:
            reader = csv.DictReader(file)

            for row in reader:
                reservations.append(row)

    except FileNotFoundError:
        print(f"\n[오류] 다음 위치에서 예약 파일을 찾을 수 없습니다: {file_path}")

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

    # 표 데이터를 담을 리스트
    table_data = []

    for index, doctor_info in enumerate(available_doctors, 1):
        # 긴 요일 문자열을 깔끔하게 축약 (예: 월,화,수,목,금 -> 월~금)
        working_days = doctor_info['진료요일'].replace('월,화,수,목,금', '월~금')
        working_time = f"{doctor_info['진료시작시간']} ~ {doctor_info['진료종료시간']}"

        table_data.append([
            index,
            doctor_info['이름'],
            working_days,
            working_time
        ])

    # 표 출력 로직
    if table_data:
        table = tabulate(
            table_data,
            headers=['번호', '의료진', '진료 요일', '진료 시간'],
            tablefmt='grid',
            disable_numparse=True,
            colalign=('center', 'center', 'center', 'center')
        )

        # 표의 테두리 길이를 계산하여 상하단 디자인을 맞춥니다.
        first_line = table.splitlines()[0]
        table_width = safe_width(first_line)
        title = f"🩺 {department} 의료진 선택"

        print()
        print('=' * table_width)
        print(center_by_width(title, table_width))
        print('=' * table_width)
        print(table)
        print(center_by_width("0. 이전 메뉴", table_width))
        print('=' * table_width)

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
    date_prefix = date_str.replace('-', '')
    max_sequence_number = 0

    for reservation_record in reservations:
        if reservation_record.get('예약날짜') == date_str:
            reservation_id = reservation_record.get('예약번호', '')

            if reservation_id.startswith(date_prefix):
                try:
                    sequence_number = int(reservation_id.split('-')[1])
                    max_sequence_number = max(
                        max_sequence_number,
                        sequence_number
                    )
                except (IndexError, ValueError):
                    pass

    new_reservation_id = (
        f'{date_prefix}-{max_sequence_number + 1:03d}'
    )

    # 예약 생성 시점에는 아직 진료 전이므로 진단명/급여/비급여/총금액은 빈 값(0)으로 두고,
    # 진료가 끝난 뒤 관리자 쪽에서 채워 넣습니다. (RESERVATION_CSV 스키마와 동일하게 전 항목 포함)
    new_reservation = {
        '예약번호': new_reservation_id,
        '환자번호': patient_id,
        '의료진번호': doctor['의료진번호'],
        '예약날짜': date_str,
        '예약시간': time_str,
        '진단명': '',
        '비급여': '0',
        '급여': '0',
        '총금액': '0',
        '상태': '예약완료'
    }

    file_path = RESERVATION_CSV
    file_exists = os.path.isfile(file_path)

    default_fieldnames = [
        '예약번호',
        '환자번호',
        '의료진번호',
        '예약날짜',
        '예약시간',
        '진단명',
        '비급여',
        '급여',
        '총금액',
        '상태'
    ]

    if file_exists:
        with open(
            file_path,
            'r',
            encoding='utf-8-sig',
            newline=''
        ) as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
    else:
        fieldnames = default_fieldnames

    if not fieldnames:
        fieldnames = default_fieldnames

    with open(
        file_path,
        'a',
        encoding='utf-8-sig',
        newline=''
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(new_reservation)

    print('\n========================= [예약 완료] =======================')
    print('예약이 아래와 같이 완료되었습니다.')
    print(f'발급된 예약번호: {new_reservation_id}')
    print('===========================================================')
    print()


'''============= 내 예약 관리 ============='''
def my_reservation(current_user):
    while True:
        my_reservation_menu()

        choice = input('메뉴를 선택하세요 > ').strip()

        if choice == '1':
            show_my_reservations(current_user)
            pause()

        elif choice == '2':
            modify_reservation(current_user)
            pause()

        elif choice == '3':
            cancel_my_reservation(current_user)
            pause()

        elif choice == '0':
            break

        else:
            print('올바른 메뉴 번호를 입력하세요.\n')

# 내 예약관리 메뉴 표출

def my_reservation_menu():
    clear_screen()
    print()

    lines = [
        '1. 예약 조회',
        '2. 예약 변경',
        '3. 예약 취소',
        '0. 이전 메뉴'
    ]

    print_box(lines, title='내 예약 관리')
    print()

# 내 예약 조회

def show_my_reservations(current_user):
    doctors = {}

    try:
        with open(
            DOCTOR_CSV,
            'r',
            encoding='utf-8-sig',
            newline=''
        ) as file:
            reader = csv.DictReader(file)

            for doctor in reader:
                doctors[doctor['의료진번호']] = doctor

    except FileNotFoundError:
        print(f'{DOCTOR_CSV} 파일을 찾을 수 없습니다.')
        return

    my_reservations = []

    try:
        with open(
            RESERVATION_CSV,
            'r',
            encoding='utf-8-sig',
            newline=''
        ) as file:
            reader = csv.DictReader(file)

            for reservation in reader:
                if (
                    reservation.get('환자번호', '').strip()
                    == current_user['환자번호'].strip()
                    and reservation.get('상태', '').strip()
                    == '예약완료'
                ):
                    my_reservations.append(reservation)

    except FileNotFoundError:
        print(f'{RESERVATION_CSV} 파일을 찾을 수 없습니다.')
        return

    if not my_reservations:
        print(f"\n{current_user['이름']}님의 예약완료 상태인 예약이 없습니다.")
        return

    my_reservations.sort(
        key=lambda x: x.get('예약번호', '')
    )

    table_data = []

    for index, reservation in enumerate(my_reservations, start=1):
        doctor = doctors.get(
            reservation.get('의료진번호', ''),
            {}
        )

        table_data.append([
            index,
            reservation.get('예약번호', '-'),
            doctor.get('진료과', '정보없음'),
            doctor.get('이름', '정보없음'),
            reservation.get('예약날짜', '-'),
            reservation.get('예약시간', '-'),
            reservation.get('상태', '-')
        ])

    table = tabulate(
        table_data,
        headers=[
            '번호',
            '예약번호',
            '진료과',
            '진료의',
            '예약날짜',
            '예약시간',
            '상태'
        ],
        tablefmt='grid',
        disable_numparse=True,
        colalign=(
            'center',
            'center',
            'center',
            'center',
            'center',
            'center',
            'center'
        )
    )

    first_line = table.splitlines()[0]
    table_width = safe_width(first_line)
    title = f"📋 [{current_user['이름']}]님의 예약 조회"

    print()
    print('=' * table_width)
    print(center_by_width(title, table_width))
    print('=' * table_width)
    print(table)
    print('=' * table_width)

def update_reservations_csv(reservations):
    default_fieldnames = [
        '예약번호',
        '환자번호',
        '의료진번호',
        '예약날짜',
        '예약시간',
        '진단명',
        '비급여',
        '급여',
        '총금액',
        '상태'
    ]

    if reservations:
        fieldnames = list(reservations[0].keys())
    else:
        fieldnames = default_fieldnames

    with open(
        RESERVATION_CSV,
        'w',
        encoding='utf-8-sig',
        newline=''
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )
        writer.writeheader()
        writer.writerows(reservations)

def modify_reservation(current_user):
    reservations = load_reservations()
    doctors = load_doctors()

    if doctors is None:
        return

    patient_id = current_user['환자번호']

    active_reservations = [
        record
        for record in reservations
        if (
            record.get('환자번호', '').strip()
            == patient_id.strip()
            and record.get('상태', '').strip()
            == '예약완료'
        )
    ]

    active_reservations.sort(
        key=lambda x: x.get('예약번호', '')
    )

    if not active_reservations:
        print("변경할 수 있는 예약 내역이 없습니다.")
        return

    doctor_dict = {
        doctor_info['의료진번호']: doctor_info
        for doctor_info in doctors
    }

    valid_active_reservations = []
    table_data = []

    for record in active_reservations:
        doctor_info = doctor_dict.get(
            record.get('의료진번호', '')
        )

        if doctor_info is None:
            continue

        valid_active_reservations.append(record)

        table_data.append([
            len(valid_active_reservations),
            record.get('예약번호', '-'),
            doctor_info.get('진료과', '정보없음'),
            doctor_info.get('이름', '정보없음'),
            record.get('예약날짜', '-'),
            record.get('예약시간', '-')
        ])

    if not table_data:
        print('\n표시할 수 있는 예약 내역이 없습니다.')
        return

    table = tabulate(
        table_data,
        headers=[
            '번호',
            '예약번호',
            '진료과',
            '의료진',
            '예약날짜',
            '예약시간'
        ],
        tablefmt='grid',
        disable_numparse=True,
        colalign=(
            'center',
            'center',
            'center',
            'center',
            'center',
            'center'
        )
    )

    first_line = table.splitlines()[0]
    table_width = safe_width(first_line)
    title = f"📝 [{current_user['이름']}]님의 예약 변경"

    print()
    print('=' * table_width)
    print(center_by_width(title, table_width))
    print('=' * table_width)
    print(table)
    print(center_by_width('0. 이전 메뉴', table_width))
    print('=' * table_width)

    while True:
        input_value = input(
            '\n변경할 예약 번호를 선택하세요: '
        ).strip()

        if input_value == '0':
            return

        if not input_value:
            print('오류: 공백 입력은 불가합니다.')
            continue

        if not input_value.isdigit():
            print('오류: 숫자로만 입력해주세요.')
            continue

        choice = int(input_value)

        if not 1 <= choice <= len(valid_active_reservations):
            print('오류: 범위를 벗어난 번호입니다.')
            continue

        target_reservation = valid_active_reservations[
            choice - 1
        ]
        break

    doctor = doctor_dict.get(
        target_reservation.get('의료진번호', '')
    )

    if doctor is None:
        print('해당 예약의 의료진 정보를 찾을 수 없습니다.')
        return

    print(
        f"\n[{doctor['진료과']} {doctor['이름']} 원장] "
        '예약 변경을 시작합니다.'
    )

    # 변경 대상인 자기 예약을 예약 가능 시간 검사에서 제외합니다.
    other_reservations = [
        reservation
        for reservation in reservations
        if (
            reservation.get('예약번호')
            != target_reservation.get('예약번호')
        )
    ]

    while True:
        new_date = select_date(
            doctor,
            other_reservations
        )

        if new_date is None:
            return

        new_time = select_time(
            doctor,
            new_date,
            other_reservations
        )

        if new_time is None:
            print(
                '\n시간 선택을 취소했습니다. '
                '다시 날짜를 선택해주세요.'
            )
            continue

        break

    if (
        new_date == target_reservation.get('예약날짜')
        and new_time == target_reservation.get('예약시간')
    ):
        print(
            '\n기존 예약과 동일한 날짜와 시간입니다. '
            '변경을 취소합니다.'
        )
        return

    print(
        '\n====================== '
        '[예약 변경 상세] ======================'
    )
    print(
        f"기존 예약: "
        f"{target_reservation.get('예약날짜')} "
        f"{target_reservation.get('예약시간')}"
    )
    print(f'변경 예약: {new_date} {new_time}')
    print(
        '==========================================================='
    )

    while True:
        confirm = input(
            '\n위 일정으로 예약을 변경하시겠습니까? '
            '(Y/N) > '
        ).strip().upper()

        if confirm == 'Y':
            old_reservation_id = target_reservation.get(
                '예약번호',
                ''
            )
            old_date = target_reservation.get(
                '예약날짜',
                ''
            )

            # 예약번호는 예약날짜를 앞부분으로 사용하므로,
            # 예약날짜가 변경되면 새 날짜에 맞춰 다시 생성합니다.
            if new_date != old_date:
                date_prefix = new_date.replace('-', '')
                max_sequence_number = 0

                for reservation in reservations:
                    # 현재 변경 중인 자기 예약은 순번 계산에서 제외합니다.
                    if reservation is target_reservation:
                        continue

                    reservation_id = reservation.get(
                        '예약번호',
                        ''
                    )

                    if not reservation_id.startswith(
                        f'{date_prefix}-'
                    ):
                        continue

                    try:
                        sequence_number = int(
                            reservation_id.split('-')[1]
                        )
                        max_sequence_number = max(
                            max_sequence_number,
                            sequence_number
                        )
                    except (IndexError, ValueError):
                        continue

                new_reservation_id = (
                    f'{date_prefix}-'
                    f'{max_sequence_number + 1:03d}'
                )
                target_reservation['예약번호'] = (
                    new_reservation_id
                )
            else:
                new_reservation_id = old_reservation_id

            target_reservation['예약날짜'] = new_date
            target_reservation['예약시간'] = new_time

            update_reservations_csv(reservations)

            print(
                '\n예약 변경이 정상적으로 완료되었습니다.'
            )

            if new_reservation_id != old_reservation_id:
                print(
                    f'예약번호도 날짜에 맞게 변경되었습니다: '
                    f'{old_reservation_id} → '
                    f'{new_reservation_id}'
                )

            print('이전 메뉴로 돌아갑니다.')
            return True

        if confirm == 'N':
            print(
                '\n예약 변경이 취소되었습니다. '
                '이전 메뉴로 돌아갑니다.'
            )
            return False

        print(
            '올바른 입력이 아닙니다. '
            'Y 또는 N을 입력해주세요.'
        )


# 내 예약 취소

def cancel_my_reservation(current_user):
    print('\n======== 예약 취소 ========')

    try:
        with open(
            RESERVATION_CSV,
            'r',
            encoding='utf-8-sig',
            newline=''
        ) as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            reservations = list(reader)

    except FileNotFoundError:
        print(f'{RESERVATION_CSV} 파일을 찾을 수 없습니다.')
        return

    if not fieldnames:
        print('예약 파일의 헤더를 확인할 수 없습니다.')
        return

    doctors = {}

    try:
        with open(
            DOCTOR_CSV,
            'r',
            encoding='utf-8-sig',
            newline=''
        ) as file:
            reader = csv.DictReader(file)

            for doctor in reader:
                doctors[doctor['의료진번호']] = doctor

    except FileNotFoundError:
        print(f'{DOCTOR_CSV} 파일을 찾을 수 없습니다.')
        return

    my_reservations = [
        reservation
        for reservation in reservations
        if (
            reservation.get('환자번호', '').strip()
            == current_user['환자번호'].strip()
            and reservation.get('상태', '').strip()
            == '예약완료'
        )
    ]

    my_reservations.sort(
        key=lambda x: x.get('예약번호', '')
    )

    if len(my_reservations) == 0:
        print("취소 가능한 예약이 없습니다.")
        return

    table_data = []

    for index, reservation in enumerate(
        my_reservations,
        start=1
    ):
        doctor = doctors.get(
            reservation.get('의료진번호', ''),
            {}
        )

        table_data.append([
            index,
            reservation.get('예약번호', '-'),
            doctor.get('진료과', '정보없음'),
            doctor.get('이름', '정보없음'),
            reservation.get('예약날짜', '-'),
            reservation.get('예약시간', '-'),
            reservation.get('상태', '-')
        ])

    table = tabulate(
        table_data,
        headers=[
            '번호',
            '예약번호',
            '진료과',
            '진료의',
            '예약날짜',
            '예약시간',
            '상태'
        ],
        tablefmt='grid',
        disable_numparse=True,
        colalign=(
            'center',
            'center',
            'center',
            'center',
            'center',
            'center',
            'center'
        )
    )

    first_line = table.splitlines()[0]
    table_width = safe_width(first_line)
    title = f"❌ [{current_user['이름']}]님의 예약 취소"

    print()
    print('=' * table_width)
    print(center_by_width(title, table_width))
    print('=' * table_width)
    print(table)
    print(center_by_width('0. 이전 메뉴', table_width))
    print('=' * table_width)

    while True:
        choice_value = input(
            '\n취소할 번호를 입력하세요: '
        ).strip()

        if choice_value == '0':
            return

        if not choice_value.isdigit():
            print('목록에 있는 숫자를 입력하세요.')
            continue

        choice = int(choice_value)

        if not 1 <= choice <= len(my_reservations):
            print('번호가 올바르지 않습니다.')
            continue

        target = my_reservations[choice - 1]
        break

    while True:
        confirm = input(
            f"예약번호 [{target['예약번호']}]을 "
            '정말 취소하시겠습니까? (Y/N) > '
        ).strip().upper()

        if confirm == 'N':
            print('예약 취소가 취소되었습니다.')
            return

        if confirm == 'Y':
            break

        print('Y 또는 N을 입력하세요.')

    for reservation in reservations:
        if (
            reservation.get('예약번호')
            == target.get('예약번호')
            and reservation.get('환자번호')
            == current_user.get('환자번호')
        ):
            reservation['상태'] = '예약취소'
            break

    with open(
        RESERVATION_CSV,
        'w',
        encoding='utf-8-sig',
        newline=''
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )
        writer.writeheader()
        writer.writerows(reservations)

    print('\n예약이 정상적으로 취소되었습니다.')