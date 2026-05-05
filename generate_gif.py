"""
生成几何粒子网络动画 GIF
白底 + 浅色粒子连线，类似 particles.js 效果
"""
import random
import math
import imageio
from PIL import Image, ImageDraw

# 参数
WIDTH, HEIGHT = 400, 400
NUM_PARTICLES = 40
CONNECT_DIST = 100  # 连线距离阈值
FRAMES = 60
DURATION = 0.05  # 每帧时长(秒)
OUTPUT = "assets/particle-network.gif"

# 颜色
BG_COLOR = (255, 255, 255)
PARTICLE_COLOR = (100, 149, 237)  # 矢车菊蓝
LINE_COLOR_BASE = (150, 180, 220)  # 浅蓝连线


class Particle:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.vx = random.uniform(-0.8, 0.8)
        self.vy = random.uniform(-0.8, 0.8)
        self.r = random.uniform(2, 4)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        # 边界反弹
        if self.x < 0 or self.x > WIDTH:
            self.vx *= -1
        if self.y < 0 or self.y > HEIGHT:
            self.vy *= -1
        self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))


def draw_frame(particles):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 画连线
    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            dx = particles[i].x - particles[j].x
            dy = particles[i].y - particles[j].y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < CONNECT_DIST:
                # 距离越近线越深
                alpha = 1 - dist / CONNECT_DIST
                r = int(LINE_COLOR_BASE[0] + (BG_COLOR[0] - LINE_COLOR_BASE[0]) * (1 - alpha))
                g = int(LINE_COLOR_BASE[1] + (BG_COLOR[1] - LINE_COLOR_BASE[1]) * (1 - alpha))
                b = int(LINE_COLOR_BASE[2] + (BG_COLOR[2] - LINE_COLOR_BASE[2]) * (1 - alpha))
                draw.line(
                    [(particles[i].x, particles[i].y), (particles[j].x, particles[j].y)],
                    fill=(r, g, b),
                    width=1,
                )

    # 画粒子
    for p in particles:
        draw.ellipse(
            [p.x - p.r, p.y - p.r, p.x + p.r, p.y + p.r],
            fill=PARTICLE_COLOR,
        )

    return img


def main():
    random.seed(42)
    particles = [Particle() for _ in range(NUM_PARTICLES)]
    frames = []

    for _ in range(FRAMES):
        frame = draw_frame(particles)
        frames.append(frame)
        for p in particles:
            p.update()

    # 保存 GIF
    imageio.mimsave(OUTPUT, frames, duration=DURATION, loop=0)
    print(f"GIF 已生成: {OUTPUT}")


if __name__ == "__main__":
    main()
