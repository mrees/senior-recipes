
"""
Generate beautiful illustrative food images for each recipe.
Uses Pillow to create warm, appetising illustrations with
colour palettes matching each dish.
"""
import os, math, random
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "/sessions/relaxed-funny-mayer/wiki/images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

W, H = 800, 480

# ── palette bank ────────────────────────────────────────────────────────────
PAL = {
    "warmred":    ["#C0392B","#E74C3C","#EC7063","#F1948A","#F7CAC9","#FFF9F5"],
    "salmon":     ["#E8896A","#F5A78A","#F7C3A9","#FDE8DA","#FBF3EE","#FFF9F7"],
    "gold":       ["#D4A017","#F0C040","#F5D576","#FDE9A2","#FEF7D6","#FFFDF5"],
    "green":      ["#1E8449","#27AE60","#58D68D","#A9DFBF","#D5F5E3","#F2FBF4"],
    "teal":       ["#117A65","#1ABC9C","#48C9B0","#A3E4D7","#D1F2EB","#F0FEFA"],
    "purple":     ["#7D3C98","#A569BD","#C39BD3","#E8DAEF","#F5EEF8","#FDF9FF"],
    "orange":     ["#CA6F1E","#E67E22","#F0A500","#F7C982","#FDEBD0","#FFF8F2"],
    "blue":       ["#1A5276","#2874A6","#5DADE2","#AED6F1","#D6EAF8","#EBF5FB"],
    "cream":      ["#8B6914","#C9A64A","#DEC27A","#EDD9A3","#F8EDD5","#FFFDF5"],
    "rose":       ["#A93226","#CB4335","#E59866","#FAD7A0","#FEF9E7","#FFFFF8"],
}

def pal(name): return PAL.get(name, PAL["gold"])

def draw_bg(draw, colors, W, H):
    """Soft gradient background using two colors."""
    c1 = hex_to_rgb(colors[-1])
    c2 = hex_to_rgb(colors[-2])
    for y in range(H):
        t = y / H
        r = int(c1[0]*(1-t) + c2[0]*t)
        g = int(c1[1]*(1-t) + c2[1]*t)
        b = int(c1[2]*(1-t) + c2[2]*t)
        draw.line([(0,y),(W,y)], fill=(r,g,b))

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2],16) for i in (0,2,4))

def draw_plate(draw, cx, cy, r, fill="#F8F4EE", rim="#E0D5C5", shadow=True):
    if shadow:
        draw.ellipse([cx-r+8, cy-r//4+8, cx+r+8, cy+r//4+8], fill="#00000018")
    draw.ellipse([cx-r, cy-r//3, cx+r, cy+r//3], fill=rim)
    draw.ellipse([cx-r+12, cy-r//3+8, cx+r-12, cy+r//3-8], fill=fill)

def draw_bowl(draw, cx, cy, rw, rh, fill="#EAE0D5", rim="#C8B89A"):
    draw.ellipse([cx-rw, cy-rh//2, cx+rw, cy+rh], fill=rim)
    draw.ellipse([cx-rw+10, cy-rh//2+6, cx+rw-10, cy+rh-6], fill=fill)

def draw_circle(draw, cx, cy, r, fill, outline=None, width=2):
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=fill, outline=outline, width=width)

def draw_rect(draw, x1, y1, x2, y2, fill, outline=None, radius=8):
    draw.rounded_rectangle([x1,y1,x2,y2], radius=radius, fill=fill, outline=outline)

def draw_leaf(draw, cx, cy, size, angle, color):
    pts = []
    for a in range(-60, 61, 10):
        r = size * math.cos(math.radians(a)) * 0.5
        th = math.radians(angle + a)
        pts.append((cx + r*math.cos(th), cy + r*math.sin(th)))
    if len(pts) >= 3:
        draw.polygon(pts, fill=color)

def draw_steam(draw, cx, cy, color="#CCCCCC80"):
    for i in range(3):
        ox = (i-1)*18
        for j in range(4):
            y0 = cy - j*14
            y1 = y0 - 10
            x0 = cx + ox + (j%2)*4
            x1 = cx + ox - (j%2)*4
            draw.line([(x0, y0),(x1, y1)], fill=color, width=2)

def add_label(img, title, colors):
    draw = ImageDraw.Draw(img)
    # Dark strip at bottom
    draw.rectangle([0, H-80, W, H], fill=hex_to_rgb(colors[0])+(230,))
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
        subfont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        font = ImageFont.load_default()
        subfont = font
    # Title
    draw.text((W//2, H-52), title, font=font, fill="white", anchor="mm")

def save_img(img, recipe_id):
    path = f"{OUTPUT_DIR}/{recipe_id}.jpg"
    img = img.convert("RGB")
    img.save(path, "JPEG", quality=90)
    return path

# ── individual recipe image generators ──────────────────────────────────────

def make_chicken_veggie_tray_bake():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    colors = pal("warmred")
    draw_bg(d, colors, W, H)
    # Tray
    draw_rect(d,120,160,680,380,fill="#8B6914",radius=4)
    draw_rect(d,130,170,670,370,fill="#C4A35A",radius=4)
    # Chicken thighs
    d.ellipse([200,195,320,295],fill="#8B4513")
    d.ellipse([210,205,310,285],fill="#A0522D")
    d.ellipse([340,195,460,295],fill="#8B4513")
    d.ellipse([350,205,450,285],fill="#A0522D")
    # Potatoes
    for cx,cy in [(200,330),(250,320),(300,335),(350,320)]:
        draw_circle(d,cx,cy,22,fill="#D4A017")
        draw_circle(d,cx,cy,18,fill="#E8C547")
    # Zucchini slices
    for cx in [450,490,530]:
        draw_circle(d,cx,290,18,fill="#27AE60")
        draw_circle(d,cx,290,12,fill="#58D68D")
    # Capsicum
    for cx,cy in [(500,230),(540,215),(480,210)]:
        draw_circle(d,cx,cy,16,fill="#E74C3C")
    # Lemon
    draw_circle(d,580,310,24,fill="#F7DC6F")
    draw_circle(d,580,310,16,fill="#F9E79F")
    # Steam
    draw_steam(d, 350, 165)
    return img

def make_salmon_honey_garlic():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("salmon"), W, H)
    draw_plate(d,400,240,200)
    # Broccoli bed
    for cx,cy,r in [(310,230,30),(360,200,28),(420,210,30),(470,230,28),(380,260,26)]:
        d.ellipse([cx-r,cy-r,cx+r,cy+r],fill="#1E8449")
        d.ellipse([cx-r+4,cy-r+4,cx+r-4,cy+r-4],fill="#27AE60")
    # Salmon fillet
    pts=[(300,270),(440,220),(490,250),(480,290),(310,310)]
    d.polygon(pts,fill="#E8896A")
    d.polygon([(310,275),(430,228),(475,255),(468,285),(315,305)],fill="#F5A78A")
    # Honey glaze lines
    for i in range(3):
        y=260+i*12
        d.line([(320,y),(460,y-10)],fill="#D4A01760",width=3)
    draw_steam(d,390,215)
    return img

def make_sausage_cabbage_apple():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("gold"), W, H)
    draw_plate(d,400,240,200)
    # Cabbage chunks
    for cx,cy in [(300,230),(360,250),(430,240),(480,230),(340,290),(410,285)]:
        d.ellipse([cx-28,cy-20,cx+28,cy+20],fill="#7DCEA0")
        d.ellipse([cx-20,cy-14,cx+20,cy+14],fill="#A9DFBF")
    # Apple slices (golden)
    for cx,cy in [(280,280),(500,270),(390,310)]:
        d.ellipse([cx-20,cy-28,cx+20,cy+28],fill="#F4D03F")
        d.ellipse([cx-13,cy-20,cx+13,cy+20],fill="#F9E79F")
    # Sausage slices
    for cx,cy in [(310,200),(380,195),(460,200),(420,265),(350,260)]:
        d.ellipse([cx-22,cy-16,cx+22,cy+16],fill="#8B4513")
        d.ellipse([cx-16,cy-10,cx+16,cy+10],fill="#A0522D")
    return img

def make_tilapia_green_beans():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("teal"), W, H)
    draw_plate(d,400,240,200)
    # Green beans
    for i in range(8):
        x1=270+i*22; y1=260+random.randint(-10,10)
        x2=x1+10; y2=y1+70
        d.rectangle([x1,y1,x2,y2],fill="#27AE60")
    # Tilapia fillet (white fish)
    pts=[(280,190),(500,200),(510,260),(280,270)]
    d.polygon(pts,fill="#ECF0F1")
    d.polygon([(290,198),(490,207),(500,252),(290,260)],fill="#F8F9FA")
    # Lemon slices
    for cx,cy in [(360,215),(420,212),(480,218)]:
        draw_circle(d,cx,cy,20,fill="#F7DC6F")
        draw_circle(d,cx,cy,14,fill="#F9E79F")
        d.line([(cx-14,cy),(cx+14,cy)],fill="#F0C040",width=2)
    # Cherry tomatoes
    for cx,cy in [(290,295),(320,285),(350,292)]:
        draw_circle(d,cx,cy,14,fill="#E74C3C")
    return img

def make_turkey_cabbage_roll():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("orange"), W, H)
    draw_bowl(d,400,240,220,100)
    # Rice base
    d.ellipse([230,215,570,310],fill="#F8F3E6")
    # Cabbage mix
    for cx,cy in [(320,230),(380,220),(440,225),(360,260),(420,255),(480,240)]:
        d.ellipse([cx-22,cy-16,cx+22,cy+16],fill="#7DCEA0")
    # Turkey mince
    for cx,cy in [(310,250),(360,245),(410,240),(460,248),(390,270)]:
        draw_circle(d,cx,cy,14,fill="#CD853F")
    # Tomato sauce drizzle
    for cx,cy in [(350,235),(410,230),(470,238)]:
        draw_circle(d,cx,cy,8,fill="#C0392B80")
    draw_steam(d,400,200)
    return img

def make_shrimp_stir_fry():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("rose"), W, H)
    draw_bowl(d,400,255,210,95)
    # Brown rice
    d.ellipse([235,215,565,310],fill="#D4A017")
    d.ellipse([245,222,555,303],fill="#E8C547")
    # Veggies
    for cx,cy,c in [(300,240,"#27AE60"),(360,230,"#E74C3C"),(430,235,"#27AE60"),
                    (490,242,"#E74C3C"),(350,265,"#F39C12"),(450,260,"#27AE60")]:
        d.ellipse([cx-16,cy-12,cx+16,cy+12],fill=c)
    # Shrimp (C-shaped pink)
    for cx,cy in [(310,210),(380,205),(460,210),(420,275)]:
        d.arc([cx-18,cy-18,cx+18,cy+18],start=30,end=240,fill="#E8896A",width=8)
    draw_steam(d,400,205)
    return img

def make_sweet_potato_black_bean():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("purple"), W, H)
    draw_bowl(d,400,255,210,95)
    # Sweet potato cubes (orange)
    for cx,cy in [(290,230),(340,215),(390,225),(440,218),(490,228),
                  (310,260),(370,255),(430,260),(480,255)]:
        draw_rect(d,cx-16,cy-16,cx+16,cy+16,fill="#E67E22",radius=4)
    # Black beans
    for cx,cy in [(320,240),(380,235),(440,240),(310,272),(380,268),(450,270)]:
        draw_circle(d,cx,cy,10,fill="#2C3E50")
    # Corn kernels
    for cx,cy in [(350,250),(400,245),(460,252)]:
        draw_circle(d,cx,cy,7,fill="#F4D03F")
    # Yoghurt dollop
    d.ellipse([370,275,430,305],fill="white")
    return img

def make_pasta_primavera():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("cream"), W, H)
    draw_bowl(d,400,255,210,95)
    # Pasta penne
    for cx,cy,a in [(300,230,45),(350,220,135),(400,235,60),(450,225,120),
                    (480,240,30),(320,260,90),(370,255,150),(430,260,45)]:
        x1=cx-20; y1=cy; x2=cx+20; y2=cy
        d.line([(x1,y1),(x2,y2)],fill="#F0E68C",width=8)
    # Tomatoes
    for cx,cy in [(290,245),(460,238),(380,275),(420,270)]:
        draw_circle(d,cx,cy,12,fill="#E74C3C")
    # Mushrooms
    for cx,cy in [(340,240),(430,245)]:
        d.arc([cx-16,cy-12,cx+16,cy+4],start=180,end=360,fill="#8B7355",width=6)
    # Spinach
    for cx,cy in [(310,265),(380,260),(450,263)]:
        draw_leaf(d,cx,cy,20,random.randint(0,360),"#27AE60")
    # Parmesan snowflakes
    for cx,cy in [(320,225),(400,218),(470,230)]:
        d.text((cx,cy),"✦",fill="white")
    draw_steam(d,400,205)
    return img

def make_mediterranean_chicken():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("blue"), W, H)
    draw_plate(d,400,240,200)
    # Chicken thighs
    d.ellipse([280,185,420,285],fill="#8B4513")
    d.ellipse([295,195,405,275],fill="#A0522D")
    d.ellipse([370,190,510,285],fill="#8B4513")
    d.ellipse([385,200,495,275],fill="#A0522D")
    # Tomatoes
    for cx,cy in [(260,300),(310,290),(540,280),(580,295)]:
        draw_circle(d,cx,cy,18,fill="#E74C3C")
    # Olives
    for cx,cy in [(290,260),(260,240),(540,255),(570,240)]:
        draw_circle(d,cx,cy,10,fill="#2C3E50")
        draw_circle(d,cx,cy,4,fill="#7D6608")
    # Olive oil pool
    d.ellipse([310,290,490,340],fill="#F0C04040")
    draw_steam(d,400,180)
    return img

def make_baked_egg_frittata():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("gold"), W, H)
    # Frying pan
    draw_rect(d,180,170,620,360,fill="#555555",radius=90)
    draw_rect(d,190,178,610,352,fill="#F5CBA7",radius=85)  # egg base
    # Spinach
    for cx,cy in [(280,230),(350,215),(430,220),(500,235),(310,270),(390,265),(460,270)]:
        draw_leaf(d,cx,cy,22,random.randint(0,360),"#27AE60")
    # Egg yolks
    for cx,cy in [(330,250),(470,245)]:
        draw_circle(d,cx,cy,26,fill="#F8F3E6")  # white
        draw_circle(d,cx,cy,16,fill="#F39C12")  # yolk
    # Tomatoes
    for cx,cy in [(390,280),(420,265),(350,285)]:
        draw_circle(d,cx,cy,12,fill="#E74C3C")
    # Feta
    for cx,cy in [(310,235),(400,228),(490,240)]:
        draw_rect(d,cx-10,cy-6,cx+10,cy+6,fill="white",radius=2)
    # Pan handle
    d.rectangle([600,255,700,290],fill="#555555")
    draw_steam(d,400,168)
    return img

# Minimal cooking recipes
def make_egg_spinach_bean_skillet():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("green"), W, H)
    draw_bowl(d,400,255,210,95)
    # Beans
    for cx,cy in [(300,245),(340,232),(390,240),(440,235),(480,242),
                  (320,265),(370,260),(430,265),(470,260)]:
        d.ellipse([cx-16,cy-10,cx+16,cy+10],fill="#F5F5DC")
    # Spinach
    for cx,cy in [(290,230),(360,225),(430,228),(490,235)]:
        draw_leaf(d,cx,cy,18,random.randint(0,180),"#1E8449")
    # Eggs
    for cx,cy in [(340,258),(460,255)]:
        draw_circle(d,cx,cy,22,fill="#F8F3E6")
        draw_circle(d,cx,cy,13,fill="#F39C12")
    draw_steam(d,400,210)
    return img

def make_pb_banana_oatmeal():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("cream"), W, H)
    draw_bowl(d,400,255,210,95)
    # Oat base
    d.ellipse([235,220,565,315],fill="#D4A017")
    d.ellipse([245,228,555,308],fill="#E8C97A")
    # Banana slices
    for cx in [300,345,390,435,480]:
        draw_circle(d,cx,260,20,fill="#F7DC6F")
        draw_circle(d,cx,260,14,fill="#F9E79F")
    # Peanut butter swirl
    pts=[(370,238),(400,245),(430,238),(418,255),(430,268),(400,262),(370,268),(382,255)]
    d.polygon(pts,fill="#C4883A")
    # Cinnamon dots
    for cx,cy in [(310,238),(350,232),(450,235),(490,238)]:
        draw_circle(d,cx,cy,4,fill="#8B4513")
    return img

def make_tuna_chickpea_skillet():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("blue"), W, H)
    draw_bowl(d,400,255,210,95)
    # Chickpeas
    for cx,cy in [(290,235),(335,225),(385,232),(435,228),(480,235),
                  (310,258),(360,253),(410,258),(460,252),(490,258)]:
        d.ellipse([cx-14,cy-10,cx+14,cy+10],fill="#D4A017")
        d.ellipse([cx-10,cy-7,cx+10,cy+7],fill="#E8C547")
    # Tuna flakes
    for cx,cy in [(320,245),(380,240),(440,244),(390,268),(440,265)]:
        d.ellipse([cx-18,cy-10,cx+18,cy+10],fill="#85929E")
    # Onion
    for cx,cy in [(295,265),(350,270),(450,268),(490,263)]:
        d.ellipse([cx-8,cy-8,cx+8,cy+8],fill="#E8C9D080")
    # Parsley
    for cx,cy in [(310,228),(400,222),(480,228)]:
        draw_circle(d,cx,cy,6,fill="#27AE60")
    return img

def make_lentil_tomato_bowl():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("orange"), W, H)
    draw_bowl(d,400,255,210,95)
    # Lentil base (brownish)
    d.ellipse([238,218,562,310],fill="#8B4513")
    d.ellipse([248,226,552,302],fill="#A0522D")
    # Tomato chunks
    for cx,cy in [(295,238),(345,228),(400,235),(455,230),(505,238),
                  (315,258),(370,252),(430,256),(478,260)]:
        draw_circle(d,cx,cy,16,fill="#E74C3C")
        draw_circle(d,cx,cy,10,fill="#EC7063")
    # Parsley
    for cx,cy in [(310,225),(400,220),(490,225)]:
        draw_circle(d,cx,cy,7,fill="#27AE60")
    draw_steam(d,400,210)
    return img

def make_cottage_cheese_apple():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("rose"), W, H)
    draw_bowl(d,400,255,210,95)
    # Cottage cheese (white lumpy)
    d.ellipse([240,222,560,308],fill="#FDFEFE")
    for cx,cy in [(300,250),(350,242),(400,248),(450,244),(490,250),
                  (320,265),(380,258),(440,264)]:
        draw_circle(d,cx,cy,10,fill="#F0F3F4")
    # Apple slices (warm)
    for cx,cy in [(295,232),(340,225),(395,230),(450,228),(500,235)]:
        d.ellipse([cx-16,cy-22,cx+16,cy+22],fill="#E8896A")
        d.ellipse([cx-11,cy-16,cx+11,cy+16],fill="#F5A78A")
    # Walnuts
    for cx,cy in [(310,270),(370,268),(440,270),(490,268)]:
        d.ellipse([cx-10,cy-8,cx+10,cy+8],fill="#8B6914")
    # Honey drizzle
    d.arc([320,255,480,290],start=10,end=170,fill="#D4A017",width=4)
    return img

def make_sardine_avocado_toast():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("teal"), W, H)
    draw_plate(d,400,250,210)
    # Toast slices
    draw_rect(d,240,200,400,310,fill="#8B6914",radius=4)
    draw_rect(d,248,208,392,302,fill="#C4A35A",radius=4)
    draw_rect(d,410,200,570,310,fill="#8B6914",radius=4)
    draw_rect(d,418,208,562,302,fill="#C4A35A",radius=4)
    # Avocado mash
    d.ellipse([252,212,388,298],fill="#A9DFBF")
    d.ellipse([260,218,380,292],fill="#27AE60")
    d.ellipse([422,212,558,298],fill="#A9DFBF")
    d.ellipse([430,218,550,292],fill="#27AE60")
    # Sardines
    for i in range(2):
        ox=i*120
        pts=[(265+ox,240),(340+ox,230),(345+ox,255),(270+ox,265)]
        d.polygon(pts,fill="#85929E")
    # Lemon wedge
    d.pieslice([490,270,545,315],start=20,end=160,fill="#F7DC6F")
    return img

def make_chicken_bean_wrap():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("warmred"), W, H)
    draw_plate(d,400,250,210)
    # Wrap (oval tortilla, folded)
    d.ellipse([220,190,580,310],fill="#F5DEB3")
    d.ellipse([235,200,565,300],fill="#FAEBD7")
    # Filling visible
    d.ellipse([260,210,420,295],fill="#2C3E50")  # beans
    for cx,cy in [(280,245),(330,238),(380,245),(350,260)]:
        draw_circle(d,cx,cy,14,fill="#2C3E50")
    # Chicken shreds
    for cx,cy in [(440,225),(460,240),(450,255),(480,235)]:
        d.ellipse([cx-18,cy-8,cx+18,cy+8],fill="#CD853F")
    # Cheese
    for cx in [410,440,470]:
        draw_rect(d,cx-8,230,cx+8,250,fill="#F4D03F",radius=2)
    return img

def make_quinoa_egg_bowl():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("green"), W, H)
    draw_bowl(d,400,255,210,95)
    # Quinoa base
    d.ellipse([240,222,560,308],fill="#F5CBA7")
    for cx,cy in [(290,248),(330,238),(380,245),(430,240),(480,248),
                  (310,262),(360,258),(415,262),(460,258)]:
        draw_circle(d,cx,cy,5,fill="#D4A017")
    # Egg
    draw_circle(d,400,248,34,fill="#F8F3E6")
    draw_circle(d,400,248,20,fill="#F39C12")
    # Pumpkin seeds
    for cx,cy in [(305,232),(345,228),(455,230),(495,235)]:
        d.ellipse([cx-10,cy-5,cx+10,cy+5],fill="#27AE60")
    draw_steam(d,400,210)
    return img

def make_greek_yogurt_berry_oats():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("purple"), W, H)
    draw_bowl(d,400,255,210,95)
    # Yoghurt base
    d.ellipse([240,222,560,308],fill="white")
    # Berries
    for cx,cy,c in [(290,238,"#8E44AD"),(330,230,"#E74C3C"),(380,235,"#8E44AD"),
                    (430,232,"#E74C3C"),(480,238,"#8E44AD"),(310,258,"#E74C3C"),
                    (370,255,"#8E44AD"),(440,258,"#E74C3C"),(490,254,"#8E44AD")]:
        draw_circle(d,cx,cy,14,fill=c)
    # Honey drizzle
    d.arc([310,248,490,278],start=15,end=165,fill="#D4A017",width=4)
    # Chia seeds
    for cx,cy in [(295,268),(340,265),(400,270),(455,266),(495,268)]:
        draw_circle(d,cx,cy,3,fill="#2C3E50")
    return img

def make_smoked_salmon_scrambled():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("salmon"), W, H)
    draw_plate(d,400,250,210)
    # Toast
    draw_rect(d,230,200,580,290,fill="#8B6914",radius=4)
    draw_rect(d,240,208,570,282,fill="#C4A35A",radius=4)
    # Scrambled eggs
    for cx,cy in [(280,240),(330,235),(380,240),(430,237),(480,240),(510,238),(300,258),(360,254),(420,257),(470,255)]:
        d.ellipse([cx-18,cy-12,cx+18,cy+12],fill="#F7DC6F")
    # Salmon
    for cx,cy in [(285,228),(335,222),(390,226),(445,224),(495,228)]:
        d.ellipse([cx-20,cy-10,cx+20,cy+10],fill="#E8896A")
    # Capers
    for cx,cy in [(300,248),(380,244),(460,248)]:
        draw_circle(d,cx,cy,5,fill="#27AE60")
    draw_steam(d,400,200)
    return img

def make_edamame_tofu_rice():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("teal"), W, H)
    draw_bowl(d,400,255,210,95)
    # Brown rice
    d.ellipse([240,220,560,308],fill="#D4A017")
    for cx,cy in [(290,248),(340,242),(390,246),(440,243),(490,248),
                  (315,262),(365,258),(420,262),(470,258)]:
        d.ellipse([cx-8,cy-4,cx+8,cy+4],fill="#E8C547")
    # Tofu cubes
    for cx,cy in [(295,228),(350,222),(415,228),(470,225),(510,232)]:
        draw_rect(d,cx-14,cy-14,cx+14,cy+14,fill="white",radius=2)
    # Edamame
    for cx,cy in [(310,258),(360,254),(430,258),(480,254)]:
        d.ellipse([cx-14,cy-8,cx+14,cy+8],fill="#27AE60")
        draw_circle(d,cx,cy,6,fill="#58D68D")
    # Sesame seeds
    for cx,cy in [(300,240),(350,235),(430,238),(490,242)]:
        draw_circle(d,cx,cy,3,fill="#F5DEB3")
    draw_steam(d,400,210)
    return img

def make_lentil_egg_shakshuka():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("warmred"), W, H)
    draw_bowl(d,400,255,210,95)
    # Tomato-lentil sauce
    d.ellipse([238,218,562,308],fill="#C0392B")
    d.ellipse([248,226,552,300],fill="#E74C3C")
    # Lentils in sauce
    for cx,cy in [(290,248),(335,240),(385,245),(435,242),(480,248),
                  (310,262),(365,258),(420,263),(470,258)]:
        d.ellipse([cx-12,cy-8,cx+12,cy+8],fill="#8B4513")
    # Eggs poached
    for cx,cy in [(330,248),(470,245)]:
        draw_circle(d,cx,cy,26,fill="#F8F3E6")
        draw_circle(d,cx,cy,16,fill="#F39C12")
    # Coriander
    for cx,cy in [(295,232),(390,228),(490,232)]:
        draw_circle(d,cx,cy,6,fill="#27AE60")
    draw_steam(d,400,210)
    return img

# Tofu recipes
def make_garlic_soy_tofu():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("gold"), W, H)
    draw_bowl(d,400,255,210,95)
    # Rice
    d.ellipse([240,218,560,308],fill="#F5DEB3")
    # Tofu cubes (golden)
    for cx,cy in [(290,235),(345,228),(400,232),(455,228),(505,235),
                  (310,258),(365,254),(420,258),(475,254)]:
        draw_rect(d,cx-16,cy-16,cx+16,cy+16,fill="#F0C040",radius=3)
        draw_rect(d,cx-12,cy-12,cx+12,cy+12,fill="#F7DC6F",radius=3)
    # Spring onion
    for cx in [300,370,440,510]:
        d.line([(cx,240),(cx+5,200)],fill="#27AE60",width=3)
    # Soy sauce drizzle
    d.arc([310,255,490,285],start=10,end=170,fill="#2C3E5080",width=5)
    draw_steam(d,400,208)
    return img

def make_savory_tofu_scramble():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("gold"), W, H)
    draw_plate(d,400,250,210)
    # Toast
    draw_rect(d,240,200,570,290,fill="#8B6914",radius=4)
    draw_rect(d,250,208,560,282,fill="#C4A35A",radius=4)
    # Scrambled tofu
    for cx,cy in [(270,238),(315,232),(360,238),(405,234),(450,238),(490,234),
                  (280,256),(330,252),(380,256),(430,253),(480,256)]:
        d.ellipse([cx-18,cy-12,cx+18,cy+12],fill="#F4D03F")
    # Turmeric dots
    for cx,cy in [(290,242),(380,238),(460,242)]:
        draw_circle(d,cx,cy,6,fill="#E67E22")
    draw_steam(d,400,200)
    return img

def make_tomato_braised_tofu():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("warmred"), W, H)
    draw_bowl(d,400,255,210,95)
    # Tomato sauce
    d.ellipse([240,220,560,308],fill="#C0392B")
    d.ellipse([250,228,550,300],fill="#E74C3C")
    # Tofu pieces
    for cx,cy in [(290,238),(345,232),(400,236),(455,233),(505,238),
                  (310,260),(365,256),(420,260),(475,256)]:
        draw_rect(d,cx-14,cy-14,cx+14,cy+14,fill="#F8F9FA",radius=3)
    # Basil leaves
    for cx,cy in [(295,225),(390,222),(490,226)]:
        draw_leaf(d,cx,cy,14,random.randint(0,180),"#1E8449")
    draw_steam(d,400,212)
    return img

def make_onion_gravy_tofu():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("cream"), W, H)
    draw_plate(d,400,250,210)
    # Mash base
    d.ellipse([240,220,560,308],fill="#F5DEB3")
    d.ellipse([250,228,550,300],fill="#FDEBD0")
    # Gravy pool
    d.ellipse([260,232,540,295],fill="#8B6914A0")
    # Tofu slices
    for cx,cy in [(300,248),(360,244),(420,248),(480,244)]:
        d.ellipse([cx-22,cy-14,cx+22,cy+14],fill="#F8F9FA")
        d.ellipse([cx-18,cy-10,cx+18,cy+10],fill="#ECF0F1")
    # Onion rings
    for cx,cy in [(310,260),(380,257),(450,260)]:
        d.arc([cx-14,cy-14,cx+14,cy+14],start=0,end=300,fill="#D4A017",width=3)
    draw_steam(d,400,210)
    return img

def make_soft_tofu_soup():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("teal"), W, H)
    draw_bowl(d,400,255,210,95)
    # Broth
    d.ellipse([240,222,560,308],fill="#117A6560")
    d.ellipse([250,230,550,300],fill="#1ABC9C30")
    # Silken tofu cubes
    for cx,cy in [(290,238),(345,232),(400,236),(455,233),(505,240),
                  (310,260),(365,256),(420,260),(475,256)]:
        draw_rect(d,cx-13,cy-13,cx+13,cy+13,fill="#F8F9FA",radius=2)
    # Carrot slices
    for cx,cy in [(295,250),(350,246),(415,250),(470,247)]:
        draw_circle(d,cx,cy,10,fill="#E67E22")
    # Spinach
    for cx,cy in [(320,228),(390,224),(460,228)]:
        draw_leaf(d,cx,cy,12,random.randint(0,180),"#27AE60")
    # Spring onion
    for cx in [305,380,455]:
        d.line([(cx,228),(cx+3,212)],fill="#27AE60",width=2)
    draw_steam(d,400,212)
    return img

def make_pan_seared_tofu():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("green"), W, H)
    draw_plate(d,400,250,210)
    # Salad greens
    for cx,cy in [(280,260),(330,250),(380,258),(440,252),(500,260),
                  (300,278),(360,272),(420,278),(480,272)]:
        draw_leaf(d,cx,cy,18,random.randint(0,360),"#27AE60")
    # Tofu cubes (golden seared)
    for cx,cy in [(300,220),(360,215),(420,220),(480,215),(340,250),(440,248)]:
        draw_rect(d,cx-18,cy-18,cx+18,cy+18,fill="#F0C040",radius=3)
        draw_rect(d,cx-14,cy-14,cx+14,cy+14,fill="#E8C547",radius=3)
        # Sear marks
        d.line([(cx-10,cy-8),(cx+10,cy+8)],fill="#8B6914",width=2)
    return img

def make_tofu_mash_gravy():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("cream"), W, H)
    draw_bowl(d,400,255,210,95)
    # Mashed potato
    d.ellipse([240,222,560,308],fill="#F5DEB3")
    d.ellipse([250,230,550,300],fill="#FDEBD0")
    # Gravy
    d.ellipse([265,235,535,298],fill="#8B691480")
    # Tofu
    for cx,cy in [(295,242),(350,238),(410,242),(465,238),(500,242)]:
        draw_rect(d,cx-14,cy-14,cx+14,cy+14,fill="#F8F9FA",radius=2)
    draw_steam(d,400,212)
    return img

def make_ginger_soy_tofu():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("orange"), W, H)
    draw_bowl(d,400,255,210,95)
    # Rice
    d.ellipse([240,220,560,308],fill="#F5DEB3")
    # Tofu slices (glazed)
    for cx,cy in [(290,235),(345,230),(400,234),(455,231),(505,237)]:
        d.ellipse([cx-22,cy-14,cx+22,cy+14],fill="#E67E22")
        d.ellipse([cx-18,cy-10,cx+18,cy+10],fill="#F0A500")
    # Ginger slivers
    for cx,cy in [(305,258),(365,254),(425,258),(475,254)]:
        d.line([(cx-8,cy-4),(cx+8,cy+4)],fill="#F7DC6F",width=3)
    # Spring onion
    for cx in [310,390,470]:
        d.line([(cx,250),(cx+3,230)],fill="#27AE60",width=2)
    draw_steam(d,400,210)
    return img

def make_cabbage_tofu_stir():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("teal"), W, H)
    draw_bowl(d,400,255,210,95)
    # Cabbage
    for cx,cy in [(285,238),(335,228),(390,233),(445,230),(495,238),
                  (305,260),(360,255),(415,260),(470,255)]:
        d.ellipse([cx-20,cy-14,cx+20,cy+14],fill="#7DCEA0")
    # Tofu cubes
    for cx,cy in [(300,245),(365,240),(430,244),(490,242)]:
        draw_rect(d,cx-13,cy-13,cx+13,cy+13,fill="#F8F9FA",radius=2)
    # Soy sauce
    d.arc([310,258,490,285],start=15,end=165,fill="#2C3E5080",width=4)
    draw_steam(d,400,210)
    return img

def make_no_energy_tofu():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("blue"), W, H)
    draw_bowl(d,400,255,210,95)
    # Silken tofu block
    draw_rect(d,280,210,520,305,fill="#F8F9FA",radius=8)
    draw_rect(d,290,218,510,297,fill="#ECF0F1",radius=6)
    # Soy sauce drizzle
    d.arc([295,240,505,275],start=10,end=170,fill="#2C3E50",width=4)
    # Sesame seeds
    for cx,cy in [(310,258),(360,255),(410,260),(460,257),(500,260)]:
        draw_circle(d,cx,cy,3,fill="#F5DEB3")
    # Spring onion rings
    for cx,cy in [(320,246),(380,243),(440,246),(490,244)]:
        draw_circle(d,cx,cy,5,fill="#27AE60",outline=None)
    # Chilli flakes
    for cx,cy in [(340,268),(400,266),(450,268)]:
        draw_circle(d,cx,cy,3,fill="#E74C3C")
    return img

# No-cook plates
def make_protein_plate():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("warmred"), W, H)
    draw_plate(d,400,240,200)
    # Crackers
    for i in range(5):
        draw_rect(d,230+i*60,290,285+i*60,330,fill="#C4A35A",radius=3)
    # Eggs
    draw_circle(d,290,215,35,fill="#F8F3E6")
    draw_circle(d,290,215,22,fill="#F39C12")
    draw_circle(d,350,210,35,fill="#F8F3E6")
    draw_circle(d,350,210,22,fill="#F39C12")
    # Avocado fan
    for i in range(4):
        a=160+i*12
        d.pieslice([430,190,510,260],start=a,end=a+10,fill="#27AE60")
    # Tomatoes
    for cx,cy in [(490,215),(510,240),(475,250)]:
        draw_circle(d,cx,cy,16,fill="#E74C3C")
    # Lemon
    d.pieslice([540,270,590,310],start=20,end=160,fill="#F7DC6F")
    return img

def make_sweet_savory_plate():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("purple"), W, H)
    draw_plate(d,400,240,200)
    # Yoghurt
    draw_circle(d,330,230,80,fill="white")
    # Honey swirl
    d.arc([280,195,380,275],start=30,end=330,fill="#D4A017",width=5)
    # Apple slices
    for i in range(5):
        a=i*30-30
        cx=510+int(40*math.cos(math.radians(a)))
        cy=230+int(20*math.sin(math.radians(a)))
        d.ellipse([cx-18,cy-28,cx+18,cy+28],fill="#F4D03F")
    # Walnuts
    for cx,cy in [(460,260),(490,275),(520,262)]:
        d.ellipse([cx-12,cy-10,cx+12,cy+10],fill="#8B6914")
    return img

def make_no_cook_chicken():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("green"), W, H)
    draw_plate(d,400,240,200)
    # Salad greens
    for cx,cy in [(290,250),(340,238),(400,244),(460,240),(510,252),
                  (300,270),(360,265),(430,268),(490,265)]:
        draw_leaf(d,cx,cy,20,random.randint(0,360),"#27AE60")
    # Chicken shreds
    for cx,cy in [(310,215),(360,210),(410,215),(460,212),(400,235)]:
        d.ellipse([cx-20,cy-9,cx+20,cy+9],fill="#CD853F")
    # Cherry tomatoes
    for cx,cy in [(285,230),(530,228),(500,250)]:
        draw_circle(d,cx,cy,16,fill="#E74C3C")
    # Dressing drizzle
    d.arc([310,255,490,285],start=10,end=170,fill="#D4A01780",width=4)
    return img

def make_tuna_fuss_plate():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("blue"), W, H)
    draw_plate(d,400,240,200)
    # Tuna mix
    d.ellipse([280,195,430,285],fill="#85929E")
    d.ellipse([292,203,418,277],fill="#95A5A6")
    # Cucumber
    for cx in [460,490,520]:
        draw_circle(d,cx,230,22,fill="#27AE60")
        draw_circle(d,cx,230,16,fill="#A9DFBF")
    # Crackers
    for i in range(4):
        draw_rect(d,280+i*62,295,335+i*62,330,fill="#C4A35A",radius=3)
    # Lemon
    d.pieslice([510,270,560,315],start=20,end=160,fill="#F7DC6F")
    return img

def make_cheese_fiber_plate():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("gold"), W, H)
    draw_plate(d,400,240,200)
    # Cheese slices
    for i in range(3):
        draw_rect(d,250+i*30,200,310+i*30,260,fill="#F4D03F",radius=3)
    # Pear slices
    for i in range(5):
        a=i*22-44
        cx=450+int(50*math.cos(math.radians(a)))
        cy=230+int(60*math.sin(math.radians(a)))
        d.ellipse([cx-15,cy-24,cx+15,cy+24],fill="#D5F5E3")
    # Almonds
    for cx,cy in [(290,285),(330,278),(370,285),(400,280),(430,285)]:
        d.ellipse([cx-14,cy-8,cx+14,cy+8],fill="#D4A017")
    # Crackers
    for i in range(4):
        draw_rect(d,445+i*50,275,490+i*50,305,fill="#C4A35A",radius=3)
    return img

def make_pb_comfort_plate():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("cream"), W, H)
    draw_plate(d,400,240,200)
    # Rice cakes
    for i in range(2):
        draw_rect(d,230+i*170,205,380+i*170,290,fill="#F5DEB3",radius=4)
        draw_rect(d,240+i*170,213,370+i*170,282,fill="#FAEBD7",radius=4)
    # Peanut butter swirl on each
    for cx in [305,475]:
        pts=[(cx-30,248),(cx,238),(cx+30,248),(cx+22,262),(cx+30,272),(cx,266),(cx-30,272),(cx-22,262)]
        d.polygon(pts,fill="#C4883A")
    # Banana slices
    for cx in [310,345,380,415,450]:
        draw_circle(d,cx,308,18,fill="#F7DC6F")
        draw_circle(d,cx,308,12,fill="#F9E79F")
    return img

def make_cottage_comeback_plate():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("rose"), W, H)
    draw_bowl(d,400,250,200,90)
    # Cottage cheese
    d.ellipse([245,218,555,305],fill="#FDFEFE")
    for cx,cy in [(295,245),(340,238),(390,244),(440,240),(490,246),
                  (315,260),(365,255),(415,260),(465,256)]:
        draw_circle(d,cx,cy,9,fill="#F0F3F4")
    # Pineapple chunks
    for cx,cy in [(300,228),(350,222),(405,226),(455,223),(500,228)]:
        draw_rect(d,cx-12,cy-12,cx+12,cy+12,fill="#F7DC6F",radius=3)
    # Sunflower seeds
    for cx,cy in [(310,265),(365,262),(425,265),(475,263)]:
        draw_circle(d,cx,cy,4,fill="#D4A017")
    # Honey drizzle
    d.arc([320,255,480,280],start=15,end=165,fill="#D4A017",width=3)
    return img

def make_smoked_salmon_plate():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("salmon"), W, H)
    draw_plate(d,400,240,200)
    # Cream cheese dollop
    draw_circle(d,310,235,40,fill="white")
    # Salmon ribbons
    for i in range(4):
        y=210+i*15
        d.arc([350,y,530,y+28],start=180,end=360,fill="#E8896A",width=6)
    # Cucumber rounds
    for cx,cy in [(275,280),(310,290),(345,283),(380,290)]:
        draw_circle(d,cx,cy,18,fill="#27AE60")
        draw_circle(d,cx,cy,12,fill="#A9DFBF")
    # Crackers
    for i in range(4):
        draw_rect(d,450+i*38,275,482+i*38,308,fill="#C4A35A",radius=3)
    # Dill
    for cx,cy in [(295,220),(325,210),(360,218)]:
        d.line([(cx,cy),(cx+5,cy-12)],fill="#27AE60",width=2)
        draw_circle(d,cx+5,cy-14,3,fill="#27AE60")
    return img

def make_bean_crunch_plate():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("orange"), W, H)
    draw_plate(d,400,240,200)
    # Chickpeas
    for cx,cy in [(280,220),(315,210),(355,218),(395,212),(430,220),(465,214),
                  (290,240),(330,235),(375,240),(415,237),(455,240)]:
        d.ellipse([cx-14,cy-10,cx+14,cy+10],fill="#D4A017")
        d.ellipse([cx-10,cy-7,cx+10,cy+7],fill="#E8C547")
    # Carrot sticks
    for i in range(5):
        x1=260+i*12; y1=260; x2=x1+8; y2=330
        d.rectangle([x1,y1,x2,y2],fill="#E67E22")
    # Crackers
    for i in range(4):
        draw_rect(d,370+i*52,265,416+i*52,300,fill="#C4A35A",radius=3)
    return img

def make_turkey_rollup_plate():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("green"), W, H)
    draw_plate(d,400,240,200)
    # Roll-ups
    for i in range(4):
        cx=280+i*60; cy=225
        d.ellipse([cx-25,cy-18,cx+25,cy+18],fill="#F5DEB3")
        d.ellipse([cx-20,cy-12,cx+20,cy+12],fill="#85929E")  # turkey
        d.ellipse([cx-14,cy-8,cx+14,cy+8],fill="#F4D03F")  # cheese
    # Pickles
    for cx,cy in [(285,280),(330,272),(380,278),(430,273),(475,280)]:
        draw_circle(d,cx,cy,16,fill="#27AE60")
        draw_circle(d,cx,cy,10,fill="#58D68D")
    # Crackers
    for i in range(4):
        draw_rect(d,445+i*48,265,487+i*48,298,fill="#C4A35A",radius=3)
    return img

def make_avocado_egg_plate():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("teal"), W, H)
    draw_plate(d,400,240,210)
    # Toast
    draw_rect(d,230,195,490,295,fill="#8B6914",radius=4)
    draw_rect(d,240,203,480,287,fill="#C4A35A",radius=4)
    # Avocado mash
    d.ellipse([248,208,472,282],fill="#27AE60")
    d.ellipse([258,215,462,275],fill="#58D68D")
    # Egg half
    draw_circle(d,530,235,42,fill="#F8F3E6")
    draw_circle(d,530,235,26,fill="#F39C12")
    # Chilli flakes
    for cx,cy in [(295,250),(345,245),(400,248),(445,245)]:
        draw_circle(d,cx,cy,3,fill="#E74C3C")
    return img

def make_grazing_board():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("warmred"), W, H)
    # Wooden board
    draw_rect(d,150,140,650,360,fill="#8B6914",radius=10)
    draw_rect(d,160,148,640,352,fill="#C4A35A",radius=8)
    # Cheese cubes
    for cx,cy in [(210,185),(250,185),(290,185),(210,215),(250,215)]:
        draw_rect(d,cx-14,cy-14,cx+14,cy+14,fill="#F4D03F",radius=2)
    # Egg halves
    draw_circle(d,350,190,30,fill="#F8F3E6")
    draw_circle(d,350,190,18,fill="#F39C12")
    draw_circle(d,410,190,30,fill="#F8F3E6")
    draw_circle(d,410,190,18,fill="#F39C12")
    # Deli meat slices
    for i in range(3):
        d.ellipse([460+i*24,175,515+i*24,210],fill="#CD853F")
    # Apple
    draw_circle(d,560,185,32,fill="#E74C3C")
    d.line([(560,153),(560,170)],fill="#8B4513",width=3)
    # Nuts
    for cx,cy in [(220,270),(255,265),(290,270),(325,265),(360,270)]:
        d.ellipse([cx-12,cy-8,cx+12,cy+8],fill="#8B6914")
    # Crackers
    for i in range(5):
        draw_rect(d,390+i*46,255,430+i*46,285,fill="#C4A35A",radius=3)
    # Grapes
    for cx,cy in [(555,255),(580,245),(570,265),(600,255),(585,270)]:
        draw_circle(d,cx,cy,14,fill="#8E44AD")
    return img

# Quick meals
def make_lazy_sandwich():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("gold"), W, H)
    draw_plate(d,400,240,210)
    # Bottom bread
    draw_rect(d,240,240,560,305,fill="#8B6914",radius=6)
    draw_rect(d,248,246,552,298,fill="#C4A35A",radius=5)
    # Fillings
    d.ellipse([248,222,552,252],fill="#85929E")  # turkey
    d.ellipse([252,210,548,228],fill="#F4D03F")  # cheese
    for cx in [280,330,380,430,480,520]:  # lettuce
        draw_leaf(d,cx,205,16,random.randint(70,110),"#27AE60")
    for cx,cy in [(290,195),(360,190),(430,195),(500,192)]:  # tomato
        draw_circle(d,cx,cy,12,fill="#E74C3C")
    # Top bread
    draw_rect(d,244,168,556,200,fill="#8B6914",radius=6)
    draw_rect(d,252,174,548,194,fill="#C4A35A",radius=5)
    return img

def make_quick_tuna_sandwich():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("blue"), W, H)
    draw_plate(d,400,240,210)
    # Bottom bread
    draw_rect(d,240,245,560,305,fill="#8B6914",radius=5)
    draw_rect(d,248,251,552,298,fill="#C4A35A",radius=4)
    # Spinach
    for cx in [268,310,360,410,460,510,542]:
        draw_leaf(d,cx,228,16,random.randint(60,120),"#27AE60")
    # Tuna mixture
    d.ellipse([255,200,545,236],fill="#85929E")
    d.ellipse([265,206,535,228],fill="#95A5A6")
    # Top bread
    draw_rect(d,244,168,556,202,fill="#8B6914",radius=5)
    draw_rect(d,252,174,548,196,fill="#C4A35A",radius=4)
    return img

def make_mashed_bean_toast():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("teal"), W, H)
    draw_plate(d,400,250,210)
    # Two toasts
    draw_rect(d,230,195,395,310,fill="#8B6914",radius=5)
    draw_rect(d,240,202,385,302,fill="#C4A35A",radius=4)
    draw_rect(d,405,195,570,310,fill="#8B6914",radius=5)
    draw_rect(d,415,202,560,302,fill="#C4A35A",radius=4)
    # Bean mash
    d.ellipse([244,204,381,298],fill="#F5DEB3")
    d.ellipse([419,204,556,298],fill="#F5DEB3")
    for cx,cy in [(280,240),(320,232),(355,240),(440,238),(480,244),(515,238)]:
        d.ellipse([cx-12,cy-8,cx+12,cy+8],fill="#D4A017")
    # Olive oil pool
    d.arc([256,240,370,268],start=15,end=165,fill="#D4A01780",width=3)
    d.arc([432,238,544,265],start=15,end=165,fill="#D4A01780",width=3)
    # Chilli flakes
    for cx,cy in [(270,260),(340,256),(445,256),(510,262)]:
        draw_circle(d,cx,cy,3,fill="#E74C3C")
    return img

def make_yogurt_fruit_bowl():
    img = Image.new("RGBA",(W,H))
    d = ImageDraw.Draw(img)
    draw_bg(d, pal("purple"), W, H)
    draw_bowl(d,400,255,210,95)
    # Yoghurt
    d.ellipse([242,220,558,308],fill="white")
    # Banana slices
    for cx in [290,335,380,425,470,515]:
        draw_circle(d,cx,260,20,fill="#F7DC6F")
        draw_circle(d,cx,260,14,fill="#F9E79F")
    # Oats
    for cx,cy in [(295,240),(345,234),(400,238),(455,235),(505,240)]:
        d.ellipse([cx-10,cy-5,cx+10,cy+5],fill="#D4A017")
    # Honey drizzle
    d.arc([310,255,490,282],start=10,end=170,fill="#D4A017",width=4)
    # Cinnamon
    for cx,cy in [(310,268),(370,265),(430,268),(490,265)]:
        draw_circle(d,cx,cy,3,fill="#8B4513")
    return img

# ── master dispatcher ────────────────────────────────────────────────────────
GENERATORS = {
    "chicken-veggie-tray-bake": make_chicken_veggie_tray_bake,
    "salmon-honey-garlic-broccoli": make_salmon_honey_garlic,
    "sheetpan-sausage-cabbage-apples": make_sausage_cabbage_apple,
    "lemon-herb-tilapia-green-beans": make_tilapia_green_beans,
    "ground-turkey-cabbage-roll": make_turkey_cabbage_roll,
    "shrimp-veggie-stir-fry": make_shrimp_stir_fry,
    "sweet-potato-black-bean-bowl": make_sweet_potato_black_bean,
    "pasta-primavera": make_pasta_primavera,
    "mediterranean-chicken-olives": make_mediterranean_chicken,
    "baked-egg-frittata": make_baked_egg_frittata,
    "egg-spinach-white-bean-skillet": make_egg_spinach_bean_skillet,
    "peanut-butter-banana-oatmeal": make_pb_banana_oatmeal,
    "tuna-chickpea-warm-skillet": make_tuna_chickpea_skillet,
    "warm-lentil-tomato-bowl": make_lentil_tomato_bowl,
    "cottage-cheese-apple-skillet": make_cottage_cheese_apple,
    "sardine-avocado-toast": make_sardine_avocado_toast,
    "chicken-bean-warm-wrap": make_chicken_bean_wrap,
    "quinoa-egg-breakfast-bowl": make_quinoa_egg_bowl,
    "warm-greek-yogurt-berry-oats": make_greek_yogurt_berry_oats,
    "smoked-salmon-scrambled-eggs": make_smoked_salmon_scrambled,
    "edamame-tofu-brown-rice": make_edamame_tofu_rice,
    "lentil-egg-shakshuka": make_lentil_egg_shakshuka,
    "garlic-soy-tofu-bowl": make_garlic_soy_tofu,
    "savory-tofu-scramble": make_savory_tofu_scramble,
    "tomato-braised-tofu": make_tomato_braised_tofu,
    "light-onion-gravy-tofu": make_onion_gravy_tofu,
    "soft-tofu-vegetable-soup": make_soft_tofu_soup,
    "pan-seared-tofu-herbs": make_pan_seared_tofu,
    "tofu-mashed-potato-gravy": make_tofu_mash_gravy,
    "ginger-soy-tofu": make_ginger_soy_tofu,
    "cabbage-tofu-stir": make_cabbage_tofu_stir,
    "no-energy-savory-tofu-bowl": make_no_energy_tofu,
    "protein-power-no-effort-plate": make_protein_plate,
    "sweet-savory-balance-plate": make_sweet_savory_plate,
    "no-cook-chicken-plate": make_no_cook_chicken,
    "tuna-without-fuss-plate": make_tuna_fuss_plate,
    "cheese-fiber-combo-plate": make_cheese_fiber_plate,
    "peanut-butter-comfort-plate": make_pb_comfort_plate,
    "cottage-cheese-comeback-plate": make_cottage_comeback_plate,
    "smoked-salmon-light-plate": make_smoked_salmon_plate,
    "bean-crunch-plate": make_bean_crunch_plate,
    "turkey-roll-ups-plate": make_turkey_rollup_plate,
    "avocado-egg-upgrade-plate": make_avocado_egg_plate,
    "snack-plate-feels-like-meal": make_grazing_board,
    "lazy-sandwich-system": make_lazy_sandwich,
    "quick-tuna-sandwich": make_quick_tuna_sandwich,
    "mashed-bean-toast": make_mashed_bean_toast,
    "yogurt-fruit-bowl": make_yogurt_fruit_bowl,
}

if __name__ == "__main__":
    import sys
    from recipes_data import RECIPES
    sys.path.insert(0, "/sessions/relaxed-funny-mayer")
    total = len(RECIPES)
    for i, recipe in enumerate(RECIPES):
        rid = recipe["id"]
        gen = GENERATORS.get(rid)
        if gen:
            img = gen()
            add_label(img, recipe["title"], list(PAL.values())[i % len(PAL)])
            path = save_img(img, rid)
            print(f"[{i+1}/{total}] {rid}")
        else:
            print(f"  MISSING generator for {rid}")
    print("Done.")
