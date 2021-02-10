# Loan Calculator

Project page: https://hyperskill.org/projects/90


## About
Personal finances are an important part of life. Sometimes you need some extra money and decide to take a loan, or you want to buy a house using a mortgage. To make an informed decision, you need to be able to calculate different financial parameters. Let’s make a program that can help us with that!

## Learning outcomes
You will practice using mathematics and Python in everyday tasks and learn how to use third-party modules and libraries. You will also learn more about different financial instruments.

## Remarks
Arguments are passed as command line arguments, multiple parameter validation checks are performed. By ommiting parameters users choose the desired calculation to be performed



### Examples:

Calculate differentiated payments given a principal of 500,000 over 8 months at an interest rate of 7.8%
```
> python creditcalc.py --type=diff --principal=500000 --periods=8 --interest=7.8
Month 1: payment is 65750
Month 2: payment is 65344
Month 3: payment is 64938
Month 4: payment is 64532
Month 5: payment is 64125
Month 6: payment is 63719
Month 7: payment is 63313
Month 8: payment is 62907

Overpayment = 14628
```
Calculate the principal for a user paying 8,722 per month for 120 months (10 years) at 5.6% interest

```
> python creditcalc.py --type=annuity --payment=8722 --periods=120 --interest=5.6
Your loan principal = 800018!
Overpayment = 246622
```
