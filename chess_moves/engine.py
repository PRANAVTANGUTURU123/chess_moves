"""
this file contains all details of game state and other parametrs
"""
class GameState():
    def __init__(self,board=[[]]):
        self.board=[['bR','bN','bB','bQ','bK','bB','bN','bR'],
                    ['bp','bp','bp','bp','bp','bp','bp','bp'],
                    ['--','--','--','--','--','--','--','--'],
                    ['--','--','--','--','--','--','--','--'],
                    ['--','--','--','--','--','--','--','--'],
                    ['--','--','--','--','--','--','--','--'],
                    ['wp','wp','wp','wp','wp','wp','wp','wp'],
                    ['wR','wN','wB','wQ','wK','wB','wN','wR']
                    ]
        
        if self.is_valid_board(board):
            self.board=board
            
        self.whiteToMove=True
        self.moveLog=[]
        self.knight_directions=[(-2, -1), (-1, -2), (-2, 1), (-1, 2), (2, -1), (1, -2), (2, 1), (1, 2)]
        self.bishop_directions= [(-1,-1),(-1,1),(1,-1),(1,1)]
        self.king_directions=[(-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
        self.check_mate = False
        self.steale_mate = False
        self.inheck = False  # if king is in check this will be True
        self.pins=[]  # if any peice stopping the check and if u move them u gona get check 
        self.checks=[]   # possible checks 
        # we need to keep track of squares where u can eliminate if u took double move in the first place 
        #that move name is empassant move
        # we can have dictionary to store functions
        
        self.protects=[[]]
        self.threatens =[[]]
        self.peices_can_move_to = [[]]
        
        
        self.move_functions={'p':self.get_pawn_moves,
                             'R':self.get_rook_moves,
                             'N':self.get_knight_moves,
                             'B':self.get_bishop_moves,
                             'K':self.get_king_moves,
                             'Q':self.get_queen_moves
                             }
        #solution 1 to checks is keep track of kings location
        self.black_king_location=(0,4)
        self.white_king_location=(7,4)
        # we need to keep track of squares where u can eliminate if u took double move in the first place 
        #that move name is empassant move
        # we can have dictionary to store functions
        self.empassant_moves=()  #square for which empassant move is possible
        self.current_castling_rights = Castling_Rights(True,True,True,True)
        self.castle_rights_log=[Castling_Rights(self.current_castling_rights.wks,self.current_castling_rights.wqs,self.current_castling_rights.bks,self.current_castling_rights.bqs)]
        self.empassant_possible_log=[self.empassant_moves]
        self.update_state_variables()
        # when current castling rights modified it creates new object and pt it in log 
        
        
        
        
    '''
    To castle, your king and the chosen rook must not have moved, 
    there must be no pieces between them, 
    the king cannot be in or pass through check, 
    and the king must not end up in check.
    castle must be first move to both king and rook
    this is the only move where two peice move 
    
    '''
    def make_move(self,move): #this is not for castling and pawn promotion just to add it for squares 
        self.board[move.start_row][move.start_col]= '--'
        self.board[move.end_row][move.end_col]= move.peice_moved
        if move.peice_moved=='bK':
            self.black_king_location= (move.end_row,move.end_col)
        if move.peice_moved=="wK":
            self.white_king_location= (move.end_row,move.end_col)
            
        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.peice_moved[0]+ move.promotion_choice
        
        #castle move 
        if move.castle:
            if move.end_col - move.start_col ==2: #king side col
                self.board [move.end_row][move.end_col-1]= self.board[move.end_row][move.end_col+1]
                self.board[move.end_row][move.end_col+1]='--'
            else:
                self.board [move.end_row][move.end_col+1]= self.board[move.end_row][move.end_col-2] #2 squares aqay from it starts
                self.board[move.end_row][move.end_col-2]='--'
                
        
        #empassant move 
        if move.is_empassant_move: # remove square that is not captured but on the road
            self.board[move.start_row][move.end_col] = '--'  # capturing the pawn 
        
        #update empassant possible 
        #only in the case 
        if move.peice_moved[1] == 'p' and abs(move.start_row-move.end_row)==2:
            self.empassant_moves=( (move.start_row + move.end_row)//2 ,move.end_col )
            
        else:
            self.empassant_moves = ()
            
        #update castling rights  whenever is is king or rook moves 
        self.update_castle_rights(move)
        self.castle_rights_log.append(Castling_Rights(self.current_castling_rights.wks,self.current_castling_rights.wqs,self.current_castling_rights.bks,self.current_castling_rights.bqs))
        self.empassant_possible_log.append(self.empassant_moves)
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove #switch turns 
    '''
    undo the previous move made 
    '''
    def undo_move(self):
        if len(self.moveLog):
            l_move = self.moveLog.pop()
            self.whiteToMove = not self.whiteToMove
            self.board[l_move.end_row][l_move.end_col]=l_move.peice_captured
            self.board[l_move.start_row][l_move.start_col]=l_move.peice_moved 
            move=l_move
            if move.peice_moved=='bK':
                self.black_king_location= (move.start_row,move.start_col)
            if move.peice_moved=="wK":
                self.white_king_location= (move.start_row,move.start_col)
            if move.is_empassant_move:
                self.board[l_move.end_row][l_move.end_col] = '--' #leave end row and column as it is 
                self.board[l_move.start_row][l_move.end_col]= move.peice_captured
            
            self.empassant_possible_log.pop()
            self.empassant_moves = self.empassant_possible_log[-1]
                
            if move.castle:
            
                if move.end_col - move.start_col ==2: #king side col
                    self.board [move.end_row][move.end_col+1]= self.board[move.end_row][move.end_col-1]
                    self.board[move.end_row][move.end_col-1]='--'
                else:
                    self.board [move.end_row][move.end_col-2]= self.board[move.end_row][move.end_col+1] #2 squares aqay from it starts
                    self.board[move.end_row][move.end_col+1]='--'
                
            
            ## undo the castling rights 
            self.castle_rights_log.pop()  #get rid of new castle rights 
            self.current_castling_rights = self.castle_rights_log[-1]

            #undo checkmate move 
            self.check_mate = False
            self.steale_mate = False
            
                
                
        else:
            print("this is our starting move ")
    #if u move then it might be check to u so need to check these possiblities 
    #so we need to generate possible moves in next turn abd based on that we need to move
    def update_state_variables(self):
        # Ensure move log is empty for a fresh board
        self.moveLog = []
        
        # Initialize game status flags
        self.whiteToMove = True
        self.checkmate = False
        self.stalemate = False
        self.in_check = False
        self.pins = []
        self.checks = []
        self.protects = []
        self.threatens = []
        self.pieces_can_move_to = []
        
        # Update king locations by scanning the board
        self.white_king_location = None
        self.black_king_location = None
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == 'wK':
                    self.white_king_location = (row, col)
                if self.board[row][col] == 'bK':
                    self.black_king_location = (row, col)
        
        # Set default king locations if not found (for standard board)
        if not self.white_king_location:
            self.white_king_location = (7, 4)
        if not self.black_king_location:
            self.black_king_location = (0, 4)
        
        # Reset en passant
        self.empassant_moves = ()
        self.empassant_possible_log = [()]
        
        # Set castling rights based on piece positions
        self.current_castling_rights = Castling_Rights(False, False, False, False)
        if self.white_king_location == (7, 4):
            if self.board[7][0] == 'wR':
                self.current_castling_rights.wqs = True
            if self.board[7][7] == 'wR':
                self.current_castling_rights.wks = True
        if self.black_king_location == (0, 4):
            if self.board[0][0] == 'bR':
                self.current_castling_rights.bqs = True
            if self.board[0][7] == 'bR':
                self.current_castling_rights.bks = True
        self.castle_rights_log = [Castling_Rights(
            self.current_castling_rights.wks, self.current_castling_rights.wqs,
            self.current_castling_rights.bks, self.current_castling_rights.bqs
        )]
        
        # Calculate pins, checks, and in_check
        self.incheck,self.pins,self.checks = self.check_for_pins_and_checks()
    
    def is_valid_board(self, board):
        if len(board) != 8:
            return False
        valid_pieces = {'bR', 'bN', 'bB', 'bQ', 'bK', 'bp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wp', '--'}
        white_kings = 0
        black_kings = 0
        for row in range(8):
            if len(board[row]) != 8:
                return False
            for col in range(8):
                cell = board[row][col]
                if cell not in valid_pieces:
                    return False
                if cell == 'wK':
                    white_kings += 1
                if cell == 'bK':
                    black_kings += 1
                # No pawns on promotion ranks
                if row in (0, 7) and cell[1] == 'p':
                    return False
        if white_kings != 1 or black_kings != 1:
            return False
        return True
 
    '''
    all moves including checks
    '''
    def update_castle_rights(self,move):
        if move.peice_moved=='wK':
            self.current_castling_rights.wks=False
            self.current_castling_rights.wqs=False
        elif move.peice_moved=='bK':
            self.current_castling_rights.bks=False
            self.current_castling_rights.bqs=False
        elif move.peice_moved=='wR' and move.start_row==0: 
            if move.start_col==7:
                self.current_castling_rights.wks=False
            elif move.start_col==0:
                self.current_castling_rights.wqs=False
        elif move.peice_moved=='bR' and move.start_row==7: 
            if move.start_col==7:
                self.current_castling_rights.bks=False
            elif move.start_col==0:
                self.current_castling_rights.bqs=False
        
        # if rook is captured
        if move.peice_captured == 'wR':
            if move.end_row == 7:
                if move.end_col == 0:
                    self.current_castling_rights.wqs=False
                elif move.end_col == 7:
                    self.current_castling_rights.wks = False
        elif move.peice_captured == 'bR':
            if move.end_row == 0:
                if move.end_col == 0:
                    self.current_castling_rights.bqs=False
                elif move.end_col == 7:
                    self.current_castling_rights.bks = False
                
            
            
            
        
    def is_valid_square(self,r,c):
        if r>=0 and r<=7 and c>=0 and c<=7:
            return True
        else:
            return False
    
    def king_safety(self, color):
        board = self.board
        score = 0

        # Find king position
        king_pos = None
        for r in range(8):
            for c in range(8):
                if board[r][c] == color + 'K':
                    king_pos = (r, c)
                    break
            if king_pos:
                break

        if not king_pos:
            return 0  # King missing? shouldn't happen.

        r, c = king_pos

        # Pawn shield (pawns in front of king)
        if color == 'w':
            pawn_row = r - 1
            if pawn_row >= 0:
                for dc in [-1, 0, 1]:
                    cc = c + dc
                    if 0 <= cc < 8:
                        if board[pawn_row][cc] == 'wp':
                            score += 30   # strong pawn shield
                        elif board[pawn_row][cc] == '--':
                            score -= 15   # weak if missing
        else:  # black
            pawn_row = r + 1
            if pawn_row < 8:
                for dc in [-1, 0, 1]:
                    cc = c + dc
                    if 0 <= cc < 8:
                        if board[pawn_row][cc] == 'bp':
                            score += 30
                        elif board[pawn_row][cc] == '--':
                            score -= 15

        # Open file penalty (if no pawn in king’s file)
        file_has_pawn = False
        for rr in range(8):
            if board[rr][c] == color + 'p':
                file_has_pawn = True
                break
        if not file_has_pawn:
            score -= 40  # open file in front of king is dangerous

        # Enemy attacks around the king (adjacent squares)
        king_zone = [(r + dr, c + dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]
        enemy_color = 'w' if color == 'b' else 'b'
        for (rr, cc) in king_zone:
            if 0 <= rr < 8 and 0 <= cc < 8:
                self.whiteToMove = not self.whiteToMove
                moves = self.get_all_possible_moves()
                for move in moves:
                    if (move.end_row, move.end_col) == (rr, cc):
                        score -= 20  # enemy attacks near king
                self.whiteToMove = not self.whiteToMove

        return score

    
    def get_valid_moves(self):
        
        #naive solution
        #this is very inefficient and generate all moves in two levels for check 
        #generate all moves 
        # for all moves try to generate next possible moves
        #for each opponent move check if he can attack your king
        #if my king is attacked then it is invalid 
        
          
        # # if u are removing then it is better to traverse list backwards 
        # #indexes wont shift 
        # for i in range(len(moves)-1,-1,-1):
        #     self.make_move(moves[i])
        #     #swap turns so this will check my check moves 
        #     self.whiteToMove = not self.whiteToMove
        #     if self.has_check():
        #         moves.remove(moves[i])
        #     self.whiteToMove = not self.whiteToMove
        #     self.undo_move()
        
        # decide algo2 
        #check for all verticals,horizantals,diagnols  and which peices can attack king
        #check for kinght attacks 
        #check for direct checks 
        #check for if i move this peice can i got any check
        #ckeck for check where u have to move 
        self.incheck,self.pins,self.checks = self.check_for_pins_and_checks()
        if self.whiteToMove:
            king_row,king_col = self.white_king_location
        else:
            king_row,king_col = self.black_king_location
        if self.incheck:
            if len(self.checks)==1:
                
                moves = self.get_all_possible_moves() 
                check_row,check_col,x_dist,y_dist = self.checks[0]
                
                peice_checking = self.board[check_row][check_col]
                valid_squares=[]
                if peice_checking[1]=='N':
                    valid_squares=[(check_row,check_col)]
                else:
                    for i in range(1,8):
                        valid_square = (king_row + i*x_dist , king_col + i*y_dist)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1]==check_col:   #once u get to peice and checks
                            break
                for i in range(len(moves)-1,-1,-1):
                    if moves[i].peice_moved[1] != 'K':
                        if not ( moves[i].end_row,moves[i].end_col) in valid_squares:  #these moves not blobk check so no need
                            moves.remove(moves[i])
            else: # double check king has to move
                moves=[]
                moves=self.get_king_moves(king_row,king_col,moves)
        else:
            
            moves = self.get_all_possible_moves() # no check so all moves are fine
        if self.whiteToMove:
            self.get_castle_moves(self.white_king_location[0],self.white_king_location[1],moves,'w')
        else:
            self.get_castle_moves(self.black_king_location[0],self.black_king_location[1],moves,'b')
            

        
        
        
        if len(moves)==0:   #either check mate or stealmate
            if self.has_check():
                self.check_mate=True
            else:
                self.steale_mate=True
        else:
            self.check_mate=False
            self.steale_mate=False
        
        return moves 
    '''
    determine if current player in check
    if player in check need to remove check otherwise game over
    '''
    
    def check_for_pins_and_checks(self):
        pins=[]
        checks=[]
        incheck=False
        if self.whiteToMove:
            my_color='w'
            enemy_color='b'
            start_row,start_col = self.white_king_location
        else:
            my_color='b'
            enemy_color='w'
            start_row,start_col = self.black_king_location
            
        for j,(x,y) in enumerate(self.king_directions):
            possible_pins = ()
            for i in range(1,8):
                new_x,new_y = start_row+ x*i , start_col + y*i
                if self.is_valid_square(new_x,new_y):
                    end_peice = self.board[new_x][new_y]
                    if end_peice[0]==my_color and end_peice[1]!='K':
                        if possible_pins == (): #first pin could be found 
                            possible_pins = (new_x,new_y,x,y) #
                        else: # 2nd allied peice or no pins break
                            break 
                    elif end_peice[0] == enemy_color :
                        type = end_peice[1]
                        #5 possibilities here in this complex situation 
                        # orthogonnaly rook
                        # diagonally king
                        #anywhere king
                        # pawn or king at one square distance 
                        #any direction 1 square away and peice is a king (necessary to not to go in other king's controlled square)
                        
   
                        if (0<=j<=3 and type=='R') or \
                        (4<=j<=7 and type=='B') or \
                        (type=='Q') or \
                        (i==1 and type=='K') or \
                        (i==1 and type=='p' and (
                            (enemy_color=='w' and j in [6,7]) or
                            (enemy_color=='b' and j in [4,5])
                        )):
                            if possible_pins == ():
                                incheck = True
                                checks.append((new_x,new_y,x,y))
                            else:
                                pins.append(possible_pins)
                                break
                        else:
                            break
                    
                else:
                    break
            
            
                        
        for x,y in self.knight_directions:
            new_x,new_y =  start_row + x,start_col + y
            if self.is_valid_square(new_x,new_y):
                end_peice = self.board[new_x][new_y]
                if end_peice[1]== 'N' and end_peice[0]==enemy_color:  #kinght attack king
                    incheck=True
                    
                    checks.append((new_x,new_y,x,y))
        
        return incheck,pins,checks

    def has_check(self):
        if self.whiteToMove:
            return self.square_under_attack(self.white_king_location[0],self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0],self.black_king_location[1])
        pass
        
    '''
    this determines if enemy can attack this square
    '''
    def square_under_attack(self,r,c):
        self.whiteToMove = not self.whiteToMove  #change to my opponent
        opp_moves = self.get_all_possible_moves()
        for move in opp_moves:
            if move.end_row == r and move.end_col == c:
                self.whiteToMove = not self.whiteToMove 
                return True
        self.whiteToMove = not self.whiteToMove 
        return False
            
        
        
    '''
    all moves without checks 
    for each possible move check to see if it is a valid move by doing the following 
    make a move 
    generate moves for opposite player 
    see if any of ur moves ur king is attacked
    king is move add valid move to the list 
    '''
    def get_all_possible_moves(self):
        moves=[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn=='b' and not self.whiteToMove):
                    peice = self.board[r][c][1]
                    self.move_functions[peice](r,c,moves) #calls the appropriate move functions
        return moves
    '''
    this func return  the pawn moves for particular pawn
    '''
    def get_pawn_moves(self,r,c,moves: list):
        peice_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1]==c:
                peice_pinned=True
                pin_direction = (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        if self.whiteToMove:
            if r == 6 :
                if not peice_pinned or pin_direction == (-1,0):
                    if self.board[4][c]=='--' and self.board[5][c]=='--':
                        moves.append(Move((6,c),(4,c),self.board))
            if self.board[r-1][c]=='--':
                if not peice_pinned or pin_direction == (-1,0):
                        moves.append(Move((r,c),(r-1,c),self.board))
            if c>=1: 
                if not peice_pinned or pin_direction == (-1,-1):
                    if self.board[r-1][c-1][0]=='b':
                        moves.append(Move((r,c),(r-1,c-1),self.board))
                    elif  (r-1,c-1)==self.empassant_moves:
                        moves.append(Move((r,c),(r-1,c-1),self.board,is_empassant_move=True))
            if c<=6 :
                if not peice_pinned or pin_direction == (-1,+1):
                    if self.board[r-1][c+1][0]=='b':
                        moves.append(Move((r,c),(r-1,c+1),self.board))
                    elif  (r-1,c+1)==self.empassant_moves:
                        moves.append(Move((r,c),(r-1,c+1),self.board,is_empassant_move=True))
        else :
            if r<=6:
                if not peice_pinned or pin_direction == (1,0):
                    if self.board[r+1][c]=='--':
                        moves.append(Move((r,c),(r+1,c),self.board))
                    if r == 1:
                        if self.board[3][c]=='--' and self.board[2][c]=='--':
                            moves.append(Move((1,c),(3,c),self.board))
                if not peice_pinned or pin_direction == (1,-1):
                    if c>=1:
                        if self.board[r+1][c-1][0]=='w':
                            moves.append(Move((r,c),(r+1,c-1),self.board))
                        elif  (r+1,c-1)==self.empassant_moves:
                            moves.append(Move((r,c),(r+1,c-1),self.board,is_empassant_move=True))
                if not peice_pinned or pin_direction == (1,1):
                    if c<=6 :
                        if  self.board[r+1][c+1][0]=='w':
                            moves.append(Move((r,c),(r+1,c+1),self.board))
                        elif  (r+1,c+1)==self.empassant_moves:
                            moves.append(Move((r,c),(r+1,c+1),self.board,is_empassant_move=True))
        return moves
    '''
    this func return  the rook moves for particular rook
    '''
    def get_rook_moves(self,r,c,moves):
        peice_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1]==c:
                peice_pinned=True
                pin_direction = (self.pins[i][2],self.pins[i][3])
                if self.board[r][c][1]!='Q':  #cannot remove queen from pin on rook moves ,onl remove it from bishop moves
                    self.pins.remove(self.pins[i])
                break
        if self.whiteToMove:
            ur_symbol= 'w'
            opp = 'b'
        else:
            ur_symbol= 'b'
            opp = 'w'
        for x,y in [(-1,0),(1,0),(0,1),(0,-1)]:
            for i in range(1,8):
                new_x,new_y = r + x*i ,c + y*i
                if not self.is_valid_square(new_x,new_y):
                    break
                else:
                    if not peice_pinned or pin_direction == (x,y) or pin_direction == (-x,-y):
                        if self.board[new_x][new_y][0]=='-':
                            moves.append(Move((r,c),(new_x,new_y),self.board))
                        elif self.board[new_x][new_y][0]==opp:
                            moves.append(Move((r,c),(new_x,new_y),self.board))
                            break
                        else :
                            break
        return moves
            
    '''
    this func return  the knight moves for particular rook
    '''
    
    
    def get_knight_moves(self,r,c,moves):
        peice_pinned = False
        
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1]==c:
                peice_pinned=True
                self.pins.remove(self.pins[i])
                break
        
        if self.whiteToMove:
            ur_symbol= 'w'
            opp = 'b'
        else:
            ur_symbol= 'b'
            opp = 'w'
        for x,y in self.knight_directions:
            new_x,new_y = r+x,c+y
            if (self.is_valid_square(new_x,new_y)):
                if not peice_pinned:
                    if self.board[new_x][new_y][0]!=ur_symbol:
                        moves.append(Move((r,c),(new_x,new_y),self.board))
        return moves
    '''
    this func return  the bishop moves for particular rook
    '''
    def get_bishop_moves(self,r,c,moves):
        peice_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1]==c:
                peice_pinned=True
                pin_direction = (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        if self.whiteToMove:
            ur_symbol= 'w'
            opp = 'b'
        else:
            ur_symbol= 'b'
            opp = 'w'
        for x,y in self.bishop_directions:
            for i in range(1,8):
                new_x,new_y = r + x*i ,c + y*i
                if not self.is_valid_square(new_x,new_y):
                    break
                else:
                    if not peice_pinned or pin_direction == (x,y) or pin_direction == (-x,-y):
                        if self.board[new_x][new_y][0]=='-':
                            moves.append(Move((r,c),(new_x,new_y),self.board))
                        elif self.board[new_x][new_y][0]==opp:
                            moves.append(Move((r,c),(new_x,new_y),self.board))
                            break
                        else :
                            break
        return moves
                        
    '''
    this func return  the king moves for particular king
    '''
    def get_king_moves(self,r,c,moves):
        
        if self.whiteToMove:
            ur_symbol= 'w'
            opp = 'b'
        else:
            ur_symbol= 'b'
            opp = 'w'
        for x,y in self.king_directions:
            new_x,new_y = r+x,c+y
            if (self.is_valid_square(new_x,new_y)):
                if self.board[new_x][new_y][0]!=ur_symbol:
                    if ur_symbol == 'w':
                        self.white_king_location = (new_x,new_y)
                    else:
                        self.black_king_location = (new_x,new_y)
                    incheck,pins,checks = self.check_for_pins_and_checks() #check for pins and checks and if not add the move 
                    if not incheck:
                        moves.append(Move((r,c),(new_x,new_y),self.board))
                    if ur_symbol == 'w':
                        self.white_king_location = (r,c)
                    else:
                        self.black_king_location = (r,c) # place king in original position                
        return moves
    '''
    this func return  the queen moves for particular rook
    '''
    def get_queen_moves(self,r,c,moves):
        return self.get_bishop_moves(r,c,moves) + self.get_rook_moves(r,c,moves)

    
    '''
    generate all castle moves 
    
    '''
    def get_castle_moves(self,r,c,moves,my_color):
        if self.square_under_attack(r,c):
            return # cannot castle if king is in check
        if (self.whiteToMove and self.current_castling_rights.wks) or (not self.whiteToMove and self.current_castling_rights.bks):
            self.king_side_castle_moves(r,c,moves,my_color)
        if (self.whiteToMove and self.current_castling_rights.wqs) or (not self.whiteToMove and self.current_castling_rights.bqs):
            self.queen_side_castle_moves(r,c,moves,my_color)
        
    def king_side_castle_moves(self,r,c,moves,my_color):
        if c + 2 <= 7:
            if self.board[r][c+1]== '--' and self.board[r][c+2]== '--':
                if not self.square_under_attack(r,c+1) and not self.square_under_attack(r,c+2):
                    moves.append ( Move((r,c),(r,c+2),self.board,castle=True))
                
                
            
    
    
    def queen_side_castle_moves(self,r,c,moves,my_color):
        if c-3 >=0: 
            if self.board[r][c-1]== '--' and self.board[r][c-2]== '--' and self.board[r][c-3]== '--':
                if not self.square_under_attack(r,c-1) and not self.square_under_attack(r,c-2)  :
                    moves.append ( Move((r,c),(r,c-2),self.board,castle=True))
                
'''
make castling right class other wise difficult to include it in main code 
'''
class Castling_Rights():
    def __init__(self,wks,wqs,bks,bqs):
        self.bks=bks
        self.bqs=bqs
        self.wks=wks
        self.wqs=wqs
    
class Move():
    ranks_to_rows = {
        '1':7,'2':6,'3':5,'4':4,'5':3,'6':2,'7':1,'8':0}
    rows_to_ranks = {v:k for k,v in ranks_to_rows.items()}
    files_to_cols = {chr(97+i):i for i in range(8)}
    cols_to_files={v:k for k,v in files_to_cols.items()}
    def __init__(self,startsq,endsq,board,choice='Q',is_empassant_move=False,castle=False):     #for undowing the move its better to store the board information
        self.start_row = startsq[0]
        self.start_col = startsq[1]
        self.end_row = endsq[0]
        self.end_col = endsq[1]
        
        self.peice_moved = board[self.start_row][self.start_col]
        self.peice_captured = board[self.end_row][self.end_col] 
        self.is_pawn_promotion = False
        if (self.peice_moved == 'wp' and self.end_row==0) or (self.peice_moved == 'bp' and self.end_row==7):
            self.is_pawn_promotion=True
        self.promotion_choice =choice
        self.is_empassant_move=False
        if is_empassant_move:
            self.is_empassant_move=True
            self.peice_captured = 'wp' if self.peice_moved =='bp' else 'bp'
        self.castle=castle
        self.is_capture = self.peice_captured!='--'
        
        self.move_id =  self.start_row*1000 + self.start_col * 100 + self.end_row * 10 + self.end_col # generate unique id and since all below 10 we can do this   
    #have to tell python if two moves are equal
    '''
    over writing a method 
    other wise python check and they are two different objects 
    ''' 
    def __eq__(self, value):
        if isinstance(value,Move):
            return value.move_id == self.move_id
        return False
            
    def get_chess_notation(self):
        #make it to look move in chess notation 
        return self.get_rank_file(self.start_row,self.start_col) + self.get_rank_file(self.end_row,self.end_col)
    
    def get_rank_file(self,r,c):
        return self.cols_to_files[c]+ self.rows_to_ranks[r] #first column than row 
    def __str__(self):
        #castle move 
        if self.castle: 
            return "o-o" if self.end_col==6 else 'o-o-o'
        end_square = self.get_rank_file(self.end_row,self.end_col)
        #pawn move
        if self.peice_moved[1] == 'p':
            if self.is_capture:
                return self.cols_to_files[self.start_col] + 'x'+ end_square + f"""   {self.peice_moved} from {self.get_rank_file(self.start_row, self.start_col)}  to   {self.get_rank_file(self.end_row, self.end_col)}"""
            else:
                return end_square+ f"""   {self.peice_moved} from {self.get_rank_file(self.start_row, self.start_col)}  to   {self.get_rank_file(self.end_row, self.end_col)}"""
        # pawn promotion
        #Nbd2 both knights can move to d2
        
        # for check and checkmate
        # peice moves 
        move_string = self.peice_moved[1]
        if self.is_capture:
            move_string+='x'
        return move_string + end_square + f"""   {self.peice_moved} from {self.get_rank_file(self.start_row, self.start_col)}  to   {self.get_rank_file(self.end_row, self.end_col)}"""
    
    
        
        
        
        