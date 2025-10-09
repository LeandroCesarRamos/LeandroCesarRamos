import pygame
import sys
import random

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
    btn_rect = pygame.Rect(WIDTH//2-180, HEIGHT-50, 160, 36)
    pygame.draw.rect(screen, X_COLOR, btn_rect, border_radius=8)
    btn_text = pygame.font.SysFont('Roboto', 24, bold=True).render('Restart', True, CARD_COLOR)
    screen.blit(btn_text, (btn_rect.x + btn_rect.width//2 - btn_text.get_width()//2, btn_rect.y + 6))
    # Botão Close Game
    close_rect = pygame.Rect(WIDTH//2+30, HEIGHT-50, 160, 36)
    pygame.draw.rect(screen, O_COLOR, close_rect, border_radius=8)
    close_text = pygame.font.SysFont('Roboto', 24, bold=True).render('Close Game', True, CARD_COLOR)
    screen.blit(close_text, (close_rect.x + close_rect.width//2 - close_text.get_width()//2, close_rect.y + 6))
    return btn_rect, close_rect

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

def minimax(board, player):
    winner = check_winner_minimax(board)
    if winner == 'O':
        return 1
    elif winner == 'X':
        return -1
    elif winner == 'Draw':
        return 0
    moves = []
    for i in range(9):
        if board[i] == '':
            board_copy = board[:]
            board_copy[i] = player
            score = minimax(board_copy, 'X' if player == 'O' else 'O')
            moves.append((score, i))
    if player == 'O':
        max_move = max(moves)
        return max_move[0] if len(moves) > 1 else max_move[0]
    else:
        min_move = min(moves)
        return min_move[0] if len(moves) > 1 else min_move[0]

def best_move(board):
    moves = []
    for i in range(9):
        if board[i] == '':
            board_copy = board[:]
            board_copy[i] = 'O'
            score = minimax(board_copy, 'X')
            moves.append((score, i))
    if moves:
        best = max(moves)
        return best[1]
    return None

def check_winner_minimax(board):
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

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over and current_player == 'X':
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
                            current_player = 'O'
            # Botões
            btn_rect, close_rect = draw_board()
            if btn_rect.collidepoint(event.pos):
                reset_board()
            if close_rect.collidepoint(event.pos):
                try:
                    import js
                    js.window.close()
                except:
                    pygame.quit()
                    sys.exit()
    # Bot joga como 'O' usando minimax
    if not game_over and current_player == 'O':
        pygame.time.wait(400)
        move = best_move(board)
        if move is not None:
            board[move] = 'O'
            winner = check_winner()
            if winner:
                game_over = True
            else:
                current_player = 'X'
    draw_board()
    pygame.display.flip()
    clock.tick(60)
