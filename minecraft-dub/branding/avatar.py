"""Аватарка канала: оригинальный пиксельный маскот-кубик в наушниках с микрофоном."""
import random
from PIL import Image, ImageDraw

N, SCALE = 32, 32  # 32x32 «пикселя» -> 1024x1024
random.seed(7)
img = Image.new("RGB", (N, N))
px = img.load()


def put(x, y, c):
    if 0 <= x < N and 0 <= y < N:
        px[x, y] = c


def rect(x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            put(x, y, c)


# фон: фиолетово-бирюзовый градиент полосами + искорки
top, bot = (58, 28, 113), (16, 150, 140)
for y in range(N):
    k = (y // 2 * 2) / (N - 1)
    col = tuple(int(top[i] + (bot[i] - top[i]) * k) for i in range(3))
    for x in range(N):
        px[x, y] = col
for _ in range(14):
    put(random.randrange(N), random.randrange(N), (255, 255, 255))

OUT = (20, 14, 30)
# кубик-голова: верхняя грань светлее, лицевая — «серно-жёлтая» с текстурой
rect(8, 9, 23, 26, OUT)
rect(9, 10, 22, 12, (255, 226, 92))
rect(9, 13, 22, 25, (245, 190, 20))
for _ in range(28):
    x, y = random.randint(9, 22), random.randint(13, 25)
    put(x, y, random.choice([(222, 160, 10), (255, 210, 60)]))
# глаза
for ex in (11, 18):
    rect(ex, 15, ex + 2, 17, (255, 255, 255))
    rect(ex + 1, 16, ex + 2, 17, OUT)
# брови-«азарт»
rect(11, 14, 12, 14, OUT); rect(19, 14, 20, 14, OUT)
# открытый рот с языком
rect(13, 20, 18, 23, (110, 20, 30))
rect(14, 22, 17, 23, (240, 90, 100))
rect(13, 20, 18, 20, (255, 255, 255))
# наушники: дуга и красные чашки
for x in range(9, 23):
    put(x, 6, OUT)
rect(7, 7, 8, 8, OUT); rect(23, 7, 24, 8, OUT)
rect(9, 5, 22, 5, (60, 60, 70))
rect(5, 13, 8, 21, OUT); rect(6, 14, 7, 20, (230, 57, 70))
rect(23, 13, 26, 21, OUT); rect(24, 14, 25, 20, (230, 57, 70))
rect(6, 14, 6, 16, (255, 120, 130)); rect(24, 14, 24, 16, (255, 120, 130))
for y in range(9, 13):
    put(6, y, OUT); put(25, y, OUT)
# микрофон на штанге от правой чашки
for i, (x, y) in enumerate([(25, 22), (24, 23), (23, 24), (22, 25), (21, 26)]):
    put(x, y, (60, 60, 70))
rect(18, 26, 20, 28, OUT)
rect(19, 27, 19, 27, (120, 120, 130))
# звуковые волны
for x, y in [(28, 15), (29, 14), (29, 16), (30, 13), (30, 17), (3, 15), (2, 14), (2, 16), (1, 13), (1, 17)]:
    put(x, y, (255, 255, 255))

big = img.resize((N * SCALE, N * SCALE), Image.NEAREST)
big.save("avatar.png")
# превью в круге, как на YouTube
mask = Image.new("L", big.size, 0)
ImageDraw.Draw(mask).ellipse((0, 0, *big.size), fill=255)
prev = Image.new("RGBA", big.size, (24, 24, 24, 255))
prev.paste(big, (0, 0), mask)
prev.resize((300, 300), Image.LANCZOS).save("avatar_preview.png")
print("ok")
