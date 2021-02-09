import random

possible_choices = ["!exit", "!rating"]

default_game = ["rock", "paper", "scissors"]

d = {}
with open("rating.txt") as f:
    for line in f:
        (key, val) = line.split()
        d[key] = int(val)


def create_user(s):
    if s not in d:
        d[s] = int(0)


def add_score(score):
    d[user_name] += score


def determine_winner(game_list, first, second):
    index_to = game_list.index(first)
    index_from = index_to + 1
    elements_after = game_list[index_from:]
    elements_before = game_list[:index_to]
    elements = elements_after + elements_before

    half = len(elements) // 2
    beating_to_option = elements[:half]
    return second not in beating_to_option


def parse_game(s):
    return s.split(",")


game_to_play = []
user_name = input("Enter your name:")
create_user(user_name)
print(f"Hello, {user_name}")
user_input = input()
if not user_input:
    game_to_play = default_game
else:
    game_to_play = parse_game(user_input)
print("Okay, let's start")
possible_choices.extend(game_to_play)


while True:

    computer_choice = random.choice(game_to_play)
    user_input = input()
    if user_input not in possible_choices:
        print("Invalid input")
        continue
    if user_input == "!exit":
        print("Bye!")
        break
    elif user_input == "!rating":
        print(f"Your rating: {d[user_name]}")
    elif user_input == computer_choice:
        print(f"There is a draw ({user_input})")
        add_score(50)
    elif determine_winner(game_to_play, user_input, computer_choice):
        print(f"Well done. The computer chose {computer_choice} and failed")
        add_score(100)
    else:
        print(f"Sorry, but the computer chose {computer_choice}")

open("rating.txt", "w").close()

with open('rating.txt', 'w') as data:
    for key, value in d.items():
        data.write(f"{key} {value}\n")
