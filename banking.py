import random
import sqlite3

"""Простейшая банковская система, генерирующая номер банковской карты (в соответствии с алгоритмом Луна) и PIN-код.
Данные карты и баланс сохраняются в таблицу SQL, в рамках программы доступен вход в личный кабинет по номеру карты и PIN-коду,
а также проведение транзакций с записью в таблицу. """



conn = sqlite3.connect("card.s3db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS card (
id INTEGER PRIMARY KEY,
number TEXT,
pin TEXT,
balance INTEGER DEFAULT 0
);""")
conn.commit()


def card_creator():
    iin = "400000"
    rest = ""
    while True:
        def digits_of(n):
            return [int(d) for d in str(n)]
        for i in range(0, 10):
            rest += "".join(str(random.randint(1, 9)))
        full_number = digits_of(iin + rest)
        odd_digits = full_number[-1::-2]
        even_digits = full_number[-2::-2]
        summ = 0
        summ += sum(odd_digits)
        for j in even_digits:
            summ += sum(digits_of(j * 2))
        if summ % 10 == 0:
            break
        else:
            rest = ""
            continue
    return int(iin + rest)


def card_checker(number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    full_number = digits_of(number)
    odd_digits = full_number[-1::-2]
    even_digits = full_number[-2::-2]
    summ = 0
    summ += sum(odd_digits)
    for j in even_digits:
        summ += sum(digits_of(j * 2))
    if summ % 10 == 0:
        return True
    else:
        return False


def pin_creator():
    pin = ""
    for i in range(4):
        pin += "".join(str(random.randint(1, 9)))
    return int(pin)


while True:
    card_id = 0
    print("""1. Create an account
2. Log into account
0. Exit""")
    a = int(input())

    if a == 0:
        print("Bye!")
        break

    if a == 1:
        card_number = card_creator()
        card_pin = pin_creator()
        c.execute(f"INSERT INTO card (number, pin) VALUES ({card_number}, {card_pin})")
        conn.commit()
        print(f"""Your card has been created
Your card number:
{str(card_number)}
Your card PIN:
{str(card_pin)}""")
        continue

    if a == 2:
        print("Enter your card number:")
        card_numb = input()
        print("Enter your PIN:")
        pin_numb = input()
        c.execute(f"SELECT * FROM card WHERE number = '{card_numb}' AND pin='{pin_numb}'")
        fetched_card = c.fetchone()
        if fetched_card is None:
            print("Wrong card number or PIN!")
            continue
        else:
            print("You have successfully logged in!")
            print("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")
            while True:
                action = int(input())
                if action == 0:
                    break
                elif action == 1:
                    c.execute(f"SELECT balance FROM card WHERE number = {card_numb} AND pin = {pin_numb}")
                    fetched_balance = c.fetchone()
                    print(f"Balance: {fetched_balance[0]}")
                    continue
                elif action == 2:
                    c.execute(f"SELECT balance FROM card WHERE number = {card_numb} AND pin = {pin_numb}")
                    fetched_balance = c.fetchone()
                    income = int(input("Enter income:"))
                    c.execute(f"UPDATE card SET balance = balance + {income} WHERE number = {card_numb}")
                    conn.commit()
                    print("Income was added!")
                    continue
                elif action == 3:
                    final_card = input("Transfer\nEnter card number:\n")
                    c.execute(f"SELECT * FROM card WHERE number = {final_card}")
                    finalised_card = c.fetchone()
                    if not card_checker(final_card):
                        print("Probably you made a mistake in the card number. Please try again!")
                        continue
                    elif card_checker(final_card) and finalised_card is None:
                        print("Such a card does not exist.")
                        continue
                    transfer = int(input("Enter how much money you want to transfer:\n"))
                    c.execute(f"SELECT balance FROM card WHERE number = {card_numb}")
                    fetched_balance = c.fetchone()
                    if transfer >= fetched_balance[0]:
                        print("Not enough money!")
                    elif transfer <= fetched_balance[0]:
                        c.execute(f"UPDATE card SET balance = balance - {transfer} WHERE number = {card_numb}")
                        c.execute(f"UPDATE card SET balance = balance + {transfer} WHERE number = {final_card}")
                        conn.commit()
                        print("Success!")
                        continue
                    continue
                elif action == 4:
                    c.execute(f"DELETE FROM card WHERE number = {card_numb}")
                    conn.commit()
                elif action == 5:
                    print("You have successfully logged out!")
                    break
            if action == 0:
                break
            continue

conn.close()
