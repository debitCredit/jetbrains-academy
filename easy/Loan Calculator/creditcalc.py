import math


class Loan:

    def options(self):
        print('What do you want to calculate? '
              '\ntype "n" for number of monthly payments,'
              '\ntype "a" for annuity monthly payment amount,'
              '\ntype "p" for loan principal:)')
        option = input()
        if option == "n":
            self.calc_number_of_monthly_payments()
        elif option == "a":
            self.calc_monthly_payment_amount()
        elif option == "p":
            self.calc_loan_principal()

    def months_to_year(self, months: int) -> str:
        if months == 1:
            return "1 month"
        elif months < 12:
            return f"{months} months"
        elif months == 12:
            return f"{1} year"
        elif months % 12 == 0:
            return f"{months / 12} years"
        elif months > 12:
            return f"{math.floor(months / 12)} years and {months % 12} months"

    def calc_number_of_monthly_payments(self):
        print("Enter the loan principal:")
        principal = int(input())
        print("Enter the monthly payment:")
        monthly_payment = int(input())
        print("Enter the loan interest:")
        loan_interest = float(input())

        nominal_interest_rate = (loan_interest / 100) / 12
        print(f"{nominal_interest_rate=}")
        months = math.ceil(math.log(monthly_payment / (monthly_payment - nominal_interest_rate * principal),
                                    nominal_interest_rate + 1))

        print(f"It will take {self.months_to_year(months)} to repay this loan!")

    def calc_monthly_payment_amount(self):
        print("Enter the loan principal:")
        principal = float(input())
        print("Enter the number of periods:")
        periods = int(input())
        print("Enter the loan interest:")
        loan_interest = float(input())

        nominal_interest_rate = (loan_interest / 100) / 12
        monthly_payment = math.ceil(principal * ((nominal_interest_rate * (1 + nominal_interest_rate) ** periods) /
                                                 ((1 + nominal_interest_rate) ** periods - 1)))

        print(f"Your monthly payment = {monthly_payment}!")

    def calc_loan_principal(self):
        print("Enter the annuity payment:")
        annuity = float(input())
        print("Enter the number of periods:")
        periods = int(input())
        print("Enter the loan interest:")
        loan_interest = float(input())

        nominal_interest_rate = (loan_interest / 100) / 12
        loan_principal = math.floor(annuity / ((nominal_interest_rate * (1 + nominal_interest_rate) ** periods) /
                                               ((1 + nominal_interest_rate) ** periods - 1)))

        print(f"Your loan principal = {loan_principal}!")


if __name__ == '__main__':
    loan = Loan()
    loan.options()
