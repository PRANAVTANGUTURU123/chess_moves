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

    return fen, str(moves), board_img


with gr.Blocks() as demo:
    gr.Markdown("# ♟️ Chess AI from Image")

    with gr.Row():
        image = gr.Image(type="pil", label="Upload Chessboard Image")
        board_display = gr.Image(type="pil", label="Detected Board")

    fen_out = gr.Textbox(label="Detected FEN")
    moves_out = gr.Textbox(label="Predicted Best Moves")

    btn = gr.Button("Analyze Board")

    btn.click(
        fn=predict_from_image,
        inputs=image,
        outputs=[fen_out, moves_out, board_display]
    )

demo.launch()
