"""
生成头部横幅粒子网络静态图 PNG
白底 + 黑色粒子/连线 + 居中文字
三个独立网络簇，长条形分布
"""
import random
import math
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 900, 180
OUTPUT_HEADER = "assets/header-particle.png"
OUTPUT_SIDE = "assets/particle-network.png"

BG_COLOR = (255, 255, 255, 255)
PARTICLE_COLOR = (0, 0, 0, 60)       # 粒子半透明
LINE_ALPHA_MAX = 0.25                 # 连线最深透明度

# 三个簇: (粒子数, 中心x, 中心y, 散布x, 散布y, 连线距离)
# 散布x远大于y，形成长条形
CLUSTERS = [
    (10, 250, 90, 250, 60, 150),   # 左侧大簇
    (7,  550, 90, 200, 60, 160),   # 中间簇
    (3,  750, 90, 120, 50, 170),   # 右侧小簇
]

TITLE = "Hi, I'm Yaochen"
SUBTITLE = "数据分析师 · 数据科学家 · 数据挖掘工程师"


def draw_cluster(draw, points, connect_dist):
    """画一个簇的粒子和连线（半透明）"""
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < connect_dist:
                a = int(255 * LINE_ALPHA_MAX * (1 - dist / connect_dist))
                draw.line(
                    [points[i][:2], points[j][:2]],
                    fill=(0, 0, 0, a),
                    width=1,
                )
    for x, y, r in points:
        draw.ellipse([x - r, y - r, x + r, y + r], fill=PARTICLE_COLOR)


def generate_header():
    random.seed(55)

    clusters = []
    for num, cx, cy, sx, sy, cd in CLUSTERS:
        points = []
        for _ in range(num):
            x = max(0, min(WIDTH, cx + random.uniform(-sx, sx)))
            y = max(0, min(HEIGHT, cy + random.uniform(-sy, sy)))
            r = random.uniform(1.5, 3.5)
            points.append((x, y, r))
        clusters.append((points, cd))

    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 42)
    except (OSError, IOError):
        title_font = ImageFont.load_default()
    try:
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Songti.ttc", 16)
    except (OSError, IOError):
        subtitle_font = ImageFont.load_default()

    # 先在透明层画粒子网络
    network_layer = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, 0))
    net_draw = ImageDraw.Draw(network_layer)
    for points, cd in clusters:
        draw_cluster(net_draw, points, cd)

    # 白底 + 网络合成
    img = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, 255))
    img = Image.alpha_composite(img, network_layer)

    # 文字画在最上层
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), TITLE, font=title_font)
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, HEIGHT // 2 - 35), TITLE, fill=(0, 0, 0, 255), font=title_font)

    bbox2 = draw.textbbox((0, 0), SUBTITLE, font=subtitle_font)
    sw = bbox2[2] - bbox2[0]
    draw.text(((WIDTH - sw) // 2, HEIGHT // 2 + 15), SUBTITLE, fill=(80, 80, 80, 255), font=subtitle_font)

    img.convert("RGB").save(OUTPUT_HEADER)
    print(f"头部横幅已生成: {OUTPUT_HEADER}")


def generate_side():
    random.seed(55)
    sw, sh = 400, 400
    clusters_side = [
        ([(random.uniform(20, 280), random.uniform(60, 120), random.uniform(1.5, 3)) for _ in range(7)], 120),
        ([(random.uniform(150, 380), random.uniform(220, 300), random.uniform(1.5, 3)) for _ in range(15)], 100),
        ([(random.uniform(50, 200), random.uniform(300, 370), random.uniform(1.5, 3)) for _ in range(5)], 130),
    ]

    img = Image.new("RGB", (sw, sh), BG_COLOR)
    draw = ImageDraw.Draw(img)
    for points, cd in clusters_side:
        draw_cluster(draw, points, cd)

    img.save(OUTPUT_SIDE)
    print(f"侧边图已生成: {OUTPUT_SIDE}")


if __name__ == "__main__":
    generate_header()
    generate_side()
