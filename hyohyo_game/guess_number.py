import random

def guess_the_number():
    """숫자 업앤다운 게임"""
    number_to_guess = random.randint(1, 100)
    attempts = 0

    print("1부터 100 사이의 숫자를 맞춰보세요!")

    while True:
        player_guess = int(input("숫자를 입력하세요: "))
        attempts += 1

        if player_guess < number_to_guess:
            print("더 큰 숫자입니다.")
        elif player_guess > number_to_guess:
            print("더 작은 숫자입니다.")
        else:
            print(f"정답입니다! {attempts}번 만에 맞추셨습니다.")
            break
