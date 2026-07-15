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
    with open('hospital_reservation_system/user.csv','r',encoding='utf-8-sig') as file:
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
    print('0. 이전 메뉴')
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

    # 3. 의료진 선택
    doctor = select_doctor(doctors, department) # select_doctor : 의료진을 선택하기 위한 함수
    if doctor is None:  # 의료진이 없어서 None이 반환되었다면
        return  # 함수를 즉시 종료하고 예약 메뉴로 돌아감

    # 4. 날짜 선택
    date_str = select_date(doctor, reservations) # select_date : 날짜를 선택하기 위한 함수
    if date_str is None:  # '취소'을 눌러서 None이 반환되었다면
        return  # 예약 메뉴로 돌아감

    # 5. 시간 선택
    time_str = select_time(doctor, date_str, reservations)

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
    history_records = [res for res in reservations if res['환자번호'] == patient_id and res['상태'] == '진료완료']

    # 3. 기록이 없을 경우 처리
    if not history_records:
        print("\n과거 진료 완료 기록이 없습니다. 예약 초기 메뉴로 돌아갑니다.")
        return

    # 의료진 번호로 의료진 정보를 쉽게 찾기 위해 딕셔너리 생성
    doctor_dict = {doc['의료진번호']: doc for doc in doctors}

    print(f"\n======== [{current_user['이름']}]님의 진료 이력 ========")

    # 출력 및 선택을 위해 리스트에 저장
    display_list = []
    for idx, record in enumerate(history_records, 1):
        doc_id = record['의료진번호']
        doctor_info = doctor_dict.get(doc_id)

        # 만약 의료진 정보가 있다면 내역에 추가
        if doctor_info:
            date = record['예약날짜']
            dept = doctor_info['진료과']
            doc_name = doctor_info['이름']

            display_list.append(doctor_info)  # 예약 진행을 위해 doctor_info만 저장
            print(f"{idx}. 진료과: {dept} / 의료진: {doc_name} / 진료 날짜: {date}")

    print("0. 이전 메뉴로 돌아가기")
    print("=====================================================")

    # 4. 예약할 항목 선택
    while True:
        try:
            val = input("\n다시 예약할 진료 항목의 번호를 선택하세요 > ").strip()

            if val == '0':
                return  # 이전 메뉴로 돌아가기

            if not val:
                raise ValueError("공백 입력은 불가합니다.")

            choice = int(val)
            if not (1 <= choice <= len(display_list)):
                raise ValueError("범위를 벗어난 번호입니다.")

            # 선택한 항목의 의료진 정보 추출
            selected_doctor = display_list[choice - 1]
            break

        except ValueError as e:
            if "invalid literal" in str(e):
                print("오류: 문자 입력은 불가합니다. 숫자로만 입력해주세요.")
            else:
                print(f"오류: {e}")

    # 5. 기존 방식과 동일하게 예약 진행 (선택한 의료진 정보 사용)
    print(f"\n[{selected_doctor['진료과']} {selected_doctor['이름']} 원장] 예약 단계로 넘어갑니다.")

    date_str = select_date(selected_doctor, reservations)
    time_str = select_time(selected_doctor, date_str, reservations)

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
            break
        elif confirm == 'N':
            print("\n진행 중인 예약이 취소되었습니다. 예약 초기 메뉴로 돌아갑니다.")
            return
        else:
            print("올바른 입력이 아닙니다. Y 또는 N을 입력해주세요.")

def load_doctors():
    """의료진 정보를 CSV에서 불러옵니다."""
    doctors = []
    try:
        with open('hospital_reservation_system/doctors.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                doctors.append(row)
    except FileNotFoundError:
        print(f"오류: {'hospital_reservation_system/doctors.csv'} 파일이 존재하지 않습니다.")
        return None
    return doctors

def load_reservations():
    """전체 예약 정보를 CSV에서 불러옵니다."""
    reservations = []
    try:
        with open('hospital_reservation_system/reservations_total_only.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                reservations.append(row)
    except FileNotFoundError:
        # 파일이 없으면 빈 리스트 반환 (나중에 새로 생성됨)
        pass
    return reservations

def select_department(doctors):
    """진료과를 선택합니다."""
    departments = sorted(list(set(doc['진료과'] for doc in doctors)))

    print("\n======== 진료과 선택 ========")
    for idx, dept in enumerate(departments, 1):
        print(f"{idx}. {dept}")

    while True:
        try:
            val = input("\n 진료과 번호를 선택하세요: ").strip()
            if not val:
                raise ValueError("공백 입력은 불가합니다.")
            choice = int(val)
            if not (1 <= choice <= len(departments)):
                raise ValueError("범위를 벗어난 번호입니다.")
            return departments[choice - 1]
        except ValueError as e:
            if "invalid literal" in str(e):
                print("오류: 문자 입력은 불가합니다. 숫자로만 입력해주세요.")
            else:
                print(f"오류: {e}")

def select_doctor(doctors, department):
    """선택한 진료과의 근무 중인 의료진을 선택합니다."""
    # 근무상태가 '진료중'인 해당 진료과 의사만 필터링
    available_doctors = [d for d in doctors if d['진료과'] == department and d['근무상태'] == '진료중']

    if not available_doctors:
        print("현재 해당 진료과에 예약 가능한 의료진이 없습니다.")
        return None

    print(f"\n==================== {department} 의료진 선택 ====================")
    for idx, doc in enumerate(available_doctors, 1):
        print(f"{idx}. {doc['이름']} (진료요일: {doc['진료요일']} / 진료시간: {doc['진료시작시간']} ~ {doc['진료종료시간']})")

    while True:
        try:
            val = input("\n 예약을 원하는 의료진 번호를 숫자로 입력하세요: ").strip()
            if not val:
                raise ValueError("공백 입력은 불가합니다.")
            choice = int(val)
            if not (1 <= choice <= len(available_doctors)):
                raise ValueError("범위를 벗어난 번호입니다.")
            return available_doctors[choice - 1]
        except ValueError as e:
            if "invalid literal" in str(e):
                print("오류: 문자 입력은 불가합니다. 숫자로만 입력해주세요.")
            else:
                print(f"오류: {e}")

def create_time_slots(start_time, end_time):
    """시작 시간부터 종료 시간까지 30분 단위의 시간 슬롯을 생성합니다."""
    slots = []
    start_h, start_m = map(int, start_time.split(':'))
    end_h, end_m = map(int, end_time.split(':'))

    curr_h, curr_m = start_h, start_m
    while curr_h < end_h or (curr_h == end_h and curr_m < end_m):
        slots.append(f"{curr_h:02d}:{curr_m:02d}")
        curr_m += 30
        if curr_m >= 60:
            curr_h += 1
            curr_m -= 60
    return slots

def get_available_times(doctor, date_str, reservations):
    """특정 날짜의 예약 가능한 시간 목록을 반환합니다."""
    # 주말(토, 일)은 예약 불가
    y, m, d = map(int, date_str.split('-'))
    target_date = datetime.date(y, m, d)
    if target_date.weekday() >= 5:  # 5: 토요일, 6: 일요일
        return []

    # 진료요일 확인
    # 파이썬의 weekday()는 0(월)~6(일)의 정수를 반환하므로 한글 요일과 매핑
    weekday_map = {0: '월', 1: '화', 2: '수', 3: '목', 4: '금', 5: '토', 6: '일'}
    target_weekday_str = weekday_map[target_date.weekday()]

    # doctors.csv의 '진료요일' 항목을 가져옴 (문자열 형태, 예: "월,수,금")
    # 혹시 csv에 '진료요일' 열이 누락되었을 때 에러를 막기 위해 기본값(월~금) 설정
    working_days = doctor.get('진료요일', '월,화,수,목,금')

    # 선택한 날짜의 요일이 해당 의사의 '진료요일'에 포함되어 있지 않다면 예약 불가
    if target_weekday_str not in working_days:
        return []

    # 과거 날짜 예약 불가
    if target_date < datetime.date.today():
        return []

    slots = create_time_slots(doctor['진료시작시간'], doctor['진료종료시간'])

    # 예약된 시간 제외 ('예약취소'는 다시 예약 가능하므로 제외하지 않음)
    for res in reservations:
        if res['의료진번호'] == doctor['의료진번호'] and res['예약날짜'] == date_str:
            if res['상태'] in ['예약완료', '진료완료']:
                if res['예약시간'] in slots:
                    slots.remove(res['예약시간'])

    return slots

def print_calendar(year, month, doctor, reservations):
    """해당 월의 달력을 출력하고 예약 마감 날짜를 표시합니다."""
    cal = calendar.monthcalendar(year, month)
    print(f"\n======== {year}년 {month}월 예약 달력 ========")
    print("월    화    수    목   금")

    fully_booked_dates = []

    for week in cal:
        week_str = ""
        # week[:5]를 사용하여 월요일(0)부터 금요일(4)까지만 반복
        for i, day in enumerate(week[:5]):
            if day == 0:
                week_str += "     "
            else:
                date_str = f"{year}-{month:02d}-{day:02d}"
                avail_times = get_available_times(doctor, date_str, reservations)

                # 예약 가능한 시간이 없으면 [17] 형태로 출력
                if len(avail_times) == 0:
                    week_str += f"[{day:2d}] "
                    fully_booked_dates.append(date_str)
                else:
                    week_str += f" {day:2d}  "

        # 3. 만약 해당 주(week)의 평일이 모두 0(공백)이라서 빈 줄이 되면 출력하지 않음
        # (예: 1일이 토요일로 시작하는 달의 첫째 주는 평일이 아예 없음)
        if week_str.strip():
            print(week_str)

    print("\n * [ ]: 예약 불가능한 날짜")
    print(f"===================================")

def select_date(doctor, reservations):
    """예약할 날짜를 달력에서 선택합니다."""
    now = datetime.date.today()
    current_year = now.year
    current_month = now.month

    while True:
        print_calendar(current_year, current_month, doctor, reservations)

        print()
        print("(이전달: 이전 /  다음달: 다음  /  취소: 취소) >> 해당 메뉴 이용 시 아래에 입력")
        print()

        try:
            val = input("예약할 날짜(일)를 숫자로 입력하세요: ").strip()

            if val.lower() == '취소':
                print("예약을 취소하고 이전 메뉴로 돌아갑니다.")
                return None
            elif val.lower() == '다음':
                current_month += 1
                if current_month > 12:
                    current_year += 1
                    current_month = 1
                continue
            elif val.lower() == '이전':
                current_month -= 1
                if current_month < 1:
                    current_year -= 1
                    current_month = 12
                continue

            if not val:
                raise ValueError("공백 입력은 불가합니다.")

            day = int(val)
            last_day = calendar.monthrange(current_year, current_month)[1]

            if not (1 <= day <= last_day):
                raise ValueError("존재하지 않는 날짜입니다.")

            date_str = f"{current_year}-{current_month:02d}-{day:02d}"

            # 예약 가능 여부 확인
            avail_times = get_available_times(doctor, date_str, reservations)
            if not avail_times:
                raise ValueError("해당 날짜는 예약 가능한 시간이 없습니다(주말, 과거 날짜, 또는 마감).")

            return date_str

        except ValueError as e:
            if "invalid literal" in str(e):
                print("오류: 문자 입력이 감지되었습니다. 숫자로만 입력해주세요.")
            else:
                print(f"오류: {e}")

def select_time(doctor, date_str, reservations):
    """해당 날짜에 예약 가능한 시간대를 선택합니다."""
    avail_times = get_available_times(doctor, date_str, reservations)

    print(f"\n=========== {date_str} 예약 가능 시간 ===========")
    for idx, t in enumerate(avail_times, 1):
        print(f"{idx}. {t}")

    while True:
        try:
            val = input("\n 예약을 원하는 시간의 번호를 숫자로 입력하세요: ").strip()
            if not val:
                raise ValueError("공백 입력은 불가합니다.")
            choice = int(val)
            if not (1 <= choice <= len(avail_times)):
                raise ValueError("잘못된 시간 선택(범위를 벗어난 번호)입니다.")
            return avail_times[choice - 1]
        except ValueError as e:
            if "invalid literal" in str(e):
                print("오류: 문자 입력이 감지되었습니다. 숫자로만 입력해주세요.")
            else:
                print(f"오류: {e}")

def save_reservation(patient_id, doctor, date_str, time_str, reservations):
    """예약을 완료하고 예약번호를 생성하여 CSV에 저장합니다."""
    # 1. 예약번호 생성 (YYYYMMDD-순번)
    date_prefix = date_str.replace("-", "")
    max_seq = 0
    total_fare = 0

    # 같은 날짜의 예약들을 찾아 최대 순번 구하기
    for res in reservations:
        if res.get('예약날짜') == date_str:
            res_id = res.get('예약번호', '')
            if res_id.startswith(date_prefix):
                try:
                    seq = int(res_id.split("-")[1])
                    if seq > max_seq:
                        max_seq = seq
                except (IndexError, ValueError):
                    pass

    new_res_id = f"{date_prefix}-{max_seq + 1:03d}"

    # 2. 저장할 새로운 예약 딕셔너리 구성
    new_reservation = {
        '예약번호': new_res_id,
        '환자번호': patient_id,
        '의료진번호': doctor['의료진번호'],
        '예약날짜': date_str,
        '예약시간': time_str,
        '총금액': total_fare,
        '상태': '예약완료'
    }

    fieldnames = ['예약번호', '환자번호', '의료진번호', '예약날짜', '예약시간', '총금액', '상태']

    # 3. 파일 존재 여부 확인 및 저장
    file_exists = os.path.isfile('hospital_reservation_system/reservations_total_only.csv')

    with open('hospital_reservation_system/reservations_total_only.csv', 'a', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(new_reservation)

    print(f"\n ======== [예약 완료] ========")
    print(f"예약이 아래와 같이 완료되었습니다.")
    print(f"발급된 예약번호: {new_res_id}")
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