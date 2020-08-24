import random
import sqlite3
from Bank_Machine import luhn

conn = sqlite3.connect('card.s3db')
c = conn.cursor()


def end_program():
    print("\nBye!")
    return


class BankMachine:
    def __init__(self):
        self.current_user_id = 0
        self.current_user_card_number = ''
        self.current_user_pin = ''
        self.current_user_balance = 0

    def run_bank_machine(self):
        try:
            c.execute('''SELECT * FROM card''')
        except sqlite3.OperationalError:
            c.execute('''CREATE TABLE card (
                id INTEGER,
                number TEXT,
                pin TEXT,
                balance INTEGER DEFAULT 0
            )''')

        conn.commit()

        return self.make_initial_selection()

    def create_new_user(self):
        card_number = luhn.generate_card_number()
        pin = str(random.randint(0, 9999)).zfill(4)
        print(f"""
Your card has been created
Your card number:
{card_number}
Your card PIN:
{pin}""")
        c.execute(
            '''INSERT INTO card (number, pin) VALUES (?,?)''', (card_number, pin)
        )
        conn.commit()
        self.make_initial_selection()

    def log_in(self):
        card_number_entry = input("\nEnter your card number:\n ")
        pin_entry = input("Enter your PIN:\n ")

        # SQL to compare card_number and pin

        try:
            c.execute('''SELECT 
                                    id, number, pin, balance
                                    FROM card 
                                    WHERE (number=? AND pin=?)''', (card_number_entry, pin_entry))
            details = c.fetchone()

            self.current_user_id = details[0]
            self.current_user_card_number = details[1]
            self.current_user_pin = details[2]
            self.current_user_balance = details[3]

            print("\nYou have successfully logged in!")
            return self.logged_in_selections()

        except TypeError:
            print("Wrong card number or PIN!")
            return self.make_initial_selection()

    def make_initial_selection(self):

        initial_selection = input("""
1. Create an account
2. Log into account
0. Exit\n""")

        if initial_selection == "1":
            self.create_new_user()

        elif initial_selection == "2":
            c.execute('''SELECT * from card''')
            details = c.fetchall()
            for row in details:
                print(row)

            self.log_in()

        elif initial_selection == "0":
            end_program()

        else:
            print("Please enter valid selection")
            return self.make_initial_selection()

    def add_income(self):
        income = input("\nEnter income: \n")
        self.current_user_balance += int(income)
        print("\nBalance: " + str(self.current_user_balance))
        c.execute('''
                        UPDATE card
                        SET balance=?
                        WHERE (number=?)''', (self.current_user_balance, self.current_user_card_number))
        conn.commit()
        print("Income was added!")
        return self.logged_in_selections()

    def transfer_funds(self):
        print("Transfer")
        number_to_check = input("Enter card number: \n")
        if not luhn.check_card_number(number_to_check):
            print("Probably you made mistake in the card number. Please try again!")
            return self.logged_in_selections()
        else:
            c.execute('''SELECT number FROM card WHERE (number=?)''', (number_to_check,))
            if not c.fetchone():
                print("Such a card does not exist.")
                return self.logged_in_selections()

            else:
                amt_to_transfer = int(input("Enter how much money you want to transfer: \n"))
                if amt_to_transfer > self.current_user_balance:
                    print("Not enough money!")
                    return self.logged_in_selections()
                else:
                    self.current_user_balance -= amt_to_transfer
                    c.execute('''
                                UPDATE card
                                SET balance=?
                                WHERE (number=?)''', (self.current_user_balance, self.current_user_card_number))
                    conn.commit()
                    c.execute('''
                                UPDATE card
                                SET balance=balance+?
                                WHERE (number=?)''', (amt_to_transfer, number_to_check))
                    conn.commit()
                    print("Success!\n")
                    return self.logged_in_selections()

    def delete_account(self):
        c.execute("""DELETE FROM card WHERE (number = ?)""", (self.current_user_card_number,))
        conn.commit()
        print("The account has been closed!")
        return self.make_initial_selection()

    def log_out(self):
        print("You have successfully logged out!")
        self.current_user_id = 0
        self.current_user_card_number = ''
        self.current_user_pin = ''
        self.current_user_balance = 0
        return self.make_initial_selection()

    def get_balance(self):
        print("\nBalance: " + str(self.current_user_balance))
        return self.logged_in_selections()

    def logged_in_selections(self):

        print("""
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")

        selection = input()

        if selection == "1":
            self.get_balance()

        elif selection == "2":
            self.add_income()

        elif selection == "3":
            self.transfer_funds()

        elif selection == "4":
            self.delete_account()

        elif selection == "5":
            self.log_out()

        elif selection == "0":
            end_program()

        else:
            print("Please enter valid selection")
            self.logged_in_selections()


my_bank_machine = BankMachine()

my_bank_machine.run_bank_machine()
