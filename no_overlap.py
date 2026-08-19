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

# 1) 小怪不能和你重叠（同层推到 42px 外，不再穿过你）+ 接触伤害调整
rep("""            e.x = Math.max(20, Math.min(MAPW - 20, e.x));
            e.y = Math.max(20, Math.min(MAPH - 20, e.y));
            if (sameFloor && d < 52 && player.hitCd <= 0) {
""",
    """            e.x = Math.max(20, Math.min(MAPW - 20, e.x));
            e.y = Math.max(20, Math.min(MAPH - 20, e.y));
            // \U0001F645 \u5c0f\u602a\u4e0d\u80fd\u548c\u4f60\u91cd\u53e0\uff08\u540c\u5c42\u63a8\u5230\u8eab\u8fb9 42px\uff0c\u4e0d\u518d\u7a7f\u8fc7\u4f60\uff09
            var cd = Math.sqrt((e.x - player.x) * (e.x - player.x) + (e.y - player.y) * (e.y - player.y));
            if (sameFloor && cd < 42 && cd > 0.001) {
                var pnx = (player.x - e.x) / cd, pny = (player.y - e.y) / cd;
                e.x = player.x - pnx * 42;
                e.y = player.y - pny * 42;
                cd = 42;
            }
            if (sameFloor && cd < 46 && player.hitCd <= 0) {
""",
    'no-overlap-player')

# 2) 小怪之间不能重叠（同层才分开）
rep("""        // \U0001F479 BOSS\uff01\uff08\u5730\u9762\u5de8\u53d8\u6012\uff0c\u53ea\u5728\u5730\u9762\uff09
""",
    """        // \U0001F465 \u5c0f\u602a\u4e4b\u95f4\u4e0d\u80fd\u91cd\u53e0\uff08\u540c\u5c42\u624d\u5206\u5f00\uff09
        for (var i = 0; i < enemies.length; i++) {
            var ea = enemies[i];
            for (var j = i + 1; j < enemies.length; j++) {
                var eb2 = enemies[j];
                if (ea.floor !== eb2.floor) continue;   // \u4e0d\u540c\u5c42\u4e0d\u78b0
                var ddx = eb2.x - ea.x, ddy = eb2.y - ea.y;
                var dd = Math.sqrt(ddx * ddx + ddy * ddy);
                if (dd < 36 && dd > 0.001) {
                    var nx = ddx / dd, ny = ddy / dd;
                    var ov = (36 - dd) / 2;
                    ea.x -= nx * ov; ea.y -= ny * ov;
                    eb2.x += nx * ov; eb2.y += ny * ov;
                }
            }
        }

        // \U0001F479 BOSS\uff01\uff08\u5730\u9762\u5de8\u53d8\u6012\uff0c\u53ea\u5728\u5730\u9762\uff09
""",
    'enemy-sep')

# 3) 楼顶加影子：显得"高高在上"！
rep("""        // \U0001F3E2 2\u697c\u697c\u9876\uff08\u7ad9\u5728\u4e0a\u9762\u4fef\u89c6\u4e0b\u65b9\uff0c\u80fd\u5c04\u51fb\u697c\u4e0b\u654c\u4eba\uff01\uff09
        if (player.floor === 2 && player.bIdx >= 0) {
            var bb = buildings[player.bIdx];
            ctx.fillStyle = 'rgba(110, 92, 60, 0.85)';
            ctx.fillRect(bb.x + T, bb.y + T, bb.w - 2 * T, bb.h - 2 * T);
""",
    """        // \U0001F3E2 2\u697c\u697c\u9876\uff08\u7ad9\u5728\u4e0a\u9762\u4fef\u89c6\u4e0b\u65b9\uff0c\u80fd\u5c04\u51fb\u697c\u4e0b\u654c\u4eba\uff01\uff09
        if (player.floor === 2 && player.bIdx >= 0) {
            var bb = buildings[player.bIdx];
            ctx.fillStyle = 'rgba(0,0,0,0.4)';
            ctx.fillRect(bb.x + T + 10, bb.y + T + 12, bb.w - 2 * T, bb.h - 2 * T);   // \U0001F3E2 \u9634\u5f71\uff0c\u663e\u9ad8\uff01
            ctx.fillStyle = 'rgba(150, 120, 75, 0.92)';
            ctx.fillRect(bb.x + T, bb.y + T, bb.w - 2 * T, bb.h - 2 * T);
""",
    'roof-shadow')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
