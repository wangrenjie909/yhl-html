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

# 1) 鼠标跟踪
old = "    resize();\n    window.addEventListener('resize', resize);\n"
new = "    resize();\n    window.addEventListener('resize', resize);\n\n    // \U0001F3AF \u9f20\u6807\u51c6\u661f\uff08\u67aa\u53e3\u8ddf\u7740\u9f20\u6807\u79fb\u52a8\uff09\n    var mouse = { x: W / 2, y: H / 2, on: false };\n    canvas.addEventListener('mousemove', function (e) {\n        mouse.x = e.clientX;\n        mouse.y = e.clientY;\n        mouse.on = true;\n    });\n"
rep(old, new, 'mouse-track')

# 2) 移动不再改朝向
old = "            dx /= l; dy /= l;\n            player.dir = Math.atan2(dy, dx);\n"
new = "            dx /= l; dy /= l;\n"
rep(old, new, 'move-no-aim')

# 3) 朝向 = 鼠标方向
old = "        if (player.atkCd > 0) player.atkCd -= dt;\n        if (player.hitCd > 0) player.hitCd -= dt;\n"
new = "        if (player.atkCd > 0) player.atkCd -= dt;\n        if (player.hitCd > 0) player.hitCd -= dt;\n\n        // \U0001F3AF \u67aa\u53e3\u8ddf\u7740\u9f20\u6807\u7784\u51c6\uff01\uff08\u79fb\u52a8\u8fd8\u662f WASD\uff09\n        var camX = Math.max(0, Math.min(MAPW - W, player.x - W / 2));\n        var camY = Math.max(0, Math.min(MAPH - H, player.y - H / 2));\n        if (mouse.on) {\n            player.dir = Math.atan2((mouse.y + camY) - player.y, (mouse.x + camX) - player.x);\n        } else if (dx || dy) {\n            player.dir = Math.atan2(dy, dx);   // \u624b\u673a\uff1a\u6ca1\u6709\u9f20\u6807\u5c31\u7528\u79fb\u52a8\u65b9\u5411\n        }\n"
rep(old, new, 'aim-with-mouse')

# 4) 画鼠标准星
old = "        ctx.restore();\n    }\n\n    function loop() {\n"
new = "        ctx.restore();\n\n        // \U0001F3AF \u9f20\u6807\u51c6\u661f\n        if (mouse.on) {\n            ctx.strokeStyle = 'rgba(255,255,255,0.85)';\n            ctx.lineWidth = 2;\n            ctx.beginPath();\n            ctx.moveTo(mouse.x - 10, mouse.y); ctx.lineTo(mouse.x + 10, mouse.y);\n            ctx.moveTo(mouse.x, mouse.y - 10); ctx.lineTo(mouse.x, mouse.y + 10);\n            ctx.stroke();\n            ctx.beginPath();\n            ctx.arc(mouse.x, mouse.y, 6, 0, Math.PI * 2);\n            ctx.stroke();\n        }\n    }\n\n    function loop() {\n"
rep(old, new, 'crosshair')

# 5) 玩法说明：从文件真实行构建 old（保证匹配）
lines = src.split('\n')
old = '\n'.join(lines[131:134]) + '\n'
new = ("        <li>\U0001F579\ufe0f WASD / \u65b9\u5411\u952e \u79fb\u52a8\uff0c\u8d70\u8fdb<b>\u623f\u95f4</b>\u641c\u5212</li>\n"
       "        <li>\U0001F3AF \u9f20\u6807\u63a7\u5236<b>\u67aa\u53e3\u7784\u51c6</b>\uff0c\u7a7a\u683c\u5c04\u51fb</li>\n"
       "        <li>\U0001F4E6 \u8e29\u5230<b>\u7bb1\u5b50</b>\u81ea\u52a8\u6253\u5f00\u2014\u2014\u53ef\u80fd\u7206\u597d\u8d27\uff0c\u4e5f\u53ef\u80fd\u53ea\u662f\u6742\u7269\uff01</li>\n")
assert src.count(old) == 1, 'instructions match = %d' % src.count(old)
src = src.replace(old, new)
print('OK instructions')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
