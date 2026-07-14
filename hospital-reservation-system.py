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

# 입력한 아이디/비밀번호가 일치하는 사용자 찾기
def find_user(user_id, password):
    with open('hospital_reservation_system/user.csv','r',encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for user in reader:
            if user['아이디'] == user_id and user['비밀번호'] == password:
                return user
    # 일치하는 사용자가 없으면 None 반환
    return None

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
    print(current_user['이름'], '님의 예약을 조회합니다.')
    print()

# 내 예약 변경
def update_my_reservation(current_user):
    print('\n======== 예약 변경 ========')
    print(current_user['이름'], '님의 예약을 변경합니다.')
    print()

# 내 예약 취소
def cancel_my_reservation(current_user):
    print('\n======== 예약 취소 ========')
    print(current_user['이름'], '님의 예약을 취소합니다.')
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
    print('\n======== 전체 진료 이력 ========')

    # 로그인한 사용자의 환자번호 확인
    # 해당 환자의 진료 이력 전체 조회
    # 진료일자 / 진료과 / 의료진 / 진료상태 출력

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

def show_all_reservations():
    print('\n======== 전체 예약 조회 ========')

    with open('reservations_total_only.csv', 'r', encoding="utf-8", newline="") as file:
        reader = csv.reader(file)

    # reservation.csv 전체 예약 조회


def search_reservation_by_patient():
    print('\n======== 환자별 예약 조회 ========')

    # 환자번호 또는 이름 입력
    # 해당 환자의 예약 조회


def update_reservation():
    print('\n======== 예약 수정 ========')

    # 수정할 예약 검색
    # 예약 날짜 또는 시간 변경
    # reservation.csv 저장


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
            user_menu(current_user)




