import os
import math
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 500, 500
BG_COLOR = "#0D1117"      # GitHub Dark BG
FRAME_COLOR = "#161B22"   # Outer Frame
DOOR_COLOR = "#21262D"    # Door Panels
DOOR_LINE = "#30363D"     # Door details
INSIDE_COLOR = "#010409"  # Pitch black inside
TEXT_COLOR = "#58A6FF"    # Neon blue text

os.makedirs("Images", exist_ok=True)


def get_font(size):
    try:
        return ImageFont.truetype("arialbd.ttf", size)
    except:
        try:
            return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
        except:
            return ImageFont.load_default()

try:
    resample_method = Image.Resampling.LANCZOS
except AttributeError:
    resample_method = Image.LANCZOS

font = get_font(70)
text = "MARKOS"

# ፅሁፉን የያዘ ትልቅ ግልፅ ምስል መፍጠር
text_base = Image.new("RGBA", (400, 200), (0, 0, 0, 0))
draw_tb = ImageDraw.Draw(text_base)
try:
    bbox = draw_tb.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
except AttributeError:
    tw, th = draw_tb.textsize(text, font=font)

draw_tb.text(((400 - tw) // 2, (200 - th) // 2), text, fill=TEXT_COLOR, font=font)

door_x1, door_y1 = 100, 100
door_x2, door_y2 = 400, 400
center_x = 250

def draw_sliding_door(draw, x1, y1, x2, y2, is_left):
    if x2 <= x1: return 
    
    draw.rectangle([x1, y1, x2, y2], fill=DOOR_COLOR, outline=DOOR_LINE, width=3)
    
    handle_w, handle_h = 8, 80
    if is_left:
        hx1 = x2 - 15 - handle_w
    else:
        hx1 = x1 + 15
    
    hx2 = hx1 + handle_w
    hy1 = 250 - (handle_h // 2)
    hy2 = 250 + (handle_h // 2)
    
    if hx1 > x1 and hx2 < x2:
        
        draw.rounded_rectangle([hx1, hy1, hx2, hy2], fill="#8B949E", radius=4)

def create_frame(slide_progress, zoom_progress):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([door_x1, door_y1, door_x2, door_y2], fill=INSIDE_COLOR)
    
    scale = 0.5 + (0.5 * zoom_progress)
    new_w, new_h = int(400 * scale), int(200 * scale)
    
    if new_w > 0 and new_h > 0:
        resized_text = text_base.resize((new_w, new_h), resample_method)
        paste_x = center_x - (new_w // 2)
        paste_y = 250 - (new_h // 2)
        img.paste(resized_text, (paste_x, paste_y), resized_text)
        
    open_width = int(150 * slide_progress)
    left_door_right = center_x - open_width
    right_door_left = center_x + open_width
    
    draw_sliding_door(draw, door_x1, door_y1, left_door_right, door_y2, True)  
    draw_sliding_door(draw, right_door_left, door_y1, door_x2, door_y2, False) 
    
    draw.rectangle([door_x1-15, door_y1-15, door_x2+15, door_y2+15], outline=FRAME_COLOR, width=15)
    
    return img

frames = []

for _ in range(15):
    frames.append(create_frame(slide_progress=0.0, zoom_progress=0.0))

open_frames = 25
for i in range(open_frames):
    progress = math.sin((i / open_frames) * (math.pi / 2))
    frames.append(create_frame(slide_progress=progress, zoom_progress=progress))

hold_frames = 35
for i in range(hold_frames):
    extra_zoom = 1.0 + (i / hold_frames) * 0.1 
    frames.append(create_frame(slide_progress=1.0, zoom_progress=extra_zoom))

close_frames = 15
for i in range(close_frames):
    progress = 1.0 - math.sin((i / close_frames) * (math.pi / 2))
    frames.append(create_frame(slide_progress=progress, zoom_progress=1.1))

for _ in range(5):
    frames.append(create_frame(slide_progress=0.0, zoom_progress=0.0))

output_path = "Images/my_avatar.gif"
frames[0].save(
    output_path,
    save_all=True,
    append_images=frames[1:],
    duration=40,
    loop=0
)
print(f"Success! Ultimate Sliding Door Animation saved to {output_path}")