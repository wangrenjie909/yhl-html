# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout.reconfigure(encoding='utf-8')

p = r'C:\ai\code\yhl-html\no_overlap.py'
src = io.open(p, encoding='utf-8').read()

# 找到 enemy-sep 的 old 锚点：字面含 \U0001F479 BOSS（...地面...
m = re.search(r'\\U0001F479 BOSS\\uff08', src)
print('found at', m.start() if m else None)
# 替换 BOSS 后加 ！  ：字面 \\uff08 前插入 \\uff01
old_lit = '\\U0001F479 BOSS\\uff08\\u5730\\u9762\\u5de8\\u53d8\\u6012'
new_lit = '\\U0001F479 BOSS\\uff01\\uff08\\u5730\\u9762\\u5de8\\u53d8\\u6012'
print('count', src.count(old_lit))
assert src.count(old_lit) == 1
src = src.replace(old_lit, new_lit)
io.open(p, 'w', encoding='utf-8').write(src)
print('patched')
