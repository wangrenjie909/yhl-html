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

# 楼顶上的小怪要重新画在楼顶上面（不然被楼顶盖住看不见！）
rep("""            ctx.fillText('\\U0001FA9C', bb.x + T + 24, bb.y + T + 40);   // \\u697c\\u68af\\u53e3
        }
        // \\u26F0\\ufe0f \\u9505\\u5854\\u9876 3 \\u697c\\uff08\\u9ad8\\u5904\\uff0c\\u80fd\\u6253\\u5230\\u4e0b\\u9762\\u4e00\\u5207\\uff09
""",
    """            ctx.fillText('\\U0001FA9C', bb.x + T + 24, bb.y + T + 40);   // \\u697c\\u68af\\u53e3
        }
        // \\U0001F47E \\u697c\\u9876\\u4e0a\\u7684\\u5c0f\\u602a\\uff1a\\u91cd\\u65b0\\u753b\\u5728\\u697c\\u9876\\u4e0a\\u9762\\uff08\\u4e0d\\u88ab\\u697c\\u9876\\u76d6\\u4f4f\\uff0c\\u80fd\\u770b\\u89c1\\uff01\\uff09
        if (player.floor === 2 && player.bIdx >= 0) {
            ctx.font = '52px sans-serif';
            for (var ri = 0; ri < enemies.length; ri++) {
                var re = enemies[ri];
                if (re.floor === 2 && re.bIdx === player.bIdx) {
                    ctx.fillText(re.ranged ? '\\U0001F916' : '\\U0001F47E', re.x, re.y + 15);
                    ctx.fillStyle = '#333';
                    ctx.fillRect(re.x - 32, re.y - 58, 64, 7);
                    ctx.fillStyle = '#ff5d5d';
                    ctx.fillRect(re.x - 32, re.y - 58, 64 * Math.max(0, re.hp / 100), 7);
                    ctx.fillStyle = '#ffd93d';
                    ctx.font = 'bold 16px sans-serif';
                    ctx.fillText(Math.max(0, re.hp), re.x, re.y - 66);
                }
            }
        }
        // \\u26F0\\ufe0f \\u9505\\u5854\\u9876 3 \\u697c\\uff08\\u9ad8\\u5904\\uff0c\\u80fd\\u6253\\u5230\\u4e0b\\u9762\\u4e00\\u5207\\uff09
""",
    'roof-enemy-visible')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
