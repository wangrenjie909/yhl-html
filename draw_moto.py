from PIL import Image, ImageDraw, ImageFilter
import math

S = 2                     # 超采样
FW, FH = 350, 760         # 最终尺寸（车头朝上）
W, H = FW * S, FH * S
im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
CX = FW // 2 * S
def Y(v): return v * S

RED   = (228, 48, 40, 255)
RED_D = (140, 24, 18, 255)
TANKC = (205, 42, 34, 255)
STEEL = (125, 127, 133, 255)
DARK  = (28, 28, 32, 255)
TIRE  = (16, 16, 18, 255)

def ellipse(cx, cy, rx, ry, fill, outline=None, wd=0):
    b = [cx - rx, cy - ry, cx + rx, cy + ry]
    if outline:
        d.ellipse(b, fill=fill, outline=outline, width=wd)
    else:
        d.ellipse(b, fill=fill)

def hgrad(x0, y0, x1, y1, rad, base):
    mask = Image.new('L', (x1 - x0, y1 - y0), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, x1 - x0 - 1, y1 - y0 - 1], radius=rad, fill=255)
    g = Image.new('RGBA', (x1 - x0, y1 - y0))
    gd = ImageDraw.Draw(g)
    for xx in range(x1 - x0):
        t = xx / (x1 - x0 - 1)
        m = 1 - 0.5 * abs(t * 2 - 1)          # 中间亮两侧暗 = 圆柱金属感
        col = tuple(int(m * c) for c in base[:3]) + (255,)
        gd.line([xx, 0, xx, y1 - y0], fill=col)
    g.putalpha(mask)
    im.alpha_composite(g, (x0, y0))

# ---------- 1) 投影 ----------
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ds = ImageDraw.Draw(sh)
ds.ellipse([CX - 100*S, Y(100), CX + 100*S, Y(660)], fill=(0, 0, 0, 150))
sh = sh.filter(ImageFilter.GaussianBlur(16 * S))
im.alpha_composite(sh)

# ---------- 2) 前后轮 ----------
def wheel(cy):
    ellipse(CX, cy, 55*S, 55*S, TIRE)
    ellipse(CX, cy, 36*S, 36*S, (198, 198, 204, 255))
    for a in range(0, 360, 60):
        rad = math.radians(a)
        x1 = CX + math.cos(rad) * 16*S; y1 = cy + math.sin(rad) * 16*S
        x2 = CX + math.cos(rad) * 34*S; y2 = cy + math.sin(rad) * 34*S
        d.line([x1, y1, x2, y2], fill=(88, 88, 94, 255), width=int(5*S))
    ellipse(CX, cy, 10*S, 10*S, (75, 75, 80, 255))
    ellipse(CX, cy, 4*S, 4*S, (225, 225, 225, 255))
wheel(Y(120))   # 前轮（上方 = 车头）
wheel(Y(640))   # 后轮

# ---------- 3) 车架主梁 + 发动机 + 排气 ----------
d.rounded_rectangle([CX - 13*S, Y(150), CX + 13*S, Y(630)], radius=13*S, fill=(45, 45, 50, 255))
d.rounded_rectangle([CX - 46*S, Y(500), CX + 46*S, Y(610)], radius=16*S, fill=(58, 60, 66, 255))
d.rectangle([CX - 36*S, Y(520), CX + 36*S, Y(534)], fill=(165, 167, 173, 255))   # 缸盖
d.rounded_rectangle([CX + 52*S, Y(430), CX + 67*S, Y(620)], radius=8*S, fill=STEEL)      # 排气管
d.rounded_rectangle([CX + 52*S, Y(540), CX + 67*S, Y(585)], radius=6*S, fill=(205, 118, 55, 255))  # 高温段

# ---------- 4) 后座/尾翼（先画，被骑手部分遮挡） ----------
d.polygon([(CX - 58*S, Y(500)), (CX + 58*S, Y(500)), (CX + 40*S, Y(635)), (CX - 40*S, Y(635))], fill=RED)
d.polygon([(CX - 40*S, Y(600)), (CX + 40*S, Y(600)), (CX + 24*S, Y(648)), (CX - 24*S, Y(648))], fill=RED_D)

# ---------- 5) 油箱（金属红渐变） ----------
hgrad(CX - 72*S, Y(330), CX + 72*S, Y(470), 30*S, TANKC)

# ---------- 6) 车把 + 手 ----------
d.rounded_rectangle([CX - 92*S, Y(222), CX + 92*S, Y(240)], radius=9*S, fill=STEEL)
ellipse(CX - 88*S, Y(231), 14*S, 12*S, (20, 20, 24, 255))
ellipse(CX + 88*S, Y(231), 14*S, 12*S, (20, 20, 24, 255))

# ---------- 7) 骑手躯干 + 手臂 ----------
d.polygon([(CX - 96*S, Y(385)), (CX + 96*S, Y(385)), (CX + 55*S, Y(520)), (CX - 55*S, Y(520))], fill=DARK)
d.line([CX, Y(395), CX, Y(505)], fill=(92, 92, 98, 255), width=int(3*S))          # 拉链
for sx in (-1, 1):
    d.line([CX + sx*74*S, Y(395), CX + sx*60*S, Y(235)], fill=(26, 26, 30, 255), width=int(30*S))
    ellipse(CX + sx*86*S, Y(231), 15*S, 13*S, (22, 22, 26, 255))                  # 手套

# ---------- 8) 头盔 ----------
ellipse(CX, Y(285), 52*S, 52*S, (226, 226, 231, 255))
ellipse(CX, Y(285), 52*S, 52*S, None, outline=(138, 138, 144, 255), wd=int(3*S))
d.pieslice([CX - 47*S, Y(286), CX + 47*S, Y(380)], 180, 360, fill=(38, 42, 58, 255))   # 面罩（朝上=前方）
d.pieslice([CX - 42*S, Y(292), CX + 26*S, Y(368)], 180, 360, fill=(96, 106, 138, 150))  # 面罩反光
hh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
hd = ImageDraw.Draw(hh)
hd.ellipse([CX - 22*S, Y(316), CX + 8*S, Y(340)], fill=(255, 255, 255, 120))            # 头顶高光
im.alpha_composite(hh)

# ---------- 9) 油箱高光 ----------
hh2 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
hd2 = ImageDraw.Draw(hh2)
hd2.line([CX - 26*S, Y(348), CX - 26*S, Y(452)], fill=(255, 255, 255, 70), width=int(8*S))
im.alpha_composite(hh2)

# ---------- 缩小保存 ----------
out = im.resize((FW, FH), Image.LANCZOS)
out.save('moto_final.png')
print('saved moto_final.png', out.size)
