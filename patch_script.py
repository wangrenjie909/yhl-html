# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

p = r'C:\ai\code\yhl-html\knife_ranged.py'
src = io.open(p, encoding='utf-8').read()

old = "src = io.open(path, encoding='utf-8').read()"
new = ("src = io.open(path, encoding='utf-8').read()\n"
       "src = src.replace('\u67aa\u68f0', '\u67aa\u68b0')   # \u4fee\u6b63\u9519\u522b\u5b57\uff1a\u67aa\u68f0 -> \u67aa\u68b0")
assert src.count(old) == 1, src.count(old)
io.open(p, 'w', encoding='utf-8').write(src.replace(old, new))
print('patched script OK')
