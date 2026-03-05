import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')

WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
BLACK = (0, 0, 0)

player = pygame.Rect(0, 550, 50, 50)
player_speed = 50

runs = 'right'
move_time = pygame.time.get_ticks()

snake_tail = []
tail_length = 0

zone_up = WIDTH // 50
zone_down = HEIGHT // 50
win_zone = pygame.Rect(random.randint(0, zone_up - 1) * 50, random.randint(0, zone_down - 1) * 50, 50, 50)

grass = pygame.image.load('grass.png')
grass = pygame.transform.scale(grass, (WIDTH, HEIGHT))
apple_image = pygame.image.load('apple.png')
apple_image = pygame.transform.scale(apple_image, (50, 50))
snake_head = pygame.image.load('snake_head.png')
snake_head = pygame.transform.scale(snake_head, (50, 50))

score = 0
dis_score = pygame.font.SysFont("Arial", 30)
score_to_win = 10

clock = pygame.time.Clock()
running = True

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and runs != 'right':
                runs = 'left'
            elif event.key == pygame.K_RIGHT and runs != 'left':
                runs = 'right'
            elif event.key == pygame.K_UP and runs != 'down':
                runs = 'up'
            elif event.key == pygame.K_DOWN and runs != 'up':
                runs = 'down'

    if current_time - move_time >= 300:

        snake_tail.insert(0, pygame.Rect(player.x, player.y, 50, 50))

        if len(snake_tail) > tail_length:
            snake_tail.pop()

        if runs == 'left':
            player.x -= player_speed
        elif runs == 'right':
            player.x += player_speed
        elif runs == 'up':
            player.y -= player_speed
        elif runs == 'down':
            player.y += player_speed

        move_time = current_time

        for segment in snake_tail:
            if player.colliderect(segment):
                print("Ви зіткнулись з своїм хвостом")
                running = False

    if player.left < 0 or player.right > WIDTH or player.top < 0 or player.bottom > HEIGHT:
        print("Ви вийшли за межі поля")
        running = False

    if player.colliderect(win_zone):
        score += 1
        tail_length += 1
        if score >= score_to_win:
            print("Перемога! Рахунок:", score)
            running = False
        else:
            win_zone.x = random.randint(0, zone_up - 1) * 50
            win_zone.y = random.randint(0, zone_down - 1) * 50

    screen.blit(grass, (0, 0))
    screen.blit(apple_image, (win_zone.x, win_zone.y))

    for segment in snake_tail:
        pygame.draw.rect(screen, BLUE, segment)
        
    head_right = snake_head
    head_left = pygame.transform.rotate(snake_head, 180)
    head_up = pygame.transform.rotate(snake_head, 90)
    head_down = pygame.transform.rotate(snake_head, -90)

    if runs == "right":
        head = head_right
    elif runs == "left":
        head = head_left
    elif runs == "up":
        head = head_up
    elif runs == "down":
        head = head_down
        
    screen.blit(head, (player.x, player.y))
    score_text = dis_score.render(f"Рахунок: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()