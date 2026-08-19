# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

p = r'C:\ai\code\yhl-html\boss_arena.py'
src = io.open(p, encoding='utf-8').read()

# 编辑4的 old 与 new 里都以 return rectHit(x, y, 4); 结尾的 bulletWallHit 为准
old1 = 'rep("""        return false;\n    }\n'
new1 = 'rep("""        return rectHit(x, y, 4);\n    }\n'
c1 = src.count(old1)
print('c1', c1)
assert c1 == 1
src = src.replace(old1, new1)

old2 = '    """        return false;\n    }\n'
new2 = '    """        return rectHit(x, y, 4);\n    }\n'
c2 = src.count(old2)
print('c2', c2)
assert c2 == 1
src = src.replace(old2, new2)

io.open(p, 'w', encoding='utf-8').write(src)
print('patched')
