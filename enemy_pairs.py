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

# 敌人成对生成：近战 + 远程 搭伴出现！
rep("""        // 18 \u4e2a\u654c\u4eba\uff1a9 \u8fd1\u6218\uff08\U0001F47E\uff09+ 9 \u8fdc\u7a0b\uff08\U0001F916\uff09\uff0c\u51fa\u751f\u70b9\u9644\u8fd1\u4e0d\u5237\u602a\uff01
        for (var i = 0; i < 18; i++) {
            var x, y, tries = 0;
            do {
                x = 120 + Math.random() * (MAPW - 240);
                y = 120 + Math.random() * (MAPH - 240);
                tries++;
            } while ((rectHit(x, y, 18) || Math.sqrt((x - 200) * (x - 200) + (y - 200) * (y - 200)) < 380) && tries < 80);
            enemies.push({ x: x, y: y, hp: 100, wander: Math.random() * 6.28, ranged: (i % 2) === 1, shotCd: 1.5 + Math.random() });
        }
""",
    """        // 18 \u4e2a\u654c\u4eba\uff1a9 \u8fd1\u6218 + 9 \u8fdc\u7a0b\uff0c\u6210\u5bf9\u51fa\u73b0\uff08\u4e00\u8d77\u642d\u4f34\uff09\uff01\u51fa\u751f\u70b9\u9644\u8fd1\u4e0d\u5237\u602a\uff01
        for (var i = 0; i < 9; i++) {
            var x, y, tries = 0;
            do {
                x = 120 + Math.random() * (MAPW - 240);
                y = 120 + Math.random() * (MAPH - 240);
                tries++;
            } while ((rectHit(x, y, 18) || Math.sqrt((x - 200) * (x - 200) + (y - 200) * (y - 200)) < 380) && tries < 80);
            // \U0001F47E \u8fd1\u6218
            enemies.push({ x: x, y: y, hp: 100, wander: Math.random() * 6.28, ranged: false, shotCd: 1.5 + Math.random() });
            // \U0001F916 \u8fdc\u7a0b\uff1a\u5c31\u5728\u8fd1\u6218\u65c1\u8fb9\uff08200~320px\uff09\uff0c\u4e24\u79cd\u59cb\u7ec8\u5728\u4e00\u8d77\uff01
            var ang = Math.random() * 6.28;
            var dist = 200 + Math.random() * 120;
            var x2 = Math.max(20, Math.min(MAPW - 20, x + Math.cos(ang) * dist));
            var y2 = Math.max(20, Math.min(MAPH - 20, y + Math.sin(ang) * dist));
            enemies.push({ x: x2, y: y2, hp: 100, wander: Math.random() * 6.28, ranged: true, shotCd: 1.5 + Math.random() });
        }
""",
    'enemies-pairs')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
