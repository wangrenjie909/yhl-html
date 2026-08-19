# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\ai\code\yhl-html\sdc.html'
src = io.open(path, encoding='utf-8').read()
n0 = len(src)

old = "            ctx.fillText('\U0001FA9C', bb.x + T + 24, bb.y + T + 40);   // \u697c\u68af\u53e3\n        }\n        // \u26F0\ufe0f \u9505\u5854\u9876 3 \u697c\uff08\u9ad8\u5904\uff0c\u80fd\u6253\u5230\u4e0b\u9762\u4e00\u5207\uff09\n"
new = ("            ctx.fillText('\U0001FA9C', bb.x + T + 24, bb.y + T + 40);   // \u697c\u68af\u53e3\n"
       "        }\n"
       "        // \U0001F47E \u697c\u9876\u4e0a\u7684\u5c0f\u602a\uff1a\u91cd\u65b0\u753b\u5728\u697c\u9876\u4e0a\u9762\uff08\u4e0d\u88ab\u697c\u9876\u76d6\u4f4f\uff0c\u80fd\u770b\u89c1\uff01\uff09\n"
       "        if (player.floor === 2 && player.bIdx >= 0) {\n"
       "            ctx.font = '52px sans-serif';\n"
       "            for (var ri = 0; ri < enemies.length; ri++) {\n"
       "                var re = enemies[ri];\n"
       "                if (re.floor === 2 && re.bIdx === player.bIdx) {\n"
       "                    ctx.fillText(re.ranged ? '\U0001F916' : '\U0001F47E', re.x, re.y + 15);\n"
       "                    ctx.fillStyle = '#333';\n"
       "                    ctx.fillRect(re.x - 32, re.y - 58, 64, 7);\n"
       "                    ctx.fillStyle = '#ff5d5d';\n"
       "                    ctx.fillRect(re.x - 32, re.y - 58, 64 * Math.max(0, re.hp / 100), 7);\n"
       "                    ctx.fillStyle = '#ffd93d';\n"
       "                    ctx.font = 'bold 16px sans-serif';\n"
       "                    ctx.fillText(Math.max(0, re.hp), re.x, re.y - 66);\n"
       "                }\n"
       "            }\n"
       "        }\n"
       "        // \u26F0\ufe0f \u9505\u5854\u9876 3 \u697c\uff08\u9ad8\u5904\uff0c\u80fd\u6253\u5230\u4e0b\u9762\u4e00\u5207\uff09\n")

print('match:', src.count(old))
assert src.count(old) == 1
src = src.replace(old, new)
assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
