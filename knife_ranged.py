# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\ai\code\yhl-html\sdc.html'
src = io.open(path, encoding='utf-8').read()
src = src.replace('枪棰', '枪械')   # 修正错别字：枪棰 -> 枪械
n0 = len(src)

def rep(old, new, name, count=1):
    global src
    assert src.count(old) == count, '%s match = %d' % (name, src.count(old))
    src = src.replace(old, new)
    print('OK', name)

# 1) WEAPONS：加 emoji + 刀（近战秒杀）
rep("""    var WEAPONS = {
        pistol:  { name: '\u624b\u67aa',   dmg: 34, rate: 0.28, speed: 720,  pellets: 1, spread: 0 },
        rifle:   { name: '\u6b65\u67aa',   dmg: 24, rate: 0.12, speed: 820,  pellets: 1, spread: 0.03 },
        shotgun: { name: '\u971c\u5f39\u67aa', dmg: 15, rate: 0.65, speed: 640,  pellets: 6, spread: 0.30 },
        sniper:  { name: '\u72d9\u51fb\u67aa', dmg: 95, rate: 0.85, speed: 1150, pellets: 1, spread: 0 },
        smg:     { name: '\u51b2\u950b\u67aa', dmg: 18, rate: 0.07, speed: 780,  pellets: 1, spread: 0.07 },
        gatling: { name: '\u52a0\u7279\u6797', dmg: 12, rate: 0.045, speed: 760, pellets: 1, spread: 0.13 },
        laser:   { name: '\u6fc0\u5149\u67aa', dmg: 42, rate: 0.16, speed: 1050, pellets: 1, spread: 0 }
    };
    function randomWeapon() {
        var ks = ['rifle', 'shotgun', 'sniper', 'smg', 'gatling', 'laser'];
        return ks[Math.floor(Math.random() * ks.length)];
    }
    function dropWeaponPickup(x, y) {
        drops.push({ x: x, y: y, kind: 'weapon', w: randomWeapon() });
    }
""",
    """    var WEAPONS = {
        pistol:  { name: '\u624b\u67aa',   emoji: '\U0001F52B', dmg: 34, rate: 0.28, speed: 720,  pellets: 1, spread: 0 },
        rifle:   { name: '\u6b65\u67aa',   emoji: '\U0001F52B', dmg: 24, rate: 0.12, speed: 820,  pellets: 1, spread: 0.03 },
        shotgun: { name: '\u971c\u5f39\u67aa', emoji: '\U0001F4A5', dmg: 15, rate: 0.65, speed: 640,  pellets: 6, spread: 0.30 },
        sniper:  { name: '\u72d9\u51fb\u67aa', emoji: '\U0001F3AF', dmg: 95, rate: 0.85, speed: 1150, pellets: 1, spread: 0 },
        smg:     { name: '\u51b2\u950b\u67aa', emoji: '\U0001F680', dmg: 18, rate: 0.07, speed: 780,  pellets: 1, spread: 0.07 },
        gatling: { name: '\u52a0\u7279\u6797', emoji: '\u2699\ufe0f', dmg: 12, rate: 0.045, speed: 760, pellets: 1, spread: 0.13 },
        laser:   { name: '\u6fc0\u5149\u67aa', emoji: '\u2728', dmg: 42, rate: 0.16, speed: 1050, pellets: 1, spread: 0 },
        knife:   { name: '\u5200',       emoji: '\U0001F52A', dmg: 999, rate: 0.4, melee: true }
    };
    function randomWeapon() {
        var ks = ['rifle', 'shotgun', 'sniper', 'smg', 'gatling', 'laser', 'knife'];
        return ks[Math.floor(Math.random() * ks.length)];
    }
    function dropWeaponPickup(x, y) {
        drops.push({ x: x, y: y, kind: 'weapon', w: randomWeapon() });
    }
    // \U0001F47E \u51fb\u6740\u654c\u4eba\uff08\u6389\u5b50\u5f39 + \u53ef\u80fd\u7206\u67aa\uff09
    function killEnemy(idx) {
        var e = enemies[idx];
        drops.push({ x: e.x, y: e.y });
        var dropGun = Math.random() < 0.25;
        if (dropGun) dropWeaponPickup(e.x + 14, e.y + 14);
        score += 20; kills++;
        showMsg(dropGun ? '\U0001F47E \u51fb\u6740\uff01\u6389\u843d \u26A1 \u5b50\u5f39 \u548c \U0001F52B \u67aa\u68f0\uff01' : '\U0001F47E \u51fb\u6740\uff01+20\u5206\uff0c\u6389\u843d \u26A1 \u5b50\u5f39');
        enemies.splice(idx, 1);
    }
""",
    'weapons-knife')

# 2) enemyShots 数组
rep("    var crates = [], enemies = [], bullets = [], drops = [], fx = [];\n",
    "    var crates = [], enemies = [], bullets = [], drops = [], fx = [], enemyShots = [];\n",
    'enemy-shots-var')

# 3) spawnEnemies：12个、混合、出生点不刷怪
rep("""    function spawnEnemies() {
        for (var i = 0; i < 6; i++) {
            var x, y, tries = 0;
            do { x = 300 + Math.random() * (MAPW - 600); y = 300 + Math.random() * (MAPH - 600); tries++; }
            while (rectHit(x, y, 18) && tries < 60);
            enemies.push({ x: x, y: y, hp: 100, wander: Math.random() * 6.28 });
        }
    }
""",
    """    function spawnEnemies() {
        // 12个敌人：6个近战冲脸（\U0001F47E）+ 6个远程射击（\U0001F916）！出生点附近不刷怪！
        for (var i = 0; i < 12; i++) {
            var x, y, tries = 0;
            do {
                x = 120 + Math.random() * (MAPW - 240);
                y = 120 + Math.random() * (MAPH - 240);
                tries++;
            } while ((rectHit(x, y, 18) || Math.sqrt((x - 200) * (x - 200) + (y - 200) * (y - 200)) < 380) && tries < 80);
            enemies.push({ x: x, y: y, hp: 100, wander: Math.random() * 6.28, ranged: i >= 6, shotCd: 1.5 + Math.random() });
        }
    }
""",
    'spawn-enemies')

# 4) resetGame：清 enemyShots、HUD 12
rep("        crates = []; enemies = []; bullets = []; drops = []; fx = [];\n",
    "        crates = []; enemies = []; bullets = []; drops = []; fx = []; enemyShots = [];\n",
    'reset-shots')
rep("        document.getElementById('ene').textContent = '6';\n",
    "        document.getElementById('ene').textContent = '12';\n",
    'hud-ene-12')

# 5) 按键 1/2 切枪
rep("""        if (k === 'q' || k === 'tab') switchWeapon();
        if (k === 'e' || k === 'f') tryPickup();
""",
    """        if (k === 'q' || k === 'tab') switchWeapon();
        if (k === '1' && player.weapons[0]) { player.weaponSlot = 0; showMsg('\U0001F52B \u5207\u5230' + WEAPONS[player.weapons[0]].name); }
        if (k === '2' && player.weapons[1]) { player.weaponSlot = 1; showMsg('\U0001F52B \u5207\u5230' + WEAPONS[player.weapons[1]].name); }
        if (k === 'e' || k === 'f') tryPickup();
""",
    'keys-12')

# 6) 射击：刀 = 近战秒杀
rep("""        // \U0001F52B \u5c04\u51fb\uff08\u9f20\u6807\u5de6\u952e / \u7a7a\u683c / J\uff09\u2014\u2014\u6309\u5f53\u524d\u67aa\u68f0\u53c2\u6570\u53d1\u5c04\uff01
        var wg = WEAPONS[currentWeapon()];
        if ((keys[' '] || keys['j'] || mouseDown) && player.atkCd <= 0) {
            if (player.bullets > 0) {
""",
    """        // \U0001F52B \u5c04\u51fb\uff08\u9f20\u6807\u5de6\u952e / \u7a7a\u683c / J\uff09\u2014\u2014\u6309\u5f53\u524d\u67aa\u68f0\u53c2\u6570\u53d1\u5c04\uff01
        var wg = WEAPONS[currentWeapon()];
        if ((keys[' '] || keys['j'] || mouseDown) && player.atkCd <= 0) {
            if (wg.melee) {
                // \U0001F52A \u5200\uff1a\u8fd1\u6218\u6325\u780d\uff0c\u9762\u524d\u654c\u4eba\u4e00\u5200\u79d2\u6740\uff01\uff08\u4e0d\u8017\u5b50\u5f39\uff09
                player.atkCd = wg.rate;
                fx.push({ x: player.x + Math.cos(player.dir) * 45, y: player.y + Math.sin(player.dir) * 45, t: 0, slash: player.dir });
                for (var mi = enemies.length - 1; mi >= 0; mi--) {
                    var me = enemies[mi];
                    var md2 = Math.sqrt((me.x - player.x) * (me.x - player.x) + (me.y - player.y) * (me.y - player.y));
                    var angTo = Math.atan2(me.y - player.y, me.x - player.x);
                    var diff = Math.abs(angTo - player.dir);
                    if (diff > Math.PI) diff = Math.PI * 2 - diff;
                    if (md2 < 95 && diff < 1.0) killEnemy(mi);   // \U0001F52A \u4e00\u5200\u79d2\uff01
                }
            } else if (player.bullets > 0) {
""",
    'knife-attack')

# 7) 子弹命中：用 killEnemy
rep("""                if (e.hp <= 0) {
                    // \u51fb\u6740\uff1a\u6389\u5b50\u5f39 + \u53ef\u80fd\u7206\u67aa\uff01
                    drops.push({ x: e.x, y: e.y });
                    var dropGun = Math.random() < 0.25;
                    if (dropGun) dropWeaponPickup(e.x + 14, e.y + 14);
                    score += 20; kills++;
                    showMsg(dropGun ? '\U0001F47E \u51fb\u6740\uff01\u6389\u843d \u26A1 \u5b50\u5f39 \u548c \U0001F52B \u67aa\u68f0\uff01' : '\U0001F47E \u51fb\u6740\uff01+20\u5206\uff0c\u6389\u843d \u26A1 \u5b50\u5f39');
                    enemies.splice(hitEnemy, 1);
                }
""",
    """                if (e.hp <= 0) {
                    killEnemy(hitEnemy);
                }
""",
    'bullet-kill')

# 8) 敌人：近战 + 远程
rep("""        // \U0001F47E \u654c\u4eba
        for (var i = 0; i < enemies.length; i++) {
            var e = enemies[i];
            var d = Math.sqrt((e.x - player.x) * (e.x - player.x) + (e.y - player.y) * (e.y - player.y));
            var es = 130 * dt;
            if (d < 260 && d > 0.01) {
                e.x += (player.x - e.x) / d * es;
                e.y += (player.y - e.y) / d * es;
            } else {
                e.wander += dt;
                e.x += Math.cos(e.wander) * es * 0.5;
                e.y += Math.sin(e.wander) * es * 0.5;
            }
            e.x = Math.max(20, Math.min(MAPW - 20, e.x));
            e.y = Math.max(20, Math.min(MAPH - 20, e.y));
            if (d < 36 && player.hitCd <= 0) {
                player.hp -= 12;
                player.hitCd = 0.8;
                showMsg('\u88ab\u6253\u4e86\u4e00\u4e0b \U0001F494');
                document.getElementById('hpbar').style.width = Math.max(0, player.hp) + '%';
                document.getElementById('hpnum').textContent = Math.max(0, player.hp);
                if (player.hp <= 0) { player.hp = 0; state = 'lose'; }
            }
        }
""",
    """        // \U0001F47E \u654c\u4eba\uff08\u8fd1\u6218\u51b2\u8138 / \u8fdc\u7a0b\u5c04\u51fb\uff09
        for (var i = 0; i < enemies.length; i++) {
            var e = enemies[i];
            var d = Math.sqrt((e.x - player.x) * (e.x - player.x) + (e.y - player.y) * (e.y - player.y));
            var es = (e.ranged ? 100 : 130) * dt;
            if (e.ranged) {
                // \U0001F916 \u8fdc\u7a0b\u654c\u4eba\uff1a\u4fdd\u6301\u8ddd\u79bb\u3001\u8fb9\u8d70\u8fb9\u5f00\u706b\uff01
                if (d < 240 && d > 0.01) {
                    e.x -= (player.x - e.x) / d * es;
                    e.y -= (player.y - e.y) / d * es;
                } else if (d > 340) {
                    e.x += (player.x - e.x) / d * es;
                    e.y += (player.y - e.y) / d * es;
                } else {
                    e.wander += dt;
                    e.x += Math.cos(e.wander) * es * 0.4;
                    e.y += Math.sin(e.wander) * es * 0.4;
                }
                if (d < 480 && e.shotCd <= 0) {
                    e.shotCd = 1.6 + Math.random() * 0.6;
                    var ea = Math.atan2(player.y - e.y, player.x - e.x);
                    enemyShots.push({ x: e.x, y: e.y, vx: Math.cos(ea) * 260, vy: Math.sin(ea) * 260, life: 2.4 });
                }
                if (e.shotCd > 0) e.shotCd -= dt;
            } else {
                // \U0001F47E \u8fd1\u6218\u654c\u4eba\uff1a\u51b2\u8138\uff01
                if (d < 280 && d > 0.01) {
                    e.x += (player.x - e.x) / d * es;
                    e.y += (player.y - e.y) / d * es;
                } else {
                    e.wander += dt;
                    e.x += Math.cos(e.wander) * es * 0.5;
                    e.y += Math.sin(e.wander) * es * 0.5;
                }
            }
            e.x = Math.max(20, Math.min(MAPW - 20, e.x));
            e.y = Math.max(20, Math.min(MAPH - 20, e.y));
            if (d < 36 && player.hitCd <= 0) {
                player.hp -= 12;
                player.hitCd = 0.8;
                showMsg('\u88ab\u6253\u4e86\u4e00\u4e0b \U0001F494');
                document.getElementById('hpbar').style.width = Math.max(0, player.hp) + '%';
                document.getElementById('hpnum').textContent = Math.max(0, player.hp);
                if (player.hp <= 0) { player.hp = 0; state = 'lose'; }
            }
        }

        // \U0001F9E8 \u654c\u4eba\u7684\u5b50\u5f39\uff01
        for (var i = enemyShots.length - 1; i >= 0; i--) {
            var sh = enemyShots[i];
            sh.x += sh.vx * dt; sh.y += sh.vy * dt;
            sh.life -= dt;
            if (sh.life <= 0 || rectHit(sh.x, sh.y, 4)) { enemyShots.splice(i, 1); continue; }
            var d2 = Math.sqrt((sh.x - player.x) * (sh.x - player.x) + (sh.y - player.y) * (sh.y - player.y));
            if (d2 < 22 && player.hitCd <= 0) {
                player.hp -= 9;
                player.hitCd = 0.6;
                enemyShots.splice(i, 1);
                showMsg('\u88ab\u8fdc\u7a0b\u6253\u4e2d \U0001F4A5');
                document.getElementById('hpbar').style.width = Math.max(0, player.hp) + '%';
                document.getElementById('hpnum').textContent = Math.max(0, player.hp);
                if (player.hp <= 0) { player.hp = 0; state = 'lose'; }
            }
        }
""",
    'enemies-ranged')

# 9) HUD：刀显示 ∞ 子弹
rep("        document.getElementById('bullets').textContent = WEAPONS[cw].name + ' ' + player.bullets + '  [1.' + slotTxt + ' | 2.' + slotTxt2 + ']';\n",
    "        document.getElementById('bullets').textContent = WEAPONS[cw].name + ' ' + (WEAPONS[cw].melee ? '\u221E' : player.bullets) + '  [1.' + slotTxt + ' | 2.' + slotTxt2 + ']';\n",
    'hud-knife')

# 10) 画敌人：近战/远程不同
rep("""        // \U0001F47E \u654c\u4eba
        ctx.font = '28px sans-serif';
        for (var i = 0; i < enemies.length; i++) {
            var e = enemies[i];
            ctx.fillText('\U0001F47E', e.x, e.y + 9);
""",
    """        // \U0001F47E \u654c\u4eba\uff08\u8fd1\u6218\U0001F47E / \u8fdc\u7a0b\U0001F916\uff09
        ctx.font = '28px sans-serif';
        for (var i = 0; i < enemies.length; i++) {
            var e = enemies[i];
            ctx.fillText(e.ranged ? '\U0001F916' : '\U0001F47E', e.x, e.y + 9);
""",
    'draw-enemies')

# 11) 画敌人的子弹 + 玩家持刀
rep("""        // \U0001F52B \u5b50\u5f39
        ctx.fillStyle = '#ffd93d';
        for (var i = 0; i < bullets.length; i++) {
            ctx.beginPath();
            ctx.arc(bullets[i].x, bullets[i].y, 4, 0, Math.PI * 2);
            ctx.fill();
        }
""",
    """        // \U0001F52B \u5b50\u5f39
        ctx.fillStyle = '#ffd93d';
        for (var i = 0; i < bullets.length; i++) {
            ctx.beginPath();
            ctx.arc(bullets[i].x, bullets[i].y, 4, 0, Math.PI * 2);
            ctx.fill();
        }

        // \U0001F9E8 \u654c\u4eba\u7684\u5b50\u5f39
        ctx.fillStyle = '#ff5d7a';
        for (var i = 0; i < enemyShots.length; i++) {
            ctx.beginPath();
            ctx.arc(enemyShots[i].x, enemyShots[i].y, 5, 0, Math.PI * 2);
            ctx.fill();
        }
""",
    'draw-enemy-shots')

# 12) 玩家：刀 vs 枪
rep("""        // \u67aa\uff08\u4e0d\u540c\u67aa\u68f0\u67aa\u7ba1\u4e0d\u4e00\u6837\u957f\uff01\uff09
        var cwg = currentWeapon();
        var glen = cwg === 'sniper' ? 30 : (cwg === 'shotgun' || cwg === 'gatling' ? 26 : (cwg === 'laser' ? 22 : 18));
        ctx.fillStyle = '#3a3f4a';
        ctx.fillRect(14, -3, glen, 6);
        ctx.fillStyle = '#ff8e3c';
        ctx.fillRect(14 + glen, -5, 6, 10);
""",
    """        // \U0001F52A \u5200 \u6216 \u67aa\uff08\u67aa\u7ba1\u957f\u5ea6\u6309\u67aa\u68f0\uff09
        var cwg = currentWeapon();
        if (cwg === 'knife') {
            ctx.fillStyle = '#e8e8e8';
            ctx.fillRect(16, -2, 22, 4);
            ctx.fillStyle = '#8a5a2b';
            ctx.fillRect(14, -4, 4, 8);
        } else {
            var glen = cwg === 'sniper' ? 30 : (cwg === 'shotgun' || cwg === 'gatling' ? 26 : (cwg === 'laser' ? 22 : 18));
            ctx.fillStyle = '#3a3f4a';
            ctx.fillRect(14, -3, glen, 6);
            ctx.fillStyle = '#ff8e3c';
            ctx.fillRect(14 + glen, -5, 6, 10);
        }
""",
    'draw-knife')

# 13) 刀劈特效（fx slash）
rep("""            } else {
                ctx.beginPath();
                ctx.arc(f.x, f.y, f.r + f.t * 26, 0, Math.PI * 2);
                ctx.strokeStyle = 'rgba(255,200,80,' + (1 - f.t) + ')';
                ctx.lineWidth = 3;
                ctx.stroke();
            }
""",
    """            } else if (f.slash !== undefined) {
                // \U0001F52A \u5200\u6325\u780d\u5f27\u5f62
                ctx.beginPath();
                ctx.arc(f.x, f.y, 50, f.slash - 0.85, f.slash + 0.85);
                ctx.strokeStyle = 'rgba(255,255,255,' + (1 - f.t) + ')';
                ctx.lineWidth = 6;
                ctx.stroke();
            } else {
                ctx.beginPath();
                ctx.arc(f.x, f.y, f.r + f.t * 26, 0, Math.PI * 2);
                ctx.strokeStyle = 'rgba(255,200,80,' + (1 - f.t) + ')';
                ctx.lineWidth = 3;
                ctx.stroke();
            }
""",
    'slash-fx')

# 14) 掉落/提示用武器自己的 emoji
rep("            ctx.fillText('\u270B \u6309 E \u62fe\u53d6 \U0001F52B ' + WEAPONS[drops[nearW].w].name, player.x, player.y - 42);\n",
    "            ctx.fillText('\u270B \u6309 E \u62fe\u53d6 ' + (WEAPONS[drops[nearW].w].emoji || '\U0001F52B') + ' ' + WEAPONS[drops[nearW].w].name, player.x, player.y - 42);\n",
    'e-prompt-emoji')
rep("""            if (dp.kind === 'weapon') {
                ctx.fillText('\U0001F52B', dp.x, dp.y + 8);
""",
    """            if (dp.kind === 'weapon') {
                ctx.fillText(WEAPONS[dp.w].emoji || '\U0001F52B', dp.x, dp.y + 8);
""",
    'drop-emoji')

# 15) 玩法说明
rep("""        <li>\U0001F52B \u53ef\u643a\u5e26<b>\u4e24\u6279\u67aa</b>\uff0c\u6309 <b>Q</b> \u5207\u6362\uff1b\u5730\u4e0a\u7684\u67aa\u8981\u6309 <b>E</b> \u624b\u52a8\u62fe\u53d6</li>
""",
    """        <li>\U0001F52B \u53ef\u643a\u5e26<b>\u4e24\u6279\u67aa</b>\uff0c\u6309 <b>1/2</b> \u6216 <b>Q</b> \u5207\u6362\uff1b\u5730\u4e0a\u7684\u67aa\u8981\u6309 <b>E</b> \u624b\u52a8\u62fe\u53d6</li>
        <li>\U0001F52A \u62fe\u5230<b>\u5200</b>\uff1a\u8fd1\u6218\u6325\u780d\uff0c\u4e00\u5200\u79d2\u6740\u9762\u524d\u654c\u4eba\uff01\uff08\u4e0d\u8017\u5b50\u5f39\uff09</li>
        <li>\U0001F916 \u6709<b>\u8fdc\u7a0b\u654c\u4eba</b>\u4f1a\u8fb9\u8d70\u8fb9\u5f00\u706b\uff0c\u6ce8\u610f\u8eb2\u907f\u5b50\u5f39\uff01</li>
""",
    'instructions')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
