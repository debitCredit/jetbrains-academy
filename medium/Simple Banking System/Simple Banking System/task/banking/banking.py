from random import choice
import string
import sqlite3


class Bank:

    ISS_ID = 400000

    def __init__(self):
        self.con = sqlite3.connect('card.s3db')
        self.create_table()
        self.first_screen()

    def create_table(self):
        sql = """create table if not exists card (
        id integer,
        number text,
        pin text,
        balance integer default 0)"""
        self.con.execute(sql)
        self.con.commit()

    def generate_new_card_number(self):
        while True:
            acc_number = self.generate_new_number(9)
            first_part = str(self.ISS_ID) + str(acc_number)
            checksum = self.luhn_generate(first_part)
            generated_card = str(first_part) + str(checksum)
            if not self.card_check(generated_card):
                continue
            else:
                return generated_card

    @staticmethod
    def generate_new_number(digits):
        chars = string.digits
        random = ''.join(choice(chars) for _ in range(digits))
        return random

    @staticmethod
    def luhn_checksum(s):
        digits = list(map(int, s))
        odd_sum = sum(digits[-1::-2])
        even_sum = sum([sum(divmod(2 * d, 10)) for d in digits[-2::-2]])
        return (odd_sum + even_sum) % 10

    def luhn_verify(self, s):
        return self.luhn_checksum(s) == 0

    def luhn_generate(self, s):
        cksum = self.luhn_checksum(s + '0')
        return (10 - cksum) % 10

    def first_screen(self):
        print("")
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
        choice = input()

        if choice == "1":
            self.card_created()
        elif choice == "2":
            self.login()
        elif choice == "0":
            print("")
            print("Bye!")
            exit()

    def logged_in(self, card, pin):
        print("")
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")

        choice = str(input())

        if choice == "1":
            print("")
            print("Balance: ", self.get_balance(card))
            self.logged_in(card, pin)
        elif choice == "2":
            self.add_income(card, pin)
        elif choice == "3":
            self.transfer(card, pin)
        elif choice == "4":
            print("")
            self.close_account(card, pin)
        elif choice == "5":
            print("")
            print("You have successfully logged out!")
            self.first_screen()
        elif choice == "0":
            print("")
            print("Bye!")
            exit()

    def card_created(self):
        number, pin = self.create_card()
        print("")
        print("Your card has been created")
        print("Your card number:")
        print(number)
        print("Your card PIN:")
        print(pin)
        self.first_screen()

    def add_income(self, card, pin):
        print("")
        print("Enter income:")
        income = int(input())
        sql = """
            update card set balance = balance + ? where number = ?"""
        self.con.execute(sql, (int(income), card))
        self.con.commit()
        print("Income was added!")
        self.logged_in(card, pin)

    def transfer(self, card, pin):
        print("Transfer")
        print("Enter card number:")
        to_account = input()

        if not self.luhn_verify(to_account):
            print("Probably you made a mistake in the card number. Please try again!")
            self.logged_in(card, pin)

        if self.card_check(to_account):
            print("Such a card does not exist.")
            self.logged_in(card, pin)

        print("Enter how much money you want to transfer:")
        transfer_amount = int(input())

        if transfer_amount > self.get_balance(card):
            print("Not enough money!")
            self.logged_in(card, pin)

        sql = """
                    update card set balance = balance - ? where number = ?"""
        self.con.execute(sql, (transfer_amount, card))
        sql = """
                    update card set balance = balance + ? where number = ?"""
        self.con.execute(sql, (transfer_amount, to_account))
        self.con.commit()
        print("Success!")
        self.logged_in(card, pin)

    def close_account(self, card, pin):
        sql = """
                            delete from card where number = ?"""
        self.con.execute(sql, (card,))
        self.con.commit()
        print("The account has been closed!")
        self.first_screen()

    def login(self):
        print("")
        print("Enter your card number:")
        entered_card = str(input())
        print("Enter your PIN:")
        entered_pin = str(input())

        if self.card_pin_check(entered_card, entered_pin):
            print("")
            print("You have successfully logged in!")
            self.logged_in(entered_card, entered_pin)

        else:
            print("")
            print("Wrong card number or PIN!")
            self.first_screen()

    def create_card(self):
        card_number = str(self.generate_new_card_number())
        pin = str(self.generate_new_number(4))
        sql = """
            insert into card (number, pin)
            values (?, ?)"""
        self.con.execute(sql, (card_number, pin))
        self.con.commit()
        return card_number, pin

    def card_check(self, card_number):
        sql = """
            select count(*) from card where number = ?"""
        result = self.con.execute(sql, (card_number,)).fetchone()
        if result is None:
            return True
        else:
            return result[0] == 0

    def card_pin_check(self, card, pin):
        sql = """
            select 1 from card where pin = ? and number = ?"""
        result = self.con.execute(sql, (pin, card)).fetchone()
        if result is None:
            return False
        else:
            return result[0] == 1

    def get_balance(self, card):
        sql = """
            select balance from card where number = ?"""
        return self.con.execute(sql, (card,)).fetchone()[0]


if __name__ == '__main__':
    run = Bank()
