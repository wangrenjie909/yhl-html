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

# 1) 视线检测函数（放在 rectHit 后面）
rep("""        return false;
    }

    var player = { x: 200, y: 200, hp: 100, dir: 0, atkCd: 0, hitCd: 0, bullets: 30, weapons: ['pistol', null], weaponSlot: 0 };
""",
    """        return false;
    }

    // \U0001F441 \u89c6\u7ebf\u68c0\u6d4b\uff1a\u4e24\u70b9\u4e4b\u95f4\u6709\u6ca1\u6709\u88ab\u5899\u6321\u4f4f
    function hasLOS(x1, y1, x2, y2) {
        var dx = x2 - x1, dy = y2 - y1;
        var dist = Math.sqrt(dx * dx + dy * dy);
        var steps = Math.max(1, Math.ceil(dist / 8));
        for (var i = 1; i < steps; i++) {
            var t = i / steps;
            if (rectHit(x1 + dx * t, y1 + dy * t, 4)) return false;
        }
        return true;
    }

    var player = { x: 200, y: 200, hp: 100, dir: 0, atkCd: 0, hitCd: 0, bullets: 30, weapons: ['pistol', null], weaponSlot: 0 };
""",
    'los-func')

# 2) 远程敌人：看不到就不开枪，先出来找你
rep("""            var mx = 0, my = 0;
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
""",
    """            var mx = 0, my = 0;
            var los = hasLOS(e.x, e.y, player.x, player.y);   // \U0001F441 \u770b\u5f97\u5230\u73a9\u5bb6\u5417\uff1f
            if (e.ranged) {
                // \U0001F916 \u8fdc\u7a0b\u654c\u4eba\uff1a\u770b\u4e0d\u5230\u5c31\u5148\u51b2\u51fa\u6765\uff0c\u770b\u5230\u624d\u5f00\u706b\uff01
                if (!los) {
                    // \u88ab\u5899\u6321\u4f4f\u4e86\uff1a\u4e0d\u6253\u67aa\uff0c\u8d70\u8fd1\u73a9\u5bb6\u627e\u89c6\u89d2
                    mx = (player.x - e.x) / d * es * 1.2;
                    my = (player.y - e.y) / d * es * 1.2;
                    e.shotCd = 0.15;   // \u5feb\u901f\u91cd\u65b0\u68c0\u6d4b
                } else if (d < 240 && d > 0.01) {
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
                if (los && d < 480 && e.shotCd <= 0) {
                    e.shotCd = 1.6 + Math.random() * 0.6;
                    var ea = Math.atan2(player.y - e.y, player.x - e.x);
                    enemyShots.push({ x: e.x, y: e.y, vx: Math.cos(ea) * 260, vy: Math.sin(ea) * 260, life: 2.4 });
                }
                if (e.shotCd > 0) e.shotCd -= dt;
            } else {
""",
    'ranged-los')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
