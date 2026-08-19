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

# 1) 爬楼半径 900 -> 400（只有楼边的小怪爬上来，远处的走过来）
rep("                    if (sdd < 900 && sdd > 0.01) {\n",
    "                    if (sdd < 400 && sdd > 0.01) {\n",
    'climb-400')

# 2) 子弹命中范围加大（36 -> 42，跟上变大的小怪！）
rep("                if (d < 36) { hitEnemy = j; break; }\n",
    "                if (d < 42) { hitEnemy = j; break; }\n",
    'bullet-hit-42')

# 3) 接触伤害 46 -> 52（大怪贴身更容易打到你）
rep("            if (sameFloor && cd < 46 && player.hitCd <= 0) {\n",
    "            if (sameFloor && cd < 52 && player.hitCd <= 0) {\n",
    'contact-52')

# 4) 伤害保险：防止 NaN 打不死
rep("                e.hp -= b.dmg;\n",
    "                e.hp -= (b.dmg || 30);   // \u4fdd\u9669\uff1a\u5b50\u5f39\u603b\u6709\u4f24\u5bb3\uff0c\u4e0d\u4f1a NaN \u6253\u4e0d\u6b7b\n",
    'dmg-guard')

# 5) 小怪再变大：52 -> 58（主绘制 + 楼顶重绘）
rep("""        ctx.font = '52px sans-serif';
        for (var i = 0; i < enemies.length; i++) {
            var e = enemies[i];
            ctx.fillText(e.ranged ? '\U0001F916' : '\U0001F47E', e.x, e.y + 15);
            ctx.fillStyle = '#333';
            ctx.fillRect(e.x - 32, e.y - 58, 64, 7);
            ctx.fillStyle = '#ff5d5d';
            ctx.fillRect(e.x - 32, e.y - 58, 64 * Math.max(0, e.hp / 100), 7);
            // \U0001F4A0 \u654c\u4eba\u8840\u91cf\u6570\u5b57
            ctx.fillStyle = '#ffd93d';
            ctx.font = 'bold 16px sans-serif';
            ctx.fillText(Math.max(0, e.hp), e.x, e.y - 66);
        }
""",
    """        ctx.font = '58px sans-serif';
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
    'enemy-58-main')

rep("""            ctx.font = '52px sans-serif';
            for (var ri = 0; ri < enemies.length; ri++) {
                var re = enemies[ri];
                if (re.floor === 2 && re.bIdx === player.bIdx) {
                    ctx.fillText(re.ranged ? '\U0001F916' : '\U0001F47E', re.x, re.y + 15);
                    ctx.fillStyle = '#333';
                    ctx.fillRect(re.x - 32, re.y - 58, 64, 7);
                    ctx.fillStyle = '#ff5d5d';
                    ctx.fillRect(re.x - 32, re.y - 58, 64 * Math.max(0, re.hp / 100), 7);
                    ctx.fillStyle = '#ffd93d';
                    ctx.font = 'bold 16px sans-serif';
                    ctx.fillText(Math.max(0, re.hp), re.x, re.y - 66);
                }
            }
""",
    """            ctx.font = '58px sans-serif';
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
    'enemy-58-roof')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
