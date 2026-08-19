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

# 1) maxHp 变量
rep("    var player = { x: 200, y: 200, hp: 100, dir: 0, atkCd: 0, hitCd: 0, bullets: 30, weapons: ['pistol', null], weaponSlot: 0 };\n",
    "    var player = { x: 200, y: 200, hp: 100, dir: 0, atkCd: 0, hitCd: 0, bullets: 30, weapons: ['pistol', null], weaponSlot: 0 };\n    var maxHp = 100;   // \u6700\u5927\u8840\u91cf\uff08\u7528\u836f\u3001\u533b\u7597\u5305\u53ef\u4ee5\u52a0\uff09\n",
    'maxhp-var')

# 2) resetGame：maxHp 一起算
rep("        player.hp = 100 + gear.hpBonus + runMeds * 20;   // \u7528\u836f\uff1a\u5f00\u5c40+\u8840\n",
    "        maxHp = 100 + gear.hpBonus + runMeds * 20;   // \u7528\u836f/\u533b\u7597\u5305\u52a0\u6700\u5927\u8840\n        player.hp = maxHp;\n",
    'reset-maxhp')

# 3) 开箱医疗包：按最大血量上限
rep("""            player.hp = Math.min(100, player.hp + 30);
            fx.push({ x: c.x, y: c.y, t: 0, text: '\u2764\ufe0f \u533b\u7597\u5305 +30' });
            showMsg('\U0001F4E6 \u7206\u51fa\u533b\u7597\u5305\uff01\u2764\ufe0f +30\u8840');
            document.getElementById('hpbar').style.width = player.hp + '%';
""",
    """            player.hp = Math.min(maxHp, player.hp + 30);   // \u4ee5\u6700\u5927\u8840\u91cf\u4e3a\u4e0a\u9650\uff01
            fx.push({ x: c.x, y: c.y, t: 0, text: '\u2764\ufe0f \u533b\u7597\u5305 +30' });
            showMsg('\U0001F4E6 \u7206\u51fa\u533b\u7597\u5305\uff01\u2764\ufe0f +30\u8840');
            document.getElementById('hpbar').style.width = (player.hp / maxHp * 100) + '%';
""",
    'heal-maxhp')

# 4) 两处受伤：血条按最大血量比例
rep("""                document.getElementById('hpbar').style.width = Math.max(0, player.hp) + '%';
                document.getElementById('hpnum').textContent = Math.max(0, player.hp);
                if (player.hp <= 0) { player.hp = 0; state = 'lose'; }
            }
        }

        // \U0001F9E8 \u654c\u4eba\u7684\u5b50\u5f39\uff01
""",
    """                document.getElementById('hpbar').style.width = (Math.max(0, player.hp) / maxHp * 100) + '%';
                document.getElementById('hpnum').textContent = Math.max(0, player.hp);
                if (player.hp <= 0) { player.hp = 0; state = 'lose'; }
            }
        }

        // \U0001F9E8 \u654c\u4eba\u7684\u5b50\u5f39\uff01
""",
    'dmg-bar-1')
rep("""                document.getElementById('hpbar').style.width = Math.max(0, player.hp) + '%';
                document.getElementById('hpnum').textContent = Math.max(0, player.hp);
                if (player.hp <= 0) { player.hp = 0; state = 'lose'; }
            }
        }

        // \u26A1 \u6361\u5b50\u5f39\uff08\u67aa\u8981\u6309 E \u624b\u52a8\u62fe\u53d6\uff09
""",
    """                document.getElementById('hpbar').style.width = (Math.max(0, player.hp) / maxHp * 100) + '%';
                document.getElementById('hpnum').textContent = Math.max(0, player.hp);
                if (player.hp <= 0) { player.hp = 0; state = 'lose'; }
            }
        }

        // \u26A1 \u6361\u5b50\u5f39\uff08\u67aa\u8981\u6309 E \u624b\u52a8\u62fe\u53d6\uff09
""",
    'dmg-bar-2')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
