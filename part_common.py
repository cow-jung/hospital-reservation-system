"""
part_common.py — 여러 모듈이 공통으로 사용하는 상수/유틸리티 함수 모음
(CSV 경로, 화면 지우기, 대기, 폭 계산, 박스 출력, rich 콘솔 객체)
"""
import os
from wcwidth import wcswidth
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()  # 매출/결제 관리 화면 등에서 공통으로 사용하는 rich 콘솔 객체
os.system("")  # cmd에서 색을 나타내기 위한 새로고침 기능

# ============================================================
# 공용 CSV 파일 경로
# ============================================================
USER_CSV = 'user_500_added.csv'                  # 회원(환자) 정보
RESERVATION_CSV = 'reservations_500_added.csv'    # 예약/진료 정보
DOCTOR_CSV = 'doctors.csv'                        # 의료진 정보


def clear_screen():
    # 화면을 지워서 이전 페이지/메뉴의 잔상이 남지 않도록 함
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    # 조회/처리 결과를 보여준 뒤, 사용자가 Enter를 눌러야 다음 화면(메뉴 재출력)으로 넘어가게 함
    input('\n계속하려면 Enter를 누르세요...')

# ============================================================
# 공용 CSV 파일 경로 (전역 변수)
# 모든 함수가 아래 3개의 변수를 공통으로 사용합니다.
# ============================================================
USER_CSV = 'user_500_added.csv'          # 회원(환자) 정보
RESERVATION_CSV = 'reservations_500_added.csv'  # 예약/진료 정보
DOCTOR_CSV = 'doctors.csv'               # 의료진 정보

def safe_width(text):
    width = 0
    for ch in text:
        w = wcswidth(ch)
        if w is None or w < 0:
            w = 2  # 이모지 등은 2칸으로 간주
        width += w
    return width

# safe_width 기준으로 가운데 정렬해주는 함수

def center_by_width(text, width):
    text_width = safe_width(text)
    total_padding = width - text_width
    left = total_padding // 2
    right = total_padding - left
    return ' ' * left + text + ' ' * right

# 내용 줄들의 실제 폭에 맞춰 상하 테두리 길이를 자동으로 맞춰주는 공용 출력 함수

def print_box(lines, title=None, border_char='='):
    content_width = max((safe_width(line) for line in lines), default=0)

    if title:
        content_width = max(content_width, safe_width(title))

    width = content_width + 4  # 좌우 여백

    print(border_char * width)

    if title:
        print(center_by_width(title, width))
        print(border_char * width)

    for line in lines:
        print(line)

    print(border_char * width)

# 선택한 진료과의 의료진 전체 출력
