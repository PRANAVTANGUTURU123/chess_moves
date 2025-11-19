import gradio as gr
import chess
import chess.svg
from PIL import Image
import io
import cairosvg

from main import get_moves   # your engine wrapper


def predict_from_image(img):
    # Save uploaded image
    img = img.convert("RGB")
    img.save("board.png", format="PNG")

    # Your function should return (fen, moves)
    fen, moves = get_moves("board.png")

    # Convert FEN -> SVG -> PNG for Gradio display
    board = chess.Board(fen)
    svg_data = chess.svg.board(board=board, size=350)

    # convert svg to png (since Gradio Image widget expects raster)
    png_bytes = cairosvg.svg2png(bytestring=svg_data)
    board_img = Image.open(io.BytesIO(png_bytes))
    moves_white = moves['white_moves']
    moves_black=moves['black_moves']
    white_moves_clean = [m[1] for m in moves_white]
    black_moves_clean = [m[1] for m in moves_black]

    return fen, "\n".join(white_moves_clean), "\n".join(black_moves_clean), board_img



with gr.Blocks() as demo:
    gr.Markdown("""
        #  chess move predictor using alpha beta pruning
        _Upload an image of an online chessboard and get the FEN & best moves._  

        ⚠️ **Warning:** Please upload screenshots from online chess games (e.g., Lichess, Chess.com).  
        Physical/real-world chessboard photos are not supported yet.
        """)

    with gr.Row():
        image = gr.Image(type="pil", label="Upload Chessboard Image")
        board_display = gr.Image(type="pil", label="Detected Board")

    fen_out = gr.Textbox(label="Detected FEN")
    moves_out = gr.Textbox(label="Predicted Best Moves")
    with gr.Row():
        moves_white = gr.Textbox(label="White's Moves", lines=6)
        moves_black = gr.Textbox(label="Black's Moves", lines=6)

    btn = gr.Button("Analyze Board")

    btn.click(
        fn=predict_from_image,
        inputs=image,
        outputs=[fen_out, moves_white, moves_black, board_display]
    )

demo.launch()
