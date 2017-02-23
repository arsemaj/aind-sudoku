# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The naked twins problem/strategy makes use of constraint propagation by enforcing the constraint that if two boxes in a unit have only two digits value possibilities, then those digits can only be solutions for those two boxes. For example, if boxes A1 and B1 can only have 1 or 2, then it must be the case that one box has '1' and another box has '2' as a value, meaning no other boxes in the unit shared by A1 and B1 can have those values. The strategy enforces this constraint by eliminating these digit values from all other boxes in a unit. The algorithm implemented enforces this constraint for all twins found in all units of the Sudoku board.


# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The diagonal sudoku problem/strategy uses constraint propagation by enforcing the constraint that each of the two unit diagonals [A1, B2, C3, D4, E5, F6, G7, H8, I9] and [A9, B8, C7, D6, E5, F4, G3, H2, I1] can each only have one instance of each of the digit values 1, 2, 3, 4, 5, 6, 7, 8, 9 assigned to their constituent boxes as a part of a solution. The coded solution.py simply adds these diagonal units to our set of units that we keep track of when performing elimination, only_choice, and naked_twins digit elimination passes. In this way, diagonal sudoku constraints are enforced.


### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.