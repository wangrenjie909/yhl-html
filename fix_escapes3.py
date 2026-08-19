# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout.reconfigure(encoding='utf-8')

p = r'C:\ai\code\yhl-html\warehouse.py'
src = io.open(p, encoding='utf-8').read()

# 找所有 \U 开头的转义（字面反斜杠 U + 十六进制）
pat = re.compile(r'\\U[0-9A-Fa-f]+')
for m in pat.finditer(src):
    tok = m.group(0)
    hexpart = tok[2:]
    if len(hexpart) != 8:
        print('BAD:', tok, '->', hexpart, 'len', len(hexpart))
        # 修复：转为 \uXXXX（若 <= 0xFFFF）
        cp = int(hexpart, 16)
        newtok = '\\u%04x' % cp if cp <= 0xFFFF else '\\U%08X' % cp
        src = src.replace(tok, newtok)

io.open(p, 'w', encoding='utf-8').write(src)
print('done')
