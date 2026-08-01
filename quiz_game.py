"""quiz_game.py

게임 전체를 관리하는 QuizGame 클래스와, 입력을 안전하게 받는 도우미 함수들을 정의한다.

- Quiz 클래스가 '문제 한 개'를 담당한다면,
  QuizGame 클래스는 '게임 전체'(메뉴, 퀴즈 목록, 점수, 파일 저장/불러오기)를 담당한다.
- 이렇게 역할을 나누면 각 클래스가 무슨 일을 하는지 한눈에 설명할 수 있다.
"""

import os
import json

from quiz import Quiz

# state.json 은 '이 파일이 있는 폴더(=프로젝트 루트)'에 저장한다.
# 어느 위치에서 실행하든 항상 같은 곳을 가리키도록 절대 경로로 계산한다.
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")


# ---------------------------------------------------------------------------
# 입력 도우미 함수 (공통 입력/예외 처리 기준을 한 곳에 모아 재사용한다)
# ---------------------------------------------------------------------------
def read_int(prompt, min_value, max_value):
    """min_value~max_value 범위의 정수를 올바르게 입력할 때까지 반복해서 받는다.

    처리하는 경우:
      - 앞뒤 공백 제거 후 판단한다.
      - 빈 입력(그냥 Enter) → 안내 후 재입력
      - 숫자가 아닌 입력(abc 등) → 안내 후 재입력
      - 허용 범위 밖 숫자 → 안내 후 재입력
    (Ctrl+C / EOF 는 여기서 잡지 않고 main.py 로 올려보내 안전하게 종료시킨다.)
    """
    while True:
        raw = input(prompt).strip()
        if raw == "":
            print("⚠️  입력이 비어 있습니다. 다시 입력하세요.")
            continue
        try:
            value = int(raw)
        except ValueError:
            print("⚠️  숫자만 입력할 수 있습니다. 다시 입력하세요.")
            continue
        if value < min_value or value > max_value:
            print(f"⚠️  {min_value}~{max_value} 사이의 숫자를 입력하세요.")
            continue
        return value


def read_text(prompt):
    """비어 있지 않은 문자열을 입력할 때까지 반복해서 받는다."""
    while True:
        text = input(prompt).strip()
        if text == "":
            print("⚠️  내용을 입력하세요.")
            continue
        return text


class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스.

    속성:
        quizzes (list): Quiz 객체들의 목록
        best_score (int): 최고 점수 (0~100)
        best_detail (dict): 최고 점수를 기록했을 때의 (정답 수/전체 문제 수)
    """

    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.best_detail = {"correct": 0, "total": 0}

    # -------------------------------------------------------------------
    # 파일 저장 / 불러오기 (state.json)
    # -------------------------------------------------------------------
    def default_quizzes(self):
        """파일이 없거나 손상됐을 때 사용할 기본 퀴즈(파이썬/프로그래밍 주제)."""
        return [
            Quiz("Python에서 리스트를 만들 때 사용하는 괄호는?",
                 ["( )", "[ ]", "{ }", "< >"], 2, "대괄호입니다."),
            Quiz("다음 중 정수를 나타내는 자료형은?",
                 ["str", "int", "bool", "list"], 2, "integer의 줄임말."),
            Quiz("Python에서 한 줄 주석을 작성할 때 쓰는 기호는?",
                 ["//", "#", "--", "/* */"], 2, "샵(#) 기호."),
            Quiz("리스트의 요소 개수를 구하는 내장 함수는?",
                 ["size()", "count()", "len()", "length()"], 3, "length 의 줄임말."),
            Quiz("화면에 값을 출력할 때 사용하는 기본 함수는?",
                 ["echo()", "printf()", "print()", "console.log()"], 3, "가장 기본적인 출력 함수."),
            Quiz("참(True)/거짓(False) 두 값만 갖는 자료형은?",
                 ["int", "float", "bool", "str"], 3, "boolean 을 줄인 이름."),
            Quiz("문자열 \"10\" 을 정수 10 으로 바꾸는 함수는?",
                 ["str()", "int()", "float()", "input()"], 2, "정수 = integer."),
        ]

    def load_state(self):
        """state.json 에서 데이터를 불러온다.

        - 파일이 없으면(첫 실행) 기본 퀴즈로 시작한다.
        - 파일이 손상됐거나 읽기 오류가 나면 안내 후 기본 퀴즈로 복구한다.
        """
        if not os.path.exists(STATE_FILE):
            self.quizzes = self.default_quizzes()
            print("ℹ️  저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            # 딕셔너리 목록을 Quiz 객체 목록으로 되돌린다.
            self.quizzes = [Quiz.from_dict(item) for item in data.get("quizzes", [])]
            self.best_score = data.get("best_score", 0)
            self.best_detail = data.get("best_detail", {"correct": 0, "total": 0})
            # 파일은 있었지만 내용이 비었으면 기본 퀴즈로 채운다.
            if not self.quizzes:
                self.quizzes = self.default_quizzes()
            print(f"📂 저장된 데이터를 불러왔습니다. "
                  f"(퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")
        except (json.JSONDecodeError, OSError, KeyError, TypeError):
            # 손상/오류 시 프로그램이 죽지 않도록 기본 퀴즈로 복구한다.
            print("⚠️  데이터 파일을 읽을 수 없어 기본 퀴즈로 복구합니다.")
            self.quizzes = self.default_quizzes()
            self.best_score = 0
            self.best_detail = {"correct": 0, "total": 0}

    def save_state(self):
        """현재 퀴즈와 점수를 state.json 에 UTF-8 로 저장한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_detail": self.best_detail,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                # ensure_ascii=False 로 한글이 깨지지 않게 저장한다.
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError:
            print("⚠️  데이터를 저장하지 못했습니다.")

    # -------------------------------------------------------------------
    # 메뉴
    # -------------------------------------------------------------------
    def show_menu(self):
        """메뉴를 출력하고, 사용자가 고른 번호(1~5)를 돌려준다."""
        print("\n" + "=" * 40)
        print("           🎯 나만의 퀴즈 게임 🎯")
        print("=" * 40)
        print("  1. 퀴즈 추가")
        print("  2. 퀴즈 목록")
        print("  3. 점수 확인")
        print("  4. 퀴즈 삭제")
        print("  5. 종료")
        print("=" * 40)
        return read_int("선택: ", 1, 5)

    # -------------------------------------------------------------------
    # 퀴즈 추가
    # -------------------------------------------------------------------
    def add_quiz(self):
        """사용자에게 문제/선택지/정답을 입력받아 새 퀴즈를 등록한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = read_text("문제를 입력하세요: ")
        choices = []
        for i in range(1, 5):
            choices.append(read_text(f"선택지 {i}: "))
        answer = read_int("정답 번호 (1-4): ", 1, 4)
        hint = input("힌트 (없으면 그냥 Enter): ").strip()  # 힌트는 선택 사항

        self.quizzes.append(Quiz(question, choices, answer, hint))
        self.save_state()
        print("✅ 퀴즈가 추가되었습니다!")

    # -------------------------------------------------------------------
    # 퀴즈 목록
    # -------------------------------------------------------------------
    def list_quizzes(self):
        """등록된 모든 퀴즈의 문제를 번호와 함께 보여준다."""
        if not self.quizzes:
            print("\n📭 등록된 퀴즈가 없습니다.")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40)

    # -------------------------------------------------------------------
    # 점수 확인
    # -------------------------------------------------------------------
    def show_score(self):
        """최고 점수를 보여준다."""
        if self.best_score == 0:
            print("\n🙅 아직 퀴즈를 푼 기록이 없습니다.")
            return

        detail = self.best_detail
        print(f"\n🏆 최고 점수: {self.best_score}점 "
              f"({detail['total']}문제 중 {detail['correct']}문제 정답)")

    # -------------------------------------------------------------------
    # 퀴즈 삭제
    # -------------------------------------------------------------------
    def delete_quiz(self):
        """목록에서 번호를 골라 퀴즈를 삭제한다."""
        if not self.quizzes:
            print("\n📭 삭제할 퀴즈가 없습니다.")
            return
        self.list_quizzes()
        number = read_int("삭제할 퀴즈 번호: ", 1, len(self.quizzes))
        removed = self.quizzes.pop(number - 1)  # 목록은 1번부터, 인덱스는 0부터
        self.save_state()
        print(f"🗑️  삭제했습니다: {removed.question}")

    # -------------------------------------------------------------------
    # 메인 루프
    # -------------------------------------------------------------------
    def run(self):
        """메뉴를 반복해서 보여주며 선택에 따라 기능을 실행한다."""
        while True:
            choice = self.show_menu()
            if choice == 1:
                self.add_quiz()
            elif choice == 2:
                self.list_quizzes()
            elif choice == 3:
                self.show_score()
            elif choice == 4:
                self.delete_quiz()
            elif choice == 5:
                self.save_state()
                print("\n👋 게임을 종료합니다. 안녕히 가세요!")
                break
