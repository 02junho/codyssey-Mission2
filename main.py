"""main.py

프로그램의 시작점(진입점).
`python main.py` 로 실행하면 이 파일이 가장 먼저 동작한다.

여기서는 게임 객체를 만들고 실행하는 일만 담당하고,
실제 기능은 QuizGame 클래스가 처리한다. (역할 분리)
"""

from quiz_game import QuizGame


def main():
    game = QuizGame()
    game.load_state()  # 저장된 데이터 불러오기 (없으면 기본 퀴즈)

    try:
        game.run()  # 메뉴 반복 실행
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C 를 누르거나 입력이 갑자기 끊겨도 프로그램이 비정상 종료되지 않게 한다.
        # 안내를 출력하고, 지금까지의 데이터를 저장한 뒤 안전하게 끝낸다.
        print("\n\n🛑 입력이 중단되어 안전하게 종료합니다. (데이터 저장 완료)")
        game.save_state()


if __name__ == "__main__":
    # 이 파일을 직접 실행할 때만 main() 이 동작한다.
    # (다른 파일에서 import 될 때는 실행되지 않는다.)
    main()
