'''
Nane: Mikhail Ermak
Exercise: 2048 Game
'''

# The list of modules we should use for 2048 as well as brief explanation to each module of why we should use it:
import os # We need this module to clear the terminal just before the next movement appears in game loop section:
import sys # We need this module to safely finish the .py script either after the winning or game-over detection:
import copy # We need this module to take a copy of the grid when we will be working on in the game loop section:
import random # We need this module to choose random cell and put there ethier the number two or the number four:
import keyboard # We need this module to maintain keyboard keys when the user wants to swipe in ethier direction:

#=========================================================================#
#============================== BASIC SETUP ==============================#
#=========================================================================#

# 2048 Grid:
GameGrid = [
[0, 0, 2, 2],
[4, 4, 4, 4],
[8, 8, 8, 8],
[16, 16, 16, 16]]

# An Empty List - we need this list to store all coordinates
empty_cell = [] # from the GameGrid that have values of zero:

# The Function - we need this function to randomly
def DropRate(): # choice ethier the number 2 or 4:
    '''
    PRE: This function does not require any precondition unless it is a function call.
    POST: Returns a random number which then will be putted in a random selected cell.
    '''
    number = random.choices([2, 4], weights=[90, 10])[0] # [0] returns the value in non-list.
    return number

# The Function - we need this function to select all cells
def NewNumber(chance): # that contains the values of zeros:
    empty_cell.clear() # Clears the list after each calling.
    '''
    PRE: Before starting, we need to pass the result of the previous function as an argument.
    POST: Returns a modified grid with a new value in the cell where there used to be a zero.
    '''
    for row in range(4):
        for col in range(4):
            if GameGrid[row][col] == 0:
                empty_cell.append((row, col))

    # Thus, the 2048 will appear a value (2 with 90% chance or 4 with 10% chance)
    row, col = random.choice(empty_cell) # after every swipe in X-axis or Y-axis:
    GameGrid[row][col] = chance
    return GameGrid

# The Function we need is used to generate a
def PrintGrid(grid): # clearly visible grid:
    '''
    PRE: The fucntion requires the current grid.
    POST: Returns a well-organized current grid.
    '''
    print("+------+------+------+------+")
    for row in grid:
        print("|", end="")

        for col in row:
            if len(str(col)) == 1:
                print("", col, end="    |")
            elif len(str(col)) == 2:
                print("", col, end="   |")
            elif len(str(col)) == 3:
                print("", col, end="  |")
            elif len(str(col)) == 4:
                print("", col, end=" |")
        print()
    print("+------+------+------+------+")

# The Function that just clears
def ClearScreen(): # the screen:
    os.system("cls" if os.name == "nt" else "clear")

# The Function we need is used to generate the screen
def InstructionsScreen(): # of 2048 game instructions:
    print(
'''
=============================
=========== 2048 ============
=============================

Controls:
W / K / ↑ : Move Up
A / H / ← : Move Left
S / J / ↓ : Move Down
D / L / → : Move Right

The Goal:
Merge numbers until you reach 2048.

Good luck!
=============================
''')

# To start the game, we should have just two numbers
# on the grid, so we should call this function twice:
NewNumber(2), NewNumber(2)
InstructionsScreen()
PrintGrid(GameGrid)

#=============================================================================#
#============================== KEYBOARD SYSTEM ==============================#
#=============================================================================#

# The Dictionary of all valid keys for 
# 2048 Game:   (key)          (value)
KeyboardKeys = {"Up"    : ["w", "k", "up"],
                "Down"  : ["s", "j", "down"],
                "Left"  : ["a", "h", "left"],
                "Right" : ["d", "l", "right"]}

# The Variable we need is used for saving
Direction = None # the following movement:

# The Function - we need this function to know which direction
def PressKey(event): # was triggered based on the pressed key:
    global Direction
    '''
    PRE: Write event in the parameters, a variable that contains information about the key press.
    POST: Returns the information about which direction is triggered based on user's pressed key.
    '''
    key = event.name

    if key in KeyboardKeys["Up"]:
        Direction = "Up"
    elif key in KeyboardKeys["Down"]:
        Direction = "Down"
    elif key in KeyboardKeys["Left"]:
        Direction = "Left"
    elif key in KeyboardKeys["Right"]:
        Direction = "Right"

# If user presses a key, then .on_press calls the function which goes through the dictionary
keyboard.on_press(PressKey) # of all valid keys for the 2048. Thereby, depending on an exact
# situation, the variable stores the name of the direction in which the player wants to move:

#=============================================================================#
#============================== MOVEMENT SYSTEM ==============================#
#=============================================================================#

# The Function we need is used to compress non-zero numbers to the LEFT or UP side,
def CompressForward(grid): # depending on which direction the player wants to move:
    '''
    PRE: Parameter "grid" in this function represents the POSITIVE direction,
    meaning that if the grid would receive row -> LEFT movement, when column -> UP.
    POST: Returns a compressed grid with all zeros to the right or bottom side.
    '''
    for row in grid:
        for col in row:
            if col == 0:
                row.remove(col) # To simulate that all integers moving to the left or up side,
                row.append(col) # we should move all zeros either to the right or bottom side.
    return grid

# The Function we need is used to compress non-zero numbers to the RIGHT or DOWN side,
def CompressBackward(grid): # depending on which direction the player wants to move:
    '''
    PRE: Parameter "grid" in this function represents the NEGATIVE direction,
    meaning that if the grid would receive row -> RIGHT movement, when column -> DOWN.
    POST: Returns a well-compressed grid with all zeros to the left or top side.
    '''
    for row in grid:
        for index in range(len(row) -1, -1, -1):
            if row[index] == 0:
                row.pop(index) # Same idea, but because movement is in negative direction,
                row.insert(0, 0) # we should move all zeros either to the left or up side.
    return grid

# The Function we need is used to merge (or sum) nearby similar numbers with
def MergeGrid(grid, direction): # valid UP, LEFT, DOWN, and RIGHT directions:<────┐
    '''                                                                           │
    PRE: Parameter "grid" in this function works for ALL MOVEMENTS like these ones┘
    when parameter "direction" represents either POSITIVE or NEGATIVE direction.
    POST: Returns a grid where adjacent equal numbers have been merged (summed).
    '''
    for row in grid:
        for col_index in range(len(row) - 1):
            if row[col_index] == row[col_index + 1]:
                sum_value = row[col_index] + row[col_index + 1]

                # If direction is forward, then move LEFT or UP.
                if direction == "Forward":
                    row[col_index] = sum_value
                    row[col_index + 1] = 0

                # If direction is back, then move RIGHT or DOWN.
                elif direction == "Back":
                    row[col_index] = 0
                    row[col_index + 1] = sum_value
    return grid

# The Function we need is used to transpose each column from the grid to rows in a temporary list,
def column_to_row(grid): # making this efficiently for compressing and merging numbers in columns.
    '''
    PRE: The function requires the grid that we are using.
    POST: Returns transposed columns in a temporary list.
    '''
    Column = [[], [], [], []]

    # The loop to transpose each column from the grid
    for row in grid: # into rows in a temporary list:
        for col in range(4):
            Column[col].append(row[col])

    return Column

# The Fucntion we need is used to transpose rows back to columns in the grid.
def row_to_column(grid, column):
    '''
    PRE: The function requires the temporary list to insert all integers back into the grid.
    POST: Places the numbers from the temporary list back into the grid and then returns it.
    '''
    for column_index in range(4):
        for row_index in range(4):
            grid[row_index][column_index] = column[column_index][row_index]

    return grid

# The Function we need is used to wrap all function calls,
def MoveLeft(grid): # that requires for the left movement.
    CompressForward(grid)
    MergeGrid(grid, "Forward")
    CompressForward(grid)
    return grid

# The Function we need is used to wrap all function calls,
def MoveRight(grid): # that requires for the right movement.
    CompressBackward(grid)
    MergeGrid(grid, "Back")
    CompressBackward(grid)
    return grid

# The Function is used to wrap all function calls,
def MoveUp(grid): # that requires for up movement.
    TransposedOne = column_to_row(grid)
    CompressedOne = CompressForward(TransposedOne)
    Merged = MergeGrid(CompressedOne, "Forward")
    CompressedTwo = CompressForward(Merged)
    TransposedTwo = row_to_column(grid, CompressedTwo)
    return TransposedTwo

# The Function is used to wrap all function calls,
def MoveDown(grid): # that requires for down motion.
    TransposedOne = column_to_row(grid)
    CompressedOne = CompressBackward(TransposedOne)
    Merged = MergeGrid(CompressedOne, "Back")
    CompressedTwo = CompressBackward(Merged)
    TransposedTwo = row_to_column(grid, CompressedTwo)
    return TransposedTwo

# The Function we need is used to determine
def GameOver(grid): # whether the game ends:
    '''
    PRE: The fucntion requires the current grid.
    POST: Returns either "Reject" or "Approved".
    '''

    # Checks for zeros in list
    for row in grid:
        if 0 in row:
            return True

    # Checks for horizontal merging:
    for row in grid:
        for col in range(len(row) - 1):
            if row[col] == row[col + 1]:
                return True

    # Checks for vertical merging:
    for row in range(len(grid) - 1):
        for col in range(len(grid[row])):
            if grid[row][col] == grid[row + 1][col]:
                return True

    return False

# Game Loop:
while True:

    # Loops when the player presses the key
    if Direction is not None: # on keyboard:
        OldGrid = copy.deepcopy(GameGrid)

        # The Motion System:
        if Direction == "Up":
            MoveUp(GameGrid)
        elif Direction == "Down":
            MoveDown(GameGrid)
        elif Direction == "Left":
            MoveLeft(GameGrid)
        elif Direction == "Right":
            MoveRight(GameGrid)

        # Resets the direction after
        Direction = None # each move:

        # Checks whether the copy of the actual grid changes, and if it does so,
        if OldGrid != GameGrid: # then a new number appears and prints the grid:
            Number = DropRate()
            NewNumber(Number)

            ClearScreen()
            InstructionsScreen()
            PrintGrid(GameGrid)

        # Checks for winning or losing after 
        for row in GameGrid: # each movement:
            if GameOver(GameGrid) == False:
                print("YOU LOST: NO MORE MOVES!", "\n")
                sys.exit()

            elif 2048 in row:
                print("YOU WIN: 2048 ACHIEVED!", "\n")
                sys.exit()

'''
NOTE: The whole code as well as design of the project were completed by myself, when
AI assistance was used only for debugging and troubleshooting during the development.
'''
