# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

p = r'C:\ai\code\yhl-html\add_map_view.py'
src = io.open(p, encoding='utf-8').read()

old = r"        <li>\U0001F916 \u6709<b>\u8fdc\u7a0b\u654c\u4eba</b>\u4f1a\u8fb9\u8d70\u8fb9\u5f00\u706b\uff0c\u6ce8\u610f\u8eb2\u907f\u5b50\u5f39\uff01</li>"
new = r"        <li>\U0001F47E \u8fd1\u6218\u654c\u4eba\u51b2\u8138 \u00b7 \U0001F916 <b>\u8fdc\u7a0b\u654c\u4eba</b>\u4f1a\u671d\u4f60\u5c04\u51fb\uff0c\u6ce8\u610f\u8eb2\u5b50\u5f39\uff01</li>"
cnt = src.count(old)
print('count:', cnt)
src = src.replace(old, new)
io.open(p, 'w', encoding='utf-8').write(src)
print('patched add_map_view.py OK')
