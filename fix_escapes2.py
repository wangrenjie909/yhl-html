# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

p = r'C:\ai\code\yhl-html\warehouse.py'
src = io.open(p, encoding='utf-8').read()

fixes = {
    '\\U0004ED3': '\\u4ed3',   # 仓
    '\\U0005E93': '\\u5e93',   # 库
    '\\U0005B58': '\\u5b58',   # 存
    '\\U0005C31': '\\u5c31',   # 就（备用）
}
for old, new in fixes.items():
    c = src.count(old)
    if c:
        src = src.replace(old, new)
        print('replaced', old, 'x', c)
io.open(p, 'w', encoding='utf-8').write(src)
print('done')
