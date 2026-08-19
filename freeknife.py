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

# 1) WEAPONS：小刀改名 + 免费刀（2刀杀敌）
rep("""        knife:   { name: '\u5200',     emoji: '\U0001F52A', dmg: 999, rate: 0.4, melee: true }
    };
""",
    """        knife:     { name: '\u5c0f\u5200',   emoji: '\U0001F52A', dmg: 999, rate: 0.4, melee: true },
        freeknife: { name: '\u514d\u8d39\u5200', emoji: '\U0001F5E1\ufe0f', dmg: 50,  rate: 0.4, melee: true }
    };
""",
    'weapons-freeknife')

# 2) 商店武器区：免费刀排第一
rep("""        var wkeys = ['rifle', 'shotgun', 'sniper', 'smg', 'gatling', 'laser', 'knife'];
""",
    """        var wkeys = ['freeknife', 'rifle', 'shotgun', 'sniper', 'smg', 'gatling', 'laser', 'knife'];
""",
    'shop-wkeys')
rep("""                btn.innerHTML = (WEAPONS[w].emoji || '\U0001F52B') + ' ' + WEAPONS[w].name +
                    '<br><span class="price">' + WEAPON_PRICES[w] + ' \U0001F4B0</span>';
""",
    """                btn.innerHTML = (WEAPONS[w].emoji || '\U0001F52B') + ' ' + WEAPONS[w].name +
                    '<br><span class="price">' + (w === 'freeknife' ? '\u514d\u8d39' : WEAPON_PRICES[w] + ' \U0001F4B0') + '</span>';
""",
    'shop-price-free')

# 3) buyWeapon：免费刀 0 元
rep("""    function buyWeapon(w) {
        if (money < WEAPON_PRICES[w]) { showMsg('\U0001F4B0 \u94b1\u4e0d\u591f\uff01'); return; }
        money -= WEAPON_PRICES[w];
        saveMoney();
        if (loadout[0] === null || loadout[0] === 'pistol') loadout[0] = w;
        else loadout[1] = w;
        showMsg('\U0001F6D2 \u8d2d\u4e70' + WEAPONS[w].name + '\uff01');
        buildShop();
    }
""",
    """    function buyWeapon(w) {
        var price = w === 'freeknife' ? 0 : WEAPON_PRICES[w];
        if (money < price) { showMsg('\U0001F4B0 \u94b1\u4e0d\u591f\uff01'); return; }
        money -= price;
        saveMoney();
        if (loadout[0] === null || loadout[0] === 'pistol') loadout[0] = w;
        else loadout[1] = w;
        showMsg(w === 'freeknife' ? '\U0001F5E1\ufe0f \u83b7\u5f97\u514d\u8d39\u5200\uff01' : '\U0001F6D2 \u8d2d\u4e70' + WEAPONS[w].name + '\uff01');
        buildShop();
    }
""",
    'buy-freeknife')

# 4) 商店：返回主界面按钮
rep("""    <button class="btn" id="btn-next">\U0001F680 \u5f00\u59cb\u4e0b\u4e00\u5c40</button>
    <a class="link" href="index.html">\u2b05 \u56de\u5230\u8dd1\u9177\u8005\u7684\u5929\u53f0</a>
</div>
""",
    """    <button class="btn" id="btn-next">\U0001F680 \u5f00\u59cb\u4e0b\u4e00\u5c40</button>
    <button class="btn shop-btn" id="btn-back">\u2b05 \u8fd4\u56de\u4e3b\u754c\u9762</button>
    <a class="link" href="index.html">\u2b05 \u56de\u5230\u8dd1\u9177\u8005\u7684\u5929\u53f0</a>
</div>
""",
    'btn-back-html')

# 5) btn-back 监听
rep("""    document.getElementById('btn-next').addEventListener('click', function () {
        document.getElementById('shop').style.display = 'none';
        document.getElementById('start').style.display = 'none';
        resetGame();
        state = 'play';
    });
""",
    """    document.getElementById('btn-next').addEventListener('click', function () {
        document.getElementById('shop').style.display = 'none';
        document.getElementById('start').style.display = 'none';
        resetGame();
        state = 'play';
    });
    document.getElementById('btn-back').addEventListener('click', function () {
        document.getElementById('shop').style.display = 'none';
        document.getElementById('start').style.display = 'flex';
        document.getElementById('start-money').textContent = '\U0001F4B0 \u91d1\u94b1\uff1a' + money;
    });
""",
    'btn-back-js')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
