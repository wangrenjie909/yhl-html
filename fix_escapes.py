# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout.reconfigure(encoding='utf-8')

p = r'C:\ai\code\yhl-html\warehouse.py'
src = io.open(p, encoding='utf-8').read()

# 找出所有 7 位（错误）的 \U000XXXX 转义
bad = sorted(set(re.findall(r'\\U000[0-9A-Fa-f]{3}(?![0-9A-Fa-f])', src)))
print('bad escapes found:', bad)
for b in bad:
    cp = int(b[2:], 16)
    src = src.replace(b, '\\u%04x' % cp)

io.open(p, 'w', encoding='utf-8').write(src)
print('fixed')
