import random

def check_answer(correct_answer):
    user = input()
    user_answer = int(user)
    
    if user_answer == correct_answer:
        print("correct")
    elif user_answer > correct_answer:
        print("too high")
    elif user_answer < correct_answer:
        print("too low")


rand = int(random.random() * 100 - 68)
check_answer(rand)