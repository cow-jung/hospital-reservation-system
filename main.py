"""
main.py — 병원 예약 관리 시스템 최종 통합 실행 파일

역할별 모듈 구성:
  part_common.py      : 공용 상수, clear_screen/pause/print_box 등 유틸
  part_auth.py         : 로그인 / 회원가입
  part_reservation.py  : 예약(신규) / 내 예약 조회·변경·취소
  part_inquiry.py      : 진료과·의료진 조회 / 진료 이력 조회 / 사용자 메뉴
  part_admin.py        : 관리자 메뉴(회원/예약/진료과/진료비 관리)
"""

from part_auth import show_login_menu, login, signup
from part_inquiry import user_view
from part_admin import admin_manage

current_user = None  # 현재 로그인한 사용자 정보를 저장

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