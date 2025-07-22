from PIL import Image, ImageDraw
import os
import random

def make_grass(path, size=48):
    # Nền cỏ xanh olive nhạt
    img = Image.new('RGBA', (size, size), (170, 200, 120, 255))
    draw = ImageDraw.Draw(img)
    # Vẽ các sọc cỏ đậm nhạt
    for i in range(0, size, 8):
        draw.rectangle([0, i, size, i+4], fill=(140, 180, 80, 255))
    # Vẽ các ngọn cỏ nhỏ ngẫu nhiên (xanh lá tươi)
    for _ in range(8):
        x = random.randint(4, size-4)
        y = random.randint(8, size-8)
        draw.line([(x, y), (x, y-6)], fill=(50, 205, 50, 255), width=2)
        draw.line([(x, y-3), (x-2, y-5)], fill=(50, 205, 50, 255), width=1)
        draw.line([(x, y-3), (x+2, y-5)], fill=(50, 205, 50, 255), width=1)
    # Viền mỏng xung quanh để phân biệt state
    draw.rectangle([0, 0, size-1, size-1], outline=(20, 60, 20, 180), width=2)
    img.save(path)

def make_rock(path, size=48):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Đá to, gồ ghề, gần sát viền ô
    points = [
        (6, size-8), (2, size//2), (10, 10), (size//2, 2), (size-10, 10), (size-2, size//2), (size-8, size-8), (size//2, size-4)
    ]
    draw.polygon(points, fill=(130, 130, 130, 255), outline=(60, 60, 60, 255))
    # Vẽ các mảng sáng tối
    draw.polygon([(10, 10), (size//2, 2), (size-10, 10), (size//2+6, size//2-6)], fill=(180, 180, 180, 255))
    draw.polygon([(size-8, size-8), (size-2, size//2), (size-10, 10), (size//2+6, size//2-6)], fill=(100, 100, 100, 255))
    # Vết nứt
    draw.line([(size//2-8, size//2+8), (size//2+8, size//2+12), (size//2+10, size//2-4)], fill=(80, 80, 80, 255), width=2)
    img.save(path)

def make_tree(path, size=48):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Thân cây vẽ trước
    trunk_w = 10
    trunk_h = 22
    trunk_x = size//2 - trunk_w//2
    trunk_y = size-8-trunk_h
    draw.rectangle([trunk_x, trunk_y, trunk_x+trunk_w, trunk_y+trunk_h], fill=(139, 69, 19, 255), outline=(100, 50, 10, 255))
    # Tán lá kiểu mây, nhiều ellipse nhỏ, dồn lên trên, không tràn viền, vẽ sau để che thân
    cloud_centers = [
        (size//2, 13), (size//2-12, 18), (size//2+12, 18),
        (size//2-16, 28), (size//2+16, 28), (size//2, 25)
    ]
    cloud_sizes = [ (30,18), (20,14), (20,14), (14,10), (14,10), (22,14) ]
    for (cx, cy), (w, h) in zip(cloud_centers, cloud_sizes):
        draw.ellipse([cx-w//2, cy-h//2, cx+w//2, cy+h//2], fill=(34, 139, 34, 255), outline=(0, 100, 0, 200), width=2)
    # Gốc thân cây bo tròn
    draw.ellipse([trunk_x-2, trunk_y+trunk_h-4, trunk_x+trunk_w+2, trunk_y+trunk_h+6], fill=(120, 60, 20, 255))
    # Thêm một vài lá rơi nhỏ
    for _ in range(2):
        lx = random.randint(trunk_x-8, trunk_x+trunk_w+8)
        ly = random.randint(trunk_y+trunk_h-2, size-4)
        draw.ellipse([lx-2, ly-1, lx+2, ly+3], fill=(50, 205, 50, 200))
    img.save(path)

def make_goal(path, size=48):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    from math import sin, cos, pi
    cx, cy, r = size//2, size//2, size//2-4
    # Hiệu ứng phát sáng
    draw.ellipse([cx-r-4, cy-r-4, cx+r+4, cy+r+4], fill=(255, 255, 100, 80))
    # Vẽ ngôi sao vàng lớn
    points = []
    for i in range(10):
        angle = pi/2 + i*pi/5
        radius = r if i%2==0 else r//2
        x = cx + radius * cos(angle)
        y = cy - radius * sin(angle)
        points.append((x, y))
    draw.polygon(points, fill=(255, 215, 0, 255), outline=(255, 180, 0, 255))
    # Viền vàng đậm ngoài cùng
    draw.polygon(points, outline=(255, 200, 0, 255), width=3)
    img.save(path)

def make_chili(path, size=48, walk=False):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Thân ớt
    draw.ellipse([size//2-8, size//2-10, size//2+8, size-8], fill=(220, 20, 60, 255), outline=(180,0,0,255))
    # Đầu ớt
    draw.ellipse([size//2-8, size//2-16, size//2+8, size//2], fill=(255, 36, 71, 255), outline=(180,0,0,255))
    # Cuống xanh
    draw.rectangle([size//2-2, size//2-20, size//2+2, size//2-12], fill=(0, 128, 0, 255))
    # Mắt đẹp: mắt to, có lòng trắng, con ngươi đen, chấm sáng
    # Mắt trái
    eye_left = [size//2-6, size//2-8, size//2-2, size//2-4]
    draw.ellipse(eye_left, fill=(255,255,255,255))
    draw.ellipse([size//2-5, size//2-7, size//2-3, size//2-5], fill=(0,0,0,255))
    draw.ellipse([size//2-4, size//2-7, size//2-3, size//2-6], fill=(255,255,255,180))
    # Mắt phải
    eye_right = [size//2+2, size//2-8, size//2+6, size//2-4]
    draw.ellipse(eye_right, fill=(255,255,255,255))
    draw.ellipse([size//2+3, size//2-7, size//2+5, size//2-5], fill=(0,0,0,255))
    draw.ellipse([size//2+4, size//2-7, size//2+5, size//2-6], fill=(255,255,255,180))
    # Miệng đơn giản: chỉ một đường cong, đặt cao lên gần mắt
    mouth_box = [size//2-5, size//2-1, size//2+5, size//2+5]
    draw.arc(mouth_box, 20, 160, fill=(0,0,0,255), width=2)
    # Chân và tay như cũ
    if walk:
        draw.line([size//2-4, size-8, size//2-8, size-2], fill=(0,0,0,255), width=2)
        draw.line([size//2+4, size-8, size//2+8, size-2], fill=(0,0,0,255), width=2)
    else:
        draw.line([size//2-4, size-8, size//2-4, size-2], fill=(0,0,0,255), width=2)
        draw.line([size//2+4, size-8, size//2+4, size-2], fill=(0,0,0,255), width=2)
    # Hai tay đơn giản
    draw.line([size//2-8, size//2, size//2-14, size//2+8], fill=(0,0,0,255), width=2)
    draw.line([size//2+8, size//2, size//2+14, size//2+8], fill=(0,0,0,255), width=2)
    img.save(path)

def make_water(path, size=48):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Giọt nước xanh dương
    draw.ellipse([size//2-8, size//2-8, size//2+8, size//2+8], fill=(30, 144, 255, 255), outline=(0, 0, 139, 255), width=2)
    draw.polygon([(size//2, size//2-12), (size//2-6, size//2-2), (size//2+6, size//2-2)], fill=(30, 144, 255, 255))
    img.save(path)

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    make_grass(os.path.join(base, 'tiles/grass.png'))
    make_tree(os.path.join(base, 'tiles/tree.png'))
    make_goal(os.path.join(base, 'tiles/goal.png'))
    make_chili(os.path.join(base, 'sprites/chili_idle.png'), walk=False)
    make_chili(os.path.join(base, 'sprites/chili_walk.png'), walk=True)
    make_water(os.path.join(base, 'tiles/water.png'))
    make_rock(os.path.join(base, 'tiles/rock.png'))
    print('Đã tạo xong các file hình ảnh!')

if __name__ == '__main__':
    main() 