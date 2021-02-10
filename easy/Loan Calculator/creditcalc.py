import math
import argparse
import re
import sys


class Loan(object):

    type_validation = re.compile("(annuity|diff)")

    def __init__(self, args, type, principal, periods, interest, payment):
        self.args = args
        self.loan_type = type
        self.principal = principal
        self.periods = periods
        self.interest = interest
        self.payment = payment

    def validate_params(self):
        if self.loan_type is None or self.interest is None:
            print("Incorrect parameters")
            sys.exit()
        if self.loan_type == "" or self.interest == "":
            print("Incorrect parameters")
            sys.exit()
        if not re.match(self.type_validation, self.loan_type):
            print("Incorrect parameters")
            sys.exit()
        if self.loan_type == "diff" and self.payment is not None:
            print("Incorrect parameters")
            sys.exit()
        if self.loan_type == "diff" and (self.principal is None or self.periods is None or self.interest is None):
            print("Incorrect parameters")
            sys.exit()
        if len(vars(args)) < 4:
            print("Incorrect parameters")
            sys.exit()

    def calc_option(self):
        if self.loan_type == "annuity":
            if self.payment is None:
                monthly_payment = self.calc_monthly_payment_amount()
                overpayment = monthly_payment * int(self.periods) - float(self.principal)
                print(f"Your annuity payment = {monthly_payment}!")
                print(f"Overpayment = {round(overpayment)}")
            if self.periods is None:
                months, overpayment = self.calc_number_of_monthly_payments()
                print(f"It will take {self.months_to_year(months)} to repay this loan!")
                print(f"Overpayment = {math.ceil(overpayment)}")
            if self.principal is None:
                principal = self.calc_loan_principal()
                print(f"Principal: {principal}")
        if self.loan_type == "diff":
            self.calc_diff_payment()

    @staticmethod
    def months_to_year(months: int) -> str:
        months = int(months)
        if months == 1:
            return "1 month"
        elif months < 12:
            return f"{months} months"
        elif months == 12:
            return f"{1} year"
        elif months % 12 == 0:
            return f"{round(months / 12)} years"
        elif months > 12:
            return f"{math.floor(months / 12)} years and {months % 12} months"

    def calc_number_of_monthly_payments(self):
        principal = int(self.principal)
        monthly_payment = int(self.payment)
        loan_interest = float(self.interest)
        if principal < 0 or monthly_payment < 0 or loan_interest < 0:
            print("Incorrect parameters")
            sys.exit()
        nominal_interest_rate = (loan_interest / 100) / 12
        months = math.ceil(math.log(monthly_payment / (monthly_payment - nominal_interest_rate * principal),
                                    nominal_interest_rate + 1))
        overpayment = monthly_payment * months - principal
        return months, overpayment

    def calc_monthly_payment_amount(self):
        principal = float(self.principal)
        periods = int(self.periods)
        loan_interest = float(self.interest)
        if principal < 0 or periods < 0 or loan_interest < 0:
            print("Incorrect parameters")
            sys.exit()
        nominal_interest_rate = (loan_interest / 100) / 12
        monthly_payment = math.ceil(principal * ((nominal_interest_rate * (1 + nominal_interest_rate) ** periods) /
                                                 ((1 + nominal_interest_rate) ** periods - 1)))
        return monthly_payment

    def calc_loan_principal(self):
        annuity = float(self.payment)
        periods = int(self.periods)
        loan_interest = float(self.interest)
        if annuity < 0 or periods < 0 or loan_interest < 0:
            print("Incorrect parameters")
            sys.exit()
        nominal_interest_rate = (loan_interest / 100) / 12
        loan_principal = math.floor(annuity / ((nominal_interest_rate * (1 + nominal_interest_rate) ** periods) /
                                               ((1 + nominal_interest_rate) ** periods - 1)))
        return loan_principal

    def calc_diff_payment(self):
        principal = float(self.principal)
        periods = float(self.periods)
        loan_interest = float(self.interest)
        if principal < 0 or periods < 0 or loan_interest < 0:
            print("Incorrect parameters")
            sys.exit()
        nominal_interest_rate = (loan_interest / 100) / 12
        print(f"{nominal_interest_rate=}")
        total_payable = 0
        for i in range(1, int(periods)+1):
            payment = principal / periods + nominal_interest_rate * (principal - ((principal * (i - 1))/periods))
            total_payable += math.ceil(payment)
            print(f"Month {i}: payment is {math.ceil(payment)}")
        print("")
        print(f"Overpayment = {math.ceil(total_payable - principal)}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--type")
    parser.add_argument("--principal")
    parser.add_argument("--periods")
    parser.add_argument("--interest")
    parser.add_argument("--payment")
    args = parser.parse_args()
    args_dict = vars(args)
    loan = Loan(args, args.type, args.principal, args.periods, args.interest, args.payment)
    loan.validate_params()
    loan.calc_option()
