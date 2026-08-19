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

# 1) 敌人移动：撞墙检测！
rep("""        // \U0001F47E \u654c\u4eba\uff08\u8fd1\u6218\u51b2\u8138 / \u8fdc\u7a0b\u5c04\u51fb\uff09
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
""",
    """        // \U0001F47E \u654c\u4eba\uff08\u8fd1\u6218\u51b2\u8138 / \u8fdc\u7a0b\u5c04\u51fb\uff09
        for (var i = 0; i < enemies.length; i++) {
            var e = enemies[i];
            var d = Math.sqrt((e.x - player.x) * (e.x - player.x) + (e.y - player.y) * (e.y - player.y));
            var es = (e.ranged ? 100 : 130) * dt;
            var mx = 0, my = 0;
            if (e.ranged) {
                // \U0001F916 \u8fdc\u7a0b\u654c\u4eba\uff1a\u4fdd\u6301\u8ddd\u79bb\u3001\u8fb9\u8d70\u8fb9\u5f00\u706b\uff01
                if (d < 240 && d > 0.01) {
                    mx = -(player.x - e.x) / d * es;
                    my = -(player.y - e.y) / d * es;
                } else if (d > 340) {
                    mx = (player.x - e.x) / d * es;
                    my = (player.y - e.y) / d * es;
                } else {
                    e.wander += dt;
                    mx = Math.cos(e.wander) * es * 0.4;
                    my = Math.sin(e.wander) * es * 0.4;
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
                    mx = (player.x - e.x) / d * es;
                    my = (player.y - e.y) / d * es;
                } else {
                    e.wander += dt;
                    mx = Math.cos(e.wander) * es * 0.5;
                    my = Math.sin(e.wander) * es * 0.5;
                }
            }
            // \U0001F9F1 \u654c\u4eba\u4e5f\u78b0\u58c1\uff01\uff08\u4e0d\u80fd\u7a7f\u5899\uff09
            if (!rectHit(e.x + mx, e.y, 14)) e.x += mx;
            if (!rectHit(e.x, e.y + my, 14)) e.y += my;
            e.x = Math.max(20, Math.min(MAPW - 20, e.x));
            e.y = Math.max(20, Math.min(MAPH - 20, e.y));
""",
    'enemy-wall')

# 2) 敌人血条上显示数字
rep("""        // \U0001F47E \u654c\u4eba\uff08\u8fd1\u6218\U0001F47E / \u8fdc\u7a0b\U0001F916\uff09
        ctx.font = '28px sans-serif';
        for (var i = 0; i < enemies.length; i++) {
            var e = enemies[i];
            ctx.fillText(e.ranged ? '\U0001F916' : '\U0001F47E', e.x, e.y + 9);
            ctx.fillStyle = '#333';
            ctx.fillRect(e.x - 20, e.y - 36, 40, 5);
            ctx.fillStyle = '#ff5d5d';
            ctx.fillRect(e.x - 20, e.y - 36, 40 * Math.max(0, e.hp / 100), 5);
        }
""",
    """        // \U0001F47E \u654c\u4eba\uff08\u8fd1\u6218\U0001F47E / \u8fdc\u7a0b\U0001F916\uff09
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
    'enemy-hp-num')

# 3) 玩家头上显示血量
rep("""        ctx.restore();

        // \U0001F52B \u5b50\u5f39
""",
    """        ctx.restore();

        // \u2764\ufe0f \u73a9\u5bb6\u5934\u4e0a\u8840\u91cf\u6570\u5b57
        ctx.fillStyle = '#ff6b6b';
        ctx.font = 'bold 14px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('\u2764\ufe0f ' + Math.max(0, player.hp) + '/' + maxHp, player.x, player.y - 42);

        // \U0001F52B \u5b50\u5f39
""",
    'player-hp-num')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
