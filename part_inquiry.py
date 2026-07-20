"""
part_inquiry.py — 일반 회원의 조회 담당 (진료과/의료진 조회, 진료 이력 조회)
                  + 사용자 메뉴 전체 흐름(user_view)
"""
import csv

from tabulate import tabulate
from rich.table import Table
from rich.panel import Panel
from rich import box

from part_common import (
    DOCTOR_CSV, RESERVATION_CSV,
    clear_screen, pause, print_box, safe_width, center_by_width, console,
)
from part_reservation import reservation, my_reservation
from part_auth import logout


'''============= 사용자 메뉴 ============='''
def user_view(current_user):
    while True:
        user_menu(current_user)
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
            current_user = logout(current_user)
            return current_user

        else:
            print('올바른 메뉴 번호를 입력하세요.\n')

def user_menu(current_user): # 사용자 로그인 시 메뉴
    clear_screen()
    print()
    lines = [
        f"현재 사용자 : {current_user['이름']} / {current_user['환자번호']}",
        '1. 진료과 조회',
        '2. 예약하기',
        '3. 내 예약 관리',
        '4. 진료 이력 조회',
        '5. 로그아웃'
    ]
    print_box(lines, title='병원 예약 관리')
    print()


'''============= 진료과/의료진 조회 ============='''
def department_doctor_view():
    while True:
        show_departments()
        choice = input('진료과를 선택하세요 > ')

        if choice == '1':
            show_doctors_by_department('내과')
            pause()

        elif choice == '2':
            show_doctors_by_department('외과')
            pause()

        elif choice == '3':
            show_doctors_by_department('정형외과')
            pause()

        elif choice == '4':
            show_doctors_by_department('소아청소년과')
            pause()

        elif choice == '5':
            show_doctors_by_department('피부과')
            pause()

        elif choice == '0':
            break

        else:
            print('올바른 메뉴 번호를 입력하세요.\n')

# 진료과 전체 목록 출력

def show_departments():
    clear_screen()
    lines = [
        '1. 내과',
        '2. 외과',
        '3. 정형외과',
        '4. 소아과',
        '5. 피부과',
        '0. 이전'
    ]
    print_box(lines, title='진료과')

# wcswidth가 폭을 모르는 문자(이모지 등)도 안전하게 처리하는 폭 계산 함수

def show_doctors_by_department(department):
    doctor_list = []
    phone_number = ''

    with open(DOCTOR_CSV, 'r', encoding='utf-8-sig',newline='') as file:
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
        table_width = safe_width(first_line)
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


'''============= 진료 이력 조회 ============='''
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
    clear_screen()
    print()
    lines = [
        '1. 전체 진료 이력 조회',
        #'2. 진료 이력 상세 조회',
        #'3. 진료비 확인',
        '0. 이전 메뉴'
    ]
    print_box(lines, title='진료 이력 조회')
    print()

# 전체 진료 이력 조회

def show_medical_history(current_user):
    # 로그인한 사용자의 환자번호 확인
    # 해당 환자의 진료 이력 전체 조회
    # 진료일자 / 진료과 / 의료진 / 진료상태 출력

    # 상세 조회에 사용할 원본 딕셔너리 목록
    medical_history_data = []

    with open(RESERVATION_CSV, 'r', encoding='utf-8-sig',newline='') as file:
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

    if not medical_history_data:
        console.print('\n[bold red]진료 이력이 없습니다.[/bold red]\n')
        return

    # 최근 진료일 순으로 정렬
    medical_history_data.sort(key=lambda h: (h['진료날짜'], h['진료시간']), reverse=True)

    while True:
        clear_screen()

        history_table = Table(
            title='🩺 전체 진료 이력',
            box=box.ROUNDED,
            header_style='bold white',
            border_style='bright_white',
            show_lines=True,
            expand=False
        )

        history_table.add_column('번호', justify='center', style='cyan', no_wrap=True)
        history_table.add_column('진료날짜', justify='center', no_wrap=True)
        history_table.add_column('진료 정보', justify='center')
        history_table.add_column('진단명', justify='center')
        history_table.add_column('총금액', justify='right', style='bold magenta', no_wrap=True)

        for index, history in enumerate(medical_history_data, start=1):
            medical_text = (
                f"[bold]{history['진료과']}[/bold]\n"
                f"[dim]{history['의료진']}[/dim]"
            )

            history_table.add_row(
                str(index),
                f"{history['진료날짜']}\n{history['진료시간']}",
                medical_text,
                history['진단명'],
                f"{int(history['총금액']):,}원"
            )

        console.print()
        console.print(history_table)
        console.print()

        history_menu = input('조회할 번호를 입력하세요 (0. 이전) : ').strip()

        if history_menu == '0':
            return

        # 빈 값 또는 숫자가 아닌 값 검사
        if not history_menu.isdigit():
            console.print('[bold red]목록에 있는 숫자를 입력하세요.[/bold red]\n')
            pause()
            continue

        history_index = int(history_menu) - 1

        if not 0 <= history_index < len(medical_history_data):
            console.print('[bold red]목록에 있는 번호를 입력하세요.[/bold red]\n')
            pause()
            continue

        show_medical_history_detail_view(medical_history_data[history_index])
        pause()

# 진료 이력 상세를 카드 형태로 예쁘게 보여주는 함수

def show_medical_history_detail_view(selected_history):
    insured_fee = int(selected_history['급여'])
    uninsured_fee = int(selected_history['비급여'])
    total_fee = int(selected_history['총금액'])

    detail_table = Table.grid(padding=(0, 2))
    detail_table.add_column(justify='left', style='bold')
    detail_table.add_column(justify='left')

    detail_table.add_row('📅 진료일자', f"{selected_history['진료날짜']}  {selected_history['진료시간']}")
    detail_table.add_row('🏥 진료과', selected_history['진료과'])
    detail_table.add_row('🩺 의료진', selected_history['의료진'])
    detail_table.add_row('📋 진단명', selected_history['진단명'] or '-')
    detail_table.add_row('✅ 진료상태', f"[bold cyan]{selected_history['상태']}[/bold cyan]")
    detail_table.add_row('', '')
    detail_table.add_row('급여', f"[green]{insured_fee:,}원[/green]")
    detail_table.add_row('비급여', f"[yellow]{uninsured_fee:,}원[/yellow]")
    detail_table.add_row('총금액', f"[bold magenta]{total_fee:,}원[/bold magenta]")

    console.print()
    console.print(
        Panel(
            detail_table,
            title=f"[bold cyan]진료 이력 상세 (예약번호 {selected_history['예약번호']})[/bold cyan]",
            border_style='cyan',
            box=box.ROUNDED,
            expand=False
        )
    )

# 의료진 찾기

def find_doctor_by_number(doctor_number):
    with open(DOCTOR_CSV, 'r', encoding='utf-8-sig',newline='') as file:
        reader = csv.DictReader(file)

        for doctor in reader:
            if doctor['의료진번호'] == doctor_number:
                return doctor
    return None

# 진료 이력 상세 조회