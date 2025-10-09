import pygame
import random
import sys

# Inicializa o pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Invaders - Leandro Ramos')
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
MENU_BG = (24, 26, 32)  # #181a20
BTN_COLOR = (255, 179, 71)  # #ffb347
BTN_TEXT_COLOR = (35, 38, 58)  # #23263a

# Jogador
player_img = pygame.Surface((50, 30))
player_img.fill(GREEN)
player_rect = player_img.get_rect(midbottom=(WIDTH//2, HEIGHT-40))
player_speed = 6

# Tiro
bullet_img = pygame.Surface((6, 18))
bullet_img.fill(WHITE)
bullets = []
bullet_speed = 8

# Inimigos
enemy_img = pygame.Surface((40, 30))
enemy_img.fill(RED)
enemies = []
enemy_speed = 2
level = 1
score = 0
font = pygame.font.SysFont('Arial', 28)
menu_font = pygame.font.SysFont('Arial', 48, bold=True)
btn_font = pygame.font.SysFont('Arial', 32, bold=True)
game_over = False
lives = 3

def spawn_enemies(level):
    new_enemies = []
    cols = 8 + level  # aumenta o número de colunas a cada nível
    rows = 2 + level // 2  # aumenta o número de linhas a cada 2 níveis
    for x in range(40, WIDTH-40, WIDTH//cols):
        for y in range(60, 180 + 20*level, 40):
            rect = enemy_img.get_rect(topleft=(x, y))
            new_enemies.append(rect)
    return new_enemies

def draw():
    screen.fill(BLACK)
    screen.blit(player_img, player_rect)
    for bullet in bullets:
        screen.blit(bullet_img, bullet)
    for enemy in enemies:
        screen.blit(enemy_img, enemy)
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (20, 20))
    level_text = font.render(f'Level: {level}', True, WHITE)
    screen.blit(level_text, (WIDTH-150, 20))
    if game_over:
        over_text = font.render('GAME OVER', True, RED)
        screen.blit(over_text, (WIDTH//2-100, HEIGHT//2-30))
        restart_text = font.render('Pressione R para reiniciar', True, WHITE)
        screen.blit(restart_text, (WIDTH//2-150, HEIGHT//2+20))
    pygame.display.flip()

def draw_menu():
    screen.fill(MENU_BG)
    title = menu_font.render('Space Invaders', True, BTN_COLOR)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 140))
    # Botão Iniciar
    start_rect = pygame.Rect(WIDTH//2-120, HEIGHT//2-30, 240, 60)
    pygame.draw.rect(screen, BTN_COLOR, start_rect, border_radius=12)
    start_text = btn_font.render('Iniciar Jogo', True, BTN_TEXT_COLOR)
    screen.blit(start_text, (start_rect.x + start_rect.width//2 - start_text.get_width()//2, start_rect.y + 10))
    # Botão Fechar
    close_rect = pygame.Rect(WIDTH//2-120, HEIGHT//2+60, 240, 60)
    pygame.draw.rect(screen, (230,57,70), close_rect, border_radius=12)
    close_text = btn_font.render('Fechar', True, BTN_TEXT_COLOR)
    screen.blit(close_text, (close_rect.x + close_rect.width//2 - close_text.get_width()//2, close_rect.y + 10))
    pygame.display.flip()
    return start_rect, close_rect

# Loop de menu
menu_active = True
while menu_active:
    start_rect, close_rect = draw_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_rect.collidepoint(event.pos):
                menu_active = False
            if close_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
    clock.tick(60)

# Inicializa inimigos
enemies = spawn_enemies(level)
game_over = False
lives = 3

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bullet = bullet_img.get_rect(midbottom=player_rect.midtop)
                bullets.append(bullet)
            if event.key == pygame.K_r and game_over:
                # Reinicia o jogo
                level = 1
                score = 0
                player_rect.midbottom = (WIDTH//2, HEIGHT-40)
                bullets.clear()
                enemy_speed = 2  # reseta velocidade ao reiniciar
                enemies = spawn_enemies(level)
                game_over = False

    if game_over:
        draw()
        clock.tick(60)
        continue

    # Movimento do jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed

    # Movimento dos tiros
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.bottom < 0:
            bullets.remove(bullet)

    # Movimento dos inimigos
    for enemy in enemies:
        enemy.x += enemy_speed
    # Inverte direção ao bater na borda
    if enemies and (max(e.x for e in enemies) > WIDTH-40 or min(e.x for e in enemies) < 0):
        enemy_speed *= -1
        for enemy in enemies:
            enemy.y += 20

    # Colisão tiro-inimigo
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                break

    # GAME OVER ou perde vida se inimigo chega ao jogador
    for enemy in enemies[:]:
        if enemy.bottom >= player_rect.top:
            lives -= 1
            enemies.remove(enemy)
            if lives <= 0:
                game_over = True
            break

    # Próximo nível
    if not enemies and not game_over:
        level += 1
        enemy_speed = 2 + level  # aumenta velocidade a cada nível
        enemies = spawn_enemies(level)

    draw()
    clock.tick(60)
