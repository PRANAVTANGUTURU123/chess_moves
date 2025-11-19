import random


piece_score = {'K': 1000, 'Q': 900, 'R': 500, 'B': 330, 'N': 320, 'p': 100,'--':0,'-':0}
CHECKMATE = 100000
STALEMATE = 0
DEPTH = 3


# Pawn (p = 100)
pawn_table = [
    [  0,  0,  0,  0,  0,  0,  0,  0],
    [  5, 10, 10,-20,-20, 10, 10,  5],
    [  5, -5,-10,  0,  0,-10, -5,  5],
    [  0,  0,  0, 20, 20,  0,  0,  0],
    [  5,  5, 10, 25, 25, 10,  5,  5],
    [ 10, 10, 20, 30, 30, 20, 10, 10],
    [ 50, 50, 50, 50, 50, 50, 50, 50],
    [  0,  0,  0,  0,  0,  0,  0,  0]
]

# Knight (N = 320)
knight_table = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

# Bishop (B = 330)
bishop_table = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

# Rook (R = 500)
rook_table = [
    [  0,  0,  0,  0,  0,  0,  0,  0],
    [  5, 10, 10, 10, 10, 10, 10,  5],
    [ -5,  0,  0,  0,  0,  0,  0, -5],
    [ -5,  0,  0,  0,  0,  0,  0, -5],
    [ -5,  0,  0,  0,  0,  0,  0, -5],
    [ -5,  0,  0,  0,  0,  0,  0, -5],
    [ -5,  0,  0,  0,  0,  0,  0, -5],
    [  0,  0,  0,  5,  5,  0,  0,  0]
]

# Queen (Q = 900)
queen_table = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  5,  0,-10],
    [-10,  0,  5,  5,  5,  5,  5,-10],
    [ -5,  0,  5,  5,  5,  5,  0, -5],
    [  0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

# King (K = 1000) – Middlegame
king_table_mid = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [ 20, 20,  0,  0,  0,  0, 20, 20],
    [ 20, 30, 10,  0,  0, 10, 30, 20]
]

# King (K = 1000) – Endgame
king_table_end = [
    [-50,-40,-30,-20,-20,-30,-40,-50],
    [-30,-20,-10,  0,  0,-10,-20,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-30,  0,  0,  0,  0,-30,-30],
    [-50,-30,-30,-30,-30,-30,-30,-50]
]

king_scores = [[0]*8 for _ in range(8)]
for r in range(8):
    for c in range(8):
        king_scores[r][c]= king_table_end[r][c]+ king_table_end[r][c]
for r in range(4):
    for c in range(8):
        pawn_table[r][c],pawn_table[7-r][c]=pawn_table[r][c],pawn_table[7-r][c]
    



peice_position_scores = {'N':knight_table,'K':king_scores,'N':knight_table,'B':bishop_table,'Q':queen_table,'p':pawn_table,'R':rook_table}

'''
use openings 
use numpy and better board representation
better use p.q or something like that
transposition tables 
save the evaluation  zobra hash 
add which moves it is stoping 
add attacking and defensive 
we can teach end game theory 
if apeice is attacked try to move that first 
storing  the data of moves not to recalculate 
'''





def random_move(valid_moves):
    ind=random.randint(0,len(valid_moves)-1)
    return valid_moves[ind]


## checking for greedy 
# for all moves check where i can have more peices/value 
#but we also need to score_material the next move so that the best possible comes out 


#greedy algorithim and try to get better position 
#score material on board
#assume black playing ai and check mate is worst
# go for level 2 
# we want to minize the maximum of opponent score 


def find_best_move_non_recursion(gs,valid_moves):
    turn = 1 if gs.whiteToMove else -1
    opponent_min_max_score=  CHECKMATE  #smallest of their maximums
    best_player_move = None
    random.shuffle(valid_moves)
    for  player_move in valid_moves:
        gs.make_move(player_move)
        opponent_moves = gs.get_valid_moves()
        if gs.check_mate:
                    opponent_max_score = -CHECKMATE
        elif gs.steale_mate:
                    opponent_max_score=STALEMATE
        else:
            opponent_max_score = -CHECKMATE
            random.shuffle(opponent_moves)
            for opponent_move in opponent_moves:
                gs.make_move(opponent_move)
                gs.get_valid_move()
                if gs.check_mate:
                        score =  CHECKMATE
                elif gs.steale_mate:
                        score=STALEMATE
                else:
                        score = -turn * score_material(gs.board)
                    
                if (score>opponent_max_score):
                        opponent_max_score=score   # try to find best move for opponent
                        
                gs.undo_move()
        if opponent_min_max_score> opponent_max_score:
            opponent_min_max_score = opponent_max_score # try to find best move for u which is worst(best) move 
            best_move  = player_move  # my new best is least of  all opponent bests 
        
        gs.undo_move()
            
    return best_move
# solve this recursively
# prune the branches we do not need


'''
helper method for best method 
'''
def find_best_move(gs, valid_moves, return_queue):
    global count, best_moves
    count = 0
    score = find_move_nega_max_alpha_beta(
        gs, gs.get_valid_moves(), DEPTH, -2*CHECKMATE, 2*CHECKMATE, 1
    )

    print("Top moves:")
    for score, mv in best_moves:
        print(mv.get_chess_notation(), "score:", score)

    # pick a random move among top N
    chosen_move = random.choice(best_moves)[1]
    return_queue.put(chosen_move)
    


'''
find min max move  
'''
def find_move_min_max(gs,valid_moves,depth,whiteToMove):
    global next_move
    if depth == 0 :
        return score_material(gs)
    if whiteToMove:  #maximize score 
        max_score = - CHECKMATE
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_move_min_max(gs,next_moves,depth-1,False)
            if score>max_score:
                max_score=score
                if depth == DEPTH :
                    next_move = move 
            gs.undo_move()
        return max_score
    else:
        min_score =  CHECKMATE
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_move_min_max(gs,next_moves,depth-1,True)
            if score<min_score:
                min_score=score
                if depth == DEPTH :
                    next_move = move 
            gs.undo_move()
        return min_score
    

'''
combine if else to one
'''

def find_move_nega_max(gs,valid_moves,depth,turn):
    #always try to maximize but with multilier
    global next_move,count
    count +=1
    if depth == 0 :
        return turn *  score_material(gs)
    
    max_score = CHECKMATE
    for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = -find_move_nega_max(gs,next_moves,depth-1,-1 * turn) #this is very important 
            if score>max_score:
                max_score=score
                if depth == DEPTH :
                    next_move = move 
            gs.undo_move()
    return max_score

'''
the alpha beta pruning 
remove branches that wont make any good 
also depends on scoring algorithim
also add positional scores 
need to control more squares and attack more squares 
alpha beta these are the maximum and minimum u can acheive  values overall

if max_score>alpha then max_score is alpha
if alpha>beta then prune that branch 
ugot best else where no need for it 
'''
# Killer moves: 2 per depth (ply)
killer_moves = {}

# History heuristic: success count
history_heuristic = {
    'w': [[0 for _ in range(8)] for _ in range(8)],
    'b': [[0 for _ in range(8)] for _ in range(8)]
}
def order_moves(gs, moves):
    scored_moves = []

    for move in moves:
        score=0
        score -= score_material(gs)

        # 1. Captures (MVV-LVA style)
        if move.is_capture:
            attacker = move.peice_moved[1]
            victim = move.peice_captured[1] if move.peice_captured[1]!='-' else '--'
            score += ( piece_score.get(victim, 0))*10 - piece_score.get(attacker, 0) 

        # 2. Checks (simulate move and test)
        gs.make_move(move)
        if gs.incheck:
            score += 80
        gs.undo_move()

        # 3. Promotions
        if move.is_pawn_promotion:
            score += 150 + piece_score['Q']*10

        # 4. Castling (good for king safety)
        if move.castle:
            score += 50

        # 5. 
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(-1,1),(1,-1)]:
            rr, cc = move.end_row + dr, move.end_col + dc
            if 0 <= rr < 8 and 0 <= cc < 8:
                piece = gs.board[rr][cc]
                if piece != "--" and piece[0] == move.peice_moved[0]:  # same color
                    score += 1 
        score += score_material(gs)
        scored_moves.append((score, move))

    # Sort by score descending
    scored_moves.sort(key=lambda x: x[0], reverse=True)
    return [m for _, m in scored_moves]

# def find_move_nega_max_alpha_beta(gs, valid_moves, depth, alpha, beta, turn):
#     global count, next_move
#     count += 1  # counts all nodes visited

#     if depth == 0:
#         return turn * score_material(gs)

#     max_score = -CHECKMATE
#     valid_moves=order_moves(gs,valid_moves)
#     for move in valid_moves:
#         gs.make_move(move)
#         next_moves = gs.get_valid_moves()
#         score = -find_move_nega_max_alpha_beta(
#             gs, next_moves, depth - 1, -beta, -alpha, -turn
#         )
#         gs.undo_move()

#         if score > max_score:
#             max_score = score
#             if depth == DEPTH:
#                 next_move = move

#         alpha = max(alpha, max_score)
#         if alpha >= beta:
#             break

#     return max_score


TOP_N = 5  # number of best moves you want

def find_move_nega_max_alpha_beta(gs, valid_moves, depth, alpha, beta, turn): 
    if depth == 0:
        return turn * score_material(gs)

    max_score = -CHECKMATE
    scored_moves = [] 

    # move ordering to improve pruning
    valid_moves = order_moves(gs, valid_moves)

    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score = -find_move_nega_max_alpha_beta(
            gs, next_moves, depth - 1, -beta, -alpha, -turn
        )
        gs.undo_move()

        scored_moves.append((score, move))

        max_score = max(max_score, score)
        alpha = max(alpha, max_score)
        if alpha >= beta:
            break  # alpha-beta cutoff

    # Only save best moves at root depth
    if depth == DEPTH:
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        best_moves = [(score, move) for score, move in scored_moves[:TOP_N]]

    return max_score


'''
score the board
positive score good for white 
a negative score good for black
increase the scoring function 
counting attacking and defending moves 
'''



def score_material(self):
    """Full evaluation of the board with material, positional, mobility, defense, etc."""

    if self.check_mate:
        if self.whiteToMove:
            return -CHECKMATE 
        else:
            return CHECKMATE   
    elif self.steale_mate:
        return STALEMATE

    board = self.board
    score = 0

    white_squares_controlled = set()
    black_squares_controlled = set()

    # Material, piece-square, and piece defense evaluation
    for r in range(8):
        for c in range(8):
            square = (r, c)
            piece_info = board[r][c]

            if piece_info == "--":
                continue

            color, piece = piece_info[0], piece_info[1]

            base_value = piece_score[piece]

            if color == 'w':
                # Material value
                score += base_value 

                
                score += peice_position_scores[piece][r][c]

                # 
                moves = self.move_functions[piece](r,c,[])
                for move in moves:
                    white_squares_controlled.add((move.end_row, move.end_col))

                    # Bonus for defending own piece
                    if board[move.end_row][move.end_col][0] == 'w':
                        defended_piece = board[move.end_row][move.end_col][1]
                        score += piece_score[defended_piece] 

                    # Bonus for killing enemy valuable piece
                    if board[move.end_row][move.end_col][0] == 'b':
                        victim = board[move.end_row][move.end_col][1]
                        score += piece_score[victim]  *10
            elif color == 'b':
                score -= base_value 
                score -= peice_position_scores[piece][7 - r][c]

                moves = self.move_functions[piece](r,c,[])
                for move in moves:
                    black_squares_controlled.add((move.end_row, move.end_col))

                    # Defense bonus
                    if board[move.end_row][move.end_col][0] == 'b':
                        defended_piece = board[move.end_row][move.end_col][1]
                        score -= piece_score[defended_piece] 

                    # Killing enemy valuable piece
                    if board[move.end_row][move.end_col][0] == 'w':
                        victim = board[move.end_row][move.end_col][1]
                        score -= piece_score[victim] *10


    # Bishop pair bonus
    white_bishops = sum(1 for r in range(8) for c in range(8) if board[r][c] == 'wB')
    black_bishops = sum(1 for r in range(8) for c in range(8) if board[r][c] == 'bB')
    if white_bishops >= 2:
        score += 50
    if black_bishops >= 2:
        score -= 50

    # King safety (penalize exposed kings)
    score += self.king_safety( "w") - self.king_safety("b")
    score += (len(white_squares_controlled) - len(black_squares_controlled))*5
   

    return score

def get_best_n_moves(gs, n=5):
    """
    Returns best n moves for both White and Black.
    """
    best_white, best_black = [], []

    # White to move
    if gs.whiteToMove:
        moves = gs.get_valid_moves()
        scored = []
        for move in moves:
            gs.make_move(move)
            score = -find_move_nega_max_alpha_beta(
                gs, gs.get_valid_moves(), DEPTH - 1, -CHECKMATE, CHECKMATE, -1
            )
            gs.undo_move()
            scored.append((score, str(move)))
        scored.sort(key=lambda x: x[0], reverse=True)
        best_white = scored[:n]

    # Black to move
    else:
        moves = gs.get_valid_moves()
        scored = []
        for move in moves:
            gs.make_move(move)
            score = -find_move_nega_max_alpha_beta(
                gs, gs.get_valid_moves(), DEPTH - 1, -CHECKMATE, CHECKMATE, 1
            )
            gs.undo_move()
            scored.append((score, str(move)))
        scored.sort(key=lambda x: x[0], reverse=True)
        best_black = scored[:n]
    return best_white if best_white else best_black
