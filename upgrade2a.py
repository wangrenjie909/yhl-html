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

# 1) 部分房子有2楼（60%）
rep("""        wallRects = [];
        for (var i = 0; i < buildings.length; i++) {
            var b = buildings[i];
""",
    """        wallRects = [];
        for (var i = 0; i < buildings.length; i++) {
            var b = buildings[i];
            b.has2 = Math.random() < 0.6;   // \U0001F3E2 \u90E8\u5206\u623F\u5B50\u624D\u67092\u697C\uff01
""",
    'has2')

# 2) 塔 + BOSS 变量
rep("    var crates = [], enemies = [], bullets = [], drops = [], fx = [], enemyShots = [];\n",
    "    var crates = [], enemies = [], bullets = [], drops = [], fx = [], enemyShots = [];\n    var towers = [];          // \u9AD8\u578B\u573A\u6C99\u9505\u5854\uff08\u76F4\u63A5\u4E0A3\u697C\uff09\n    var boss = null;          // \U0001F479 BOSS\uff01\n",
    'tower-boss-vars')

# 3) player 加 tIdx
rep("    var player = { x: 200, y: 200, hp: 100, dir: 0, atkCd: 0, hitCd: 0, bullets: 30, weapons: ['pistol', null], weaponSlot: 0, floor: 1, bIdx: -1 };\n",
    "    var player = { x: 200, y: 200, hp: 100, dir: 0, atkCd: 0, hitCd: 0, bullets: 30, weapons: ['pistol', null], weaponSlot: 0, floor: 1, bIdx: -1, tIdx: -1 };\n",
    'player-tidx')

# 4) resetGame：重置楼层/塔/BOSS
rep("""        player.x = 200; player.y = 200;
        player.floor = 1; player.bIdx = -1; floorCd = 0;
""",
    """        player.x = 200; player.y = 200;
        player.floor = 1; player.bIdx = -1; player.tIdx = -1; floorCd = 0;
        boss = null;
""",
    'reset-floor2')
rep("""        setupMap();
        mapOpen = false;
        crates = []; enemies = []; bullets = []; drops = []; fx = []; enemyShots = [];
        spawnCrates(); spawnEnemies();
""",
    """        setupMap();
        mapOpen = false;
        crates = []; enemies = []; bullets = []; drops = []; fx = []; enemyShots = [];
        // \u9AD8\u578B\u573A\u6C99\u9505\u5854\uff1a\u6BCF\u5C40\u968F\u673A\u4F4D\u7F6E\uff01
        towers = [];
        for (var ti = 0; ti < 5; ti++) {
            var twx, twy, tries = 0;
            do { twx = 150 + Math.random() * (MAPW - 300); twy = 150 + Math.random() * (MAPH - 300); tries++; }
            while (rectHit(twx, twy, 70) && tries < 70);
            towers.push({ x: twx, y: twy, w: 130, h: 130 });
        }
        spawnCrates(); spawnEnemies();
""",
    'reset-towers')

# 5) spawnEnemies：敌人楼层 + BOSS 出生
rep("""            enemies.push({ x: x, y: y, hp: 100, wander: Math.random() * 6.28, ranged: false, shotCd: 1.5 + Math.random() });
            // \U0001F916 \u8fdc\u7a0b\uff1a\u5c31\u5728\u8fd1\u6218\u65c1\u8fb9\uff08200~320px\uff09\uff0c\u4e24\u79cd\u59cb\u7ec8\u5728\u4e00\u8d77\uff01
            var ang = Math.random() * 6.28;
            var dist = 200 + Math.random() * 120;
            var x2 = Math.max(20, Math.min(MAPW - 20, x + Math.cos(ang) * dist));
            var y2 = Math.max(20, Math.min(MAPH - 20, y + Math.sin(ang) * dist));
            enemies.push({ x: x2, y: y2, hp: 100, wander: Math.random() * 6.28, ranged: true, shotCd: 1.5 + Math.random() });
        }
""",
    """            enemies.push({ x: x, y: y, hp: 100, wander: Math.random() * 6.28, ranged: false, shotCd: 1.5 + Math.random(), floor: 1, bIdx: -1 });
            // \U0001F916 \u8fdc\u7a0b\uff1a\u5c31\u5728\u8fd1\u6218\u65c1\u8fb9\uff08200~320px\uff09\uff0c\u4e24\u79cd\u59cb\u7ec8\u5728\u4e00\u8d77\uff01
            var ang = Math.random() * 6.28;
            var dist = 200 + Math.random() * 120;
            var x2 = Math.max(20, Math.min(MAPW - 20, x + Math.cos(ang) * dist));
            var y2 = Math.max(20, Math.min(MAPH - 20, y + Math.sin(ang) * dist));
            enemies.push({ x: x2, y: y2, hp: 100, wander: Math.random() * 6.28, ranged: true, shotCd: 1.5 + Math.random(), floor: 1, bIdx: -1 });
        }
        // \U0001F479 BOSS \u51fa\u751f\uff08\u79bb\u73a9\u5bb6\u8fdc\u70b9\uff09
        var bx2, by2, tries2 = 0;
        do {
            bx2 = 400 + Math.random() * (MAPW - 800);
            by2 = 400 + Math.random() * (MAPH - 800);
            tries2++;
        } while (rectHit(bx2, by2, 30) && tries2 < 80);
        boss = { x: bx2, y: by2, hp: 500, maxHp: 500, shotCd: 2.0, wander: 0 };
""",
    'spawn-boss')

# 6) 移动：3楼在塔顶范围内
rep("""        if (player.floor === 2 && player.bIdx >= 0) {
            // \U0001F3E2 2\u697c\uff1a\u53ea\u80fd\u5728\u697c\u9876\u8303\u56f4\u5185\u8d70\u52a8\uff08\u4e0d\u78b0\u5899\uff09
            var bb = buildings[player.bIdx];
            player.x = Math.max(bb.x + T + 4, Math.min(bb.x + bb.w - T - 4, nx));
            player.y = Math.max(bb.y + T + 4, Math.min(bb.y + bb.h - T - 4, ny));
        } else {
""",
    """        if (player.floor === 2 && player.bIdx >= 0) {
            // \U0001F3E2 2\u697c\uff1a\u53ea\u80fd\u5728\u697c\u9876\u8303\u56f4\u5185\u8d70\u52a8\uff08\u4e0d\u78b0\u5899\uff09
            var bb = buildings[player.bIdx];
            player.x = Math.max(bb.x + T + 4, Math.min(bb.x + bb.w - T - 4, nx));
            player.y = Math.max(bb.y + T + 4, Math.min(bb.y + bb.h - T - 4, ny));
        } else if (player.floor === 3 && player.tIdx >= 0) {
            // \U0001F3DC\ufe0f \u9505\u5854\u9876\uff1a\u53ea\u80fd\u5728\u5854\u9876\u8303\u56f4\u5185\u8d70
            var tw = towers[player.tIdx];
            player.x = Math.max(tw.x + 8, Math.min(tw.x + tw.w - 8, nx));
            player.y = Math.max(tw.y + 8, Math.min(tw.y + tw.h - 8, ny));
        } else {
""",
    'move-floor3')

# 7) 楼梯：部分房子2楼 + 哨塔3楼
rep("""        // \U0001FA9C \u697c\u68af\uff1a\u8e29\u4e0a\u53bb\u81ea\u52a8\u4e0a\u4e0b\u697c\uff01
        if (floorCd > 0) floorCd -= dt;
        if (floorCd <= 0) {
            if (player.floor === 1) {
                for (var si = 0; si < buildings.length; si++) {
                    var sb = buildings[si];
                    var stx = sb.x + T + 24, sty = sb.y + T + 24;
                    if (Math.abs(player.x - stx) < 26 && Math.abs(player.y - sty) < 26) {
                        player.floor = 2; player.bIdx = si;
                        player.x = sb.x + sb.w / 2; player.y = sb.y + T + 30;
                        floorCd = 0.8;
                        showMsg('\u2B06\ufe0f \u4e0a\u5230 2 \u697c\uff01');
                        break;
                    }
                }
            } else if (player.bIdx >= 0) {
                var cb = buildings[player.bIdx];
                var stx2 = cb.x + T + 24, sty2 = cb.y + T + 24;
                if (Math.abs(player.x - stx2) < 26 && Math.abs(player.y - sty2) < 26) {
                    player.floor = 1; player.bIdx = -1;
                    player.x = stx2; player.y = sty2;
                    floorCd = 0.8;
                    showMsg('\u2B07\ufe0f \u4e0b\u5230 1 \u697c\uff01');
                }
            }
        }
""",
    """        // \U0001FA9C \u697c\u68af\uff1a\u90e8\u5206\u623f\u5b50\u4e0a2\u697c\uff0c\u9505\u5854\u76f4\u63a5\u4e0a3\u697c\uff01
        if (floorCd > 0) floorCd -= dt;
        if (floorCd <= 0) {
            if (player.floor === 1) {
                // \U0001F3E2 \u623f\u5b50\u53ea\u6709\u6709\u697c\u68af\u7684\u624d\u80fd\u4e0a2\u697c\uff01
                for (var si = 0; si < buildings.length; si++) {
                    var sb = buildings[si];
                    if (!sb.has2) continue;
                    var stx = sb.x + T + 24, sty = sb.y + T + 24;
                    if (Math.abs(player.x - stx) < 26 && Math.abs(player.y - sty) < 26) {
                        player.floor = 2; player.bIdx = si; player.tIdx = -1;
                        player.x = sb.x + sb.w / 2; player.y = sb.y + T + 30;
                        floorCd = 0.8;
                        showMsg('\u2B06\ufe0f \u4e0a\u5230 2 \u697c\uff01');
                        break;
                    }
                }
                // \U0001F3DC\ufe0f \u9505\u5854\uff1a\u8e29\u68af\u5b50\u4e00\u4e0b\u5b50\u76f4\u63a5\u4e0a3\u697c\uff01
                for (var ti = 0; ti < towers.length; ti++) {
                    var tw = towers[ti];
                    var tlx = tw.x + tw.w / 2, tly = tw.y + tw.h + 24;
                    if (Math.abs(player.x - tlx) < 30 && Math.abs(player.y - tly) < 30) {
                        player.floor = 3; player.tIdx = ti; player.bIdx = -1;
                        player.x = tw.x + tw.w / 2; player.y = tw.y + 20;
                        floorCd = 0.8;
                        showMsg('\u26F0\ufe0f \u76f4\u63a5\u4e0a\u5230\u9505\u5854 3 \u697c\uff01');
                        break;
                    }
                }
            } else if (player.floor === 2 && player.bIdx >= 0) {
                var cb = buildings[player.bIdx];
                var stx2 = cb.x + T + 24, sty2 = cb.y + T + 24;
                if (Math.abs(player.x - stx2) < 26 && Math.abs(player.y - sty2) < 26) {
                    player.floor = 1; player.bIdx = -1;
                    player.x = stx2; player.y = sty2;
                    floorCd = 0.8;
                    showMsg('\u2B07\ufe0f \u4e0b\u5230 1 \u697c\uff01');
                }
            } else if (player.floor === 3 && player.tIdx >= 0) {
                var ctw = towers[player.tIdx];
                var tlx2 = ctw.x + ctw.w / 2, tly2 = ctw.y + 10;
                if (Math.abs(player.x - tlx2) < 30 && Math.abs(player.y - tly2) < 30) {
                    player.floor = 1; player.tIdx = -1;
                    player.x = ctw.x + ctw.w / 2; player.y = ctw.y + ctw.h + 24;
                    floorCd = 0.8;
                    showMsg('\u2B07\ufe0f \u4e0b\u5854\uff01');
                }
            }
        }
""",
    'stairs-v2')

# 8) bulletWallHit：3楼无视所有墙（能打到2楼和地面）
rep("""    function bulletWallHit(x, y) {
        if (player.floor === 2 && player.bIdx >= 0) {
""",
    """    function bulletWallHit(x, y) {
        if (player.floor === 3) return false;   // \u26F0\ufe0f \u9505\u5854\u9876\u9ad8\u5904\uff1a\u80fd\u6253\u5230 2 \u697c\u548c\u5730\u9762\uff01
        if (player.floor === 2 && player.bIdx >= 0) {
""",
    'bulletwall-floor3')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('PART 1 done')
