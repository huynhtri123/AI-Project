import pygame
import sys
from pygame.locals import *
from collections import deque
import heapq
import time as timeL
import copy
import mazemap
import history_io

pygame.init()

#SETTING
WIDTH, HEIGHT = 900, 770
GRID_SIZE = 30
PLAYER_SIZE = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
XANH = (0,195,0)
XANH2 = (60,179,113)
RED = (205,32,31)
XANHLA = (0, 255, 0)
VANG = (255, 255, 0)

font = pygame.font.Font(None, 36)
button1_dfs_rect = pygame.Rect(750, 10, 120, 50)
button2_bfs_rect = pygame.Rect(750, 80, 120, 50)
button3_astar_rect = pygame.Rect(750, 150, 120, 50)
button4_dijkstra_rect = pygame.Rect(750, 220, 120, 50)
button5_greedy_rect = pygame.Rect(750, 290, 120, 50)
button6_ucs_rect = pygame.Rect(750, 360, 120, 50)
button7_pause_rect = pygame.Rect(750, 430, 120, 50)
button8_nextmap_rect = pygame.Rect(750, 500, 120, 50)
button9_premap_rect = pygame.Rect(750, 570, 120, 50)
button10_step_rect = pygame.Rect(10, 700, 120, 50)
button11_time_rect = pygame.Rect(110, 700, 120, 50)
button12_restart_rect = pygame.Rect(250, 700, 120, 50)
button13_nodes_rect = pygame.Rect(360, 700, 120, 50)
button14_Time_rect = pygame.Rect(750, 640, 120, 50)
button15_result_rect = pygame.Rect(490, 700, 120, 50)
button16_Steps_rect = pygame.Rect(600, 700, 120, 50)
button17_history_rect = pygame.Rect(750, 700, 120, 50)

wall_img = pygame.image.load("images/brick.png")
scaled_wall_img = pygame.transform.scale(wall_img, (GRID_SIZE, GRID_SIZE))

boy_img = pygame.image.load("images/boyrun.png");
scaled_boy_img = pygame.transform.scale(boy_img, (GRID_SIZE, GRID_SIZE))

girl_img = pygame.image.load("images/girlrun.png");
scaled_girl_img = pygame.transform.scale(girl_img, (GRID_SIZE, GRID_SIZE))

house_img = pygame.image.load("images/house.png");
scaled_house_img = pygame.transform.scale(house_img, (GRID_SIZE, GRID_SIZE))

mazes = [mazemap.maze0, mazemap.maze1, mazemap.maze2, mazemap.maze3, mazemap.maze4, mazemap.maze5, mazemap.maze6, mazemap.maze7, mazemap.maze8, mazemap.maze9]
maze = copy.deepcopy(mazemap.maze0)

entrance_pos = [(row, col) for row in range(len(maze)) for col in range(len(maze[0])) if maze[row][col] == 2][0]
exit_pos = [(row, col) for row in range(len(maze)) for col in range(len(maze[0])) if maze[row][col] == 3][0]

player1_y, player1_x = entrance_pos
player2_y, player2_x = entrance_pos

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()

#màn hình thứ 2 (khi ấn lịch sử)
open_window = False
original_size = screen.get_size()

#Function
def drawButtons(step, time, result):
    mouse_pos = pygame.mouse.get_pos()
    buttons = [button1_dfs_rect, button2_bfs_rect, button3_astar_rect, button4_dijkstra_rect, button5_greedy_rect, 
               button6_ucs_rect, button7_pause_rect, button8_nextmap_rect, button9_premap_rect, button11_time_rect, 
               button13_nodes_rect, button14_Time_rect, button10_step_rect, button12_restart_rect, button16_Steps_rect, 
               button15_result_rect, button17_history_rect]
    button_texts = ["DFS", "BFS", "A*", "Dijkstra", "Greedy", "UCS", 
                    "PAUSE","NextMap","PrevMap", step, time, "Restart", "Nodes", "Time", result, "Steps", "History"]

    for i in range(len(buttons)):
        if buttons[i].collidepoint(mouse_pos):  
            #hover
            pygame.draw.rect(screen, XANH, buttons[i])
            pygame.draw.rect(screen, YELLOW, buttons[i], 1)
        else:   
            #ko hover
            pygame.draw.rect(screen, XANH2, buttons[i])
            pygame.draw.rect(screen, BLACK, buttons[i], 1)
        # Vẽ chữ lên button
        button_text_surface = font.render(button_texts[i], True, BLACK)
        button_text_rect = button_text_surface.get_rect()
        button_text_rect.center = (buttons[i].centerx, buttons[i].centery)
        screen.blit(button_text_surface, button_text_rect)

def draw_maze(maze, player_color):
    global step
    global time
    screen.fill(WHITE)
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 1:
                screen.blit(scaled_wall_img, (col * GRID_SIZE, row * GRID_SIZE))
            elif maze[row][col] == 2:
                pygame.draw.rect(screen, XANHLA, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif maze[row][col] == 3:
                screen.blit(scaled_house_img, (col * GRID_SIZE, row * GRID_SIZE))
            elif maze[row][col] == 4:  #đường đi trong quá trình tìm kiếm (tô màu vàng)
                pygame.draw.rect(screen, player_color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif maze[row][col] == 5:  #đường đi cuối cùng (tô màu xanh lá)
                pygame.draw.rect(screen, XANHLA, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    # Draw the players
    screen.blit(scaled_boy_img, (player1_x * GRID_SIZE, player1_y * GRID_SIZE))
    screen.blit(scaled_girl_img, (player2_x * GRID_SIZE, player2_y * GRID_SIZE))
    drawButtons(step, time, result)

def display_text(text, color, position):
    font = pygame.font.Font(None, 72) 
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

def draw_final_path(maze, path):
    global result
    for row, col in path:
        maze[row][col] = 5
        result=int(result)+1
        result=str(result)
    a,b = exit_pos
    maze[a][b]=3
            
font1 = pygame.font.Font(None, 24)
def history_window(screen, width, height, history_list):
    cell_height = height // len(history_list)
    screen.fill(WHITE)  # Xóa màn hình và vẽ màu trắng

    for i, history_entry in enumerate(history_list):
        # Lấy giá trị từ từ điển
        algorithms_name = history_entry['algorithms_name']
        visited_nodes = history_entry['visited_nodes']
        execute_time = history_entry['execute_time']
        steps = history_entry['steps']
        player_win = history_entry['player_win']

        # Hiển thị thông tin của mỗi phần tử trên một dòng
        text = f"Algorithm: {algorithms_name}, Visited Nodes: {visited_nodes}, Execute Time: {execute_time}, Steps: {steps}, Player Win: {player_win}"
        text_render = font1.render(text, True, BLACK)
        text_rect = text_render.get_rect(center=(width // 2 + 300, i * cell_height + cell_height // 2))
        screen.blit(text_render, text_rect)

#THUAT TOAN
#UCS
auto_mode_ucs = False
ucs_steps_player2 = []
current_step_ucs_player2 = 0

def ucs_search_player2(maze, start_pos, exit_pos):
    heap = [(0, start_pos, [])]
    visited = set()
    global step
    while heap:
        cost, (row, col), path = heapq.heappop(heap)
        if (row, col) == exit_pos:
            draw_final_path(maze,path)
            return path
        if (row, col) in visited:
            continue
        step = int(step) + 1
        step = str(step)
        visited.add((row, col))
        maze[row][col] = 4  
        pygame.time.delay(50)  
        draw_maze(maze, VANG) 
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

#Greedy
auto_mode_greedy_a = False
greedy_a_steps_player2 = []
current_step_greedy_a_player2 = 0

def greedy_a_star_search_player2(maze, start_pos, exit_pos):
    heap = [(heuristic(start_pos, exit_pos), start_pos, [])]
    visited = set()
    global step
    while heap:
        _, (row, col), path = heapq.heappop(heap)

        if (row, col) == exit_pos:
            draw_final_path(maze,path)
            return path

        if (row, col) in visited:
            continue
        step = int(step) + 1
        step = str(step)
        visited.add((row, col))
        maze[row][col] = 4 
        pygame.time.delay(50)  
        draw_maze(maze, (255, 255, 0))  
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

#Dijkstra
auto_mode_dijkstra = False
dijkstra_steps_player2 = []
current_step_dijkstra_player2 = 0

def dijkstra_search_player2(maze, start_pos, exit_pos):
    # Thiết lập chi phí cho mỗi bước di chuyển
    step_cost = 1

    heap = [(0, start_pos, [])]
    visited = set()
    global step
    while heap:
        cost, (row, col), path = heapq.heappop(heap)

        if (row, col) == exit_pos:
            draw_final_path(maze, path)
            return path

        if (row, col) in visited:
            continue
        step = int(step) + 1
        step = str(step)
        visited.add((row, col))
        maze[row][col] = 4  
        pygame.time.delay(50) 
        draw_maze(maze, (255, 255, 0))  
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
                new_cost = cost + step_cost  # Sử dụng chi phí cho mỗi bước di chuyển
                heapq.heappush(heap, (new_cost, (new_row, new_col), path + [(new_row, new_col)]))

    return None

#A*
auto_mode_a_star = False
a_star_steps_player2 = []
current_step_a_star_player2 = 0

def heuristic(pos, exit_pos):
    return abs(pos[0] - exit_pos[0]) + abs(pos[1] - exit_pos[1])

def a_star_search_player2(maze, start_pos, exit_pos):
    heap = [(0, start_pos, [])] #cost, (row,col), path
    visited = set()
    global step
    while heap:
        f_cost, (row, col), path = heapq.heappop(heap)  #pop phần tử có cost nhỏ nhất (cũng là đầu heap)

        if (row, col) == exit_pos:
            draw_final_path(maze,path)
            return path

        if (row, col) in visited:
            continue
        step = int(step) + 1
        step = str(step)
        visited.add((row, col))
        maze[row][col] = 4  
        pygame.time.delay(50) 
        draw_maze(maze, (255, 255, 0)) 
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
                g_cost = len(path)  
                h_cost = heuristic((new_row, new_col), exit_pos)
                f_cost = g_cost + h_cost
                heapq.heappush(heap, (f_cost, (new_row, new_col), path + [(new_row, new_col)]))

    return None

#BFS
auto_mode_bfs = False
bfs_steps_player2 = []
current_step_bfs_player2 = 0

def bfs_player2(maze, start_pos, exit_pos):
    queue = deque([(start_pos, [])])
    visited = set()
    global step
    while queue:
        (row, col), path = queue.popleft()
        if (row, col) == exit_pos:
            draw_final_path(maze,path)
            return path
        if (row, col) in visited:
            continue
        step = int(step) + 1
        step = str(step)
        visited.add((row, col))
        maze[row][col] = 4  
        pygame.time.delay(50) 
        draw_maze(maze, (255, 255, 0))
        pygame.display.flip()
        pygame.event.pump()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]) and maze[new_row][new_col] != 1 and (new_row, new_col) not in visited):
                queue.append(((new_row, new_col), path + [(new_row, new_col)]))
    return None

#DFS
visited_cells = []  
visited_player2 = [[False] * len(maze[0]) for _ in range(len(maze))]
dfs_steps_player2 = []
current_step_player2 = 0
auto_mode_dfs = False

def dfs_player2(maze, current_pos, visited, steps):
    global step
    row, col = current_pos
    visited[row][col] = True
    visited_cells.append((row, col))  
    step = int(step) + 1
    step = str(step)
    maze[row][col] = 4  
    pygame.time.delay(50) 
    draw_maze(maze, (255, 255, 0))  
    pygame.display.flip()
    pygame.event.pump()
    if current_pos == exit_pos:
        steps.append((row, col))
        draw_final_path(maze,steps)
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

def add_new_history(player_win):
    global algorithms_name, step, time, result
    new_history = {
        'algorithms_name': algorithms_name,
        'visited_nodes': step,
        'execute_time': time,
        'steps': result,
        'player_win': player_win
    }
    history_list = history_io.load_history_list()
    history_list.append(new_history)
    history_io.save_history_list(history_list)

algorithms_name=None
step="0"
time="0"
result="0"
current_index=0
paused = False

while True:
    drawButtons(step,time,result)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button1_dfs_rect.collidepoint(mouse_x, mouse_y):
                algorithms_name="DFS"
                result="0"
                step ="0"
                paused = False
                auto_mode_dfs = True
                start_time = timeL.time()
                solvable = dfs_player2(maze, (player2_y, player2_x), visited_player2, dfs_steps_player2)
                end_time = timeL.time()
                execution_time = end_time - start_time
                execution_time = round(execution_time, 2)
                time=str(execution_time)+"s"
            elif button2_bfs_rect.collidepoint(mouse_x, mouse_y):
                algorithms_name = "BFS"
                result="0"
                step = "0"
                paused = False
                auto_mode_bfs = True
                start_time = timeL.time()
                bfs_steps_player2 = bfs_player2(maze, (player2_y, player2_x), exit_pos)
                end_time = timeL.time()
                execution_time = end_time - start_time
                execution_time = round(execution_time, 2)
                time=str(execution_time)+"s"
            elif button3_astar_rect.collidepoint(mouse_x, mouse_y):
                algorithms_name = "A*"
                step = "0"
                result="0"
                paused = False
                auto_mode_a_star = True
                start_time = timeL.time()
                a_star_steps_player2 = a_star_search_player2(maze, (player2_y, player2_x), exit_pos)
                end_time = timeL.time()
                execution_time = end_time - start_time
                execution_time = round(execution_time, 2)
                time=str(execution_time)+"s"
            elif button4_dijkstra_rect.collidepoint(mouse_x, mouse_y):
                algorithms_name = "Dijkstra"
                result="0"
                step = "0"
                paused = False
                auto_mode_dijkstra = True
                start_time = timeL.time()
                dijkstra_steps_player2 = dijkstra_search_player2(maze, (player2_y, player2_x), exit_pos)
                end_time = timeL.time()
                execution_time = end_time - start_time
                execution_time = round(execution_time, 2)
                time=str(execution_time)+"s"
            elif button5_greedy_rect.collidepoint(mouse_x, mouse_y):
                algorithms_name = "Greedy_A*"
                result="0"
                step = "0"
                paused = False
                auto_mode_greedy_a = True
                start_time = timeL.time()
                greedy_a_steps_player2 = greedy_a_star_search_player2(maze, (player2_y, player2_x), exit_pos)
                end_time = timeL.time()
                execution_time = end_time - start_time
                execution_time = round(execution_time, 2)
                time=str(execution_time)+"s"
            elif button6_ucs_rect.collidepoint(mouse_x, mouse_y):
                algorithms_name = "UCS"
                result="0"
                step = "0"
                paused = False
                auto_mode_ucs = True
                start_time = timeL.time()
                ucs_steps_player2 = ucs_search_player2(maze, (player2_y, player2_x), exit_pos)
                end_time = timeL.time()
                execution_time = end_time - start_time
                execution_time = round(execution_time, 2)
                time=str(execution_time)+"s"
            elif button7_pause_rect.collidepoint(mouse_x, mouse_y):
                algorithms_name=None
                result="0"
                step = "0"
                time="0"
                paused = True
                auto_mode_a_star=False
                auto_mode_bfs=False
                auto_mode_ucs=False
                auto_mode_dijkstra=False
                auto_mode_greedy_a=False
                auto_mode_dfs=False
                for row in range(len(maze)) :
                    for col in range(len(maze[0])):
                        if maze[row][col] == 4 or maze[row][col] == 5:
                            maze[row][col] = 0
            elif button8_nextmap_rect.collidepoint(mouse_x,mouse_y):
                algorithms_name = None
                result="0"
                time="0"
                step = "0"
                if current_index < len(mazes) - 1:
                    current_index += 1
                    maze = copy.deepcopy(mazes[current_index])
                    entrance_pos = [(row, col) for row in range(len(maze)) for col in range(len(maze[0])) if maze[row][col] == 2][0]
                    exit_pos = [(row, col) for row in range(len(maze)) for col in range(len(maze[0])) if maze[row][col] == 3][0]
                    player1_y, player1_x = entrance_pos
                    player2_y, player2_x = entrance_pos
                    draw_maze(maze, WHITE)
                    paused = True
                    auto_mode_a_star = False
                    auto_mode_bfs = False
                    auto_mode_ucs = False
                    auto_mode_dijkstra = False
                    auto_mode_greedy_a = False
                    auto_mode_dfs = False
                    current_step_a_star_player2 = 0
                    current_step_player2 = 0
                    current_step_bfs_player2 = 0
                    current_step_dijkstra_player2 = 0
                    current_step_greedy_a_player2 = 0
                    current_step_ucs_player2 = 0
                else:
                    display_text("Het map roi", XANH, (WIDTH // 2, HEIGHT // 2))
                    pygame.time.delay(2000)
            elif button9_premap_rect.collidepoint(mouse_x,mouse_y):
                algorithms_name = None
                result="0"
                time="0"
                step = "0"
                if current_index > 0:
                    current_index -= 1
                    maze = copy.deepcopy(mazes[current_index])
                    entrance_pos = [(row, col) for row in range(len(maze)) for col in range(len(maze[0])) if maze[row][col] == 2][0]
                    exit_pos = [(row, col) for row in range(len(maze)) for col in range(len(maze[0])) if maze[row][col] == 3][0]
                    player1_y, player1_x = entrance_pos
                    player2_y, player2_x = entrance_pos
                    draw_maze(maze, WHITE)
                    paused = True
                    auto_mode_a_star = False
                    auto_mode_bfs = False
                    auto_mode_ucs = False
                    auto_mode_dijkstra = False
                    auto_mode_greedy_a = False
                    auto_mode_dfs = False
                    current_step_a_star_player2 = 0
                    current_step_player2 = 0
                    current_step_bfs_player2 = 0
                    current_step_dijkstra_player2 = 0
                    current_step_greedy_a_player2 = 0
                    current_step_ucs_player2 = 0
                else:
                    display_text("Het map roi", XANH, (WIDTH // 2, HEIGHT // 2))
                    pygame.time.delay(2000)
            elif button14_Time_rect.collidepoint(mouse_x,mouse_y):
                algorithms_name = None
                result="0"
                time="0"
                step = "0"
                maze = copy.deepcopy(mazes[current_index])
                entrance_pos = [(row, col) for row in range(len(maze)) for col in range(len(maze[0])) if maze[row][col] == 2][0]
                exit_pos = [(row, col) for row in range(len(maze)) for col in range(len(maze[0])) if maze[row][col] == 3][0]
                player1_y, player1_x = entrance_pos
                player2_y, player2_x = entrance_pos
                draw_maze(maze, (WHITE))
                paused = True
                auto_mode_a_star = False
                auto_mode_bfs = False
                auto_mode_ucs = False
                auto_mode_dijkstra = False
                auto_mode_greedy_a = False
                auto_mode_dfs = False
                current_step_a_star_player2 = 0
                current_step_player2 = 0
                current_step_bfs_player2 = 0
                current_step_dijkstra_player2 = 0
                current_step_greedy_a_player2 = 0
                current_step_ucs_player2 = 0
            elif button17_history_rect.collidepoint(mouse_x,mouse_y):
                open_window = True

        elif not auto_mode_dfs and event.type == pygame.KEYDOWN:
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

    if auto_mode_dfs and current_step_player2 < len(dfs_steps_player2):
        current_pos_player2 = dfs_steps_player2[current_step_player2]
        player2_y, player2_x = current_pos_player2
        current_step_player2 += 1

    if auto_mode_bfs and not paused and current_step_bfs_player2 < len(bfs_steps_player2):
        current_pos_bfs_player2 = bfs_steps_player2[current_step_bfs_player2]
        player2_y, player2_x = current_pos_bfs_player2
        current_step_bfs_player2 += 1
    if auto_mode_a_star and not paused and current_step_a_star_player2 < len(a_star_steps_player2):
        current_pos_a_star_player2 = a_star_steps_player2[current_step_a_star_player2]
        player2_y, player2_x = current_pos_a_star_player2
        current_step_a_star_player2 += 1
    if auto_mode_dijkstra and not paused and current_step_dijkstra_player2 < len(dijkstra_steps_player2):
        current_pos_dijkstra_player2 = dijkstra_steps_player2[current_step_dijkstra_player2]
        player2_y, player2_x = current_pos_dijkstra_player2
        current_step_dijkstra_player2 += 1
    if auto_mode_greedy_a and not paused and current_step_greedy_a_player2 < len(greedy_a_steps_player2):
        current_pos_greedy_a_player2 = greedy_a_steps_player2[current_step_greedy_a_player2]
        player2_y, player2_x = current_pos_greedy_a_player2
        current_step_greedy_a_player2 += 1
    if auto_mode_ucs and not paused and current_step_ucs_player2 < len(ucs_steps_player2):
        current_pos_ucs_player2 = ucs_steps_player2[current_step_ucs_player2]
        player2_y, player2_x = current_pos_ucs_player2
        current_step_ucs_player2 += 1
    drawButtons(step,time,result)
    pygame.display.flip()

    #dành cho button lịch sử
    if open_window:
        # Tạo cửa sổ mới khi open_window = True
        new_window = pygame.display.set_mode((1000, 1000))
        pygame.display.set_caption('Lịch sử chạy thuật toán')

        while open_window:
            loaded_history_list = history_io.load_history_list()
            history_window(screen, 300, 300, loaded_history_list)

            pygame.display.flip()

            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        open_window = False
                        # Khi tắt cửa sổ mới, thiết lập lại kích thước cửa sổ ban đầu
                        screen = pygame.display.set_mode(original_size)
                        pygame.display.set_caption('Maze Game')

    if (player1_y, player1_x) == exit_pos:
        display_text("PLAYER 1 WINS", XANH, (WIDTH // 2, HEIGHT // 2))
        add_new_history(1)

        pygame.time.delay(2000)
        player1_y, player1_x = entrance_pos

    if (player2_y, player2_x) == exit_pos:
        display_text("PLAYER 2 WINS", XANH, (WIDTH // 2, HEIGHT // 2))
        add_new_history(2)

        pygame.time.delay(2000)
        player2_y, player2_x = entrance_pos


    clock.tick(10)
