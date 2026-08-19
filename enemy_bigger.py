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

# 1) 小怪再变大！
rep("""        // \U0001F47E \u654c\u4eba\uff08\u8fd1\u6218\U0001F47E / \u8fdc\u7a0b\U0001F916\uff09\u2014\u2014\u53d8\u5927\u4e86\uff01
        ctx.font = '42px sans-serif';
        for (var i = 0; i < enemies.length; i++) {
            var e = enemies[i];
            ctx.fillText(e.ranged ? '\U0001F916' : '\U0001F47E', e.x, e.y + 12);
            ctx.fillStyle = '#333';
            ctx.fillRect(e.x - 26, e.y - 48, 52, 6);
            ctx.fillStyle = '#ff5d5d';
            ctx.fillRect(e.x - 26, e.y - 48, 52 * Math.max(0, e.hp / 100), 6);
            // \U0001F4A0 \u654c\u4eba\u8840\u91cf\u6570\u5b57
            ctx.fillStyle = '#ffd93d';
            ctx.font = 'bold 14px sans-serif';
            ctx.fillText(Math.max(0, e.hp), e.x, e.y - 56);
        }
""",
    """        // \U0001F47E \u654c\u4eba\uff08\u8fd1\u6218\U0001F47E / \u8fdc\u7a0b\U0001F916\uff09\u2014\u2014\u518d\u53d8\u5927\uff01
        ctx.font = '52px sans-serif';
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
    'enemy-big2')

# 2) 命中/接触范围也加大
rep("""                var d = Math.sqrt((e.x - b.x) * (e.x - b.x) + (e.y - b.y) * (e.y - b.y));
                if (d < 30) { hitEnemy = j; break; }
""",
    """                var d = Math.sqrt((e.x - b.x) * (e.x - b.x) + (e.y - b.y) * (e.y - b.y));
                if (d < 36) { hitEnemy = j; break; }
""",
    'bullet-hit-36')
rep("            if (sameFloor && d < 44 && player.hitCd <= 0) {\n",
    "            if (sameFloor && d < 52 && player.hitCd <= 0) {\n",
    'enemy-contact-52')

# 3) 小怪爬楼更积极：900px 内全爬上来！
rep("""                    if (sdd < 420 && sdd > 0.01) {
                        // \u5df2\u7ecf\u9760\u8fd1\u623f\u5b50\uff1a\u76f4\u63a5\u722c\u4e0a 2 \u697c\uff01
""",
    """                    if (sdd < 900 && sdd > 0.01) {
                        // \u5df2\u7ecf\u9760\u8fd1\u623f\u5b50\uff1a\u76f4\u63a5\u722c\u4e0a 2 \u697c\uff01
""",
    'climb-900')

if len(src) != n0:
    print('content changed')
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
