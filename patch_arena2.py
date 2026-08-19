# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

p = r'C:\ai\code\yhl-html\boss_arena.py'
src = io.open(p, encoding='utf-8').read()

# 编辑4 old：注释行 + hasLOS 函数行
old = '"""    // \U0001F441 \u89c6\u7ebf\u68c0\u6d4b\uff1a\u4e24\u70b9\u4e4b\u95f4\u6709\u6ca1\u6709\u88ab\u5899\u6321\u4f4f\n    function hasLOS(x1, y1, x2, y2) {\n"""'
new = '"""    // \U0001F441 \u89c6\u7ebf\u68c0\u6d4b\uff1a\u4e24\u70b9\u4e4b\u95f4\u6709\u6ca1\u6709\u88ab\u5899\u6321\u4f4f\n    function hasLOS(x1, y1, x2, y2) {\n"""'

# 编辑4 new：末尾要带 hasLOS 注释 + 函数行
old_new = '"""    // \U0001F479 BOSS \u573a\u5730\u5708\u5899\uff1a\u5708\u73af\u5e26\u78b0\u649e\uff08\u95e8\u53e3\u4e0d\u78b0\uff09\n    function arenaHit(x, y, rad) {\n        if (!arena) return false;\n        var dx = x - arena.x, dy = y - arena.y;\n        var d = Math.sqrt(dx * dx + dy * dy);\n        if (d < arena.r - 16 - rad || d > arena.r + 16 + rad) return false;\n        var ang = Math.atan2(dy, dx);\n        if (Math.abs(ang - arena.gateAng) < arena.gateHalf) return false;   // \u95e8\u53e3\u901a\u884c\n        return true;\n    }\n\n    // \U0001F441 \u89c6\u7ebf\u68c0\u6d4b\uff1a\u4e24\u70b9\u4e4b\u95f4\u6709\u6ca1\u6709\u88ab\u5899\u6321\u4f4f\n"""'
new_new = '"""    // \U0001F479 BOSS \u573a\u5730\u5708\u5899\uff1a\u5708\u73af\u5e26\u78b0\u649e\uff08\u95e8\u53e3\u4e0d\u78b0\uff09\n    function arenaHit(x, y, rad) {\n        if (!arena) return false;\n        var dx = x - arena.x, dy = y - arena.y;\n        var d = Math.sqrt(dx * dx + dy * dy);\n        if (d < arena.r - 16 - rad || d > arena.r + 16 + rad) return false;\n        var ang = Math.atan2(dy, dx);\n        if (Math.abs(ang - arena.gateAng) < arena.gateHalf) return false;   // \u95e8\u53e3\u901a\u884c\n        return true;\n    }\n\n    // \U0001F441 \u89c6\u7ebf\u68c0\u6d4b\uff1a\u4e24\u70b9\u4e4b\u95f4\u6709\u6ca1\u6709\u88ab\u5899\u6321\u4f4f\n    function hasLOS(x1, y1, x2, y2) {\n"""'

print('old count:', src.count(old))
print('old_new count:', src.count(old_new))
assert src.count(old) == 1
assert src.count(old_new) == 1
src = src.replace(old_new, new_new)
io.open(p, 'w', encoding='utf-8').write(src)
print('patched new ending OK')
