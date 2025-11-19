import chess
import chess.svg
import pygame
import engine
from pygame import Vector2
import move_finder
from multiprocessing import Process,Queue
from final import get_board

move_width =200
move_height=0
width,height=512,512 #can be 768,768
dimensions = 8 #chess board is 64 squares
sq_size  = int(height/dimensions)
max_fps=15
images ={} 
#load images 
#loading image sis very expensive so load only once per game 
# board = chess.Board('rnbqkbnr/8/8/8/8/8/8/8')
# svg = chess.svg.board(board)

# make engine that recognize legal chess move or not 
#hopefully 2 player game
# with open('b.svg', 'w', encoding="utf-8") as f:
#     f.write(svg)


'''
load images in global dictionary .
called exactly on the main
'''
def load_images():
    peices=['bQ','bK','bB','bN','bR','wQ','wK','wB','wN','wR','bp','wp']
    for peice in peices:
        images[peice] = pygame.transform.scale(pygame.image.load("./images/"+peice+".png"),(sq_size,sq_size)) #cenetr peice nicely 
        
    # we can access an peice by calling image['wp] we added them in the dictionary
    
'''
draw squares on board 
always top left square is white
'''
def draw_board(screen):
    global colors  #so that we can use them globally
    colors = [pygame.Color('white'),pygame.Color(194, 194, 194)]
    for r in range(dimensions):
        for c in range(dimensions):
            parity = (r+c) & 1
            color = colors[parity]
            pygame.draw.rect(screen,color,pygame.Rect(c*sq_size,r*sq_size,sq_size,sq_size))
            
    
'''
draw peices using current game state (board)
'''
def draw_peices(screen,board):
    for r in range(dimensions):
        for c in range(dimensions):
            peice = board[r][c]
            if peice !='--':
                screen.blit(images[peice],pygame.Rect(c*sq_size,r*sq_size,sq_size,sq_size))
                
import pygame

scroll_offset = 0  # global scroll variable

def draw_move_log(screen, gs, width, move_width, height):
    global scroll_offset
    font = pygame.font.SysFont('Arial', 16, False, False)
    move_log_rect = pygame.Rect(width, 0, move_width, height)

    # Draw background
    pygame.draw.rect(screen, pygame.Color('black'), move_log_rect)

    moves = gs.moveLog
    text_y = 5 - scroll_offset  # apply scroll offset here

    for j, i in enumerate(moves):
        text = f"{j+1}. {str(i)}"
        text_object = font.render(text, True, pygame.Color('white'))
        text_location = move_log_rect.move(5, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + 5


def handle_scroll(event):
    """Handles mouse wheel scrolling"""
    global scroll_offset
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4:  # scroll up
            scroll_offset = max(0, scroll_offset - 20)
        elif event.button == 5:  # scroll down
            scroll_offset += 20

    
'''
rensonsible for graphics in current game state
'''
def draw_game_state(screen,gs,valid_moves,sq_selected):
    draw_board(screen)   #draw squares on board
    high_light_squares(screen,gs,valid_moves,sq_selected)
    draw_peices(screen,gs.board)
    draw_move_log(screen,gs,512,200,512)
'''
hgihlight the square selected and moves for peices selected
'''

def high_light_squares(screen,gs,valid_moves,sqselected):
    if sqselected != ():
        r,c = sqselected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):  #sq selected is a peice 
            # highlight selected square 
            # use surface
            s = pygame.Surface((sq_size,sq_size))
            
            s.set_alpha(100)  # transparent 
            s.fill(pygame.Color('blue'))
            screen.blit(s,(c*sq_size,r*sq_size))
            # highlist moves from that square 
            s.fill(pygame.Color('red'))
            
            for move in valid_moves:
                if move.start_row == r and move.start_col==c:
                    pygame.draw.circle(screen,pygame.Color(0,255,0),( int(sq_size*(move.end_col + 0.5)),int(sq_size*(move.end_row + 0.5))),7.5)
                    if gs.board[move.end_row][move.end_col][0]== ('b' if gs.whiteToMove else 'w'):
                        screen.blit(s,(sq_size*move.end_col,sq_size*move.end_row))
            if len(gs.moveLog)>=1:
                prev_move= gs.moveLog[-1]
                s.set_alpha(100)  # transparent 
                s.fill(pygame.Color('dark green'))
                r,c = prev_move.end_row,prev_move.end_col
                screen.blit(s,(c*sq_size,r*sq_size))
                
                  
    
#what the board does is redraw images when u move 
#animation is simply slow the change such that u see every frame 

def main():
    pygame.init() 
    screen = pygame.display.set_mode((width+move_width,height+move_height))
    clock = pygame.time.Clock() #clock 
    screen.fill(pygame.Color('white'))
    gs = engine.GameState() #create a game state and craete variables 
    load_images() # load only once before whilw
    running  = True
    sqselected = ()
    player_clicks=[] #two squares of player clicks 
    valid_moves = gs.get_valid_moves()
    game_over=False
    player_one = True  # white true , machine is playing false
    player_two = False # similarly but for player two
    ai_thinking = False
    move_finder_procee = None
    move_undone = False
    if len(valid_moves)<=5:
        for move in valid_moves:
            print(move.peice_captured ,move.peice_moved, move.id)
    move_made = False   #until the valid move we need not generate valid moves
    # make ui changes
    animate=False 
    while running:
        human_Turn = (gs.whiteToMove and player_one) or (not gs.whiteToMove and player_two)
        for e in pygame.event.get():
            #mouse handler
            if e.type == pygame.QUIT:
                running=False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not game_over and human_Turn:
                    location =pygame.mouse.get_pos() #location of mouse 
                    col = int(location[0]//sq_size)
                    row = int(location[1]//sq_size)
                    if sqselected == (row,col) or col>=8: #user click same square then unmove 
                        sqselected=()
                        player_clicks=[]
                    else:
                        sqselected = (row,col)
                        player_clicks.append(sqselected) # append for both first and second cicks 
                    if len(player_clicks)==2: #after the second click
                        move = engine.Move(player_clicks[0],player_clicks[1],gs.board) 
                        for i in range(len(valid_moves)):
                            if move==valid_moves[i]:#move is pretty cheap
                                print("move taken",move.get_chess_notation(),"peice_moved:",gs.board[move.start_row][move.start_col])
                                gs.make_move(valid_moves[i])
                                move_made=True
                                animate=True
                                sqselected=() 
                                player_clicks=[]
                        if not move_made:
                            print("invalid_move",move.get_chess_notation(),move.peice_captured,move.peice_moved) 
                            player_clicks=[sqselected] #after move is doen reset squares 
                    if gs.check_mate or gs.steale_mate:
                        running=False
                
            #keyboard handlers
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    gs.undo_move()
                    move_made=True
                    game_over=False
                    if ai_thinking:
                        move_find_process.terminate()
                        ai_thinking=False
                    move_undone=True
                    
                elif e.key == pygame.K_r:
                    gs = engine.GameState()
                    valid_moves=gs.get_valid_moves()
                    sqselected=()
                    player_clicks=[]
                    move_made=False
                    animate=True
                    game_over=False
                    if ai_thinking:
                        move_find_process.terminate()
                        ai_thinking=False
                    move_undone=True
                    #reset the board 
        # best moves 
        if not game_over and not human_Turn and not move_undone:
            if not ai_thinking:
                ai_thinking = True  # threads wont share data
                returnQueue = Queue()  # used to pass data between threads 
                move_find_process = Process(target=move_finder.find_best_move,args=(gs,valid_moves,returnQueue)) # passing function as parameter
                
                move_find_process.start() #creates new thread without waiting this code tun
            if not move_find_process.is_alive():
                print('done thinking')
                move = returnQueue.get()
                if move is None:
                    move = move_finder.random_move(valid_moves)
                gs.make_move(move)
                move_made = True
                animate = True
                ai_thinking = False           
        if move_made:
            valid_moves = gs.get_valid_moves()
            if animate:
                animateMove(gs.moveLog[-1],screen,gs.board,clock)
                animate=False
            print('valid_moves:',len(valid_moves))
            if len(valid_moves)<=5:
                for move in valid_moves:
                    print(move.peice_captured ,move.peice_moved, move.move_id)
            
            move_made=False
            move_undone = False
            
        draw_game_state(screen,gs,valid_moves,sqselected)  #add mouse hnadlers
        if gs.check_mate:
            game_over=True
            if gs.whiteToMove:
                draw_end_game_text(screen,'black wins by checkmate')
            else:
                draw_end_game_text(screen,"white wins by checkmate")
        elif gs.steale_mate:
            game_over=True
            draw_end_game_text(screen,'stealmate no moves for king and no check')
        clock.tick(max_fps)
        pygame.display.flip()
from pygame.math import Vector2

def animateMove(move, screen, board, clock):
    start = Vector2(move.start_col, move.start_row)
    end = Vector2(move.end_col, move.end_row)
    distance = end.distance_to(start)
    frames_per_sq = 10
    frame_count = int(distance * frames_per_sq)

    for frame in range(frame_count + 1):
        t = frame / frame_count  # in [0, 1]
        current = start.lerp(end, t)  # linear interpolation
        c, r = current.x, current.y

        draw_board(screen)
        draw_peices(screen, board)

        # erase ending square
        colour = colors[(move.end_row + move.end_col) & 1]
        end_sq = pygame.Rect(move.end_col * sq_size, move.end_row * sq_size, sq_size, sq_size)
        pygame.draw.rect(screen, colour, end_sq)

        # draw captured piece if any
        if move.peice_captured != '--':
            if move.is_empassant_move:
                screen.blit(images[move.peice_captured], end_sq)
            else:
                screen.blit(images[move.peice_captured], end_sq)

        # draw moving piece at interpolated position
        screen.blit(images[move.peice_moved],
                    pygame.Rect(c * sq_size, r * sq_size, sq_size, sq_size))

        pygame.display.flip()
        clock.tick(120)

def draw_end_game_text(screen,text):
    font = pygame.font.SysFont('Helvitca',32,True,False)
    text_object = font.render(text,0,pygame.Color('Gray'))
    text_location = pygame.Rect(0,0,width,height).move(width/2,height/2)
    screen.blit(text_object,text_location)
    text_object = font.render(text,0,pygame.Color('Black'))
    screen.blit(text_object,text_location.move(2,2))
    
def get_moves(image_path):
    board,fen = get_board(image_path)
    gs= engine.GameState(board)
    moves = move_finder.get_best_n_moves(gs)
    gs = engine.GameState(board)
    gs.whiteToMove = not gs.whiteToMove
    moves2 = move_finder.get_best_n_moves(gs)
    colour = ('white_moves','black_moves') if not gs.whiteToMove  else ('black_moves','white_moves') 
    return fen, {colour[0]:moves,colour[1]:moves2}

if __name__=='__main__':
    #handle and update graphics and input
    #whenever u import this module else where  this wont run this fucntion 
    #main()
    get_moves('./image.png')
    
    
    
    

