"""quiz.py

개별 퀴즈 한 문제를 표현하는 Quiz 클래스를 정의한다.
'문제 하나'라는 개념을 객체로 묶어두면, 문제/선택지/정답을 따로따로 관리하지 않고
하나의 덩어리로 다룰 수 있어 코드가 훨씬 이해하기 쉬워진다.
"""


class Quiz:
    """퀴즈 한 문제를 담는 클래스.

    속성(attribute):
        question (str): 문제 내용
        choices (list): 선택지 4개
        answer (int): 정답 번호 (1~4)
        hint (str): 힌트 (보너스 기능, 없으면 빈 문자열)
    """

    def __init__(self, question, choices, answer, hint=""):
        # __init__ 은 객체가 만들어질 때 자동으로 불리며,
        # self(자기 자신)에 전달받은 값을 속성으로 저장한다.
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def show(self, number):
        """문제 번호와 함께 문제/선택지를 화면에 출력한다."""
        print(f"\n[문제 {number}]")
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            # enumerate(..., start=1) 로 1번부터 번호를 매겨 출력한다.
            print(f"  {index}. {choice}")

    def is_correct(self, user_choice):
        """사용자가 고른 번호가 정답과 같은지 True/False 로 돌려준다."""
        return user_choice == self.answer

    def to_dict(self):
        """객체를 JSON에 저장할 수 있는 딕셔너리 형태로 바꾼다.

        JSON은 Quiz 같은 파이썬 객체를 그대로 저장하지 못하므로,
        저장 직전에 dict(문자열/숫자/리스트)로 변환해 둔다.
        """
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data):
        """JSON에서 읽어온 딕셔너리를 다시 Quiz 객체로 되돌린다.

        classmethod 라서 cls(=Quiz) 를 통해 새 객체를 만들어 돌려준다.
        예전 저장 파일에 hint 키가 없을 수도 있으므로 get 으로 안전하게 읽는다.
        """
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
            hint=data.get("hint", ""),
        )
