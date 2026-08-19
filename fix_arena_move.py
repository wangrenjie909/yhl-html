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

# 1) arenaHit：只撞外墙薄圈，内部自由走动
rep("""    function arenaHit(x, y, rad) {
        if (!arena) return false;
        var dx = x - arena.x, dy = y - arena.y;
        var d = Math.sqrt(dx * dx + dy * dy);
        if (d < arena.r - 16 - rad || d > arena.r + 16 + rad) return false;
        var ang = Math.atan2(dy, dx);
        if (arena.locked) return true;   // \U0001F512 \u95e8\u9501\u4e86\uff1a\u6574\u5708\u90fd\u78b0\uff01
        if (Math.abs(ang - arena.gateAng) < arena.gateHalf) return false;   // \u95e8\u53e3\u901a\u884c
        return true;
    }
""",
    """    function arenaHit(x, y, rad) {
        if (!arena) return false;
        var dx = x - arena.x, dy = y - arena.y;
        var d = Math.sqrt(dx * dx + dy * dy);
        if (d > arena.r + 16 + rad) return false;      // \u5916\u8fb9\u592a\u8fdc\uff1a\u4e0d\u78b0
        if (d < arena.r - 6 - rad) return false;        // \u573a\u5730\u5185\u90e8\uff1a\u81ea\u7531\u8d70\u52a8\uff01
        var ang = Math.atan2(dy, dx);
        var inGate = Math.abs(ang - arena.gateAng) < arena.gateHalf;
        if (inGate && !arena.locked) return false;      // \u95e8\u53e3\u901a\u884c\uff08\u672a\u9501\uff09
        return true;                                    // \u5899\u9762 / \u9501\u4f4f\u7684\u95e8
    }
""",
    'arena-hit-fix')

# 2) 哨塔：避开其他塔和竞技场，不重叠！
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
            var twx, twy, tries = 0, overlap = true;
            do {
                twx = 150 + Math.random() * (MAPW - 300);
                twy = 150 + Math.random() * (MAPH - 300);
                tries++;
                overlap = rectHit(twx, twy, 70);
                // \u907f\u5f00\u5176\u4ed6\u9505\u5854\uff08\u4e0d\u91cd\u53e0\uff09
                for (var tj = 0; tj < towers.length; tj++) {
                    var ot = towers[tj];
                    if (Math.abs(ot.x - twx) < 270 && Math.abs(ot.y - twy) < 270) overlap = true;
                }
                // \u907f\u5f00 BOSS\u573a\u5730\uff08\u4e0d\u8fdb\u573a\u5730\uff09
                if (arena && Math.sqrt((twx - arena.x) * (twx - arena.x) + (twy - arena.y) * (twy - arena.y)) < arena.r + 110) overlap = true;
            } while (overlap && tries < 90);
            towers.push({ x: twx, y: twy, w: 130, h: 130 });
        }
""",
    'tower-no-overlap')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
