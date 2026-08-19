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

# 1) 塔不能建在房子里面！
rep("""                tries++;
                overlap = rectHit(twx, twy, 70);
                // \u907f\u5f00\u5176\u4ed6\u9505\u5854\uff08\u4e0d\u91cd\u53e0\uff09
""",
    """                tries++;
                overlap = rectHit(twx, twy, 70);
                // \u907f\u5f00\u623f\u5b50\uff08\u4e0d\u80fd\u5efa\u5728\u623f\u5b50\u91cc\u9762\uff01\uff09
                for (var bi = 0; bi < buildings.length; bi++) {
                    var bd2 = buildings[bi];
                    if (twx > bd2.x - 60 && twx < bd2.x + bd2.w + 60 && twy > bd2.y - 60 && twy < bd2.y + bd2.h + 60) overlap = true;
                }
                // \u907f\u5f00\u5176\u4ed6\u9505\u5854\uff08\u4e0d\u91cd\u53e0\uff09
""",
    'tower-not-in-house')

# 2) 决斗场避开撤离点！
rep("""        } while ((rectHit(ax, ay, 240) || Math.sqrt((ax - 200) * (ax - 200) + (ay - 200) * (ay - 200)) < 500) && tries3 < 90);
""",
    """        } while ((rectHit(ax, ay, 240) || Math.sqrt((ax - 200) * (ax - 200) + (ay - 200) * (ay - 200)) < 500 ||
                  Math.sqrt((ax - extract.x) * (ax - extract.x) + (ay - extract.y) * (ay - extract.y)) < extract.r + 340) && tries3 < 90);
""",
    'arena-not-extract')

# 3) arenaHit：只有薄薄一圈墙，进门不卡住！
rep("""    function arenaHit(x, y, rad) {
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
    """    function arenaHit(x, y, rad) {
        if (!arena) return false;
        var dx = x - arena.x, dy = y - arena.y;
        var d = Math.sqrt(dx * dx + dy * dy);
        if (Math.abs(d - arena.r) > 14 + rad) return false;   // \u4e0d\u5728\u5899\u4e0a\uff1a\u4e0d\u78b0\uff08\u91cc\u9762\u81ea\u7531\u8d70\uff01\uff09
        var ang = Math.atan2(dy, dx);
        var inGate = Math.abs(ang - arena.gateAng) < arena.gateHalf;
        if (inGate && !arena.locked) return false;            // \u95e8\u53e3\u901a\u884c\uff08\u672a\u9501\uff09
        return true;                                          // \u5899\u9762 / \u9501\u4f4f\u7684\u95e8
    }
""",
    'arena-hit-thin')

# 4) 锁门条件：要走进深处 + BOSS还活着才锁！
rep("""        if (arena) {
            var ain = Math.sqrt((player.x - arena.x) * (player.x - arena.x) + (player.y - arena.y) * (player.y - arena.y)) < arena.r - 16;
            if (!arena.locked && ain && player.floor === 1) {
                arena.locked = true;
                showMsg('\U0001F512 \u5927\u95e8\u9501\u4e0a\u4e86\uff01\u6253\u8d25 BOSS \u624d\u80fd\u51fa\u53bb\uff01');
            }
        }
""",
    """        if (arena) {
            var ain = Math.sqrt((player.x - arena.x) * (player.x - arena.x) + (player.y - arena.y) * (player.y - arena.y)) < arena.r - 40;
            if (!arena.locked && ain && player.floor === 1 && boss && boss.hp > 0) {
                arena.locked = true;
                showMsg('\U0001F512 \u5927\u95e8\u9501\u4e0a\u4e86\uff01\u6253\u8d25 BOSS \u624d\u80fd\u51fa\u53bb\uff01');
            }
        }
""",
    'lock-boss-alive')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
