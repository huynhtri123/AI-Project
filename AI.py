import pygame
import sys
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 500, 500
GRID_SIZE = 20
PLAYER_SIZE = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.Font(None, 36)
button1_rect = pygame.Rect(330, 10, 120, 50)

visited_cells = []  # New list to store visited cells during DFS

def drawButtons():
    pygame.draw.rect(screen, BLACK, button1_rect, 1)

    button1_text = "Auto"
    button1_text_surface = font.render(button1_text, True, BLACK)
    button1_text_rect = button1_text_surface.get_rect()
    button1_text_rect.center = (button1_rect.centerx, button1_rect.centery)
    screen.blit(button1_text_surface, button1_text_rect)

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 3, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

entrance_pos = [(row, col) for row in range(len(maze)) for col in range(len(maze[0])) if maze[row][col] == 2][0]
exit_pos = [(row, col) for row in range(len(maze)) for col in range(len(maze[0])) if maze[row][col] == 3][0]

player1_y, player1_x = entrance_pos
player2_y, player2_x = entrance_pos

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

clock = pygame.time.Clock()

def dfs_player2(maze, current_pos, visited, steps):
    row, col = current_pos
    visited[row][col] = True
    visited_cells.append((row, col))  # Store the visited cell

    if current_pos == exit_pos:
        steps.append((row, col))
        return True

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if (
            0 <= new_row < len(maze)
            and 0 <= new_col < len(maze[0])
            and maze[new_row][new_col] != 1
            and not visited[new_row][new_col]
        ):
            steps.append((new_row, new_col))
            if dfs_player2(maze, (new_row, new_col), visited, steps):
                return True
            steps.pop()

    return False

visited_player2 = [[False] * len(maze[0]) for _ in range(len(maze))]
dfs_steps_player2 = []
current_step_player2 = 0

auto_mode = False

while True:
    drawButtons()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button1_rect.collidepoint(mouse_x, mouse_y):
                auto_mode = True
                solvable = dfs_player2(maze, (player2_y, player2_x), visited_player2, dfs_steps_player2)
        elif not auto_mode and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and player1_y > 0 and maze[player1_y - 1][player1_x] != 1:
                player1_y -= 1
            elif event.key == pygame.K_DOWN and player1_y < len(maze) - 1 and maze[player1_y + 1][player1_x] != 1:
                player1_y += 1
            elif event.key == pygame.K_LEFT and player1_x > 0 and maze[player1_y][player1_x - 1] != 1:
                player1_x -= 1
            elif event.key == pygame.K_RIGHT and player1_x < len(maze[0]) - 1 and maze[player1_y][player1_x + 1] != 1:
                player1_x += 1

            if event.key == pygame.K_w and player2_y > 0 and maze[player2_y - 1][player2_x] != 1:
                player2_y -= 1
            elif event.key == pygame.K_s and player2_y < len(maze) - 1 and maze[player2_y + 1][player2_x] != 1:
                player2_y += 1
            elif event.key == pygame.K_a and player2_x > 0 and maze[player2_y][player2_x - 1] != 1:
                player2_x -= 1
            elif event.key == pygame.K_d and player2_x < len(maze[0]) - 1 and maze[player2_y][player2_x + 1] != 1:
                player2_x += 1

    screen.fill(WHITE)
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, BLACK, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif maze[row][col] == 2:
                pygame.draw.rect(screen, (0, 255, 0), (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif maze[row][col] == 3:
                pygame.draw.rect(screen, (0, 0, 255), (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    for row, col in visited_cells:
        pygame.draw.rect(screen, (255, 255, 0), (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen, (0, 0, 255), (player1_x * GRID_SIZE, player1_y * GRID_SIZE, PLAYER_SIZE, PLAYER_SIZE))

    if auto_mode and current_step_player2 < len(dfs_steps_player2):
        current_pos_player2 = dfs_steps_player2[current_step_player2]
        pygame.draw.rect(screen, (255, 0, 0),( current_pos_player2[1] * GRID_SIZE,current_pos_player2[0] * GRID_SIZE,GRID_SIZE,GRID_SIZE,), 3,)
        player2_y, player2_x = current_pos_player2
        current_step_player2 += 1

    pygame.draw.rect(screen, (255, 0, 0), (player2_x * GRID_SIZE, player2_y * GRID_SIZE, PLAYER_SIZE, PLAYER_SIZE))

    drawButtons()
    pygame.display.flip()

    if (player1_y, player1_x) == exit_pos:
        print("Xanh thang")
        pygame.quit()
        sys.exit()
    elif (player2_y, player2_x) == exit_pos:
        print("Do thang")
        pygame.quit()
        sys.exit()

    clock.tick(10)