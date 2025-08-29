import random

def rock_paper_scissors():
    """가위바위보 게임 (콘솔 버전)"""
    choices = ["가위", "바위", "보"]
    computer_choice = random.choice(choices)

    print("가위, 바위, 보 중 하나를 고르세요!")
    player_choice = input("당신의 선택: ")

    print(f"컴퓨터의 선택: {computer_choice}")

    if player_choice == computer_choice:
        print("비겼습니다!")
    elif (player_choice == "가위" and computer_choice == "보") or \
         (player_choice == "바위" and computer_choice == "가위") or \
         (player_choice == "보" and computer_choice == "바위"):
        print("당신이 이겼습니다!")
    else:
        print("당신이 졌습니다!")
