import random

def generate_number():
    """3자리 랜덤 숫자 생성"""
    digits = random.sample(range(0, 10), 3)
    return ''.join(map(str, digits))

def check_guess(secret, guess):
    """스트라이크와 볼 계산"""
    strikes = sum(1 for i in range(3) if secret[i] == guess[i])
    balls = sum(1 for i in range(3) if secret[i] != guess[i] and guess[i] in secret)
    return strikes, balls

def number_baseball():
    """숫자야구 3자리 게임"""
    secret_number = generate_number()
    attempts = 0

    print("숫자 야구 게임을 시작합니다! 3자리 숫자를 맞춰보세요.")

    while True:
        guess = input("숫자를 입력하세요: ")
        if len(guess) != 3 or not guess.isdigit():
            print("3자리 숫자를 입력해주세요.")
            continue

        attempts += 1
        strikes, balls = check_guess(secret_number, guess)

        print(f"{strikes} 스트라이크, {balls} 볼")

        if strikes == 3:
            print(f"정답입니다! {attempts}번 만에 맞추셨습니다.")
            break
