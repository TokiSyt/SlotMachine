import random
from constants import *

symbols_amount = {
    "*" : 3,
    "º" : 5,
    "?" : 7,
    "@" : 9,
}


three_symbols_value = {
    "*" : 4,
    "º" : 3,
    "?" : 2,
    "@" : 1.5,
}


two_symbols_value = {
    "*" : 1.8,
    "º" : 1.3,
    "?" : 1.2,
    "@" : 1.1,
}


def check_winnings(columns, lines, bet, two_values, three_values):

    winnings = 0
    winning_lines = []

    for line in range(lines):
        symbol_counts = {}

        for column in columns:
            symbol_to_check = column[line]

            if symbol_to_check in symbol_counts:
                symbol_counts[symbol_to_check] += 1
            else:
                symbol_counts[symbol_to_check] = 1

        for symbol, symbol_amount in symbol_counts.items():
            if symbol_amount == 2:
                    winnings += two_values[symbol] * bet
                    if line + 1 not in winning_lines:
                        winning_lines.append(line + 1)

            elif symbol_amount == 3:
                    winnings += three_values[symbol] * bet
                    if line + 1 not in winning_lines:
                        winning_lines.append(line + 1)

    return winnings, winning_lines


def get_slot_spins(rows, cols, symbols):

    all_symbols = []
    for symbol, symbols_amount in symbols.items():
        for _ in range(symbols_amount):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        symbols_avaiable = all_symbols[:]
        for _ in range(rows):
            symbol_choosen = random.choice(symbols_avaiable)
            symbols_avaiable.remove(symbol_choosen)
            column.append(symbol_choosen)

        columns.append(column)
    return columns


def print_slot_machine(columns):

    for row in range(len(columns[0])):
        for index, column in enumerate(columns):
            if index != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row])


def deposit():

    while True:
        deposited_money = input("How much money you want to deposit? Czk: ")

        if deposited_money.isdigit():
            deposited_money = int(deposited_money)
            if deposited_money > 0:
                break
            else:
                print("Invalid amount.")
        else:
            print("Please enter a valid amount.")

    return deposited_money


def get_number_of_lines():

    while True:
        lines_number = input(f'''
How many slot machine lines you wish to bet on?

Input = (1 to {MAX_LINES})
                             
1 line: Top line.
2 lines: Top & Middle lines.
3 lines: All lines.

Write here: ''')

        if lines_number.isdigit():
                    lines_number = int(lines_number)
                    if 1 <= lines_number <= MAX_LINES:
                        break
                    else:
                        print("Invalid number of lines.")
        else:
            print("Please enter a valid number of lines.")
    return lines_number


def get_bet():

    while True:
        bet_amount = input(f"\nHow much would you like to bet on each line? Czk: ")

        if bet_amount.isdigit():
            bet_amount = int(bet_amount)
            if MIN_BET <= bet_amount <= MAX_BET:
                break
            else:
                print(f"Bet amount must be between {MIN_BET}czk and {MAX_BET}czk")
        else:
            print("Please enter a valid amount to bet.")

    return bet_amount


def spin(balance):

    lines_number = get_number_of_lines()
    while True:
        bet_amount = get_bet()
        total_bet = lines_number * bet_amount

        if total_bet > balance:
            print(f"\nYou do not have enough money to make this bet! Your current balance is {balance}.\n")
        else:
            break
    print(f"\nYou are betting {bet_amount} on {lines_number} lines.\nYour total bet is: {total_bet}\n")

    slots = get_slot_spins(ROWS, COLS, symbols_amount)
    print_slot_machine(slots)

    winnings, winning_lines = check_winnings(slots, lines_number, bet_amount, two_symbols_value, three_symbols_value)
    winnings = int(winnings)

    print(f"You won: {winnings} czk!")

    if winning_lines:
        print(f"You won on these lines:", *winning_lines)
    else:
        print("Better luck next time!")

    return winnings - total_bet


def main():

    balance = deposit()
    while True:
        print(f"Current balance is: {balance} czk.")
        spin_check = input("Press enter to play (q to quit).\n")
        if spin_check == "q":
            break
        balance += spin(balance)
        if balance <= 0:
            print("You are broken now, congrats! You have no money for Xmas now.\n")
            break

    print(f"You left with {balance} czk.\n")

main()
