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

# 1) 墙面标记属于哪栋楼（2楼射击时忽略脚下这栋楼的墙）
rep("""        for (var i = 0; i < buildings.length; i++) {
            var b = buildings[i];
            wallRects.push({ x: b.x, y: b.y, w: b.w, h: T });
            wallRects.push({ x: b.x, y: b.y + b.h - T, w: (b.w - DW) / 2, h: T });
            wallRects.push({ x: b.x + (b.w + DW) / 2, y: b.y + b.h - T, w: (b.w - DW) / 2, h: T });
            wallRects.push({ x: b.x, y: b.y, w: T, h: b.h });
            wallRects.push({ x: b.x + b.w - T, y: b.y, w: T, h: b.h });
        }
""",
    """        for (var i = 0; i < buildings.length; i++) {
            var b = buildings[i];
            wallRects.push({ x: b.x, y: b.y, w: b.w, h: T, b: i });
            wallRects.push({ x: b.x, y: b.y + b.h - T, w: (b.w - DW) / 2, h: T, b: i });
            wallRects.push({ x: b.x + (b.w + DW) / 2, y: b.y + b.h - T, w: (b.w - DW) / 2, h: T, b: i });
            wallRects.push({ x: b.x, y: b.y, w: T, h: b.h, b: i });
            wallRects.push({ x: b.x + b.w - T, y: b.y, w: T, h: b.h, b: i });
        }
""",
    'walls-tag')

# 2) 玩家加楼层状态 + floorCd
rep("    var player = { x: 200, y: 200, hp: 100, dir: 0, atkCd: 0, hitCd: 0, bullets: 30, weapons: ['pistol', null], weaponSlot: 0 };\n    var maxHp = 100;   // \u6700\u5927\u8840\u91cf\uff08\u7528\u836f\u3001\u533b\u7597\u5305\u53ef\u4ee5\u52a0\uff09\n",
    "    var player = { x: 200, y: 200, hp: 100, dir: 0, atkCd: 0, hitCd: 0, bullets: 30, weapons: ['pistol', null], weaponSlot: 0, floor: 1, bIdx: -1 };\n    var maxHp = 100;   // \u6700\u5927\u8840\u91cf\uff08\u7528\u836f\u3001\u533b\u7597\u5305\u53ef\u4ee5\u52a0\uff09\n    var floorCd = 0;    // \u697c\u68af\u5207\u6362\u51b7\u5374\n",
    'player-floor')

# 3) resetGame：楼层重置
rep("        player.x = 200; player.y = 200;\n        maxHp = 100 + gear.hpBonus + runMeds * 20;   // \u7528\u836f/\u533b\u7597\u5305\u52a0\u6700\u5927\u8840\n        player.hp = maxHp;\n",
    "        player.x = 200; player.y = 200;\n        player.floor = 1; player.bIdx = -1; floorCd = 0;\n        maxHp = 100 + gear.hpBonus + runMeds * 20;   // \u7528\u836f/\u533b\u7597\u5305\u52a0\u6700\u5927\u8840\n        player.hp = maxHp;\n",
    'reset-floor')

# 4) 移动：2楼在楼顶范围内走（不撞墙）
rep("""        var nx = player.x + dx * spd, ny = player.y + dy * spd;
        if (!rectHit(nx, player.y, 16)) player.x = nx;
        if (!rectHit(player.x, ny, 16)) player.y = ny;
        player.x = Math.max(20, Math.min(MAPW - 20, player.x));
        player.y = Math.max(20, Math.min(MAPH - 20, player.y));
""",
    """        var nx = player.x + dx * spd, ny = player.y + dy * spd;
        if (player.floor === 2 && player.bIdx >= 0) {
            // \U0001F3E2 2\u697c\uff1a\u53ea\u80fd\u5728\u697c\u9876\u8303\u56f4\u5185\u8d70\u52a8\uff08\u4e0d\u78b0\u5899\uff09
            var bb = buildings[player.bIdx];
            player.x = Math.max(bb.x + T + 4, Math.min(bb.x + bb.w - T - 4, nx));
            player.y = Math.max(bb.y + T + 4, Math.min(bb.y + bb.h - T - 4, ny));
        } else {
            if (!rectHit(nx, player.y, 16)) player.x = nx;
            if (!rectHit(player.x, ny, 16)) player.y = ny;
        }
        player.x = Math.max(20, Math.min(MAPW - 20, player.x));
        player.y = Math.max(20, Math.min(MAPH - 20, player.y));
""",
    'move-floor')

# 5) 楼梯：踩上去自动上下楼
rep("""        // \U0001F4E6 \u5f00\u7bb1\uff08\u8e29\u5230\u81ea\u52a8\u5f00\uff09
""",
    """        // \U0001FA9C \u697c\u68af\uff1a\u8e29\u4e0a\u53bb\u81ea\u52a8\u4e0a\u4e0b\u697c\uff01
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

        // \U0001F4E6 \u5f00\u7bb1\uff08\u8e29\u5230\u81ea\u52a8\u5f00\uff09
""",
    'stairs')

# 6) 子弹撞墙：2楼忽略脚下这栋楼的墙（能俯射楼下！）
rep("""    // \U0001F441 \u89c6\u7ebf\u68c0\u6d4b\uff1a\u4e24\u70b9\u4e4b\u95f4\u6709\u6ca1\u6709\u88ab\u5899\u6321\u4f4f
""",
    """    // \U0001F52B \u5b50\u5f39\u78b0\u5891\uff1a2\u697c\u65f6\u5ffd\u7565\u811a\u4e0b\u8fd9\u680b\u697c\u7684\u5899\uff08\u80fd\u4ece\u697c\u4e0a\u4fef\u5c04\u4e0b\u53bb\uff09
    function bulletWallHit(x, y) {
        if (player.floor === 2 && player.bIdx >= 0) {
            var bi = player.bIdx;
            for (var i = 0; i < wallRects.length; i++) {
                if (wallRects[i].b === bi) continue;   // \u8df3\u8fc7\u81ea\u5df1\u8eab\u4e0b\u7684\u5899
                var r = wallRects[i];
                var cx = Math.max(r.x, Math.min(x, r.x + r.w));
                var cy = Math.max(r.y, Math.min(y, r.y + r.h));
                var dx = x - cx, dy = y - cy;
                if (dx * dx + dy * dy < 16) return true;
            }
            return false;
        }
        return rectHit(x, y, 4);
    }

    // \U0001F441 \u89c6\u7ebf\u68c0\u6d4b\uff1a\u4e24\u70b9\u4e4b\u95f4\u6709\u6ca1\u6709\u88ab\u5899\u6321\u4f4f
""",
    'bullet-wall-func')
rep("            var hitWall = rectHit(b.x, b.y, 4);\n",
    "            var hitWall = bulletWallHit(b.x, b.y);\n",
    'bullet-wall-use')

# 7) 敌人视线：玩家在2楼时地面敌人看不到/打不到
rep("            var los = hasLOS(e.x, e.y, player.x, player.y);   // \U0001F441 \u770b\u5f97\u5230\u73a9\u5bb6\u5417\uff1f\n",
    "            var los = (player.floor === 2) ? false : hasLOS(e.x, e.y, player.x, player.y);   // \U0001F441 \u73a9\u5bb6\u57282\u697c\uff0c\u5730\u9762\u654c\u4eba\u770b\u4e0d\u5230\uff01\n",
    'los-floor')
rep("""            if (d2 < 22 && player.hitCd <= 0) {
""",
    """            if (d2 < 22 && player.hitCd <= 0 && player.floor === 1) {   // 2\u697c\u65f6\u5730\u9762\u5b50\u5f39\u6253\u4e0d\u5230\u4f60\uff01
""",
    'enemyshot-floor')

# 8) 2楼可能刷宝箱（35%）
rep("""        for (var i = 0; i < buildings.length; i++) {
            var p = spotInBuilding(buildings[i]);
            crates.push({ x: p.x, y: p.y });
        }
""",
    """        for (var i = 0; i < buildings.length; i++) {
            var p = spotInBuilding(buildings[i]);
            crates.push({ x: p.x, y: p.y });
            // \U0001F3E2 2\u697c\u53ef\u80fd\u5237\u5b9d\u7bb1\uff0835%\u6982\u7387\uff09\uff01
            if (Math.random() < 0.35) {
                var b2 = buildings[i];
                crates.push({ x: b2.x + T + 24 + Math.random() * (b2.w - 2 * T - 48), y: b2.y + T + 36 });
            }
        }
""",
    'roof-crates')

# 9) 画：一楼楼梯标记
rep("""            ctx.fillStyle = 'rgba(255,255,255,0.35)';
            ctx.font = '13px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('\u623f', b.x + b.w / 2, b.y + T + 16);
""",
    """            ctx.fillStyle = 'rgba(255,255,255,0.35)';
            ctx.font = '13px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('\u623f', b.x + b.w / 2, b.y + T + 16);
            // \U0001FA9C \u697c\u68af\u6807\u8bb0
            ctx.font = '16px sans-serif';
            ctx.fillText('\U0001FA9C', b.x + T + 24, b.y + T + 34);
""",
    'draw-stairs')

# 10) 画：2楼楼顶（在敌人之后、玩家之前，盖住楼下敌人）
rep("""        // \U0001F3C3 \u73a9\u5bb6\uff08\u62ff\u67aa\u5c0f\u4eba\uff09
        ctx.save();
""",
    """        // \U0001F3E2 2\u697c\u697c\u9876\uff08\u7ad9\u5728\u4e0a\u9762\u4fef\u89c6\u4e0b\u65b9\uff0c\u80fd\u5c04\u51fb\u697c\u4e0b\u654c\u4eba\uff01\uff09
        if (player.floor === 2 && player.bIdx >= 0) {
            var bb = buildings[player.bIdx];
            ctx.fillStyle = 'rgba(110, 92, 60, 0.85)';
            ctx.fillRect(bb.x + T, bb.y + T, bb.w - 2 * T, bb.h - 2 * T);
            ctx.strokeStyle = '#8a7a55';
            ctx.lineWidth = 3;
            ctx.strokeRect(bb.x + T, bb.y + T, bb.w - 2 * T, bb.h - 2 * T);
            ctx.fillStyle = 'rgba(255,255,255,0.85)';
            ctx.font = 'bold 14px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('\U0001F3E2 2\u697c', bb.x + bb.w / 2, bb.y + T + 20);
            // \U0001F4E6 \u697c\u9876\u5b9d\u7bb1\u91cd\u7ed8\uff08\u88ab\u697c\u9876\u8986\u76d6\u7684\u90a3\u4e2a\uff09
            ctx.font = '26px sans-serif';
            for (var ci = 0; ci < crates.length; ci++) {
                var cr = crates[ci];
                if (cr.x > bb.x && cr.x < bb.x + bb.w && cr.y > bb.y && cr.y < bb.y + bb.h) {
                    ctx.fillText('\U0001F4E6', cr.x, cr.y + 9);
                }
            }
            ctx.fillText('\U0001FA9C', bb.x + T + 24, bb.y + T + 40);   // \u697c\u68af\u53e3
        }

        // \U0001F3C3 \u73a9\u5bb6\uff08\u62ff\u67aa\u5c0f\u4eba\uff09
        ctx.save();
""",
    'draw-roof')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
