from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # 创建一个512x512的图标
    size = (512, 512)
    icon = Image.new('RGB', size, color='#2196F3')
    draw = ImageDraw.Draw(icon)
    
    # 绘制一个简单的聊天气泡形状
    draw.ellipse([100, 100, 412, 412], fill='white')
    draw.polygon([256, 412, 200, 450, 256, 412], fill='white')
    
    icon.save('data/icon.png')

def create_presplash():
    # 创建一个720x1280的启动画面
    size = (720, 1280)
    splash = Image.new('RGB', size, color='#2196F3')
    draw = ImageDraw.Draw(splash)
    
    # 添加应用名称
    draw.text((360, 640), "Mobile Chat", fill='white', anchor='mm', font=None)
    
    splash.save('data/presplash.png')

if __name__ == '__main__':
    if not os.path.exists('data'):
        os.makedirs('data')
    create_icon()
    create_presplash()
