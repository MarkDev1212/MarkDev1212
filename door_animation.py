import os
import math
from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 700, 400
BG_COLOR = "#0D1117"
FRAME_COLOR = "#161B22"
DOOR_COLOR = "#FFD700"
DOOR_LINE = "#30363D"
INSIDE_COLOR = "#010409"
TEXT_COLOR = "#58A6FF"      
SUB_COLOR = "#C9D1D9"       

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

font_main = get_font(80)
font_sub = get_font(28)  

text_main = "MARKOS"
text_sub = "Software Developer"

text_base = Image.new("RGBA", (500, 150), (0, 0, 0, 0))
draw_tb = ImageDraw.Draw(text_base)
try:
    bbox = draw_tb.textbbox((0, 0), text_main, font=font_main)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
except AttributeError:
    tw, th = draw_tb.textsize(text_main, font=font_main)
draw_tb.text(((500 - tw) // 2, (150 - th) // 2), text_main, fill=TEXT_COLOR, font=font_main)


sub_base = Image.new("RGBA", (500, 80), (0, 0, 0, 0))
draw_sub = ImageDraw.Draw(sub_base)
try:
    bbox = draw_sub.textbbox((0, 0), text_sub, font=font_sub)
    sw = bbox[2] - bbox[0]
    sh = bbox[3] - bbox[1]
except AttributeError:
    sw, sh = draw_sub.textsize(text_sub, font=font_sub)
draw_sub.text(((500 - sw) // 2, (80 - sh) // 2), text_sub, fill=SUB_COLOR, font=font_sub)


door_x1, door_y1 = 100, 50
door_x2, door_y2 = 600, 350
center_x = 350

def draw_sliding_door(draw, x1, y1, x2, y2, is_left):
    if x2 <= x1: return 
    draw.rectangle([x1, y1, x2, y2], fill=DOOR_COLOR, outline=DOOR_LINE, width=3)
    
    handle_w, handle_h = 10, 100
    if is_left:
        hx1 = x2 - 20 - handle_w
    else:
        hx1 = x1 + 20
    
    hx2 = hx1 + handle_w
    hy1 = 200 - (handle_h // 2)
    hy2 = 200 + (handle_h // 2)
    
    if hx1 > x1 and hx2 < x2:
        draw.rounded_rectangle([hx1, hy1, hx2, hy2], fill="#8B949E", radius=5)

def create_frame(slide_progress, zoom_progress, sub_opacity):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
   
    draw.rectangle([door_x1, door_y1, door_x2, door_y2], fill=INSIDE_COLOR)
    
    
    scale = 0.5 + (0.5 * zoom_progress)
    new_w, new_h = int(500 * scale), int(150 * scale)
    if new_w > 0 and new_h > 0:
        resized_text = text_base.resize((new_w, new_h), resample_method)
        paste_x = center_x - (new_w // 2)
        paste_y = 180 - (new_h // 2) - int(20 * scale) # ፅሁፉን ትንሽ ወደ ላይ ማድረግ
        img.paste(resized_text, (paste_x, paste_y), resized_text)
        
    # Software Developer ብቅ ሲል (Fade-in)
    if sub_opacity > 0:
        if sub_opacity < 1.0:
            alpha_sub = sub_base.copy()
            alpha_data = alpha_sub.getdata()
            new_data = [(r, g, b, int(a * sub_opacity)) for r, g, b, a in alpha_data]
            alpha_sub.putdata(new_data)
            paste_sub = alpha_sub
        else:
            paste_sub = sub_base
        
        sub_paste_x = center_x - (500 // 2)
        sub_paste_y = 220 # ከ MARKOS ስር
        img.paste(paste_sub, (sub_paste_x, sub_paste_y), paste_sub)
        
   
    open_width = int(250 * slide_progress)
    left_door_right = center_x - open_width
    right_door_left = center_x + open_width
    
    draw_sliding_door(draw, door_x1, door_y1, left_door_right, door_y2, True)  
    draw_sliding_door(draw, right_door_left, door_y1, door_x2, door_y2, False) 
    
   
    draw.rectangle([door_x1-15, door_y1-15, door_x2+15, door_y2+15], outline=FRAME_COLOR, width=15)
    
    return img

frames = []


for _ in range(15):
    frames.append(create_frame(0.0, 0.0, 0.0))


open_frames = 25
for i in range(open_frames):
    progress = math.sin((i / open_frames) * (math.pi / 2))
    frames.append(create_frame(progress, progress, 0.0))


fade_frames = 15
for i in range(fade_frames):
    sub_progress = i / float(fade_frames)
    extra_zoom = 1.0 + (i / fade_frames) * 0.02
    frames.append(create_frame(1.0, extra_zoom, sub_progress))


hold_frames = 30
for i in range(hold_frames):
    extra_zoom = 1.02 + (i / hold_frames) * 0.05
    frames.append(create_frame(1.0, extra_zoom, 1.0))


close_frames = 15
for i in range(close_frames):
    progress = 1.0 - math.sin((i / close_frames) * (math.pi / 2))
    frames.append(create_frame(progress, 1.07, 0.0))


for _ in range(5):
    frames.append(create_frame(0.0, 0.0, 0.0))


output_path = "Images/my_avatar.gif"
frames[0].save(
    output_path,
    save_all=True,
    append_images=frames[1:],
    duration=40,
    loop=0
)
print(f"Success! Wide Door Animation with Subtitle saved to {output_path}")