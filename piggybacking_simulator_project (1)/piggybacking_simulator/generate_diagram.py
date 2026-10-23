import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("assets", exist_ok=True)

# Generate high-resolution image (1600 x 560)
W, H = 1600, 560
img = Image.new("RGB", (W, H), color="#111620")
draw = ImageDraw.Draw(img)

# Try loading standard Windows fonts
try:
    font_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 34)
    font_station = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 32)
    font_label = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 26)
    font_bold_label = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 27)
except Exception:
    font_title = ImageFont.load_default()
    font_station = font_title
    font_label = font_title
    font_bold_label = font_title

# Outer card border
draw.rounded_rectangle([10, 10, W - 10, H - 10], radius=16, outline="#2d3748", width=2)

# Center divider between Left (Normal ACK) and Right (Piggybacking)
draw.line([(W // 2, 35), (W // 2, H - 35)], fill="#2d3748", width=2)

# ==================== LEFT: Normal ACK ====================
left_center_x = W // 4
left_a_x = left_center_x - 270
left_b_x = left_center_x + 270

# Title
title_left = "Normal ACK: frames"
bbox_tl = draw.textbbox((0, 0), title_left, font=font_title)
tw_tl = bbox_tl[2] - bbox_tl[0]
draw.text((left_center_x - tw_tl // 2, 40), title_left, fill="#ff5252", font=font_title)

# Station headers
draw.text((left_a_x - 12, 95), "A", fill="#ffffff", font=font_station)
draw.text((left_b_x - 12, 95), "B", fill="#ffffff", font=font_station)

# Vertical timeline lines
draw.line([(left_a_x, 140), (left_a_x, H - 45)], fill="#718096", width=3)
draw.line([(left_b_x, 140), (left_b_x, H - 45)], fill="#718096", width=3)

# Helper function to draw arrowheads
def draw_arrow_head(x, y, direction="right", color="#ff5252", size=14):
    if direction == "right":
        points = [(x, y), (x - size, y - size // 2), (x - size + 2, y), (x - size, y + size // 2)]
    else:  # left
        points = [(x, y), (x + size, y - size // 2), (x + size - 2, y), (x + size, y + size // 2)]
    draw.polygon(points, fill=color)

# Helper for dashed line
def draw_dashed_line(x1, y1, x2, y2, fill="#a0aec0", width=2, dash=10, gap=8):
    if x1 > x2:
        x1, x2 = x2, x1
        reverse = True
    else:
        reverse = False
    curr_x = x1
    while curr_x < x2:
        end_x = min(curr_x + dash, x2)
        draw.line([(curr_x, y1), (end_x, y2)], fill=fill, width=width)
        curr_x += dash + gap

# 4 Rows for Left Side
rows_y = [185, 270, 355, 440]

# Row 1: DATA (A -> B)
lbl1 = "DATA"
bbox = draw.textbbox((0, 0), lbl1, font=font_label)
draw.text((left_center_x - (bbox[2] - bbox[0]) // 2, rows_y[0] - 32), lbl1, fill="#e2e8f0", font=font_label)
draw.line([(left_a_x + 5, rows_y[0]), (left_b_x - 8, rows_y[0])], fill="#ff5252", width=4)
draw_arrow_head(left_b_x - 2, rows_y[0], direction="right", color="#ff5252", size=16)

# Row 2: ACK (B -> A)
lbl2 = "ACK"
bbox = draw.textbbox((0, 0), lbl2, font=font_label)
draw.text((left_center_x - (bbox[2] - bbox[0]) // 2, rows_y[1] - 32), lbl2, fill="#cbd5e1", font=font_label)
draw_dashed_line(left_a_x + 12, rows_y[1], left_b_x - 5, rows_y[1], fill="#94a3b8", width=3, dash=12, gap=8)
draw_arrow_head(left_a_x + 2, rows_y[1], direction="left", color="#94a3b8", size=14)

# Row 3: DATA (A -> B)
lbl3 = "DATA"
bbox = draw.textbbox((0, 0), lbl3, font=font_label)
draw.text((left_center_x - (bbox[2] - bbox[0]) // 2, rows_y[2] - 32), lbl3, fill="#e2e8f0", font=font_label)
draw.line([(left_a_x + 5, rows_y[2]), (left_b_x - 8, rows_y[2])], fill="#ff5252", width=4)
draw_arrow_head(left_b_x - 2, rows_y[2], direction="right", color="#ff5252", size=16)

# Row 4: ACK (B -> A)
lbl4 = "ACK"
bbox = draw.textbbox((0, 0), lbl4, font=font_label)
draw.text((left_center_x - (bbox[2] - bbox[0]) // 2, rows_y[3] - 32), lbl4, fill="#cbd5e1", font=font_label)
draw_dashed_line(left_a_x + 12, rows_y[3], left_b_x - 5, rows_y[3], fill="#94a3b8", width=3, dash=12, gap=8)
draw_arrow_head(left_a_x + 2, rows_y[3], direction="left", color="#94a3b8", size=14)


# ==================== RIGHT: Piggybacking ====================
right_center_x = (3 * W) // 4
right_a_x = right_center_x - 270
right_b_x = right_center_x + 270

# Title
title_right = "Piggybacking: ACK rides on data"
bbox_tr = draw.textbbox((0, 0), title_right, font=font_title)
tw_tr = bbox_tr[2] - bbox_tr[0]
draw.text((right_center_x - tw_tr // 2, 40), title_right, fill="#2ecc71", font=font_title)

# Station headers
draw.text((right_a_x - 12, 95), "A", fill="#ffffff", font=font_station)
draw.text((right_b_x - 12, 95), "B", fill="#ffffff", font=font_station)

# Vertical timeline lines
draw.line([(right_a_x, 140), (right_a_x, H - 45)], fill="#718096", width=3)
draw.line([(right_b_x, 140), (right_b_x, H - 45)], fill="#718096", width=3)

# Row 1: DATA (A -> B)
bbox = draw.textbbox((0, 0), lbl1, font=font_label)
draw.text((right_center_x - (bbox[2] - bbox[0]) // 2, rows_y[0] - 32), lbl1, fill="#e2e8f0", font=font_label)
draw.line([(right_a_x + 5, rows_y[0]), (right_b_x - 8, rows_y[0])], fill="#ff5252", width=4)
draw_arrow_head(right_b_x - 2, rows_y[0], direction="right", color="#ff5252", size=16)

# Row 2: DATA + ACK (B -> A) - THICK SOLID GREEN
lbl_piggy = "DATA + ACK"
bbox = draw.textbbox((0, 0), lbl_piggy, font=font_bold_label)
draw.text((right_center_x - (bbox[2] - bbox[0]) // 2, rows_y[1] - 34), lbl_piggy, fill="#2ecc71", font=font_bold_label)
draw.line([(right_b_x - 5, rows_y[1]), (right_a_x + 14, rows_y[1])], fill="#2ecc71", width=6)
draw_arrow_head(right_a_x + 2, rows_y[1], direction="left", color="#2ecc71", size=18)

# Row 3: DATA (A -> B)
bbox = draw.textbbox((0, 0), lbl3, font=font_label)
draw.text((right_center_x - (bbox[2] - bbox[0]) // 2, rows_y[2] - 32), lbl3, fill="#e2e8f0", font=font_label)
draw.line([(right_a_x + 5, rows_y[2]), (right_b_x - 8, rows_y[2])], fill="#ff5252", width=4)
draw_arrow_head(right_b_x - 2, rows_y[2], direction="right", color="#ff5252", size=16)

# Row 4: DATA + ACK (B -> A) - THICK SOLID GREEN
bbox = draw.textbbox((0, 0), lbl_piggy, font=font_bold_label)
draw.text((right_center_x - (bbox[2] - bbox[0]) // 2, rows_y[3] - 34), lbl_piggy, fill="#2ecc71", font=font_bold_label)
draw.line([(right_b_x - 5, rows_y[3]), (right_a_x + 14, rows_y[3])], fill="#2ecc71", width=6)
draw_arrow_head(right_a_x + 2, rows_y[3], direction="left", color="#2ecc71", size=18)

# Save image
out_path = "assets/transmission_sequence_comparison.png"
img.save(out_path, format="PNG")
print(f"Diagram successfully generated at: {out_path}")
