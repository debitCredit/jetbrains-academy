# Python Banking System

Simple Banking System in Python and using SQLite

Project page: https://hyperskill.org/projects/109

## About
Everything goes digital these days, and so does money. Today, most people have credit cards, which save us time, energy and nerves. From not having to carry a wallet full of cash to consumer protection, cards make our lives easier in many ways. In this project, you will develop a simple banking system with database.
## Learning outcomes
In this project, you will find out how the banking system works and learn about SQL. We'll also see how Luhn algorithm can help us avoid mistakes when entering the card number. As an overall result, you'll get new experience in Python.

## Features ##

* Card management with card number checking using Luhn algorithm
* Income and Transfers

## Example

```
1. Create an account
2. Log into account
0. Exit
> 2

Enter your card number:
> 4000009052164731
Enter your PIN:
> 6171

You have successfully logged in!

1. Balance
2. Add income 
3. Make transfer
4. Close account
5. Log out
0. Exit
> 3

Transfer
Enter card number:
> 4000003997357290 
Probably you made a mistake in the card number. Please try again!

1. Balance
2. Add income
3. Make transfer
4. Close account
5. Log out
0. Exit
> 3

Transfer
Enter card number:
> 4000003997357294
Enter how much money you want to transfer:
> 10000
Not enough money!

1. Balance
2. Add income
3. Make transfer
4. Close account
5. Log out
0. Exit
> 3

Transfer
Enter card number:
> 4000003997357294
Enter how much money you want to transfer:
> 100
Success!

1. Balance
2. Add income
3. Make transfer
4. Close account
5. Log out
0. Exit
> 1

Balance: 1134

1. Balance
2. Add income
3. Make transfer
4. Close account
5. Log out
0. Exit
> 4

The account has been closed!
```