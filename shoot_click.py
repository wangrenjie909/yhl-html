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

# 1) 鼠标左键 = 开火（在鼠标准星监听后加）
old = "    canvas.addEventListener('mousemove', function (e) {\n        mouse.x = e.clientX;\n        mouse.y = e.clientY;\n        mouse.on = true;\n    });\n"
new = ("    canvas.addEventListener('mousemove', function (e) {\n"
       "        mouse.x = e.clientX;\n"
       "        mouse.y = e.clientY;\n"
       "        mouse.on = true;\n"
       "    });\n"
       "    // \U0001F52B \u9f20\u6807\u5de6\u952e\u5f00\u706b\uff01\n"
       "    var mouseDown = false;\n"
       "    canvas.addEventListener('mousedown', function (e) { if (e.button === 0) mouseDown = true; });\n"
       "    canvas.addEventListener('mouseup', function (e) { if (e.button === 0) mouseDown = false; });\n"
       "    canvas.addEventListener('mouseleave', function () { mouseDown = false; });\n")
rep(old, new, 'left-click')

# 2) 射击条件 + 子弹从身体中心发射（贴脸也能打中！）
old = ("        // \U0001F52B \u5c04\u51fb\n"
       "        if ((keys[' '] || keys['j']) && player.atkCd <= 0) {\n"
       "            if (player.bullets > 0) {\n"
       "                player.atkCd = 0.28;\n"
       "                player.bullets--;\n"
       "                bullets.push({\n"
       "                    x: player.x + Math.cos(player.dir) * 20,\n"
       "                    y: player.y + Math.sin(player.dir) * 20,\n"
       "                    vx: Math.cos(player.dir) * 720,\n"
       "                    vy: Math.sin(player.dir) * 720,\n"
       "                    life: 1.2\n"
       "                });\n"
       "                fx.push({ x: player.x + Math.cos(player.dir) * 20, y: player.y + Math.sin(player.dir) * 20, r: 8, t: 0 });\n"
       "            } else {\n"
       "                player.atkCd = 0.4;\n"
       "                showMsg('\u5494\u5494\u2026\u6ca1\u5b50\u5f39\u4e86\uff01\u53bb\u5f00\u7bb1\u5b50\u6216\u6253\u654c\u4eba \U0001F52B');\n"
       "            }\n"
       "        }\n")
new = ("        // \U0001F52B \u5c04\u51fb\uff08\u9f20\u6807\u5de6\u952e / \u7a7a\u683c / J\uff09\n"
       "        if ((keys[' '] || keys['j'] || mouseDown) && player.atkCd <= 0) {\n"
       "            if (player.bullets > 0) {\n"
       "                player.atkCd = 0.28;\n"
       "                player.bullets--;\n"
       "                bullets.push({\n"
       "                    x: player.x,   // \U0001F52B \u5b50\u5f39\u4ece\u8eab\u4f53\u4e2d\u5fc3\u53d1\u5c04\uff1a\u8d34\u8138\u654c\u4eba\u4e5f\u80fd\u6253\u4e2d\uff01\n"
       "                    y: player.y,\n"
       "                    vx: Math.cos(player.dir) * 720,\n"
       "                    vy: Math.sin(player.dir) * 720,\n"
       "                    life: 1.2\n"
       "                });\n"
       "                fx.push({ x: player.x + Math.cos(player.dir) * 20, y: player.y + Math.sin(player.dir) * 20, r: 8, t: 0 });\n"
       "            } else {\n"
       "                player.atkCd = 0.4;\n"
       "                showMsg('\u5494\u5494\u2026\u6ca1\u5b50\u5f39\u4e86\uff01\u53bb\u5f00\u7bb1\u5b50\u6216\u6253\u654c\u4eba \U0001F52B');\n"
       "            }\n"
       "        }\n")
rep(old, new, 'shoot-fix')

# 3) 玩法说明：鼠标左键射击
old = "        <li>\U0001F3AF \u9f20\u6807\u63a7\u5236<b>\u67aa\u53e3\u7784\u51c6</b>\uff0c\u7a7a\u683c\u5c04\u51fb</li>\n"
new = "        <li>\U0001F3AF \u9f20\u6807\u63a7\u5236<b>\u67aa\u53e3\u7784\u51c6</b>\uff0c\u9f20\u6807<b>\u5de6\u952e</b>\u5c04\u51fb\uff08\u7a7a\u683c\u4e5f\u884c\uff09</li>\n"
rep(old, new, 'instructions')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
