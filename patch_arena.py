# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

p = r'C:\ai\code\yhl-html\boss_arena.py'
src = io.open(p, encoding='utf-8').read()

# 把编辑4的旧锚点改为 hasLOS 注释行
old = '"""        return false;\n    }\n\n    // \U0001F441 \u89c6\u7ebf\u68c0\u6d4b\uff1a\u4e24\u70b9\u4e4b\u95f4\u6709\u6ca1\u6709\u88ab\u5899\u6321\u4f4f\n"""'
new = '"""    // \U0001F441 \u89c6\u7ebf\u68c0\u6d4b\uff1a\u4e24\u70b9\u4e4b\u95f4\u6709\u6ca1\u6709\u88ab\u5899\u6321\u4f4f\n    function hasLOS(x1, y1, x2, y2) {\n"""'
assert src.count(old) == 1, src.count(old)
src = src.replace(old, new)

# 编辑4的新内容也要带出 hasLOS 开头，这里把 new 里的 hasLOS 注释放前面
old2 = '"""    // \U0001F479 BOSS \u573a\u5730\u5708\u5899\uff1a\u5708\u73af\u5e26\u78b0\u649e\uff08\u95e8\u53e3\u4e0d\u78b0\uff09'
new2 = '"""    // \U0001F479 BOSS \u573a\u5730\u5708\u5899\uff1a\u5708\u73af\u5e26\u78b0\u649e\uff08\u95e8\u53e3\u4e0d\u78b0\uff09'
assert src.count(old2) == 1, src.count(old2)

io.open(p, 'w', encoding='utf-8').write(src)
print('patched')
