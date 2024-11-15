import pygame
import chess
import chess.svg

# Set up constants
WIDTH, HEIGHT = 800, 800  # Window size
SQUARE_SIZE = WIDTH // 8  # Size of each square
COLORS = [(238, 238, 210), (118, 150, 86)]  # Light and dark colors for squares

pygame.init()
FONT = pygame.font.SysFont("Arial", 36)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess50!')

# Initialize the chess board
board = chess.Board()

# tables for evaluating position
pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 5, 50, 50, 5, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 5, 15, 15, 5, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -5, -5, -5, -5, -5, -10, -20]

rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 10, 5, 5, 10, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]

def evaluate_board(board):
    if board.is_checkmate():
        return -99999 if board.turn else 99999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    piece_values = {
        chess.KING: 200,
        chess.QUEEN: 9,
        chess.ROOK: 5,
        chess.BISHOP: 3.5,
        chess.KNIGHT: 3,
        chess.PAWN: 1
    }
    
    # Factors for pawn structure and mobility
    mobility_factor = 0.1
    
    # Material Evaluation
    material_score = 0
    for piece_type, value in piece_values.items():
        white_pieces = len(board.pieces(piece_type, chess.WHITE))
        black_pieces = len(board.pieces(piece_type, chess.BLACK))
        material_score += value * (white_pieces - black_pieces)



    # Mobility Evaluation
    mobility_score = (len(list(board.legal_moves)) * mobility_factor) * (1 if board.turn == chess.WHITE else -1)

    # Total Evaluation
    total_score = material_score + mobility_score
    return total_score

def ai_move(depth):
    best_move = None
    best_eval = 9999
    for move in board.legal_moves:
        board.push(move)
        current_eval = minimax(board, depth - 1, -float('inf'), float('inf'), True) # since white plays next
        # minimise eval since ai plays on black
        if current_eval < best_eval:
            best_eval = current_eval
            best_move = move
        board.pop()
    print(best_eval)
    return best_move

def minimax(board, depth, alpha, beta, is_white):
    max_eval = -9999
    min_eval = 9999
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    # maximise for white
    if is_white:
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, -float('inf'), float('inf'), False) # since the next turn is black's
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(max_eval, eval)
            if beta <= alpha:
                break
        return max_eval
    # minimise for black
    elif not is_white:
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, -float('inf'), float('inf'), True) # since the next turn is white's
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(min_eval, eval)
            if beta <= alpha:
                break
        return min_eval

def draw_board(screen):
    for row in range(8):
        for col in range(8):
            color = COLORS[(row + col) % 2]
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Load piece images
PIECE_IMAGES = {}
for piece in chess.PIECE_TYPES:
    for color in [chess.WHITE, chess.BLACK]:
        piece_char = chess.piece_symbol(piece).upper() if color == chess.WHITE else chess.piece_symbol(piece)
        PIECE_IMAGES[piece_char] = pygame.image.load(f'images/{piece_char}.png').convert_alpha()
        PIECE_IMAGES[piece_char] = pygame.transform.scale(PIECE_IMAGES[piece_char], (SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen, board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row = 7 - (square // 8)
            col = square % 8
            screen.blit(PIECE_IMAGES[piece.symbol()], (col * SQUARE_SIZE, row * SQUARE_SIZE))

selected_square = None

# Handle user input
def handle_click(pos, board):
    global selected_square
    col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
    square = chess.square(col, 7 - row)

    if selected_square is None:
        if board.piece_at(square) and board.color_at(square) == (board.turn == chess.WHITE):
            selected_square = square
    else:
        move = chess.Move(selected_square, square)
        if move in board.legal_moves:
            board.push(move)
        elif board.piece_type_at(selected_square) == chess.PAWN and (square // 8 == 0 or square // 8 == 7):
            print("Prompting for promotion...")
            
            # Display promotion overlay to choose piece
            overlay_width = WIDTH / 2
            overlay_height = HEIGHT / 4
            centre_x = (WIDTH - overlay_width) // 2
            centre_y = (HEIGHT - overlay_height) // 2
            pygame.draw.rect(screen, (255, 255, 255), (centre_x, centre_y, overlay_width, overlay_height))
            piece_size = int(overlay_width / 4)

            # Draw piece options in the overlay
            screen.blit(PIECE_IMAGES['Q'], (centre_x + piece_size * 0, centre_y))
            screen.blit(PIECE_IMAGES['R'], (centre_x + piece_size * 1, centre_y))
            screen.blit(PIECE_IMAGES['B'], (centre_x + piece_size * 2, centre_y))
            screen.blit(PIECE_IMAGES['N'], (centre_x + piece_size * 3, centre_y))
            pygame.display.flip()
            
            # Wait for user to choose piece
            chosen_piece = None
            waiting_for_choice = True
            while waiting_for_choice:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if centre_x + piece_size * 0 <= mouse_x <= centre_x + piece_size * 1 and centre_y <= mouse_y <= centre_y + piece_size:
                            chosen_piece = chess.QUEEN
                        elif centre_x + piece_size * 1 <= mouse_x <= centre_x + piece_size * 2 and centre_y <= mouse_y <= centre_y + piece_size:
                            chosen_piece = chess.ROOK
                        elif centre_x + piece_size * 2 <= mouse_x <= centre_x + piece_size * 3 and centre_y <= mouse_y <= centre_y + piece_size:
                            chosen_piece = chess.BISHOP
                        elif centre_x + piece_size * 3 <= mouse_x <= centre_x + piece_size * 4 and centre_y <= mouse_y <= centre_y + piece_size:
                            chosen_piece = chess.KNIGHT

                        # Proceed if a piece was chosen
                        if chosen_piece:
                            waiting_for_choice = False

            # Once piece is chosen, create promotion move and push to board
            promotion_move = chess.Move(selected_square, square, promotion=chosen_piece)
            if promotion_move in board.legal_moves:
                board.push(promotion_move)
            else:
                print("Illegal promotion move!")
        else:
            print("illegal move!")
        selected_square = None

# Handle game over
def check_gameover():
    outcome = board.outcome()
    if outcome:
        termination_map = {
            chess.Termination.CHECKMATE: 2,
            chess.Termination.STALEMATE: 1,
            chess.Termination.THREEFOLD_REPETITION: 3,
            chess.Termination.INSUFFICIENT_MATERIAL: 4,
        }
        return termination_map.get(outcome.termination, 0)
    return 0
    
def print_gameover(game_state):
    outcome = board.outcome()
    gameover_message = "Game over!"
    # print game over message overlay
    gameover_colour = (255, 255, 255)
    overlay_width = WIDTH / 2
    overlay_height = HEIGHT / 4
    # calculate the position of the top left corner
    centre_x = (WIDTH - overlay_width) // 2
    centre_y = (HEIGHT - overlay_height) // 2
    if game_state == 1:
        gameover_message = "Stalemate!"
    elif game_state == 2:
        # check which side has won
        winner = outcome.winner
        if winner:
            winner_text = "White wins!"
        else:
            winner_text = "Black wins!"
        gameover_message = "Checkmate: " + winner_text
    elif game_state == 3:
        gameover_message = "Draw by repetition!"
    elif game_state == 4:
        gameover_message = "Insufficient material!"

    text_surface = FONT.render(gameover_message, True, (0, 0, 0))
    pygame.draw.rect(screen, gameover_colour, (centre_x, centre_y, overlay_width, overlay_height))
    screen.blit(text_surface, (centre_x, centre_y))
    pygame.display.flip()

def draw_selected_square():
    # check if there is a selected square
    if selected_square:
        # use a different colour to draw the square
        row = 7 - (selected_square // 8)
        col = selected_square % 8
        selected_colour = (249, 249, 134)
        pygame.draw.rect(screen, selected_colour, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Run game loop
running = True
game_over = False
depth = 3
player_turn = chess.WHITE
draw_board(screen)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over == False and player_turn == chess.WHITE:
            pos = pygame.mouse.get_pos()
            handle_click(pos, board)
            draw_board(screen)
            draw_selected_square()
            draw_pieces(screen, board)
            if board.turn == chess.BLACK:
                player_turn = chess.BLACK               
    if player_turn == chess.BLACK and not board.is_game_over():
        best_move = ai_move(depth)
        if best_move:
            board.push(best_move)
            player_turn = chess.WHITE  # Switch back to player's turn
        else:
            print("best move not found")

    draw_board(screen)
    draw_selected_square()
    draw_pieces(screen, board)

    game_state = check_gameover()
    if game_state != 0:
        game_over = True
        print_gameover(game_state)

    pygame.display.flip()
pygame.quit()