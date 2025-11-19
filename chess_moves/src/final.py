import chess.svg
import chess
import re
import cv2
import random as rd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
import chess, chess.svg
from pathlib import Path
import webbrowser
piece_symbols = 'prbnkqPRBNKQ-'
try:
    model = load_model('./chess_model.h5')
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    
def onehot_from_fen(fen):
    eye = np.eye(13)
    output = np.empty((0, 13))
    fen = re.sub('[-]', '', fen)

    for char in fen:
        if(char in '12345678'):
            output = np.append(output, np.tile(eye[12], (int(char), 1)), axis=0)
        else:
            idx = piece_symbols.index(char)
            output = np.append(output, eye[idx].reshape((1, 13)), axis=0)
    return output
import numpy as np
import re



def board_from_fen(fen):
    board = []
    fen = fen.split()[0]   # just the board part (ignore turn, castling, etc.)
    
    for row in fen.split('/'):
        row_out = []
        for char in row:
            if char.isdigit():
                # expand empty squares
                row_out.extend([0] * int(char))
            else:
                idx = piece_symbols.index(char) + 1  # +1 so 0 = empty
                row_out.append(idx)
        board.append(row_out)

    return np.array(board, dtype=np.int8)  # shape (8,8)

def fen_from_onehot(one_hot):
    output = ''
    for j in range(8):
        for i in range(8):
            if(one_hot[j][i] == 12):
                output += ' '
            else:
                output += piece_symbols[one_hot[j][i]]
        if(j != 7):
            output += '-'

    for i in range(8, 0, -1):
        output = output.replace(' ' * i, str(i))
    return output


def order_points(pts):
    # Order 4 points: top-left, top-right, bottom-right, bottom-left
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def preprocess_chessboard(image_path, target_size=(30, 30)):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    edges = cv2.Canny(blur, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cropped_board = None
    warped = None
    squares = []

    if contours:
        cnt = max(contours, key=cv2.contourArea)
        epsilon = 0.02 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # If we found 4 corners, warp
        if len(approx) == 4:
            pts = approx.reshape(4,2)
            rect = order_points(pts)
            board_size = 256  # fixed square board
            dst = np.array([
                [0, 0],
                [board_size-1, 0],
                [board_size-1, board_size-1],
                [0, board_size-1]
            ], dtype="float32")

            M = cv2.getPerspectiveTransform(rect, dst)
            warped = cv2.warpPerspective(img, M, (board_size, board_size))
            cropped_board = warped
        else:
            # fallback: just resize whole image
            warped = cv2.resize(img, (256, 256))
            cropped_board = warped
    else:
        # no contours, fallback
        warped = cv2.resize(img, (256, 256))
        cropped_board = warped

    # Split into 64 squares
    board_size = warped.shape[0]
    sq_size = board_size // 8
    for row in range(8):
        for col in range(8):
            square = warped[row*sq_size:(row+1)*sq_size,
                            col*sq_size:(col+1)*sq_size]
            square = cv2.resize(square, target_size)
            square = square / 255.0
            squares.append(square)

    return np.array(squares), cropped_board

def display_with_predicted_fen(image):
    squares,_ = preprocess_chessboard(image)
    pred = model.predict(squares).argmax(axis=1).reshape(8, 8)
    fen = fen_from_onehot(pred)
    return fen

def get_board_from_image(img_path):
    image = cv2.imread(img_path)
    if image is None:
        print('sorry image is null')
        return
    ext = img_path.split('.')[-1]
    if not (ext=='jpg' or ext == 'jpeg' or ext == 'png'):
        print('sorry image needs to be in jpg/jpeg/png format')
        return
    predicted_fen = display_with_predicted_fen(img_path)
    # Create board from predicted FEN
    board = chess.Board(predicted_fen.replace('-','/'))
    return predicted_fen
def get_board_from_fen(fen:str):
    print(type(fen))
    fen=fen.split('-')
    if len(fen)!=8:
        return [[]]
    answers = [[] for _ in range(8)]
    map={'p':'bp','r':'bR','n':'bN','k':'bK','q':'bQ','b':'bB','P':'wp','R':'wR','N':'wN','K':'wK','Q':'wQ','B':'wB'}
    for i,f in enumerate(fen):
        for char in f:
            
            if char in '12345678':
                answers[i].extend(['--']*(int(char)))
            elif char in piece_symbols:
                answers[i].append(map[char])
    return answers
                
    
def get_board(image_path):
    fen_notation = get_board_from_image(image_path)
    if fen_notation:
        board = get_board_from_fen(fen_notation)
        
    else:
        return [[]],""
    return board,fen_notation.replace('-','/')
    
if __name__ == "__main__":
    get_board()
    