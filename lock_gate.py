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

# 1) arena 加 locked
rep("        arena = { x: ax, y: ay, r: 210, gateAng: Math.PI / 2, gateHalf: 0.45 };\n",
    "        arena = { x: ax, y: ay, r: 210, gateAng: Math.PI / 2, gateHalf: 0.45, locked: false };\n",
    'arena-locked-var')

# 2) arenaHit：锁门时整圈都撞
rep("""        var ang = Math.atan2(dy, dx);
        if (Math.abs(ang - arena.gateAng) < arena.gateHalf) return false;   // \u95e8\u53e3\u901a\u884c
        return true;
""",
    """        var ang = Math.atan2(dy, dx);
        if (arena.locked) return true;   // \U0001F512 \u95e8\u9501\u4e86\uff1a\u6574\u5708\u90fd\u78b0\uff01
        if (Math.abs(ang - arena.gateAng) < arena.gateHalf) return false;   // \u95e8\u53e3\u901a\u884c
        return true;
""",
    'arena-locked-hit')

# 3) 一进门就锁门（插在楼梯逻辑前）
rep("""        // \U0001FA9C \u697c\u68af\uff1a\u90e8\u5206\u623f\u5b50\u4e0a2\u697c\uff0c\u9505\u5854\u76f4\u63a5\u4e0a3\u697c\uff01
""",
    """        // \U0001F512 BOSS\u573a\u5730\uff1a\u4e00\u8fdb\u95e8\u5c31\u9501\u4e0a\uff0c\u6253\u8d62\u624d\u5f00\uff01
        if (arena) {
            var ain = Math.sqrt((player.x - arena.x) * (player.x - arena.x) + (player.y - arena.y) * (player.y - arena.y)) < arena.r - 16;
            if (!arena.locked && ain && player.floor === 1) {
                arena.locked = true;
                showMsg('\U0001F512 \u5927\u95e8\u9501\u4e0a\u4e86\uff01\u6253\u8d25 BOSS \u624d\u80fd\u51fa\u53bb\uff01');
            }
        }

        // \U0001FA9C \u697c\u68af\uff1a\u90e8\u5206\u623f\u5b50\u4e0a2\u697c\uff0c\u9505\u5854\u76f4\u63a5\u4e0a3\u697c\uff01
""",
    'arena-lock-entry')

# 4) killBoss：开门！
rep("""        showMsg('\U0001F479 \u51fb\u8d25 BOSS\uff01+200\u5206\uff0c\u7206\u51fa 2 \u628a\u67aa\u548c\u5b50\u5f39\uff01');
        boss = null;
        document.getElementById('bossbar-wrap').style.display = 'none';
""",
    """        showMsg('\U0001F479 \u51fb\u8d25 BOSS\uff01+200\u5206\uff0c\u7206\u51fa 2 \u628a\u67aa\u548c\u5b50\u5f39\uff01\U0001F513 \u5927\u95e8\u5f00\u4e86\uff01');
        boss = null;
        if (arena) arena.locked = false;   // \U0001F513 \u6253\u8d25\u624d\u5f00\u95e8\uff01
        document.getElementById('bossbar-wrap').style.display = 'none';
""",
    'killboss-unlock')

# 5) 画场地：锁门显示红门 + 🔒
rep("""            var g0 = arena.gateAng - arena.gateHalf, g1 = arena.gateAng + arena.gateHalf;
            ctx.strokeStyle = 'rgba(20, 20, 20, 0.9)';
            ctx.lineWidth = 18;
            ctx.beginPath();
            ctx.arc(arena.x, arena.y, arena.r, g0, g1);
            ctx.stroke();
            ctx.fillStyle = '#ff8e6b';
            ctx.font = 'bold 15px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('\U0001F479 BOSS\u573a\u5730\uff08\u8fdb\u53bb\u5c31\u8981\u5f00\u6253\uff09', arena.x, arena.y - arena.r - 20);
""",
    """            var g0 = arena.gateAng - arena.gateHalf, g1 = arena.gateAng + arena.gateHalf;
            if (arena.locked) {
                // \U0001F512 \u9501\u95e8\uff1a\u7ea2\u8272\u5c01\u95ed\u5927\u95e8
                ctx.strokeStyle = '#d44';
                ctx.lineWidth = 18;
                ctx.beginPath();
                ctx.arc(arena.x, arena.y, arena.r, g0, g1);
                ctx.stroke();
            } else {
                ctx.strokeStyle = 'rgba(20, 20, 20, 0.9)';
                ctx.lineWidth = 18;
                ctx.beginPath();
                ctx.arc(arena.x, arena.y, arena.r, g0, g1);
                ctx.stroke();
            }
            ctx.fillStyle = '#ff8e6b';
            ctx.font = 'bold 15px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('\U0001F479 BOSS\u573a\u5730' + (arena.locked ? ' \U0001F512\u5df2\u9501\u95e8\uff01' : '\uff08\u8fdb\u53bb\u5c31\u8981\u5f00\u6253\uff09'), arena.x, arena.y - arena.r - 20);
""",
    'draw-arena-lock')

# 6) 梯子标记：只有有2楼的房子才显示！
rep("""            // \U0001FA9C \u697c\u68af\u6807\u8bb0
            ctx.font = '16px sans-serif';
            ctx.fillText('\U0001FA9C', b.x + T + 24, b.y + T + 34);
""",
    """            // \U0001FA9C \u697c\u68af\u6807\u8bb0\uff08\u53ea\u6709\u67092\u697c\u7684\u623f\u5b50\u624d\u6709\uff01\uff09
            if (b.has2) {
                ctx.font = '16px sans-serif';
                ctx.fillText('\U0001FA9C', b.x + T + 24, b.y + T + 34);
            }
""",
    'stairs-marker-has2')

# 7) 楼顶宝箱：只有有2楼的房子才刷
rep("""            // \U0001F3E2 2\u697c\u53ef\u80fd\u5237\u5b9d\u7bb1\uff0835%\u6982\u7387\uff09\uff01
            if (Math.random() < 0.35) {
                var b2 = buildings[i];
                crates.push({ x: b2.x + T + 24 + Math.random() * (b2.w - 2 * T - 48), y: b2.y + T + 36 });
            }
""",
    """            // \U0001F3E2 2\u697c\u53ef\u80fd\u5237\u5b9d\u7bb1\uff0835%\u6982\u7387\uff09\uff01
            if (buildings[i].has2 && Math.random() < 0.35) {
                var b2 = buildings[i];
                crates.push({ x: b2.x + T + 24 + Math.random() * (b2.w - 2 * T - 48), y: b2.y + T + 36 });
            }
""",
    'roof-crate-has2')

# 8) 小怪爬楼更积极（半径 240 -> 420）
rep("""                    if (sdd < 240 && sdd > 0.01) {
                        // \u5df2\u7ecf\u9760\u8fd1\u623f\u5b50\uff1a\u76f4\u63a5\u722c\u4e0a 2 \u697c\uff01
""",
    """                    if (sdd < 420 && sdd > 0.01) {
                        // \u5df2\u7ecf\u9760\u8fd1\u623f\u5b50\uff1a\u76f4\u63a5\u722c\u4e0a 2 \u697c\uff01
""",
    'enemy-climb-radius')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
