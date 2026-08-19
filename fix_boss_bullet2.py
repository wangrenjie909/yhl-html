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

# 1) 小怪主绘制 58 -> 64
rep("""        ctx.font = '58px sans-serif';
        for (var i = 0; i < enemies.length; i++) {
            var e = enemies[i];
            ctx.fillText(e.ranged ? '\U0001F916' : '\U0001F47E', e.x, e.y + 17);
            ctx.fillStyle = '#333';
            ctx.fillRect(e.x - 36, e.y - 64, 72, 7);
            ctx.fillStyle = '#ff5d5d';
            ctx.fillRect(e.x - 36, e.y - 64, 72 * Math.max(0, e.hp / 100), 7);
            // \U0001F4A0 \u654c\u4eba\u8840\u91cf\u6570\u5b57
            ctx.fillStyle = '#ffd93d';
            ctx.font = 'bold 16px sans-serif';
            ctx.fillText(Math.max(0, e.hp), e.x, e.y - 72);
        }
""",
    """        ctx.font = '64px sans-serif';
        for (var i = 0; i < enemies.length; i++) {
            var e = enemies[i];
            ctx.fillText(e.ranged ? '\U0001F916' : '\U0001F47E', e.x, e.y + 18);
            ctx.fillStyle = '#333';
            ctx.fillRect(e.x - 38, e.y - 70, 76, 8);
            ctx.fillStyle = '#ff5d5d';
            ctx.fillRect(e.x - 38, e.y - 70, 76 * Math.max(0, e.hp / 100), 8);
            // \U0001F4A0 \u654c\u4eba\u8840\u91cf\u6570\u5b57
            ctx.fillStyle = '#ffd93d';
            ctx.font = 'bold 17px sans-serif';
            ctx.fillText(Math.max(0, e.hp), e.x, e.y - 78);
        }
""",
    'enemy-64-main')

# 2) 楼顶重绘 58 -> 64
rep("""            ctx.font = '58px sans-serif';
            for (var ri = 0; ri < enemies.length; ri++) {
                var re = enemies[ri];
                if (re.floor === 2 && re.bIdx === player.bIdx) {
                    ctx.fillText(re.ranged ? '\U0001F916' : '\U0001F47E', re.x, re.y + 17);
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
                    ctx.fillText(re.ranged ? '\U0001F916' : '\U0001F47E', re.x, re.y + 18);
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

# 3) 子弹命中 42 -> 48
rep("                if (d < 42) { hitEnemy = j; break; }\n",
    "                if (d < 48) { hitEnemy = j; break; }\n",
    'bullet-hit-48')

io.open(path, 'w', encoding='utf-8').write(src)
print('done')
