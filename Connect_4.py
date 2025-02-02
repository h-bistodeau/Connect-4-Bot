
# Hailey Bistodeau 10/21
# for this project I made three additional helper functions to handle the strategy and to pull it into the minimax function
# the first function I created was ideal_move and that is the function that breaks apart the board into smaller/more manageable
# sections. To do this I created 1x4 sections going horizonal, vertical, and both positive and negative diagonals. With these
# smaller sections I move into my evaluate_move function because that works directly with ideal_move. Evaluate_Move is what gives
# the ai 'points' for certain movements or strategies. I could have just had these two functions combined but it got repetitive
# so i chose to just call evaluate_move within ideal move (as you'll probably see). The last is the choose_move function which
# compares the scores of potential moves and keeps track of the best possible score and the column associated with that score.

import pygame
import statistics
import sys
import math
import numpy as np
import random
import time  # Import time module to measure AI move time
import matplotlib
matplotlib.use('Agg') # doesn't show the graph onscreen but adds it as a file downloaded to your laptop (geeksforgeeks.com)
import matplotlib.pyplot as plt

# Initialize Pygame
pygame.init()

# Define colors for the game
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Define constants for the game (e.g., board size and Connect 4 rule)
ROW_COUNT = 6
COLUMN_COUNT = 7
CONNECT = 4  # Number of pieces needed to connect (can be changed for Connect 5/6)
# so to make this work originally i just had a variable within the functions that was static but that wont work quite right
# so i basically set my function variable ('section') equal to count and added in an extra step to the for loops of ideal_move
# to better handle the increased count


# Screen setup constants
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 5)

# Initialize the Pygame display window
screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("monospace", 75)

# AI timing variables to measure how long the AI takes for each move
total_time = 0
move_count = 0

# Create a blank Connect 4 board (6 rows by 7 columns filled with zeros)
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# Drop a piece in the specified location on the board
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Check if a column is a valid move (i.e., if there's space to drop a piece)
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0  # True if top row in column is empty

# Get the next open row for a piece in a specific column
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:  # Return the first open row (bottom-most available space)
            return r

# Print the board in a way that's visually helpful (flipped so player sees it correctly)
def print_board(board):
    print(np.flip(board, 0))  # Flip the board for display purposes (row 0 at the bottom)

# Check if a player has won the game by connecting pieces
def winning_move(board, piece):
    # Check horizontal locations for a win
    for c in range(COLUMN_COUNT - CONNECT + 1):
        for r in range(ROW_COUNT):
            if np.all(board[r, c:c+CONNECT] == piece):
                return True

    # Check vertical locations for a win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - CONNECT + 1):
            if np.all(board[r:r+CONNECT, c] == piece):
                return True

    # Check positively sloped diagonals (bottom-left to top-right)
    for c in range(COLUMN_COUNT - CONNECT + 1):
        for r in range(ROW_COUNT - CONNECT + 1):
            if all([board[r+i][c+i] == piece for i in range(CONNECT)]):
                return True

    # Check negatively sloped diagonals (top-left to bottom-right)
    for c in range(COLUMN_COUNT - CONNECT + 1):
        for r in range(CONNECT-1, ROW_COUNT):
            if all([board[r-i][c+i] == piece for i in range(CONNECT)]):
                return True

    return False  # No win found

# Minimax function to determine the best move for the AI
def minimax(board, depth, maximizingPlayer):
    valid_locations = get_valid_locations(board)  # Get valid columns to drop the piece
    is_terminal = is_terminal_node(board)

    # Terminal state evaluation (game over: win/loss/draw)
    # here is where you will add Max depth and the return of the evaluation
    #function

    if is_terminal or depth == 0:
        if is_terminal:
        # Finish this after the alpha beta pruning is worked out
        # set the max depth for the minimax and make sure to return it so that it can be used for a heuristic evaluation
            # new variable bsed on the heurstics to be set.
            if winning_move(board, 2):
                return (None, 100000000000000)  # Large score for AI win
            elif winning_move(board, 1):
                return (None, -10000000000000)  # Large negative score for player win
            else:  # Game over, no moves left
                return (None, 0)
        else: # Ai is piece 2
            return None, ideal_move(board, 2)

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)

        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()  # Copy the board
            drop_piece(b_copy, row, col, 2)
            new_score = minimax(b_copy, depth-1, False)[1]

            if new_score > value:
                value = new_score
                column = col

        return column, value

    else:
        value = math.inf
        column = random.choice(valid_locations)

        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, 1)
            #gets the min value between the current value and the child node below it (depth-1)
            new_score = minimax(b_copy, depth-1, True)[1]

            if new_score < value:
                value = new_score
                column = col

        return column, value

def evaluate_move(section, piece):
    score = 0
    opponent = 2 if piece == 1 else 1 #optimized if statement (i looked up how to get it on one line since the file is long enough)

    # blocking the opponent (piece = 2) has a high priority so it will avoid beign penalized
    if section.count(opponent) == (CONNECT - 1) and section.count(0) == (CONNECT - 3):
        score -= 450

    # gives points for the Ai getting a certain amount of pieces in a row (all 4, 3 and 2 with 4 getting most points)
    if section.count(piece) == CONNECT:
        score += 200
    elif section.count(piece) == (CONNECT - 1) and section.count(0) == (CONNECT - 3):
        score += 10
    elif section.count(piece) == 2 and section.count(0) == 2:
        score += 5

    return score

def ideal_move(board, piece):
    score = 0
    section_length = CONNECT

    # should fine the center column of the board in order to try and control that center meaning more win options further down the line
    # I added this functionality in last (after the other window counting (so the list syntax is explained)
    center_list = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_score = center_list.count(piece)
    score += center_score * 6 # gives a bunch more points for having pieces in the center

    # take a look at all the horizontal positions by looking at 1x4 rectangles and seeing how many pieces are in each
    # so basically I want to look at the first four spots in each row then shift over by one and look at the next section of four
    for row in range(ROW_COUNT):
        row_list = list(board[row,:])
        for c in range(COLUMN_COUNT - section_length + 1):
            section = row_list[c: c + section_length]
            score += evaluate_move(section, piece)

        # vertical sectioning, checking for how many pieces are within groupings of four and prioritizing the locations
        # with the most pices in a line vertically. (legit the same as horizontal above but swapped rows and columns)
    for col in range(COLUMN_COUNT):
        col_list = list(board[:,col])  # Same as the horizontal list just with columns
        for r in range(ROW_COUNT - section_length + 1):
            section = col_list[r: r + section_length]
            score += evaluate_move(section, piece)

# diagonal (positively sloped) by always adding one to each row and column in the list to get proper sectioning
# Easiest of the diagonals as you just add one to both the row and the column
    for row in range(ROW_COUNT - section_length + 1):
        for col in range(COLUMN_COUNT - section_length + 1):
            section = [board[row + i, col + i] for i in range(section_length)] # typically I would have this separated out but it
        #caused some errors so I looked up a way to optimize creating this list (geeks for geeks.com)
            score += evaluate_move(section, piece)

#negatively sloped diagonal by adding three to the row to get that very first top piece
# This one was pretty tricky, so the very first piece in this window is the highest, so you need to account for that then
# subtract i from there. (other then that its the same section and score evaluation
    for row in range(ROW_COUNT - section_length + 1):
        for col in range(COLUMN_COUNT - section_length + 1):
            section = [board[row + 3 - i, col + i] for i in range(section_length)]
            score += evaluate_move(section, piece)

    return score

def choose_ideal_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -100000 # initialize a really low negative number as i do deduct points so negativity is a option
    best_column = random.choice(valid_locations) #start with a random column then update upon score eval.

    # look through each of the columns and find the score to compare and find the best score for the given board
    for column in valid_locations:
        row = get_next_open_row(board, column)
        b_copy = board.copy()
        drop_piece(b_copy, row, column, piece)
        score = ideal_move(b_copy, piece) # run our ideal move function

        # compare the two potential scores and save that score and the column of that score so that it isn't lost
        if score > best_score:
            best_score = score
            best_column = column

    return best_column # we don't really need the score at this point it was purely for evaluation/strategy so only return column

# Get a list of all valid columns (i.e., those with open spaces)
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

# Check if the game is over (win or no valid moves left)
def is_terminal_node(board):
    return winning_move(board, 1) or winning_move(board, 2) or len(get_valid_locations(board)) == 0

# Function to draw the board (visual representation)
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):      
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()  # Update the display with the new board state


# Main game logic
board = create_board()  # Create the initial empty board
print_board(board)
game_over = False
turn = 0  # Variable to track turns (0 for Player 1, 1 for Player 2/AI)

draw_board(board)  # Draw the initial empty board

# Main game loop
while not game_over:
    # Event handler to check for user input and quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the user closes the game window
            sys.exit()

        # Display the piece that the human player is about to drop
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))  # Clear the top row
            posx = event.pos[0]  # Get the x-position of the mouse
            if turn == 0:  # Player 1's turn
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:  # Player 2's (AI's) turn
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()  # Update the display

        # Handle mouse click event (drop a piece)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))  # Clear the top row
            if turn == 0:  # Player 1's turn
                posx = event.pos[0]  # Get the x-position of the click
                col = int(math.floor(posx/SQUARESIZE))  # Determine the column based on the x-position

                if is_valid_location(board, col):  # Check if the column is valid
                    row = get_next_open_row(board, col)  # Get the next open row in the column
                    drop_piece(board, row, col, 1)  # Drop Player 1's piece

                    if winning_move(board, 1):  # Check if Player 1 wins
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40, 10))  # Display the winning message
                        game_over = True  # End the game

                    turn += 1  # Switch to the next turn
                    turn = turn % 2  # Ensure turn alternates between 0 and 1

                    print_board(board)  # Print the board to the console
                    draw_board(board)  # Draw the updated board

    # AI's turn (Player 2)
    if turn == 1 and not game_over:

        start_time = time.time()  # Start timer to measure AI move time
        #here is where you will call min/max
        col, minimax_score = minimax(board, 4, False)  # Make AI choose a random column for now

        end_time = time.time()  # Stop the timer
        time_taken = end_time - start_time  # Calculate the time taken for the AI's move

        # Update the total time and number of moves for performance analysis
        total_time += time_taken
        move_count += 1

        print(f"AI Move Time: {time_taken:.4f} seconds")  # Print the time for the current move
        print(f"Average AI Move Time: {total_time / move_count:.4f} seconds")  # Print the average move time

        if is_valid_location(board, col):  # Check if the column is valid
            pygame.time.wait(500)  # Delay for visual effect
            row = get_next_open_row(board, col)  # Get the next open row in the column
            drop_piece(board, row, col, 2)  # Drop the AI's piece

            if winning_move(board, 2):  # Check if the AI wins
                label = myfont.render("Player 2 wins!!", 1, YELLOW)
                screen.blit(label, (40, 10))  # Display the winning message
                game_over = True  # End the game

            print_board(board)  # Print the board to the console
            draw_board(board)  # Draw the updated board

            turn += 1  # Switch to the next turn
            turn = turn % 2  # Ensure turn alternates between 0 and 1

    # End the game if someone has won
    if game_over:
        pygame.time.wait(3000)  # Wait for 3 seconds before exiting
