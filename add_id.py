# -*- coding: utf-8 -*-
import io

path = r'C:\ai\code\yhl-html\index.html'
src = io.open(path, encoding='utf-8').read()

old = 'class="btn-primary">\U0001F680 \u4e86\u89e3\u66f4\u591a</a>'
new = 'class="btn-primary" id="hero-btn">\U0001F680 \u4e86\u89e3\u66f4\u591a</a>'

assert src.count(old) == 1, 'match count = %d' % src.count(old)
io.open(path, 'w', encoding='utf-8').write(src.replace(old, new))
print('OK hero-btn id added')
