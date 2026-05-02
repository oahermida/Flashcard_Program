import json
from pathlib import Path
import datetime
import uuid

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
        choice = get_valid_input("1. Add a card\n2. View all cards\n3. Quit\n", 1, 3)
        if choice == 1:
            deck["cards"].append(create_card())
            save_deck(path, deck)
        elif choice == 2:
            view_cards(deck)
        elif choice == 3:
            break



if __name__ == "__main__":
    main()