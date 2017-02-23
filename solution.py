#! /usr/bin/env python
#**********************************************************************
#* Name: solution (Sudoku)                                            *
#*                                                                    *
#* Function: Given an unsolved, encoded Sudoku puzzle provided in the *
#* 'main' function, use constraint propagation and search to find a   *
#* solution. If no solution is possible, the program exits with no    *
#* response. If a solution is found, it is displayed in textual format*
#* on the command-line and, if pygame is installed, will display a    *
#* graphical animation of the algorithm solving the puzzle on a Sudoku*
#* board.                                                             *
#* An example 81-box Sudoku grid encoding would be:                   *
#*    '2.............62....1....7...6..8...3...9...7...6..4...4....8  *
#*     ....52.............3'                                          *
#* where each dot represents an unsolved box in the grid.             *
#*                                                                    *
#* Usage: python solution.py                                          *
#*                                                                    *
#* Written:  02/23/2017  James Damgar (Based on Udacity AIND content) *
#* Modified:                                                          *
#*                                                                    *
#**********************************************************************


# Record our board assignments as we go for later visualization
assignments = []


# Some information about the board and a utility "cross" function
rows = 'ABCDEFGHI'
cols = '123456789'
def cross(A, B):
    """
    Return a list of boxes based on row and column values
    Args:
        A(list): List of row values
        B(list): List of column values
        
    Returns:
        a list of boxes based on row and column values
    """
    return [s+t for s in A for t in B]
   
   
# Populate some helper variables for keeping track of aspects of the board
boxes        = cross(rows, cols)
row_units    = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units   = [[''.join(z) for z in zip(rows, cols)]] + [[''.join(z) for z in zip(rows, cols[::-1])]]
unitlist     = row_units + column_units + square_units + diag_units
units        = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers        = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Update the values dictionary
    Assigns a value to a given box. If it updates the board record it.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        box(str)    : a box to update
        value(str)  : a value to update the box to
        
    Returns:
        the values dictionary with the box assigned its new value
        
    Side-effects:
        the assignments variable is updated if a single digit is assigned to a box
    """
    # Assign the specified box a value
    values[box] = value
    # If this assignment leads to knowing the digit for sure, update assignments for historical purposes
    if len(value) == 1:
        assignments.append(values.copy())
    return values

    
def naked_twins(values):
    """
    Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers
    """
    # Iterate over each unit
    for unit in unitlist:
        # Find all instances of naked twins for this unit
        twins = [values[ba] for ba in unit for bb in unit if ba != bb and len(values[ba]) == 2 and values[ba] == values[bb] ]
        # For each twin, eliminate its digits from boxes in the same unit that have >1 digit possibilities
        #print("UNIT:" + str(unit))
        for twin in twins:
            #print("TWIN:" + str(twin))
            for box in unit:
                if len(values[box]) > 1 and values[box] != twin:
                   for digit in twin:
                       values = assign_value(values, box, values[box].replace(digit,''))
    return values

    
def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form
        
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    # The possible digits
    digits = '123456789'
    # A dictionary mapping of the board to be filled in
    values = []
    # For each element of the gird, expand '.' into all possible digits.
    # If a digit is already assigned for a grid location, then use it
    for b in grid:
        if b == '.':
            values.append(digits)
        elif b in digits:
            values.append(b)
    # Make sure we have a valid board and return it
    assert len(values) == 81
    return dict(zip(boxes, values))

    
def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    # Nicely display values in the board with proper width spacing
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

    
def eliminate(values):
    """
    Eliminate digits by removing solved values from other peer-boxes in each unit
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with solved values eliminated as box possibilities
    """
    # Remove solved values from other peer-boxes in each unit
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values

    
def only_choice(values):
    """
    Eliminate digits by removing digits that occur only once in a unit from other boxes in that unit
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with digits having only one possibility in a unit removed from unit-peers
    """
    # If a digit occurs only once in a unit, then the box containing it should have it as its value
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
    return values

    
def reduce_puzzle(values):
    """
    Iterate over the Sudoku puzzle, using the eliminate, only_choice, and naked_twins strategies
    to reduce the board until we can no longer make progress
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary after reducing using the eliminate, only_choice, and naked_twins
        strategies one or more times
    """
    stalled = False
    while not stalled:
        # Count the number of boxes we have solved
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Eliminate more boxes using peer-unit elimination and "only choice"
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        # Count the number of boxes we have solved now
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

    
def search(values):
    """
    Using depth-first search and propagation, create a search tree and solve the Sudoku puzzle
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the solved board in dictionary form, if a solution exists. False otherwise
    """
    # First, reduce the puzzle using the previous function
    # Check if we're done
    values = reduce_puzzle(values)
    if values is False:
        return False
    themax = max( len(v) for v in values.values() )
    if themax == 1:
        return values
    
    # Choose one of the unfilled squares with the fewest possibilities
    themin = min( len(v) for v in values.values() if len(v) > 1 )

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    min_boxes = [ box for box in values.keys() if len(values[box]) == themin ]
    min_box = min_boxes[0]
    for v in values[min_box]:
        new_values = values.copy()
        new_values[min_box] = v
        result = search(new_values)
        if result:
            return result
    return False
    

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # Convert the input grid encoding into a dictionary representation of the board,
    # then search for the solution and return it. If no solution can be found, return False
    return search(grid_values(grid))

    
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

