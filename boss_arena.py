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

# 1) arena 变量
rep("    var towers = [];          // \u9AD8\u578B\u573A\u6C99\u9505\u5854\uff08\u76F4\u63A5\u4E0A3\u697C\uff09\n    var boss = null;          // \U0001F479 BOSS\uff01\n",
    "    var towers = [];          // \u9AD8\u578B\u573A\u6C99\u9505\u5854\uff08\u76F4\u63A5\u4E0A3\u697C\uff09\n    var boss = null;          // \U0001F479 BOSS\uff01\n    var arena = null;         // \U0001F479 BOSS \u4E13\u5C5E\u573A\u5730\uff08\u5706\u5F62\u76D1\u72F1\uff09\n",
    'arena-var')

# 2) resetGame：生成 BOSS 场地
rep("""        towers = [];
        for (var ti = 0; ti < 5; ti++) {
            var twx, twy, tries = 0;
            do { twx = 150 + Math.random() * (MAPW - 300); twy = 150 + Math.random() * (MAPH - 300); tries++; }
            while (rectHit(twx, twy, 70) && tries < 70);
            towers.push({ x: twx, y: twy, w: 130, h: 130 });
        }
""",
    """        towers = [];
        for (var ti = 0; ti < 5; ti++) {
            var twx, twy, tries = 0;
            do { twx = 150 + Math.random() * (MAPW - 300); twy = 150 + Math.random() * (MAPH - 300); tries++; }
            while (rectHit(twx, twy, 70) && tries < 70);
            towers.push({ x: twx, y: twy, w: 130, h: 130 });
        }
        // \U0001F479 BOSS \u4E13\u5C5E\u573A\u5730\uff08\u573A\u5730\u5185\u624D\u80FD\u89E6\u53D1\u5B83\uff09
        var ax, ay, tries3 = 0;
        do {
            ax = 350 + Math.random() * (MAPW - 700);
            ay = 350 + Math.random() * (MAPH - 700);
            tries3++;
        } while ((rectHit(ax, ay, 240) || Math.sqrt((ax - 200) * (ax - 200) + (ay - 200) * (ay - 200)) < 500) && tries3 < 90);
        arena = { x: ax, y: ay, r: 210, gateAng: Math.PI / 2, gateHalf: 0.45 };
""",
    'arena-spawn')

# 3) BOSS 在场地中央出生
rep("""        boss = { x: bx2, y: by2, hp: 500, maxHp: 500, shotCd: 2.0, wander: 0 };
""",
    "        boss = { x: arena.x, y: arena.y, hp: 500, maxHp: 500, shotCd: 2.0, wander: 0 };\n",
    'boss-arena-spawn')

# 4) arenaHit 碰撞函数（放在 rectHit 后面）
rep("""        return rectHit(x, y, 4);
    }

    // \U0001F441 \u89c6\u7ebf\u68c0\u6d4b\uff1a\u4e24\u70b9\u4e4b\u95f4\u6709\u6ca1\u6709\u88ab\u5899\u6321\u4f4f
""",
    """        return rectHit(x, y, 4);
    }

    // \U0001F479 BOSS \u573A\u5730\u5708\u5899\uff1a\u5708\u73af\u5e26\u78b0\u649e\uff08\u95e8\u53e3\u4e0d\u78b0\uff09
    function arenaHit(x, y, rad) {
        if (!arena) return false;
        var dx = x - arena.x, dy = y - arena.y;
        var d = Math.sqrt(dx * dx + dy * dy);
        if (d < arena.r - 16 - rad || d > arena.r + 16 + rad) return false;
        var ang = Math.atan2(dy, dx);
        if (Math.abs(ang - arena.gateAng) < arena.gateHalf) return false;   // \u95e8\u53e3\u901a\u884c
        return true;
    }

    // \U0001F441 \u89c6\u7ebf\u68c0\u6d4b\uff1a\u4e24\u70b9\u4e4b\u95f4\u6709\u6ca1\u6709\u88ab\u5899\u6321\u4f4f
""",
    'arena-hit-func')

# 5) 玩家移动：一楼也撞场地圈墙
rep("""        } else {
            if (!rectHit(nx, player.y, 16)) player.x = nx;
            if (!rectHit(player.x, ny, 16)) player.y = ny;
        }
        player.x = Math.max(20, Math.min(MAPW - 20, player.x));
""",
    """        } else {
            if (!rectHit(nx, player.y, 16) && !arenaHit(nx, player.y, 16)) player.x = nx;
            if (!rectHit(player.x, ny, 16) && !arenaHit(player.x, ny, 16)) player.y = ny;
        }
        player.x = Math.max(20, Math.min(MAPW - 20, player.x));
""",
    'player-arena')

# 6) 玩家子弹：也被场地圈墙挡住（3楼除外已处理）
rep("""        return rectHit(x, y, 4);
    }

    // \U0001F441 \u89c6\u7ebf\u68c0\u6d4b\uff1a\u4e24\u70b9\u4e4b\u95f4\u6709\u6ca1\u6709\u88ab\u5899\u6321\u4f4f
""",
    """        if (arenaHit(x, y, 4)) return true;
        return rectHit(x, y, 4);
    }

    // \U0001F441 \u89c6\u7ebf\u68c0\u6d4b\uff1a\u4e24\u70b9\u4e4b\u95f4\u6709\u6ca1\u6709\u88ab\u5899\u6321\u4f4f
""",
    'bullet-arena')

# 7) 敌人移动：撞场地圈墙 + 碰撞半径变大
rep("""            } else {
                if (!rectHit(e.x + mx, e.y, 14)) e.x += mx;
                if (!rectHit(e.x, e.y + my, 14)) e.y += my;
            }
""",
    """            } else {
                if (!rectHit(e.x + mx, e.y, 18) && !arenaHit(e.x + mx, e.y, 18)) e.x += mx;
                if (!rectHit(e.x, e.y + my, 18) && !arenaHit(e.x, e.y + my, 18)) e.y += my;
            }
""",
    'enemy-move-arena')

# 8) 小怪变大：接触范围 + 子弹命中范围
rep("            if (sameFloor && d < 36 && player.hitCd <= 0) {\n",
    "            if (sameFloor && d < 44 && player.hitCd <= 0) {\n",
    'enemy-contact')
rep("""                var d = Math.sqrt((e.x - b.x) * (e.x - b.x) + (e.y - b.y) * (e.y - b.y));
                if (d < 24) { hitEnemy = j; break; }
""",
    """                var d = Math.sqrt((e.x - b.x) * (e.x - b.x) + (e.y - b.y) * (e.y - b.y));
                if (d < 30) { hitEnemy = j; break; }
""",
    'bullet-hit-enemy')

# 9) 小怪画大一点！
rep("""        // \U0001F47E \u654c\u4eba\uff08\u8fd1\u6218\U0001F47E / \u8fdc\u7a0b\U0001F916\uff09
        ctx.font = '28px sans-serif';
        for (var i = 0; i < enemies.length; i++) {
            var e = enemies[i];
            ctx.fillText(e.ranged ? '\U0001F916' : '\U0001F47E', e.x, e.y + 9);
            ctx.fillStyle = '#333';
            ctx.fillRect(e.x - 20, e.y - 36, 40, 5);
            ctx.fillStyle = '#ff5d5d';
            ctx.fillRect(e.x - 20, e.y - 36, 40 * Math.max(0, e.hp / 100), 5);
            // \U0001F4A0 \u654c\u4eba\u8840\u91cf\u6570\u5b57
            ctx.fillStyle = '#ffd93d';
            ctx.font = 'bold 12px sans-serif';
            ctx.fillText(Math.max(0, e.hp), e.x, e.y - 42);
        }
""",
    """        // \U0001F47E \u654c\u4eba\uff08\u8fd1\u6218\U0001F47E / \u8fdc\u7a0b\U0001F916\uff09\u2014\u2014\u53d8\u5927\u4e86\uff01
        ctx.font = '42px sans-serif';
        for (var i = 0; i < enemies.length; i++) {
            var e = enemies[i];
            ctx.fillText(e.ranged ? '\U0001F916' : '\U0001F47E', e.x, e.y + 12);
            ctx.fillStyle = '#333';
            ctx.fillRect(e.x - 26, e.y - 48, 52, 6);
            ctx.fillStyle = '#ff5d5d';
            ctx.fillRect(e.x - 26, e.y - 48, 52 * Math.max(0, e.hp / 100), 6);
            // \U0001F4A0 \u654c\u4eba\u8840\u91cf\u6570\u5b57
            ctx.fillStyle = '#ffd93d';
            ctx.font = 'bold 14px sans-serif';
            ctx.fillText(Math.max(0, e.hp), e.x, e.y - 56);
        }
""",
    'enemy-big')

# 10) BOSS 画大 + 命中范围 + 场地圈住
rep("""            if (bd < 32) {
                boss.hp -= b.dmg;
""",
    """            if (bd < 40) {
                boss.hp -= b.dmg;
""",
    'boss-hit-r')
rep("""            if (!rectHit(boss.x + bmx, boss.y, 20)) boss.x += bmx;
            if (!rectHit(boss.x, boss.y + bmy, 20)) boss.y += bmy;
            boss.x = Math.max(20, Math.min(MAPW - 20, boss.x));
            boss.y = Math.max(20, Math.min(MAPH - 20, boss.y));
""",
    """            if (!rectHit(boss.x + bmx, boss.y, 20)) boss.x += bmx;
            if (!rectHit(boss.x, boss.y + bmy, 20)) boss.y += bmy;
            // \U0001F479 \u573A\u5730\u56F4\u4F4F BOSS\uff0c\u4E0D\u80FD\u8DD1\u51FA\u53BB\uff01
            if (arena) {
                var adx = boss.x - arena.x, ady = boss.y - arena.y;
                var ad = Math.sqrt(adx * adx + ady * ady);
                if (ad > arena.r - 26) {
                    boss.x = arena.x + adx / ad * (arena.r - 26);
                    boss.y = arena.y + ady / ad * (arena.r - 26);
                }
            }
            boss.x = Math.max(20, Math.min(MAPW - 20, boss.x));
            boss.y = Math.max(20, Math.min(MAPH - 20, boss.y));
""",
    'boss-constrain')

rep("""            ctx.font = '48px sans-serif';
            ctx.fillText('\U0001F479', boss.x, boss.y + 16);
""",
    """            ctx.font = '60px sans-serif';
            ctx.fillText('\U0001F479', boss.x, boss.y + 20);
""",
    'boss-big')

# 11) 画 BOSS 场地
rep("""        // \U0001F3DC\ufe0f \u9505\u5854\uff08\u76f4\u63a5\u4e0a3\u697c\uff01\uff09
""",
    """        // \U0001F479 BOSS \u573A\u5730\uff08\u5706\u5f62\u76d1\u72f1\uff0c\u95e8\u5728\u4e0b\u65b9\uff09
        if (arena) {
            ctx.beginPath();
            ctx.arc(arena.x, arena.y, arena.r, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(120, 30, 30, 0.18)';
            ctx.fill();
            ctx.strokeStyle = '#a33';
            ctx.lineWidth = 14;
            ctx.stroke();
            // \u95e8\u53e3\u7f3a\u53e3
            var g0 = arena.gateAng - arena.gateHalf, g1 = arena.gateAng + arena.gateHalf;
            ctx.strokeStyle = 'rgba(20, 20, 20, 0.9)';
            ctx.lineWidth = 18;
            ctx.beginPath();
            ctx.arc(arena.x, arena.y, arena.r, g0, g1);
            ctx.stroke();
            ctx.fillStyle = '#ff8e6b';
            ctx.font = 'bold 15px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('\U0001F479 BOSS\u573A\u5730\uff08\u8fdb\u53bb\u5c31\u8981\u5f00\u6253\uff09', arena.x, arena.y - arena.r - 20);
        }

        // \U0001F3DC\ufe0f \u9505\u5854\uff08\u76f4\u63a5\u4e0a3\u697c\uff01\uff09
""",
    'draw-arena')

# 12) 小地图 + 大地图：显示 BOSS 位置
rep("""        // \u73a9\u5bb6\uff08\u4e0d\u663e\u793a\u654c\u4eba\uff01\uff09
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(ox + player.x * sc, oy + player.y * sc, 4, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = 'rgba(255,255,255,0.6)';
        ctx.font = '11px sans-serif';
        ctx.textAlign = 'left';
        ctx.fillText('\U0001F5FA\ufe0f \u5730\u56fe\uff08M\uff09', mx, my + mh + 14);
""",
    """        // \u73a9\u5bb6\uff08\u4e0d\u663e\u793a\u666e\u901a\u654c\u4eba\uff01\uff09
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(ox + player.x * sc, oy + player.y * sc, 4, 0, Math.PI * 2);
        ctx.fill();
        // \U0001F479 \u5730\u56fe\u4e0a\u663e\u793a BOSS \u4f4d\u7f6e\uff01
        if (boss && boss.hp > 0) {
            ctx.fillStyle = '#ff2d55';
            ctx.beginPath();
            ctx.arc(ox + boss.x * sc, oy + boss.y * sc, 7, 0, Math.PI * 2);
            ctx.fill();
            ctx.font = '10px sans-serif';
            ctx.fillText('BOSS', ox + boss.x * sc + 9, oy + boss.y * sc + 4);
        }
        ctx.fillStyle = 'rgba(255,255,255,0.6)';
        ctx.font = '11px sans-serif';
        ctx.textAlign = 'left';
        ctx.fillText('\U0001F5FA\ufe0f \u5730\u56fe\uff08M\uff09', mx, my + mh + 14);
""",
    'minimap-boss')

rep("""        // \u73a9\u5bb6
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(ox + player.x * sc, oy + player.y * sc, 6, 0, Math.PI * 2);
        ctx.fill();
        ctx.font = '12px sans-serif';
        ctx.fillText('\u6211', ox + player.x * sc, oy + player.y * sc - 10);
""",
    """        // \u73a9\u5bb6
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(ox + player.x * sc, oy + player.y * sc, 6, 0, Math.PI * 2);
        ctx.fill();
        ctx.font = '12px sans-serif';
        ctx.fillText('\u6211', ox + player.x * sc, oy + player.y * sc - 10);
        // \U0001F479 \u5927\u5730\u56fe\u4e0a\u663e\u793a BOSS \u4f4d\u7f6e
        if (boss && boss.hp > 0) {
            ctx.fillStyle = '#ff2d55';
            ctx.beginPath();
            ctx.arc(ox + boss.x * sc, oy + boss.y * sc, 10, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#ff8e9a';
            ctx.font = 'bold 14px sans-serif';
            ctx.fillText('\U0001F479 BOSS', ox + boss.x * sc, oy + boss.y * sc - 14);
        }
""",
    'bigmap-boss')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
