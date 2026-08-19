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

# 1) 子弹：BOSS 和小怪分开判断！（BOSS 在时也能打小怪！）
rep("""            if (b.life <= 0 || hitWall) {
                bullets.splice(i, 1);
            } else if (boss && boss.hp > 0) {
                var bd = Math.sqrt((boss.x - b.x) * (boss.x - b.x) + (boss.y - b.y) * (boss.y - b.y));
                if (bd < 40) {
                boss.hp -= b.dmg;
                    fx.push({ x: b.x, y: b.y, r: 6, t: 0 });
                    bullets.splice(i, 1);
                    if (boss.hp <= 0) killBoss();
                }
            } else if (hitEnemy >= 0) {
                var e = enemies[hitEnemy];
                e.hp -= (b.dmg || 30);   // 保险：子弹总有伤害，不会 NaN 打不死
                fx.push({ x: b.x, y: b.y, r: 6, t: 0 });
                bullets.splice(i, 1);
                if (e.hp <= 0) killEnemy(hitEnemy);
            }
""",
    """            if (b.life <= 0 || hitWall) {
                bullets.splice(i, 1);
            } else {
                // BOSS 和 小怪分开判断：BOSS 活着也能打小怪！
                var hitBoss = boss && boss.hp > 0 &&
                    Math.sqrt((boss.x - b.x) * (boss.x - b.x) + (boss.y - b.y) * (boss.y - b.y)) < 44;
                if (hitBoss) {
                    boss.hp -= (b.dmg || 30);
                    fx.push({ x: b.x, y: b.y, r: 6, t: 0 });
                    bullets.splice(i, 1);
                    if (boss.hp <= 0) killBoss();
                } else if (hitEnemy >= 0) {
                    var e = enemies[hitEnemy];
                    e.hp -= (b.dmg || 30);
                    fx.push({ x: b.x, y: b.y, r: 6, t: 0 });
                    bullets.splice(i, 1);
                    if (e.hp <= 0) killEnemy(hitEnemy);
                }
            }
""",
    'bullet-boss-fix')

# 2) 小怪再变大：58 -> 64（主绘制）
rep("""        ctx.font = '58px sans-serif';
        for (var i = 0; i < enemies.length; i++) {
            var e = enemies[i];
            ctx.fillText(e.ranged ? '\\U0001F916' : '\\U0001F47E', e.x, e.y + 17);
            ctx.fillStyle = '#333';
            ctx.fillRect(e.x - 36, e.y - 64, 72, 7);
            ctx.fillStyle = '#ff5d5d';
            ctx.fillRect(e.x - 36, e.y - 64, 72 * Math.max(0, e.hp / 100), 7);
            // \\U0001F4A0 \\u654c\\u4eba\\u8840\\u91cf\\u6570\\u5b57
            ctx.fillStyle = '#ffd93d';
            ctx.font = 'bold 16px sans-serif';
            ctx.fillText(Math.max(0, e.hp), e.x, e.y - 72);
        }
""",
    """        ctx.font = '64px sans-serif';
        for (var i = 0; i < enemies.length; i++) {
            var e = enemies[i];
            ctx.fillText(e.ranged ? '\\U0001F916' : '\\U0001F47E', e.x, e.y + 18);
            ctx.fillStyle = '#333';
            ctx.fillRect(e.x - 38, e.y - 70, 76, 8);
            ctx.fillStyle = '#ff5d5d';
            ctx.fillRect(e.x - 38, e.y - 70, 76 * Math.max(0, e.hp / 100), 8);
            // \\U0001F4A0 \\u654c\\u4eba\\u8840\\u91cf\\u6570\\u5b57
            ctx.fillStyle = '#ffd93d';
            ctx.font = 'bold 17px sans-serif';
            ctx.fillText(Math.max(0, e.hp), e.x, e.y - 78);
        }
""",
    'enemy-64-main')

# 3) 小怪再变大：58 -> 64（楼顶重绘）
rep("""            ctx.font = '58px sans-serif';
            for (var ri = 0; ri < enemies.length; ri++) {
                var re = enemies[ri];
                if (re.floor === 2 && re.bIdx === player.bIdx) {
                    ctx.fillText(re.ranged ? '\\U0001F916' : '\\U0001F47E', re.x, re.y + 17);
                    ctx.fillStyle = '#333';
                    ctx.fillRect(re.x - 36, re.y - 64, 72, 7);
                    ctx.fillStyle = '#ff5d5d';
                    ctx.fillRect(re.x - 36, re.y - 64, 72 * Math.max(0, re.hp / 100), 7);
                    ctx.fillStyle = '#ffd93d';
                    ctx.font = 'bold 16px sans-serif';
                    ctx.fillText(Math.max(0, re.hp), re.x, re.y - 72);
                }
            }
""",
    """            ctx.font = '64px sans-serif';
            for (var ri = 0; ri < enemies.length; ri++) {
                var re = enemies[ri];
                if (re.floor === 2 && re.bIdx === player.bIdx) {
                    ctx.fillText(re.ranged ? '\\U0001F916' : '\\U0001F47E', re.x, re.y + 18);
                    ctx.fillStyle = '#333';
                    ctx.fillRect(re.x - 38, re.y - 70, 76, 8);
                    ctx.fillStyle = '#ff5d5d';
                    ctx.fillRect(re.x - 38, re.y - 70, 76 * Math.max(0, re.hp / 100), 8);
                    ctx.fillStyle = '#ffd93d';
                    ctx.font = 'bold 17px sans-serif';
                    ctx.fillText(Math.max(0, re.hp), re.x, re.y - 78);
                }
            }
""",
    'enemy-64-roof')

# 4) 子弹命中范围 42 -> 48
rep("                if (d < 42) { hitEnemy = j; break; }\n",
    "                if (d < 48) { hitEnemy = j; break; }\n",
    'bullet-hit-48')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
