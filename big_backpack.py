# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\ai\code\yhl-html\sdc.html'
src = io.open(path, encoding='utf-8').read()
n0 = len(src)

def rep(old, new, name, count=1):
    global src
    assert src.count(old) == count, '%s match = %d' % (name, src.count(old))
    src = src.replace(old, new)
    print('OK', name)

# 1) 背包 24 -> 80 格
rep("    var INV_SIZE = 24;\n",
    "    var INV_SIZE = 80;   // \U0001F392 \u8d85\u7ea7\u5927\u80cc\u5305\uff018\u5217 x 10\u884c\uff01\n",
    'inv-80')

# 2) 格子更小更密：8 列
rep("    .wh-grid { display: grid; grid-template-columns: repeat(6, 64px); gap: 6px; justify-content: center; margin: 12px auto; }\n",
    "    .wh-grid { display: grid; grid-template-columns: repeat(8, 56px); gap: 5px; justify-content: center; margin: 12px auto; }\n",
    'wh-8col')
rep("""    .wh-slot {
        width: 64px; height: 64px;
""",
    """    .wh-slot {
        width: 56px; height: 56px;
""",
    'wh-slot-size')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
