import pygame
import socket
import pickle
import threading

pygame.init()

# Параметри сервера
server_ip = 'localhost'
server_port = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))

# Глобальний стан гри
game_state = {}

# Параметри екрану
WIDTH, HEIGHT = 800, 600
CELL = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')

# Кольори
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Власний гравець
player = pygame.Rect(0, 550, CELL, CELL)
player_speed = CELL
direction = 'right'
move_time = pygame.time.get_ticks()
snake_tail = []
tail_length = 0
started = False

# Зображення
grass = pygame.image.load('grass.png')
grass = pygame.transform.scale(grass, (WIDTH, HEIGHT))
apple_image = pygame.image.load('apple.png')
apple_image = pygame.transform.scale(apple_image, (CELL, CELL))
snake_head = pygame.image.load('snake_head.png')
snake_head = pygame.transform.scale(snake_head, (CELL, CELL))

# Кількість кадрів в секунду
clock = pygame.time.Clock()
running = True

# Функція для отримання стану гри від сервера
def receive_game_state():
    global game_state
    while True:
        try:
            data = client.recv(4096)
            if not data:
                break
            game_state = pickle.loads(data)
        except:
            break
    client.close()

threading.Thread(target=receive_game_state, daemon=True).start()

font_score = pygame.font.SysFont("Arial", 30)

while running:
    current_time = pygame.time.get_ticks()

    # Обробка подій
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != 'right':
                direction = 'left'
                started = True
            elif event.key == pygame.K_RIGHT and direction != 'left':
                direction = 'right'
                started = True
            elif event.key == pygame.K_UP and direction != 'down':
                direction = 'up'
                started = True
            elif event.key == pygame.K_DOWN and direction != 'up':
                direction = 'down'
                started = True

    # Рух гравця
    if started and current_time - move_time >= 300:
        move_time = current_time

        # Відправка стану на сервер
        state = {"direction": direction}
        try:
            client.sendall(pickle.dumps(state))
        except:
            print("Втрата з'єднання з сервером")

    # Малювання
    screen.blit(grass, (0, 0))

    # Яблуко
    if "apple" in game_state:
        screen.blit(apple_image, (game_state["apple"][0], game_state["apple"][1]))

    # Малюємо всіх гравців
    if "players" in game_state:
        for pid, pdata in game_state["players"].items():
            # хвіст
            for x, y in pdata["tail"]:
                pygame.draw.rect(screen, BLUE, (x, y, CELL, CELL))

            # голова з поворотом
            pd_direction = pdata.get("direction", "right")
            head_image = snake_head
            if pd_direction == "left":
                head_image = pygame.transform.rotate(snake_head, 180)
            elif pd_direction == "up":
                head_image = pygame.transform.rotate(snake_head, 90)
            elif pd_direction == "down":
                head_image = pygame.transform.rotate(snake_head, -90)
            screen.blit(head_image, (pdata["x"], pdata["y"]))

            # рахунок над головою
            score_text = font_score.render(str(pdata.get("score", 0)), True, BLACK)
            screen.blit(score_text, (pdata["x"], pdata["y"] - 30))

    # Перевірка переможця
    if "winner" in game_state:
        winner_text = font_score.render(f"Переміг: {game_state['winner']}", True, (255,0,0))
        screen.blit(winner_text, (WIDTH//2 - 100, HEIGHT//2 - 20))
        pygame.display.flip()
        pygame.time.delay(3000)  # показуємо 3 секунди
        running = False  # зупиняємо гру

    pygame.display.flip()
    clock.tick(60)

pygame.quit()