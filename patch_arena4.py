# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

p = r'C:\ai\code\yhl-html\boss_arena.py'
src = io.open(p, encoding='utf-8').read()

# 编辑6 old：去掉后面的 hasLOS 注释（arenaHit 已插入中间）
old = 'rep("""        return rectHit(x, y, 4);\n    }\n\n    // \\U0001F441 \\u89c6\\u7ebf\\u68c0\\u6d4b\\uff1a\\u4e24\\u70b9\\u4e4b\\u95f4\\u6709\\u6ca1\\u6709\\u88ab\\u5899\\u6321\\u4f4f\n""",'
new = 'rep("""        return rectHit(x, y, 4);\n    }\n""",'
print('c', src.count(old))
assert src.count(old) == 1
src = src.replace(old, new)

# 编辑6 new 尾部也去掉多余的 hasLOS 注释
old2 = "    \"\"\"        if (arenaHit(x, y, 4)) return true;\n        return rectHit(x, y, 4);\n    }\n\n    // \\U0001F441 \\u89c6\\u7ebf\\u68c0\\u6d4b\\uff1a\\u4e24\\u70b9\\u4e4b\\u95f4\\u6709\\u6ca1\\u6709\\u88ab\\u5899\\u6321\\u4f4f\n\"\"\","
new2 = "    \"\"\"        if (arenaHit(x, y, 4)) return true;\n        return rectHit(x, y, 4);\n    }\n\"\"\","
print('c2', src.count(old2))
assert src.count(old2) == 1
src = src.replace(old2, new2)

io.open(p, 'w', encoding='utf-8').write(src)
print('patched edit6')
