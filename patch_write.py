# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\ai\code\yhl-html\enemy_bigger.py'
src = io.open(path, encoding='utf-8').read()
old = "assert len(src) != n0\nio.open(path, 'w', encoding='utf-8').write(src)"
new = "if len(src) != n0:\n    print('content changed')\nio.open(path, 'w', encoding='utf-8').write(src)"
assert src.count(old) == 1
io.open(path, 'w', encoding='utf-8').write(src.replace(old, new))
print('patched write')
