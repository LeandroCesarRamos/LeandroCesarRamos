import pygame
import sys

# Cores do portfólio
BG_COLOR = (24, 26, 32)     # #181a20
CARD_COLOR = (35, 38, 58)     # #23263a
LINE_COLOR = (207, 217, 223)  # #cfd9df
X_COLOR = (255, 179, 71)      # #ffb347
O_COLOR = (230, 57, 70)       # #e63946

WIDTH, HEIGHT = 1100, 540
CELL_SIZE = 100
MARGIN = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BG_COLOR)  # Garante fundo do portfólio
pygame.display.set_caption('TicTacToe - Leandro Ramos')
font = pygame.font.SysFont('Roboto', 64, bold=True)
small_font = pygame.font.SysFont('Roboto', 32, bold=True)
clock = pygame.time.Clock()

board = [''] * 9
current_player = 'X'
game_over = False
winner = None

# Funções auxiliares
def draw_board():
    screen.fill(BG_COLOR)
    # Título
    title = small_font.render('TicTacToe', True, X_COLOR)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 24))
    # Centralização do tabuleiro
    board_width = 3 * CELL_SIZE + 2 * MARGIN
    start_x = (WIDTH - board_width) // 2
    start_y = 80
    for i in range(9):
        x = start_x + (i % 3) * (CELL_SIZE + MARGIN)
        y = start_y + (i // 3) * (CELL_SIZE + MARGIN)
        pygame.draw.rect(screen, CARD_COLOR, (x, y, CELL_SIZE, CELL_SIZE), border_radius=12)
        pygame.draw.rect(screen, LINE_COLOR, (x, y, CELL_SIZE, CELL_SIZE), 3, border_radius=12)
        if board[i] == 'X':
            text = font.render('X', True, X_COLOR)
            screen.blit(text, (x + CELL_SIZE//2 - text.get_width()//2, y + CELL_SIZE//2 - text.get_height()//2))
        elif board[i] == 'O':
            text = font.render('O', True, O_COLOR)
            screen.blit(text, (x + CELL_SIZE//2 - text.get_width()//2, y + CELL_SIZE//2 - text.get_height()//2))
    status_y = HEIGHT - 80
    if game_over:
        if winner:
            status = small_font.render(f'Player {winner} won!', True, O_COLOR if winner == 'O' else X_COLOR)
        else:
            status = small_font.render('Draw!', True, (50,50,50))
    else:
        status = small_font.render(f'Player turn: {current_player}', True, X_COLOR if current_player == 'X' else O_COLOR)
    screen.blit(status, (WIDTH//2 - status.get_width()//2, status_y))
    # Botão reiniciar
    btn_rect = pygame.Rect(WIDTH//2-80, HEIGHT-50, 160, 36)
    pygame.draw.rect(screen, X_COLOR, btn_rect, border_radius=8)
    btn_text = pygame.font.SysFont('Roboto', 24, bold=True).render('Restart', True, CARD_COLOR)
    screen.blit(btn_text, (btn_rect.x + btn_rect.width//2 - btn_text.get_width()//2, btn_rect.y + 6))
    return btn_rect

def check_winner():
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] != '':
            return board[a]
    if '' not in board:
        return 'Draw'
    return None

def reset_board():
    global board, current_player, game_over, winner
    board = [''] * 9
    current_player = 'X'
    game_over = False
    winner = None

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:
                mx, my = event.pos
                board_width = 3 * CELL_SIZE + 2 * MARGIN
                start_x = (WIDTH - board_width) // 2
                start_y = 80
                for i in range(9):
                    x = start_x + (i % 3) * (CELL_SIZE + MARGIN)
                    y = start_y + (i // 3) * (CELL_SIZE + MARGIN)
                    rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                    if rect.collidepoint(mx, my) and board[i] == '':
                        board[i] = current_player
                        winner = check_winner()
                        if winner:
                            game_over = True
                        else:
                            current_player = 'O' if current_player == 'X' else 'X'
            # Botão reiniciar
            btn_rect = pygame.Rect(WIDTH//2-80, HEIGHT-50, 160, 36)
            if btn_rect.collidepoint(event.pos):
                reset_board()
    draw_board()
    pygame.display.flip()
    clock.tick(60)
