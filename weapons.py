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

# 1) 玩家加 weapon 字段 + 枪械大全
old = "    var player = { x: 200, y: 200, hp: 100, dir: 0, atkCd: 0, hitCd: 0, bullets: 30 };\n"
new = ("    var player = { x: 200, y: 200, hp: 100, dir: 0, atkCd: 0, hitCd: 0, bullets: 30, weapon: 'pistol' };\n"
       "\n"
       "    // \U0001F52B \u67aa\u68f0\u5927\u5168\uff01\n"
       "    var WEAPONS = {\n"
       "        pistol:  { name: '\u624b\u67aa',   dmg: 34, rate: 0.28, speed: 720,  pellets: 1, spread: 0 },\n"
       "        rifle:   { name: '\u6b65\u67aa',   dmg: 24, rate: 0.12, speed: 820,  pellets: 1, spread: 0.03 },\n"
       "        shotgun: { name: '\u971c\u5f39\u67aa', dmg: 15, rate: 0.65, speed: 640,  pellets: 6, spread: 0.30 },\n"
       "        sniper:  { name: '\u72d9\u51fb\u67aa', dmg: 95, rate: 0.85, speed: 1150, pellets: 1, spread: 0 }\n"
       "    };\n"
       "    function randomWeapon() {\n"
       "        var ks = ['rifle', 'shotgun', 'sniper'];\n"
       "        return ks[Math.floor(Math.random() * ks.length)];\n"
       "    }\n"
       "    function dropWeaponPickup(x, y) {\n"
       "        drops.push({ x: x, y: y, kind: 'weapon', w: randomWeapon() });\n"
       "    }\n")
rep(old, new, 'weapons-config')

# 2) 开箱：加枪械掉落
old = ("    function openCrate(c) {\n"
       "        cratesOpened++;\n"
       "        var r = Math.random();\n"
       "        if (r < 0.15) {\n"
       "            player.bullets += 25;\n"
       "            fx.push({ x: c.x, y: c.y, t: 0, text: '\U0001F4A5 \u5b50\u5f39 x25' });\n"
       "            showMsg('\U0001F4E6 \u7206\u51fa\u5b50\u5f39 x25\uff01');\n"
       "        } else if (r < 0.30) {\n"
       "            player.hp = Math.min(100, player.hp + 30);\n"
       "            fx.push({ x: c.x, y: c.y, t: 0, text: '\u2764\ufe0f \u533b\u7597\u5305 +30' });\n"
       "            showMsg('\U0001F4E6 \u7206\u51fa\u533b\u7597\u5305\uff01\u2764\ufe0f +30\u8840');\n"
       "            document.getElementById('hpbar').style.width = player.hp + '%';\n"
       "            document.getElementById('hpnum').textContent = player.hp;\n"
       "        } else if (r < 0.45) {\n"
       "            score += 50;\n"
       "            fx.push({ x: c.x, y: c.y, t: 0, text: '\U0001F4B0 \u5927\u91d1\u5757 +50' });\n"
       "            showMsg('\U0001F4E6 \u7206\u51fa\u5927\u91d1\u5757\uff01\U0001F4B0 +50\u5206');\n"
       "        } else if (r < 0.80) {\n"
       "            score += 5;\n"
       "            fx.push({ x: c.x, y: c.y, t: 0, text: '\U0001F36A \u997c\u5e72 +5' });\n"
       "            showMsg('\U0001F4E6 \u666e\u901a\u7269\u54c1\uff1a\u997c\u5e72 \U0001F36A +5\u5206');\n"
       "        } else {\n"
       "            fx.push({ x: c.x, y: c.y, t: 0, text: '\U0001F9E6 \u65e7\u889c\u5b50\u2026' });\n"
       "            showMsg('\U0001F4E6 \u5c31\u8fd9\uff1f\u4e00\u53cc\u65e7\u889c\u5b50 \U0001F9E6');\n"
       "        }\n"
       "        fx.push({ x: c.x, y: c.y, r: 8, t: 0 });\n"
       "    }\n")
new = ("    function openCrate(c) {\n"
       "        cratesOpened++;\n"
       "        var r = Math.random();\n"
       "        if (r < 0.12) {\n"
       "            player.bullets += 25;\n"
       "            fx.push({ x: c.x, y: c.y, t: 0, text: '\U0001F4A5 \u5b50\u5f39 x25' });\n"
       "            showMsg('\U0001F4E6 \u7206\u51fa\u5b50\u5f39 x25\uff01');\n"
       "        } else if (r < 0.22) {\n"
       "            player.hp = Math.min(100, player.hp + 30);\n"
       "            fx.push({ x: c.x, y: c.y, t: 0, text: '\u2764\ufe0f \u533b\u7597\u5305 +30' });\n"
       "            showMsg('\U0001F4E6 \u7206\u51fa\u533b\u7597\u5305\uff01\u2764\ufe0f +30\u8840');\n"
       "            document.getElementById('hpbar').style.width = player.hp + '%';\n"
       "            document.getElementById('hpnum').textContent = player.hp;\n"
       "        } else if (r < 0.34) {\n"
       "            // \U0001F52B \u5f00\u51fa\u67aa\u68f0\uff01\n"
       "            var w = randomWeapon();\n"
       "            drops.push({ x: c.x, y: c.y, kind: 'weapon', w: w });\n"
       "            fx.push({ x: c.x, y: c.y, t: 0, text: '\U0001F381 \u7206\u51fa ' + WEAPONS[w].name + '\uff01' });\n"
       "            showMsg('\U0001F4E6 \u7206\u51fa\u67aa\u68f0\uff1a' + WEAPONS[w].name + '\uff01');\n"
       "        } else if (r < 0.40) {\n"
       "            score += 50;\n"
       "            fx.push({ x: c.x, y: c.y, t: 0, text: '\U0001F4B0 \u5927\u91d1\u5757 +50' });\n"
       "            showMsg('\U0001F4E6 \u7206\u51fa\u5927\u91d1\u5757\uff01\U0001F4B0 +50\u5206');\n"
       "        } else if (r < 0.75) {\n"
       "            score += 5;\n"
       "            fx.push({ x: c.x, y: c.y, t: 0, text: '\U0001F36A \u997c\u5e72 +5' });\n"
       "            showMsg('\U0001F4E6 \u666e\u901a\u7269\u54c1\uff1a\u997c\u5e72 \U0001F36A +5\u5206');\n"
       "        } else {\n"
       "            fx.push({ x: c.x, y: c.y, t: 0, text: '\U0001F9E6 \u65e7\u889c\u5b50\u2026' });\n"
       "            showMsg('\U0001F4E6 \u5c31\u8fd9\uff1f\u4e00\u53cc\u65e7\u889c\u5b50 \U0001F9E6');\n"
       "        }\n"
       "        fx.push({ x: c.x, y: c.y, r: 8, t: 0 });\n"
       "    }\n")
rep(old, new, 'crate-weapon')

# 3) 射击：按枪械参数发射
old = ("        // \U0001F52B \u5c04\u51fb\uff08\u9f20\u6807\u5de6\u952e / \u7a7a\u683c / J\uff09\n"
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
new = ("        // \U0001F52B \u5c04\u51fb\uff08\u9f20\u6807\u5de6\u952e / \u7a7a\u683c / J\uff09\u2014\u2014\u6309\u5f53\u524d\u67aa\u68f0\u53c2\u6570\u53d1\u5c04\uff01\n"
       "        var wg = WEAPONS[player.weapon];\n"
       "        if ((keys[' '] || keys['j'] || mouseDown) && player.atkCd <= 0) {\n"
       "            if (player.bullets > 0) {\n"
       "                player.atkCd = wg.rate;\n"
       "                player.bullets--;\n"
       "                for (var pi = 0; pi < wg.pellets; pi++) {\n"
       "                    var pang = player.dir + (Math.random() - 0.5) * 2 * wg.spread;   // \u6563\u5c04\n"
       "                    bullets.push({\n"
       "                        x: player.x,   // \U0001F52B \u5b50\u5f39\u4ece\u8eab\u4f53\u4e2d\u5fc3\u53d1\u5c04\uff1a\u8d34\u8138\u654c\u4eba\u4e5f\u80fd\u6253\u4e2d\uff01\n"
       "                        y: player.y,\n"
       "                        vx: Math.cos(pang) * wg.speed,\n"
       "                        vy: Math.sin(pang) * wg.speed,\n"
       "                        life: 1.2,\n"
       "                        dmg: wg.dmg\n"
       "                    });\n"
       "                }\n"
       "                fx.push({ x: player.x + Math.cos(player.dir) * 20, y: player.y + Math.sin(player.dir) * 20, r: 8, t: 0 });\n"
       "            } else {\n"
       "                player.atkCd = 0.4;\n"
       "                showMsg('\u5494\u5494\u2026\u6ca1\u5b50\u5f39\u4e86\uff01\u53bb\u5f00\u7bb1\u5b50\u6216\u6253\u654c\u4eba \U0001F52B');\n"
       "            }\n"
       "        }\n")
rep(old, new, 'shoot-by-weapon')

# 4) 子弹伤害按枪械 + 击杀掉枪
old = ("            } else if (hitEnemy >= 0) {\n"
       "                var e = enemies[hitEnemy];\n"
       "                e.hp -= 34;\n"
       "                fx.push({ x: b.x, y: b.y, r: 6, t: 0 });\n"
       "                bullets.splice(i, 1);\n"
       "                if (e.hp <= 0) {\n"
       "                    // \u51fb\u6740\uff1a\u6389\u5b50\u5f39\n"
       "                    drops.push({ x: e.x, y: e.y });\n"
       "                    score += 20; kills++;\n"
       "                    showMsg('\U0001F47E \u51fb\u6740\uff01+20\u5206\uff0c\u6389\u843d \u26A1 \u5b50\u5f39');\n"
       "                    enemies.splice(hitEnemy, 1);\n"
       "                }\n"
       "            }\n")
new = ("            } else if (hitEnemy >= 0) {\n"
       "                var e = enemies[hitEnemy];\n"
       "                e.hp -= b.dmg;   // \u4f24\u5bb3\u6309\u67aa\u68f0\uff01\n"
       "                fx.push({ x: b.x, y: b.y, r: 6, t: 0 });\n"
       "                bullets.splice(i, 1);\n"
       "                if (e.hp <= 0) {\n"
       "                    // \u51fb\u6740\uff1a\u6389\u5b50\u5f39 + \u53ef\u80fd\u7206\u67aa\uff01\n"
       "                    drops.push({ x: e.x, y: e.y });\n"
       "                    var dropGun = Math.random() < 0.25;\n"
       "                    if (dropGun) dropWeaponPickup(e.x + 14, e.y + 14);\n"
       "                    score += 20; kills++;\n"
       "                    showMsg(dropGun ? '\U0001F47E \u51fb\u6740\uff01\u6389\u843d \u26A1 \u5b50\u5f39 \u548c \U0001F52B \u67aa\u68f0\uff01' : '\U0001F47E \u51fb\u6740\uff01+20\u5206\uff0c\u6389\u843d \u26A1 \u5b50\u5f39');\n"
       "                    enemies.splice(hitEnemy, 1);\n"
       "                }\n"
       "            }\n")
rep(old, new, 'kill-drop-weapon')

# 5) 捡起：子弹 or 枪械
old = ("        // \u26A1 \u6361\u5b50\u5f39\n"
       "        for (var i = drops.length - 1; i >= 0; i--) {\n"
       "            var dp = drops[i];\n"
       "            var d = Math.sqrt((dp.x - player.x) * (dp.x - player.x) + (dp.y - player.y) * (dp.y - player.y));\n"
       "            if (d < 34) {\n"
       "                player.bullets += 10;\n"
       "                fx.push({ x: dp.x, y: dp.y, t: 0, text: '\u26A1 +10 \u5b50\u5f39' });\n"
       "                showMsg('\u26A1 \u6361\u5230\u5b50\u5f39 x10\uff01');\n"
       "                drops.splice(i, 1);\n"
       "            }\n"
       "        }\n")
new = ("        // \u26A1 \u6361\u5b50\u5f39 / \U0001F52B \u6361\u67aa\u68f0\n"
       "        for (var i = drops.length - 1; i >= 0; i--) {\n"
       "            var dp = drops[i];\n"
       "            var d = Math.sqrt((dp.x - player.x) * (dp.x - player.x) + (dp.y - player.y) * (dp.y - player.y));\n"
       "            if (d < 34) {\n"
       "                if (dp.kind === 'weapon') {\n"
       "                    player.weapon = dp.w;\n"
       "                    fx.push({ x: dp.x, y: dp.y, t: 0, text: '\U0001F52B ' + WEAPONS[dp.w].name + '\uff01' });\n"
       "                    showMsg('\U0001F52B \u6361\u5230' + WEAPONS[dp.w].name + '\uff01');\n"
       "                } else {\n"
       "                    player.bullets += 10;\n"
       "                    fx.push({ x: dp.x, y: dp.y, t: 0, text: '\u26A1 +10 \u5b50\u5f39' });\n"
       "                    showMsg('\u26A1 \u6361\u5230\u5b50\u5f39 x10\uff01');\n"
       "                }\n"
       "                drops.splice(i, 1);\n"
       "            }\n"
       "        }\n")
rep(old, new, 'pickup-weapon')

# 6) 画掉落：枪械显示名字
old = ("        // \u26A1 \u5b50\u5f39\u6389\u843d\n"
       "        ctx.font = '22px sans-serif';\n"
       "        for (var i = 0; i < drops.length; i++) {\n"
       "            ctx.fillText('\u26A1', drops[i].x, drops[i].y + 8);\n"
       "        }\n")
new = ("        // \u26A1 \u5b50\u5f39 / \U0001F52B \u67aa\u68f0\u6389\u843d\n"
       "        ctx.font = '22px sans-serif';\n"
       "        for (var i = 0; i < drops.length; i++) {\n"
       "            var dp = drops[i];\n"
       "            if (dp.kind === 'weapon') {\n"
       "                ctx.fillText('\U0001F52B', dp.x, dp.y + 8);\n"
       "                ctx.font = 'bold 12px sans-serif';\n"
       "                ctx.fillStyle = '#ffd93d';\n"
       "                ctx.fillText(WEAPONS[dp.w].name, dp.x, dp.y + 26);\n"
       "                ctx.font = '22px sans-serif';\n"
       "            } else {\n"
       "                ctx.fillText('\u26A1', dp.x, dp.y + 8);\n"
       "            }\n"
       "        }\n")
rep(old, new, 'draw-drops')

# 7) HUD 显示当前枪械
old = "        document.getElementById('bullets').textContent = player.bullets;\n"
new = "        document.getElementById('bullets').textContent = WEAPONS[player.weapon].name + ' ' + player.bullets;\n"
rep(old, new, 'hud-weapon')

# 8) resetGame 重置枪械
old = "        player.x = 200; player.y = 200; player.hp = 100; player.bullets = 30;\n"
new = "        player.x = 200; player.y = 200; player.hp = 100; player.bullets = 30; player.weapon = 'pistol';\n"
rep(old, new, 'reset-weapon')

# 9) 玩家画枪：按枪械画枪管长度
old = ("        // \u67aa\n"
       "        ctx.fillStyle = '#3a3f4a';\n"
       "        ctx.fillRect(14, -3, 18, 6);\n"
       "        ctx.fillStyle = '#ff8e3c';\n"
       "        ctx.fillRect(26, -5, 6, 10);\n")
new = ("        // \u67aa\uff08\u4e0d\u540c\u67aa\u68f0\u67aa\u7ba1\u4e0d\u4e00\u6837\u957f\uff01\uff09\n"
       "        var glen = player.weapon === 'sniper' ? 30 : (player.weapon === 'shotgun' ? 24 : 18);\n"
       "        ctx.fillStyle = '#3a3f4a';\n"
       "        ctx.fillRect(14, -3, glen, 6);\n"
       "        ctx.fillStyle = '#ff8e3c';\n"
       "        ctx.fillRect(14 + glen, -5, 6, 10);\n")
rep(old, new, 'draw-gun')

# 10) 玩法说明：加枪械说明
old = "        <li>\U0001F47E \u51fb\u6740\u654c\u4eba\u6389\u843d \u26A1<b>\u5b50\u5f39</b>\uff0c\u6361\u8d77\u6765\u8865\u5145\uff01</li>\n"
new = ("        <li>\U0001F47E \u51fb\u6740\u654c\u4eba\u6389\u843d \u26A1<b>\u5b50\u5f39</b>\uff0c\u8fd8\u53ef\u80fd\u7206 \U0001F52B<b>\u67aa\u68f0</b>\uff01</li>\n"
       "        <li>\U0001F4E6 \u5f00\u7bb1\u4e5f\u53ef\u80fd\u7206\u51fa<b>\u67aa\u68f0</b>\uff1a\u6b65\u67aa\uff08\u5feb\uff09/\u971c\u5f39\u67aa\uff08\u6563\u5f39\uff09/\u72d9\u51fb\u67aa\uff08\u7206\u5934\uff09</li>\n")
rep(old, new, 'instructions')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
