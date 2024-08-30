from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import io
import random
import math

def create_realistic_puzzle(output_pdf, rows=3, cols=4, size=(800, 600)):
    try:
        width, height = size
        pdf_width, pdf_height = A4
        piece_width = width // cols
        piece_height = height // rows

        lock_size = min(piece_width, piece_height) // 3

        def draw_edge(draw, x, y, width, height, direction, is_tab):
            points = []
            for i in range(0, 101):
                t = i / 100
                if direction in ['right', 'left']:
                    x_offset = width * t
                    y_offset = height * (0.2 * math.sin(math.pi * t) + (0.5 if is_tab else -0.5) * math.sin(2 * math.pi * t))
                else:  # up or down
                    x_offset = width * (0.2 * math.sin(math.pi * t) + (0.5 if is_tab else -0.5) * math.sin(2 * math.pi * t))
                    y_offset = height * t
                
                if direction == 'left':
                    points.append((x + width - x_offset, y + y_offset))
                elif direction == 'right':
                    points.append((x + x_offset, y + y_offset))
                elif direction == 'up':
                    points.append((x + x_offset, y + height - y_offset))
                else:  # down
                    points.append((x + x_offset, y + y_offset))
            
            draw.line(points, fill='black', width=2, joint='curve')

        # Vytvoření PDF
        c = canvas.Canvas(output_pdf, pagesize=A4)

        for i in range(rows):
            for j in range(cols):
                img = Image.new('RGB', (piece_width, piece_height), color='white')
                draw = ImageDraw.Draw(img)
                
                # Horní okraj
                if i > 0:
                    is_tab = random.choice([True, False])
                    draw_edge(draw, 0, 0, piece_width, lock_size, 'up', is_tab)
                else:
                    draw.line([(0, 0), (piece_width, 0)], fill='black', width=2)

                # Levý okraj
                if j > 0:
                    is_tab = random.choice([True, False])
                    draw_edge(draw, 0, 0, lock_size, piece_height, 'left', is_tab)
                else:
                    draw.line([(0, 0), (0, piece_height)], fill='black', width=2)

                # Pravý okraj
                if j < cols - 1:
                    is_tab = random.choice([True, False])
                    draw_edge(draw, piece_width - lock_size, 0, lock_size, piece_height, 'right', is_tab)
                else:
                    draw.line([(piece_width, 0), (piece_width, piece_height)], fill='black', width=2)

                # Dolní okraj
                if i < rows - 1:
                    is_tab = random.choice([True, False])
                    draw_edge(draw, 0, piece_height - lock_size, piece_width, lock_size, 'down', is_tab)
                else:
                    draw.line([(0, piece_height), (piece_width, piece_height)], fill='black', width=2)

                # Konverze PIL Image na ImageReader
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                img_reader = ImageReader(io.BytesIO(img_byte_arr))

                # Přidání dílku do PDF
                c.drawImage(img_reader, 0, 0, width=pdf_width, height=pdf_height, preserveAspectRatio=True)
                c.showPage()

        c.save()
        print(f"PDF soubor {output_pdf} byl úspěšně vytvořen.")
    except Exception as e:
        print(f"Došlo k neočekávané chybě: {e}")

# Použití funkce
output_pdf = input("Zadejte název výstupního PDF souboru: ")
create_realistic_puzzle(output_pdf)