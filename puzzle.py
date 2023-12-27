import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 4
TILE_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sliding Puzzle")

# Fonts
font = pygame.font.Font(None, 36)

# Function to draw the grid
def draw_grid(board):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(screen, WHITE, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)
            if board[row][col] != 0:
                text = font.render(str(board[row][col]), True, BLACK)
                text_rect = text.get_rect(center=(col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2))
                screen.blit(text, text_rect)

# Function to check if the puzzle is solved
def is_solved(board):
    return all(board[row][col] == row * GRID_SIZE + col + 1 for row in range(GRID_SIZE) for col in range(GRID_SIZE - 1))

# Function to shuffle the puzzle
def shuffle_board(board):
    flat_board = [tile for row in board for tile in row]
    random.shuffle(flat_board)
    return [flat_board[i:i+GRID_SIZE] for i in range(0, len(flat_board), GRID_SIZE)]

# Initialize game board
original_board = [[row * GRID_SIZE + col + 1 for col in range(GRID_SIZE)] for row in range(GRID_SIZE)]
original_board[GRID_SIZE - 1][GRID_SIZE - 1] = 0  # Empty tile
current_board = shuffle_board(original_board.copy())

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            empty_row, empty_col = [(row, col) for row in range(GRID_SIZE) for col in range(GRID_SIZE) if current_board[row][col] == 0][0]

            if event.key == pygame.K_UP and empty_row < GRID_SIZE - 1:
                current_board[empty_row][empty_col], current_board[empty_row + 1][empty_col] = current_board[empty_row + 1][empty_col], current_board[empty_row][empty_col]

            elif event.key == pygame.K_DOWN and empty_row > 0:
                current_board[empty_row][empty_col], current_board[empty_row - 1][empty_col] = current_board[empty_row - 1][empty_col], current_board[empty_row][empty_col]

            elif event.key == pygame.K_LEFT and empty_col < GRID_SIZE - 1:
                current_board[empty_row][empty_col], current_board[empty_row][empty_col + 1] = current_board[empty_row][empty_col + 1], current_board[empty_row][empty_col]

            elif event.key == pygame.K_RIGHT and empty_col > 0:
                current_board[empty_row][empty_col], current_board[empty_row][empty_col - 1] = current_board[empty_row][empty_col - 1], current_board[empty_row][empty_col]

    screen.fill(WHITE)
    draw_grid(current_board)

    if is_solved(current_board):
        text = font.render("Puzzle Solved!", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()
    pygame.time.Clock().tick(30)
