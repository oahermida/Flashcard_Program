import json
from pathlib import Path
import datetime
import uuid
import random

def load_deck(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "name": "Python Knowledge",
            "created": datetime.date.today().isoformat(),
            "cards": []
        }


def save_deck(path, deck):
    with open(path, 'w') as f:
        json.dump(deck, f, indent=4)

def create_card():
    front = input("What should be on the front of the card?\n")
    back = input("What should be on the back of the card?\n")
    card = {
        "id": str(uuid.uuid4())[:8],
        "front": front,       
        "back": back,        
        "created": datetime.date.today().isoformat(),     
        "seen": 0,
        "correct": 0,
        "last_seen": None
    }
    return card

def view_cards(deck):
    if not deck["cards"]:
        print("No cards yet")
        return
    
    print("the cards") #placeholder
    for i, card in enumerate(deck["cards"], start=1): #this function is still a bit unclear to me
        print(i, card["front"], card["back"])

def get_valid_input(prompt, min_val, max_val):
    while True:
        try:
          user_input = int(input(prompt))
          if user_input >= min_val and user_input <= max_val:
              return user_input
          else:
              print(f"Out of range! Please choose a number between {min_val} and {max_val}")
        except ValueError:
            print(f"Invalid input! Please enter a number between {min_val} and {max_val}")


def main():
    BASE_DIR = Path(__file__).parent
    path = BASE_DIR / "data" / "python_knowledge.json"
    deck = load_deck(path)

    while True:
        choice = get_valid_input("1. Add a card\n2. View all cards\n3. Quiz me\n4. View stats\n5. Review weak cards\n6. Quit\n", 1, 6)
        if choice == 1:
            deck["cards"].append(create_card())
            save_deck(path, deck)
        elif choice == 2:
            view_cards(deck)
        elif choice == 3:
            quiz_loop(deck, path)
        elif choice == 4:
            view_stats(deck)
        elif choice == 5:
            review_weak(deck, path)
        elif choice == 6:
            break

def quiz_loop(deck, path):
    random.shuffle(deck["cards"])
    session_correct = 0
    session_total = 0
    for card in deck["cards"]:
        print(card["front"])
        input("Press ENTER to flip...")
        print(card["back"])
        choice = get_valid_input("Did you get it right?\n1. Yes\n2. No\n", 1, 2)
        card["last_seen"] = datetime.date.today().isoformat()
        card["seen"] += 1
        session_total += 1
        if choice == 1:
            session_correct += 1
            card["correct"] += 1
    print(f"You got {session_correct}/{session_total} correct.")
    save_deck(path, deck)

def get_accuracy(card):
    if card["seen"] > 0:
        accuracy = card["correct"] / card["seen"]
        return accuracy
    else:
        return 0

def view_stats(deck):
    if not deck["cards"]:
        print("The deck is empty.")
        return
    sorted_cards = sorted(deck["cards"], key=get_accuracy) #no clue how this works
    for nr, card in enumerate(sorted_cards, start=1):
        print(f"{nr}    {round(get_accuracy(card) * 100)}%   {card["front"]}")

def review_weak(deck, path):
    laccu_cards = []
    for card in deck["cards"]:
        if get_accuracy(card) < 0.6 and card["seen"] > 0:
            laccu_cards.append(card)
    if not laccu_cards:
        print("No weak cards, great job!")
        return
    
    random.shuffle(laccu_cards)
    session_correct = 0
    session_total = 0
    for card in laccu_cards:
        print(card["front"])
        input("Press ENTER to flip...")
        print(card["back"])
        choice = get_valid_input("Did you get it right?\n1. Yes\n2. No\n", 1, 2)
        card["last_seen"] = datetime.date.today().isoformat()
        card["seen"] += 1
        session_total += 1
        if choice == 1:
            session_correct += 1
            card["correct"] += 1
    print(f"You got {session_correct}/{session_total} correct.")
    save_deck(path, deck)


if __name__ == "__main__":
    main()