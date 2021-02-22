# Tic-Tac-Toe with AI


Project page: https://hyperskill.org/projects/82


## About
Everybody remembers this paper-and-pencil game from childhood: Tic-Tac-Toe, also known as Noughts and Crosses or X's and O's. A single mistake usually costs you the game, but thankfully it's simple enough that most players discover the best strategy quickly. Let’s program Tic-Tac-Toe and create an AI opponent to do battle with!
## Learning outcomes
After finishing this project, you'll know a lot about planning and developing a complex program from scratch, using classes and functions, handling errors, and processing user input. You will also learn to use OOP (Object-Oriented Programming) in the process.
## Remarks
Three levels of difficulty implemented for the AI player:
- easy - random moves
- medium - checks for a win/block of a win in one move 
- hard - based on minimax algorithm, perfect play




## Example
Usage:

start [user, easy, medium, hard] [user, easy, medium, hard]

coordinates are: number or row, number of column
```
Input command: > start hard user
Making move level "hard"
---------
|       |
| X     |
|       |
---------
Enter the coordinates: > 2 2
---------
|       |
| X O   |
|       |
---------
Making move level "hard"
---------
|   X   |
| X O   |
|       |
---------
Enter the coordinates: > 3 2
---------
|   X   |
| X O   |
|   O   |
---------
Making move level "hard"
---------
| X X   |
| X O   |
|   O   |
---------
Enter the coordinates: > 3 1
---------
| X X   |
| X O   |
| O O   |
---------
Making move level "hard"
---------
| X X X |
| X O   |
| O O   |
---------
X wins

Input command: > exit
```






