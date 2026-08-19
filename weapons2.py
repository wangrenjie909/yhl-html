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

# 1) 玩家：两把枪槽
rep("    var player = { x: 200, y: 200, hp: 100, dir: 0, atkCd: 0, hitCd: 0, bullets: 30, weapon: 'pistol' };\n",
    "    var player = { x: 200, y: 200, hp: 100, dir: 0, atkCd: 0, hitCd: 0, bullets: 30, weapons: ['pistol', null], weaponSlot: 0 };\n",
    'player-slots')

# 2) 更多枪械 + 切枪/拾取函数
rep("""    // \U0001F52B \u67aa\u68f0\u5927\u5168\uff01
    var WEAPONS = {
        pistol:  { name: '\u624b\u67aa',   dmg: 34, rate: 0.28, speed: 720,  pellets: 1, spread: 0 },
        rifle:   { name: '\u6b65\u67aa',   dmg: 24, rate: 0.12, speed: 820,  pellets: 1, spread: 0.03 },
        shotgun: { name: '\u971c\u5f39\u67aa', dmg: 15, rate: 0.65, speed: 640,  pellets: 6, spread: 0.30 },
        sniper:  { name: '\u72d9\u51fb\u67aa', dmg: 95, rate: 0.85, speed: 1150, pellets: 1, spread: 0 }
    };
    function randomWeapon() {
        var ks = ['rifle', 'shotgun', 'sniper'];
        return ks[Math.floor(Math.random() * ks.length)];
    }
    function dropWeaponPickup(x, y) {
        drops.push({ x: x, y: y, kind: 'weapon', w: randomWeapon() });
    }
""",
    """    // \U0001F52B \u67aa\u68f0\u5927\u5168\uff01
    var WEAPONS = {
        pistol:  { name: '\u624b\u67aa',   dmg: 34, rate: 0.28, speed: 720,  pellets: 1, spread: 0 },
        rifle:   { name: '\u6b65\u67aa',   dmg: 24, rate: 0.12, speed: 820,  pellets: 1, spread: 0.03 },
        shotgun: { name: '\u971c\u5f39\u67aa', dmg: 15, rate: 0.65, speed: 640,  pellets: 6, spread: 0.30 },
        sniper:  { name: '\u72d9\u51fb\u67aa', dmg: 95, rate: 0.85, speed: 1150, pellets: 1, spread: 0 },
        smg:     { name: '\u51b2\u950b\u67aa', dmg: 18, rate: 0.07, speed: 780,  pellets: 1, spread: 0.07 },
        gatling: { name: '\u52a0\u7279\u6797', dmg: 12, rate: 0.045, speed: 760, pellets: 1, spread: 0.13 },
        laser:   { name: '\u6fc0\u5149\u67aa', dmg: 42, rate: 0.16, speed: 1050, pellets: 1, spread: 0 }
    };
    function currentWeapon() {
        return player.weapons[player.weaponSlot] || 'pistol';
    }
    function randomWeapon() {
        var ks = ['rifle', 'shotgun', 'sniper', 'smg', 'gatling', 'laser'];
        return ks[Math.floor(Math.random() * ks.length)];
    }
    function dropWeaponPickup(x, y) {
        drops.push({ x: x, y: y, kind: 'weapon', w: randomWeapon() });
    }
    // \U0001F52B \u5207\u67aa\uff1aQ / \u9009\u9879\u5361 \u8f6e\u6362\u4e24\u4e2a\u67aa\u69fd
    function switchWeapon() {
        var other = 1 - player.weaponSlot;
        if (player.weapons[other] !== null) {
            player.weaponSlot = other;
            showMsg('\U0001F52B \u5207\u5230' + WEAPONS[currentWeapon()].name);
        }
    }
    // \u270B \u624b\u52a8\u62fe\u53d6\uff1a\u9760\u8fd1\u5730\u4e0a\u7684\u67aa\u6309 E
    function tryPickup() {
        var idx = -1;
        for (var i = 0; i < drops.length; i++) {
            if (drops[i].kind !== 'weapon') continue;
            var d = Math.sqrt((drops[i].x - player.x) * (drops[i].x - player.x) + (drops[i].y - player.y) * (drops[i].y - player.y));
            if (d < 60) { idx = i; break; }
        }
        if (idx < 0) { showMsg('\u270B \u6ca1\u6709\u53ef\u4ee5\u62fe\u53d6\u7684\u67aa\u5668'); return; }
        var wp = drops[idx].w;
        drops.splice(idx, 1);
        if (player.weapons[0] === null) {
            player.weapons[0] = wp;
            showMsg('\U0001F52B \u62fe\u53d6' + WEAPONS[wp].name + '\uff01\u6309 Q \u5207\u6362');
        } else if (player.weapons[1] === null) {
            player.weapons[1] = wp;
            showMsg('\U0001F52B \u62fe\u53d6' + WEAPONS[wp].name + '\uff01\u6309 Q \u5207\u6362');
        } else {
            var old = player.weapons[player.weaponSlot];
            player.weapons[player.weaponSlot] = wp;
            drops.push({ x: player.x + 14, y: player.y + 14, kind: 'weapon', w: old });
            showMsg('\U0001F504 \u6362\u4e0b' + WEAPONS[old].name + '\uff0c\u62fe\u8d77' + WEAPONS[wp].name + '\uff01');
        }
    }
""",
    'weapons-more')

# 3) 按键：Q切枪 / E拾取
rep("""    document.addEventListener('keydown', function (e) {
        if (e.key === ' ') e.preventDefault();
        keys[e.key.toLowerCase()] = true;
    });
""",
    """    document.addEventListener('keydown', function (e) {
        if (e.key === ' ') e.preventDefault();
        var k = e.key.toLowerCase();
        keys[k] = true;
        if (k === 'q' || k === 'tab') switchWeapon();
        if (k === 'e' || k === 'f') tryPickup();
    });
""",
    'keys-qe')

# 4) 手机按钮：加 切枪 + 拾取
rep("""    <button class="tbtn" data-k=" ">\U0001F52B</button>
</div>
""",
    """    <div style="display:flex;flex-direction:column;gap:6px">
        <button class="tbtn" data-k=" ">\U0001F52B</button>
        <button class="tbtn" id="btn-switch">\U0001F501</button>
        <button class="tbtn" id="btn-pickup">\u270B</button>
    </div>
</div>
""",
    'touch-btns')

rep("""    var tbs = document.querySelectorAll('.tbtn');
""",
    """    document.getElementById('btn-switch').addEventListener('click', switchWeapon);
    document.getElementById('btn-pickup').addEventListener('click', tryPickup);

    var tbs = document.querySelectorAll('.tbtn');
""",
    'touch-listeners')

# 5) 射击用当前枪
rep("        var wg = WEAPONS[player.weapon];\n",
    "        var wg = WEAPONS[currentWeapon()];\n",
    'shoot-current')

# 6) 拾取：武器不再自动捡（等玩家按E）
rep("""            if (d < 34) {
                if (dp.kind === 'weapon') {
                    player.weapon = dp.w;
                    fx.push({ x: dp.x, y: dp.y, t: 0, text: '\U0001F52B ' + WEAPONS[dp.w].name + '\uff01' });
                    showMsg('\U0001F52B \u6361\u5230' + WEAPONS[dp.w].name + '\uff01');
                } else {
                    player.bullets += 10;
                    fx.push({ x: dp.x, y: dp.y, t: 0, text: '\u26A1 +10 \u5b50\u5f39' });
                    showMsg('\u26A1 \u6361\u5230\u5b50\u5f39 x10\uff01');
                }
                drops.splice(i, 1);
            }
""",
    """            if (d < 34) {
                // \u67aa\u68f0\u8981\u73a9\u5bb6\u81ea\u5df1\u6309 E \u62fe\u53d6\uff08\u4e0d\u81ea\u52a8\u62fe\uff09\uff0c\u5b50\u5f39\u81ea\u52a8\u62fe
                if (dp.kind !== 'weapon') {
                    player.bullets += 10;
                    fx.push({ x: dp.x, y: dp.y, t: 0, text: '\u26A1 +10 \u5b50\u5f39' });
                    showMsg('\u26A1 \u6361\u5230\u5b50\u5f39 x10\uff01');
                    drops.splice(i, 1);
                }
            }
""",
    'no-auto-weapon')

# 7) HUD 显示当前枪 + 槽位
rep("        document.getElementById('bullets').textContent = WEAPONS[player.weapon].name + ' ' + player.bullets;\n",
    ("        var cw = currentWeapon();\n"
     "        var slotTxt = player.weapons[0] ? WEAPONS[player.weapons[0]].name : '\u7a7a';\n"
     "        var slotTxt2 = player.weapons[1] ? WEAPONS[player.weapons[1]].name : '\u7a7a';\n"
     "        document.getElementById('bullets').textContent = WEAPONS[cw].name + ' ' + player.bullets + '  [1.' + slotTxt + ' | 2.' + slotTxt2 + ']';\n"),
    'hud-slots')

# 8) 重置：两把枪
rep("        player.x = 200; player.y = 200; player.hp = 100; player.bullets = 30; player.weapon = 'pistol';\n",
    "        player.x = 200; player.y = 200; player.hp = 100; player.bullets = 30; player.weapons = ['pistol', null]; player.weaponSlot = 0;\n",
    'reset-slots')

# 9) 画枪用当前枪
rep("        var glen = player.weapon === 'sniper' ? 30 : (player.weapon === 'shotgun' ? 24 : 18);\n",
    ("        var cwg = currentWeapon();\n"
     "        var glen = cwg === 'sniper' ? 30 : (cwg === 'shotgun' || cwg === 'gatling' ? 26 : (cwg === 'laser' ? 22 : 18));\n"),
    'draw-gun-current')

# 10) 画"按E拾取"提示
rep("""        // \u26A1 \u5b50\u5f39 / \U0001F52B \u67aa\u68f0\u6389\u843d
""",
    """        // \u270B \u9644\u8fd1\u6709\u67aa\uff1a\u63d0\u793a\u6309 E \u62fe\u53d6
        var nearW = -1;
        for (var i = 0; i < drops.length; i++) {
            if (drops[i].kind === 'weapon') {
                var dd = Math.sqrt((drops[i].x - player.x) * (drops[i].x - player.x) + (drops[i].y - player.y) * (drops[i].y - player.y));
                if (dd < 70) { nearW = i; break; }
            }
        }
        if (nearW >= 0) {
            ctx.fillStyle = '#ffd93d';
            ctx.font = 'bold 15px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('\u270B \u6309 E \u62fe\u53d6 \U0001F52B ' + WEAPONS[drops[nearW].w].name, player.x, player.y - 42);
        }

        // \u26A1 \u5b50\u5f39 / \U0001F52B \u67aa\u68f0\u6389\u843d
""",
    'e-prompt')

# 11) 玩法说明
rep("""        <li>\U0001F47E \u51fb\u6740\u654c\u4eba\u6389\u843d \u26A1<b>\u5b50\u5f39</b>\uff0c\u8fd8\u53ef\u80fd\u7206 \U0001F52B<b>\u67aa\u68f0</b>\uff01</li>
        <li>\U0001F4E6 \u5f00\u7bb1\u4e5f\u53ef\u80fd\u7206\u51fa<b>\u67aa\u68f0</b>\uff1a\u6b65\u67aa\uff08\u5feb\uff09/\u971c\u5f39\u67aa\uff08\u6563\u5f39\uff09/\u72d9\u51fb\u67aa\uff08\u7206\u5934\uff09</li>
""",
    """        <li>\U0001F47E \u51fb\u6740\u654c\u4eba\u6389\u843d \u26A1<b>\u5b50\u5f39</b>\uff0c\u8fd8\u53ef\u80fd\u7206 \U0001F52B<b>\u67aa\u68f0</b>\uff01</li>
        <li>\U0001F4E6 \u5f00\u7bb1\u4e5f\u53ef\u80fd\u7206\u51fa<b>\u67aa\u68f0</b>\uff08\u6b65\u67aa/\u971c\u5f39\u67aa/\u72d9\u51fb\u67aa/\u51b2\u950b\u67aa/\u52a0\u7279\u6797/\u6fc0\u5149\u67aa\uff09</li>
        <li>\U0001F52B \u53ef\u643a\u5e26<b>\u4e24\u6279\u67aa</b>\uff0c\u6309 <b>Q</b> \u5207\u6362\uff1b\u5730\u4e0a\u7684\u67aa\u8981\u6309 <b>E</b> \u624b\u52a8\u62fe\u53d6</li>
""",
    'instructions')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
