# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

p = r'C:\ai\code\yhl-html\no_overlap.py'
src = io.open(p, encoding='utf-8').read()

old_lit = '\\U0001F479 BOSS\\uff08\\u5730\\u9762\\u5de8\\u53d8\\u6012'
new_lit = '\\U0001F479 BOSS\\uff01\\uff08\\u5730\\u9762\\u5de8\\u53d8\\u6012'
cnt = src.count(old_lit)
print('count', cnt)
src = src.replace(old_lit, new_lit)
io.open(p, 'w', encoding='utf-8').write(src)
print('patched all')
