import pygame
import sys
from pygame.locals import *
pygame.init()
from collections import deque
import heapq

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
PLAYER_SIZE = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.Font(None, 36)
button1_rect = pygame.Rect(470, 10, 120, 50)
button2_rect = pygame.Rect(470,80, 120, 50)
button3_rect = pygame.Rect(470,150, 120, 50)
button4_rect = pygame.Rect(470,220, 120, 50)
button5_rect = pygame.Rect(470,290, 120, 50)
button6_rect = pygame.Rect(470,360, 120, 50)


visited_cells = []  # New list to store visited cells during DFS

def drawButtons():
    pygame.draw.rect(screen, BLACK, button1_rect, 1)
    pygame.draw.rect(screen, BLACK, button2_rect, 1)
    pygame.draw.rect(screen, BLACK, button3_rect, 1)
    pygame.draw.rect(screen, BLACK, button4_rect, 1)
    pygame.draw.rect(screen, BLACK, button5_rect, 1)
    pygame.draw.rect(screen, BLACK, button6_rect, 1)


    button1_text = "DFS"
    button1_text_surface = font.render(button1_text, True, BLACK)
    button1_text_rect = button1_text_surface.get_rect()
    button1_text_rect.center = (button1_rect.centerx, button1_rect.centery)
    screen.blit(button1_text_surface, button1_text_rect)

    button2_text = "BFS"
    button2_text_surface = font.render(button2_text, True, BLACK)
    button2_text_rect = button2_text_surface.get_rect()
    button2_text_rect.center = (button2_rect.centerx, button2_rect.centery)
    screen.blit(button2_text_surface, button2_text_rect)

    button3_text = "A*"
    button3_text_surface = font.render(button3_text, True, BLACK)
    button3_text_rect = button3_text_surface.get_rect()
    button3_text_rect.center = (button3_rect.centerx, button3_rect.centery)
    screen.blit(button3_text_surface, button3_text_rect)

    button4_text = "Dijkstra"
    button4_text_surface = font.render(button4_text, True, BLACK)
    button4_text_rect = button4_text_surface.get_rect()
    button4_text_rect.center = (button4_rect.centerx, button4_rect.centery)
    screen.blit(button4_text_surface, button4_text_rect)

    button5_text = "Greedy A*"
    button5_text_surface = font.render(button5_text, True, BLACK)
    button5_text_rect = button5_text_surface.get_rect()
    button5_text_rect.center = (button5_rect.centerx, button5_rect.centery)
    screen.blit(button5_text_surface, button5_text_rect)

    button6_text = "UCS"
    button6_text_surface = font.render(button6_text, True, BLACK)
    button6_text_rect = button6_text_surface.get_rect()
    button6_text_rect.center = (button6_rect.centerx, button6_rect.centery)
    screen.blit(button6_text_surface, button6_text_rect)

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 3, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

entrance_pos = [(row, col) for row in range(len(maze)) for col in range(len(maze[0])) if maze[row][col] == 2][0]
exit_pos = [(row, col) for row in range(len(maze)) for col in range(len(maze[0])) if maze[row][col] == 3][0]

player1_y, player1_x = entrance_pos
player2_y, player2_x = entrance_pos

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

clock = pygame.time.Clock()

auto_mode_a_star = False
a_star_steps_player2 = []
current_step_a_star_player2 = 0


auto_mode_dijkstra = False
dijkstra_steps_player2 = []
current_step_dijkstra_player2 = 0

def ucs_search_player2(maze, start_pos, exit_pos):
    heap = [(0, start_pos, [])]
    visited = set()

    while heap:
        cost, (row, col), path = heapq.heappop(heap)

        if (row, col) == exit_pos:
            return path

        if (row, col) in visited:
            continue

        visited.add((row, col))
        maze[row][col] = 4  # Mark the path in the maze
        pygame.time.delay(100)  # Delay for visualization
        draw_maze(maze, (255, 255, 0))  # Draw the maze with the path
        pygame.display.flip()
        pygame.event.pump()

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (
                0 <= new_row < len(maze)
                and 0 <= new_col < len(maze[0])
                and maze[new_row][new_col] != 1
                and (new_row, new_col) not in visited
            ):
                new_cost = cost + 1  # Uniform cost for each step
                heapq.heappush(heap, (new_cost, (new_row, new_col), path + [(new_row, new_col)]))

    return None

auto_mode_ucs = False
ucs_steps_player2 = []
current_step_ucs_player2 = 0

def greedy_a_star_search_player2(maze, start_pos, exit_pos):
    heap = [(heuristic(start_pos, exit_pos), start_pos, [])]
    visited = set()

    while heap:
        _, (row, col), path = heapq.heappop(heap)

        if (row, col) == exit_pos:
            return path

        if (row, col) in visited:
            continue

        visited.add((row, col))
        maze[row][col] = 4  # Mark the path in the maze
        pygame.time.delay(100)  # Delay for visualization
        draw_maze(maze, (255, 255, 0))  # Draw the maze with the path
        pygame.display.flip()
        pygame.event.pump()

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (
                0 <= new_row < len(maze)
                and 0 <= new_col < len(maze[0])
                and maze[new_row][new_col] != 1
                and (new_row, new_col) not in visited
            ):
                heapq.heappush(heap, (heuristic((new_row, new_col), exit_pos), (new_row, new_col), path + [(new_row, new_col)]))

    return None

auto_mode_greedy_a = False
greedy_a_steps_player2 = []
current_step_greedy_a_player2 = 0

def dijkstra_search_player2(maze, start_pos, exit_pos):
    heap = [(0, start_pos, [])]
    visited = set()

    while heap:
        _, (row, col), path = heapq.heappop(heap)

        if (row, col) == exit_pos:
            return path

        if (row, col) in visited:
            continue

        visited.add((row, col))
        maze[row][col] = 4  # Mark the path in the maze
        pygame.time.delay(100)  # Delay for visualization
        draw_maze(maze, (255, 255, 0))  # Draw the maze with the path
        pygame.display.flip()
        pygame.event.pump()

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (
                0 <= new_row < len(maze)
                and 0 <= new_col < len(maze[0])
                and maze[new_row][new_col] != 1
                and (new_row, new_col) not in visited
            ):
                heapq.heappush(heap, (0, (new_row, new_col), path + [(new_row, new_col)]))

    return None

def heuristic(pos, exit_pos):
    return abs(pos[0] - exit_pos[0]) + abs(pos[1] - exit_pos[1])

def a_star_search_player2(maze, start_pos, exit_pos):
    heap = [(0, start_pos, [])]
    visited = set()

    while heap:
        f_cost, (row, col), path = heapq.heappop(heap)

        if (row, col) == exit_pos:
            return path

        if (row, col) in visited:
            continue

        visited.add((row, col))
        maze[row][col] = 4  # Mark the path in the maze
        pygame.time.delay(100)  # Delay for visualization
        draw_maze(maze, (255, 255, 0))  # Draw the maze with the path
        pygame.display.flip()
        pygame.event.pump()

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (
                0 <= new_row < len(maze)
                and 0 <= new_col < len(maze[0])
                and maze[new_row][new_col] != 1
                and (new_row, new_col) not in visited
            ):
                g_cost = len(path)  # g-cost is the length of the path so far
                h_cost = heuristic((new_row, new_col), exit_pos)
                f_cost = g_cost + h_cost
                heapq.heappush(heap, (f_cost, (new_row, new_col), path + [(new_row, new_col)]))

    return None

def bfs_player2(maze, start_pos, exit_pos):
    queue = deque([(start_pos, [])])
    visited = set()

    while queue:
        (row, col), path = queue.popleft()
        if (row, col) == exit_pos:
            return path
        if (row, col) in visited:
            continue
        visited.add((row, col))
        maze[row][col] = 4  # Mark the path in the maze
        pygame.time.delay(100)  # Delay for visualization
        draw_maze(maze, (255, 255, 0))  # Draw the maze with the path
        pygame.display.flip()
        pygame.event.pump()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]) and maze[new_row][new_col] != 1 and (new_row, new_col) not in visited):
                queue.append(((new_row, new_col), path + [(new_row, new_col)]))
    return None
auto_mode_bfs = False
bfs_steps_player2 = []
current_step_bfs_player2 = 0

def dfs_player2(maze, current_pos, visited, steps):
    row, col = current_pos
    visited[row][col] = True
    visited_cells.append((row, col))  # Store the visited cell
    maze[row][col] = 4  # Mark the path in the maze
    pygame.time.delay(100)  # Delay for visualization
    draw_maze(maze, (255, 255, 0))  # Draw the maze with the path
    pygame.display.flip()
    pygame.event.pump()
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
def draw_maze(maze, player_color):
    screen.fill(WHITE)
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, BLACK, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif maze[row][col] == 2:
                pygame.draw.rect(screen, (0, 255, 0), (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif maze[row][col] == 3:
                pygame.draw.rect(screen, (255, 0, 0), (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif maze[row][col] == 4:  # Path color
                pygame.draw.rect(screen, player_color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw the players
    pygame.draw.rect(screen, (0, 0, 255), (player1_x * GRID_SIZE, player1_y * GRID_SIZE, PLAYER_SIZE, PLAYER_SIZE))
    pygame.draw.rect(screen, (255, 0, 0), (player2_x * GRID_SIZE, player2_y * GRID_SIZE, PLAYER_SIZE, PLAYER_SIZE))

    drawButtons()
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
            elif button2_rect.collidepoint(mouse_x, mouse_y):
                auto_mode_bfs = True
                bfs_steps_player2 = bfs_player2(maze, (player2_y, player2_x), exit_pos)
            elif button3_rect.collidepoint(mouse_x, mouse_y):
                auto_mode_a_star = True
                a_star_steps_player2 = a_star_search_player2(maze, (player2_y, player2_x), exit_pos)
            elif button4_rect.collidepoint(mouse_x, mouse_y):
                auto_mode_dijkstra = True
                dijkstra_steps_player2 = dijkstra_search_player2(maze, (player2_y, player2_x), exit_pos)
            elif button5_rect.collidepoint(mouse_x, mouse_y):
                auto_mode_greedy_a = True
                greedy_a_steps_player2 = greedy_a_star_search_player2(maze, (player2_y, player2_x), exit_pos)
            elif button6_rect.collidepoint(mouse_x, mouse_y):
                auto_mode_ucs = True
                ucs_steps_player2 = ucs_search_player2(maze, (player2_y, player2_x), exit_pos)
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
    draw_maze(maze,(255, 255, 255))

    if auto_mode and current_step_player2 < len(dfs_steps_player2):
        current_pos_player2 = dfs_steps_player2[current_step_player2]
        pygame.draw.rect(screen, (255, 0, 0),(current_pos_player2[1] * GRID_SIZE,current_pos_player2[0] * GRID_SIZE,GRID_SIZE,GRID_SIZE,), 3,)
        player2_y, player2_x = current_pos_player2
        current_step_player2 += 1

    if auto_mode_bfs and current_step_bfs_player2 < len(bfs_steps_player2):
        current_pos_bfs_player2 = bfs_steps_player2[current_step_bfs_player2]
        pygame.draw.rect(screen, (255, 0, 0), (current_pos_bfs_player2[1] * GRID_SIZE, current_pos_bfs_player2[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE,), 3)
        player2_y, player2_x = current_pos_bfs_player2
        current_step_bfs_player2 += 1
    if auto_mode_a_star and current_step_a_star_player2 < len(a_star_steps_player2):
        current_pos_a_star_player2 = a_star_steps_player2[current_step_a_star_player2]
        pygame.draw.rect(screen, (255, 0, 0), (current_pos_a_star_player2[1] * GRID_SIZE, current_pos_a_star_player2[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE), 3)
        player2_y, player2_x = current_pos_a_star_player2
        current_step_a_star_player2 += 1
    elif auto_mode_dijkstra and current_step_dijkstra_player2 < len(dijkstra_steps_player2):
        current_pos_dijkstra_player2 = dijkstra_steps_player2[current_step_dijkstra_player2]
        pygame.draw.rect(screen, (255, 0, 0), (current_pos_dijkstra_player2[1] * GRID_SIZE, current_pos_dijkstra_player2[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE), 3)
        player2_y, player2_x = current_pos_dijkstra_player2
        current_step_dijkstra_player2 += 1
    if auto_mode_greedy_a and current_step_greedy_a_player2 < len(greedy_a_steps_player2):
        current_pos_greedy_a_player2 = greedy_a_steps_player2[current_step_greedy_a_player2]
        pygame.draw.rect(screen, (255, 0, 0), ( current_pos_greedy_a_player2[1] * GRID_SIZE, current_pos_greedy_a_player2[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE),3)
        player2_y, player2_x = current_pos_greedy_a_player2
        current_step_greedy_a_player2 += 1
    if auto_mode_ucs and current_step_ucs_player2 < len(ucs_steps_player2):
        current_pos_ucs_player2 = ucs_steps_player2[current_step_ucs_player2]
        pygame.draw.rect(screen, (255, 0, 0), (current_pos_ucs_player2[1] * GRID_SIZE, current_pos_ucs_player2[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE), 3)
        player2_y, player2_x = current_pos_ucs_player2
        current_step_ucs_player2 += 1
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