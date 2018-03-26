# coding=utf-8
from django.shortcuts import render, HttpResponse
from io import BytesIO

from .models import *
from django.urls import reverse

import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

_letter_cases = "abcdefghjkmnpqrstuvwxy"  # 小写字母，去除可能干扰的i，l，o，z
_upper_cases = _letter_cases.upper()  # 大写字母
_numbers = ''.join(map(str, range(3, 10)))  # 数字
init_chars = ''.join((_letter_cases, _upper_cases, _numbers))




def create_validate_code(size=(120, 30),
                         chars=init_chars,
                         img_type="GIF",
                         mode="RGB",
                         bg_color=(238, 99, 99),
                         fg_color=(0, 0, 255),
                         font_size=18,
                         font_type="C:\\Windows\\Fonts\\11673_u.ttf",
                         length=4,
                         draw_lines=True,
                         n_line=(1, 2),
                         draw_points=True,
                         point_chance=2):
    """
    @todo: 生成验证码图片
    @param size: 图片的大小，格式（宽，高），默认为(120, 30)
    @param chars: 允许的字符集合，格式字符串
    @param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
    @param mode: 图片模式，默认为RGB
    @param bg_color: 背景颜色，默认为白色
    @param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
    @param font_size: 验证码字体大小
    @param font_type: 验证码字体，默认为 ae_AlArabiya.ttf
    @param length: 验证码字符个数
    @param draw_lines: 是否划干扰线
    @param n_lines: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
    @param draw_points: 是否画干扰点
    @param point_chance: 干扰点出现的概率，大小范围[0, 100]
    @return: [0]: PIL Image实例
    @return: [1]: 验证码图片中的字符串
    """
    width, height = size  # 宽高
    # 创建图形
    img = Image.new(mode, size, bg_color)
    draw = ImageDraw.Draw(img)  # 创建画笔

    def get_chars():
        """生成给定长度的字符串，返回列表格式"""
        return random.sample(chars, length)

    def create_lines():
        """绘制干扰线"""
        line_num = random.randint(*n_line)  # 干扰线条数
        for i in range(line_num):
            # 起始点
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            # 结束点
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill=(0, 0, 0))

    def create_points():
        """绘制干扰点"""
        chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs():
        """绘制验证码字符"""
        c_chars = get_chars()
        strs = ' %s ' % ' '.join(c_chars)  # 每个字符前后以空格隔开
        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs)

        draw.text(((width - font_width) / 3, (height - font_height) / 3),
                  strs, font=font, fill=fg_color)

        return ''.join(c_chars)

    if draw_lines:
        create_lines()
    if draw_points:
        create_points()
    strs = create_strs()
    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）
    return img, strs













def index(request):
    # hero = HeroInfo.objects.get(pk=1)
    # context = {'hero':hero}
    # return render(request, 'booktest/index.html', context)
    list = HeroInfo.objects.all()
    context = {'list': list}
    return render(request, "booktest/index.html", context)

def show(request, id):
    context = {'id': id}
    return  render(request, 'booktest/show.html', context)

def htmlTest(request):
    context = {"t1": "<h1>11321</h1>"}
    return render(request, 'booktest/htmlTest.html', context)

def csrf1(request):
    return render(request, 'booktest/csrf1.html')

def csrf2(request):
    uname = request.POST['uname']
    return HttpResponse(uname)

def verifyCode(request):
    from PIL import Image, ImageDraw, ImageFont
    import random
    from io import BytesIO
    #创建背景色
    bgColor = (random.randrange(0, 100),random.randrange(0, 100), random.randrange(0, 100))
    # 规定宽高
    width = 100
    height = 25
    image = Image.new('RGB', (width, height), bgColor)
    # image.show() 这里是创建一张图片 如果使用show的话就表示要展示出来
    # 创建画笔
    draw= ImageDraw.Draw(image)
    # 绘制内容
    text = 'hfhd56y1c89dj879iu5dc8erth895jv86c4565csa5648n31c984tfjh15'
    font = ImageFont.truetype(r"C:\Windows\Fonts\ariali.ttf", 24)
    # 逐个绘制
    temp = ''
    for t1 in range(4):
        temp1 = text[random.randrange(0, len(text))]
        temp += temp1
        draw.text(
            (t1*20, 2),
            temp1,
            (random.randrange(0, 255),random.randrange(0, 100),random.randrange(0, 100)),
            font)
    # session 保存到下来
    request.session['sess'] = temp
    f = BytesIO()
    image.save(f, 'png')
    data = f.getvalue()
    return HttpResponse(data, 'image/png')

def verifyTest1(request):
    return render(request, 'booktest/verifyTest.html')
def verifyTest2(request):
    verify = request.POST['code1']
    session1 = request.session['sess']
    if verify==session1:
        context={"login": 'scuessful'}
        return render(request, 'booktest/verifyTest2.html',context)
    else:
        context={"login": 'failed'}
        return render(request, 'booktest/verifyTest2.html', context)

def yz_home(requset):
    print(requset.method)

    if requset.method == 'GET':
        print("--------------------")
        return render(requset, 'booktest/yz_home.html')
    else:
        return HttpResponse('ok')
def yanzheng(requset):
    f=BytesIO()
    img, code= create_validate_code()
    requset.session['check_code']=code
    img.save(f, 'PNG')
    return HttpResponse(f.getvalue(),'image/png')
