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

# 1) 刀：先扣血再判断死亡（免费刀2刀、小刀1刀）
rep("""                fx.push({ x: player.x + Math.cos(player.dir) * 45, y: player.y + Math.sin(player.dir) * 45, t: 0, slash: player.dir });
                for (var mi = enemies.length - 1; mi >= 0; mi--) {
                    var me = enemies[mi];
                    var md2 = Math.sqrt((me.x - player.x) * (me.x - player.x) + (me.y - player.y) * (me.y - player.y));
                    var angTo = Math.atan2(me.y - player.y, me.x - player.x);
                    var diff = Math.abs(angTo - player.dir);
                    if (diff > Math.PI) diff = Math.PI * 2 - diff;
                    if (md2 < 95 && diff < 1.0) killEnemy(mi);   // \U0001F52A \u4e00\u5200\u79d2\uff01
                }
""",
    """                fx.push({ x: player.x + Math.cos(player.dir) * 45, y: player.y + Math.sin(player.dir) * 45, t: 0, slash: player.dir });
                for (var mi = enemies.length - 1; mi >= 0; mi--) {
                    var me = enemies[mi];
                    var md2 = Math.sqrt((me.x - player.x) * (me.x - player.x) + (me.y - player.y) * (me.y - player.y));
                    var angTo = Math.atan2(me.y - player.y, me.x - player.x);
                    var diff = Math.abs(angTo - player.dir);
                    if (diff > Math.PI) diff = Math.PI * 2 - diff;
                    if (md2 < 95 && diff < 1.0) {
                        me.hp -= wg.dmg;   // \U0001F52A \u5148\u6263\u8840\uff01\u514d\u8d39\u5200\u8d34 2 \u5200\u624d\u80fd\u780d\u6b7b\uff01
                        fx.push({ x: me.x, y: me.y, r: 6, t: 0 });
                        if (me.hp <= 0) killEnemy(mi);
                        else showMsg('\U0001F52A \u780d\u4e2d\u654c\u4eba\uff01');
                    }
                }
""",
    'knife-hp')

# 2) 敌人交替生成：近战、远程、近战、远程…
rep("""            enemies.push({ x: x, y: y, hp: 100, wander: Math.random() * 6.28, ranged: i >= 9, shotCd: 1.5 + Math.random() });
""",
    """            enemies.push({ x: x, y: y, hp: 100, wander: Math.random() * 6.28, ranged: (i % 2) === 1, shotCd: 1.5 + Math.random() });
""",
    'enemies-alternate')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
