# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\ai\code\yhl-html\index.html'
src = io.open(path, encoding='utf-8').read()
n0 = len(src)

def rep(old, new, name, count=1):
    global src
    assert src.count(old) == count, '%s match = %d' % (name, src.count(old))
    src = src.replace(old, new)
    print('OK', name)

# 1) 缩略图 CSS：图片填满
rep("""        .work-thumb {
            height: 150px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 60px;
            border-radius: 10px;
        }
""",
    """        .work-thumb {
            height: 150px;
            border-radius: 10px;
            overflow: hidden;
        }
        .work-thumb img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }
""",
    'thumb-css')

# 2) 三张卡片换真实截图
rep('                <div class="work-thumb thumb-rooftop">\U0001F3D9\ufe0f</div>\n',
    '                <div class="work-thumb"><img src="shot_home.png" alt="\u8dd1\u9177\u8005\u7684\u5929\u53f0"></div>\n',
    'thumb-home')
rep('                <div class="work-thumb thumb-moto">\U0001F3CD\ufe0f</div>\n',
    '                <div class="work-thumb"><img src="shot_moto.png" alt="\u6469\u6258\u98de\u9a70"></div>\n',
    'thumb-moto')
rep('                <div class="work-thumb thumb-sdc">\U0001F525</div>\n',
    '                <div class="work-thumb"><img src="shot_sdc.png" alt="\u641c\u6253\u64a4"></div>\n',
    'thumb-sdc')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
