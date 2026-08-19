# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

p = r'C:\ai\code\yhl-html\boss_arena2.py'
src = io.open(p, encoding='utf-8').read()

old = 'rep("""            if (bd < 32) {\n                boss.hp -= b.dmg;\n"""'
new = 'rep("""            if (bd < 32) {\n                    boss.hp -= b.dmg;\n"""'
print('c', src.count(old))
assert src.count(old) == 1
io.open(p, 'w', encoding='utf-8').write(src.replace(old, new))
print('patched')
