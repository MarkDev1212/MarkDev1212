import os
from PIL import Image, ImageDraw, ImageFont

# Setup Configuration
WIDTH, HEIGHT = 500, 500
BG_COLOR = "#0D1117"
TERMINAL_BG = "#161B22"
BORDER_COLOR = "#30363D"
TEXT_COLOR = "#C9D1D9"
ACCENT_COLOR = "#58A6FF"
KEYWORD_COLOR = "#FF7B72"
STRING_COLOR = "#A5D6FF"

os.makedirs("Images", exist_ok=True)

# Font selection
def get_font(size):
    try:
        return ImageFont.truetype("consola.ttf", size)
    except:
        try:
            return ImageFont.truetype("Menlo.ttc", size)
        except:
            return ImageFont.load_default()

font_title = get_font(24)
font_code = get_font(18)
font_large = get_font(28)

def create_base_terminal():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([20, 20, 480, 480], radius=10, fill=TERMINAL_BG, outline=BORDER_COLOR, width=2)
    draw.ellipse([35, 35, 47, 47], fill="#FF5F56")
    draw.ellipse([55, 35, 67, 47], fill="#FFBD2E")
    draw.ellipse([75, 35, 87, 47], fill="#27C93F")
    draw.line([20, 60, 480, 60], fill=BORDER_COLOR, width=2)
    return img, draw

frames = []

# --- SCENE 1: Identity ---
for i in range(20):
    img, draw = create_base_terminal()
    if i > 5:
        draw.text((150, 220), "Markos Abebe", fill=TEXT_COLOR, font=font_large)
    if i > 10:
        draw.text((120, 260), "Full Stack Software Developer", fill=ACCENT_COLOR, font=font_title)
    frames.append(img)

# --- SCENE 2: Coding Animation ---
code_text = [
    ('const ', KEYWORD_COLOR), ('developer ', TEXT_COLOR), ('= {\n', TEXT_COLOR),
    ('  name: ', KEYWORD_COLOR), ('"Markos",\n', STRING_COLOR),
    ('  role: ', KEYWORD_COLOR), ('"Software Engineer",\n', STRING_COLOR),
    ('  build: ', KEYWORD_COLOR), ('"Digital Solutions"\n', STRING_COLOR),
    ('};', TEXT_COLOR)
]

total_chars = sum(len(part[0]) for part in code_text)

for i in range(40):
    img, draw = create_base_terminal()
    chars_to_draw = int((i / 40) * total_chars)
    
    x, y = 50, 100
    drawn = 0
    for text, color in code_text:
        for char in text:
            if drawn < chars_to_draw:
                if char == '\n':
                    y += 30
                    x = 50
                else:
                    draw.text((x, y), char, fill=color, font=font_code)
                    x += draw.textlength(char, font=font_code)
            drawn += 1
    frames.append(img)

for _ in range(10): frames.append(frames[-1])

# --- SCENE 3: Tech Stack ---
stack = ["Flutter", "React Native", "Next.js", "Node.js", "PostgreSQL"]
for i in range(30):
    img, draw = create_base_terminal()
    draw.text((50, 90), "> _load_tech_stack()", fill=ACCENT_COLOR, font=font_code)
    y = 140
    for j, tech in enumerate(stack):
        if i > j * 5:
            draw.text((70, y), f"• {tech}", fill=TEXT_COLOR, font=font_code)
            y += 35
    frames.append(img)

for _ in range(10): frames.append(frames[-1])

# --- SCENE 4: Engineering Mindset ---
mindset = ["Build", "Learn", "Improve", "Repeat"]
for i in range(30):
    img, draw = create_base_terminal()
    draw.text((50, 100), "Initializing Mindset...", fill=TEXT_COLOR, font=font_code)
    
    progress = min(400, int((i / 25) * 400))
    draw.rectangle([50, 150, 450, 165], outline=BORDER_COLOR, fill=BG_COLOR)
    draw.rectangle([50, 150, 50 + progress, 165], fill=ACCENT_COLOR)
    
    y = 200
    for j, word in enumerate(mindset):
        if progress > (j + 1) * 80:
            draw.text((50 + (j * 100), y), word, fill=STRING_COLOR, font=font_code)
    frames.append(img)

# --- SCENE 5: Final Frame ---
for i in range(20):
    img, draw = create_base_terminal()
    draw.text((110, 220), "Building Digital Solutions 🚀", fill=ACCENT_COLOR, font=font_large)
    frames.append(img)

for _ in range(20): frames.append(frames[-1])

# 2. Save as GIF
output_path = "Images/about_me.gif"
frames[0].save(
    output_path,
    save_all=True,
    append_images=frames[1:],
    optimize=True,
    duration=100, 
    loop=0
)
print(f"Success! Saved GIF to {output_path}")