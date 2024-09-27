import os
import platform
import random

MAX_LINES = 3
MIN_BET = 1
MAX_BET = 100

ROWS = 3
COLS = 3

symbol_count = {
    "O": 20,
    "L": 15,
    "C": 10,
    "P": 12,
    "B": 5,
    "S": 3,
    "7": 1
}

symbol_value = {
    "O": 2,
    "L": 3,
    "C": 4,
    "P": 5,
    "B": 10,
    "S": 20,
    "7": 50
}

def wipe():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def deposit():
    while True:
        amount = input("Enter deposit amount. > $")
        if amount.isdigit():
            amount = int(amount)
            if amount >= 10:
                break
            else:
                print("Minimum deposit is $10.")
        else:
            print("Please enter a number.")
    return amount

def get_lines():
    while True:
        lines = input(f"Enter number of lines to bet on {1}-{MAX_LINES}. > ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Minimum lines amount is 1.")
        else:
            print("Please enter a number.")
    return lines

def get_bet():
    while True:
        amount = input("Enter bet amount for each line. > $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Bet amount must be between ${MIN_BET}-${MAX_BET}.")
        else:
            print("Please enter a number.")
    return amount

def get_spin(rows, cols, symbol_count):
    all_symbols = []
    for symbol, symbol_count in symbol_count.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)
    
    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns

def print_slot(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")
        print()

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            check = column[line]
            if symbol != check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines

def spin(balance):
    if balance == 0:
        print("You ran out of balance.")
        exit()

    wipe()
    lines = get_lines()

    while True:
        bet = get_bet()
        total_bet = bet * lines
        if total_bet > balance:
            print(f"Insufficient balance. Total bet is ${total_bet}, your balance is ${balance}.")
        else:
            break

    wipe()
    print(f"Betting ${bet} on {lines} lines. Total bet is ${total_bet}.\n")
    slots = get_spin(ROWS, COLS, symbol_count)
    print_slot(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    
    if winnings > 0:
        print(f"\nYou won ${winnings}.")
        print(f"Winning lines:", *winning_lines)
        print()
    else:
        print("\nYou won nothing.\n")
    
    return winnings - total_bet

def main():
    wipe()
    old_balance = deposit()
    new_balance = old_balance
    wipe()
    while True:
        print(f"Current balance is ${new_balance}.")
        choice = input("\nPress enter to spin! (Q to Quit) > ")
        if choice == "Q" or choice == "q":
            break
        new_balance += spin(new_balance)
    
    wipe()
    print(f"You entered with ${old_balance} and left with ${new_balance}.")
    if new_balance > old_balance:
        print(f"Total winnings are ${new_balance - old_balance}")

main()
