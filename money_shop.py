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

# 1) 金钱 & 装备 & 武器价格
rep("    var msgTimer = null;\n",
    """    var msgTimer = null;

    // \U0001F4B0 \u91d1\u94b1 & \u88c5\u5907 & \u4e0b\u4e00\u5c40\u6b66\u5668\u88c5\u5907\uff08\u8de8\u5c40\u4fdd\u5b58\uff09
    var money = 0;
    var gear = { hpBonus: 0, bulletsBonus: 0, armor: false };
    var loadout = ['pistol', null];
    try { money = parseInt(localStorage.getItem('sdcMoney') || '0', 10) || 0; } catch (e) {}
    try { gear = JSON.parse(localStorage.getItem('sdcGear') || 'null') || { hpBonus: 0, bulletsBonus: 0, armor: false }; } catch (e) {}
    function saveMoney() { try { localStorage.setItem('sdcMoney', money); } catch (e) {} }
    function saveGear() { try { localStorage.setItem('sdcGear', JSON.stringify(gear)); } catch (e) {} }
    var WEAPON_PRICES = { rifle: 100, shotgun: 150, sniper: 200, smg: 120, gatling: 300, laser: 180, knife: 80 };
""",
    'money-vars')

# 2) resetGame：应用装备 + 保留枪槽
rep("""        player.x = 200; player.y = 200; player.hp = 100; player.bullets = 30;
        player.weapons = ['pistol', null]; player.weaponSlot = 0;
""",
    """        player.x = 200; player.y = 200;
        player.hp = 100 + gear.hpBonus;
        player.bullets = 30 + gear.bulletsBonus;
        player.weapons = loadout.slice(); player.weaponSlot = 0;
""",
    'reset-gear')
rep("""        document.getElementById('hpnum').textContent = '100';
        document.getElementById('bullets').textContent = '手枪 30';
""",
    """        document.getElementById('hpnum').textContent = player.hp;
        document.getElementById('bullets').textContent = WEAPONS[currentWeapon()].name + ' ' + player.bullets;
""",
    'reset-hud-gear')

# 3) 防弹衣减伤
rep("                player.hp -= 12;\n",
    "                player.hp -= Math.round(12 * (gear.armor ? 0.7 : 1));\n",
    'armor-12')
rep("                player.hp -= 9;\n",
    "                player.hp -= Math.round(9 * (gear.armor ? 0.7 : 1));\n",
    'armor-9')

# 4) 商店面板 HTML（插在 over 面板前）
rep("""<div class="panel" id="over" style="display:none">
    <h1 id="over-title">\U0001F3C6 \u64a4\u79bb\u6210\u529f\uff01</h1>
""",
    """<div class="panel" id="shop" style="display:none">
    <h1>\U0001F6D2 \u64a4\u79bb\u5546\u5e97</h1>
    <p id="shop-info"></p>
    <p>\U0001F4B0 \u91d1\u94b1\uff1a<span id="shop-money">0</span></p>
    <p style="font-size:14px;opacity:0.8">\U0001F52B \u6b66\u5668\uff08\u70b9\u51fb\u8d2d\u4e70\uff0c\u81ea\u52a8\u653e\u5165\u67aa\u69fd\uff09</p>
    <div class="shop-grid" id="shop-weapons"></div>
    <p style="font-size:14px;opacity:0.8">\U0001F392 \u88c5\u5907</p>
    <div class="shop-grid" id="shop-gear"></div>
    <p id="shop-slots"></p>
    <button class="btn" id="btn-next">\U0001F680 \u5f00\u59cb\u4e0b\u4e00\u5c40</button>
    <a class="link" href="index.html">\u2b05 \u56de\u5230\u8dd1\u9177\u8005\u7684\u5929\u53f0</a>
</div>

<div class="panel" id="over" style="display:none">
    <h1 id="over-title">\U0001F3C6 \u64a4\u79bb\u6210\u529f\uff01</h1>
""",
    'shop-html')

# 5) 开始面板：金钱 + 商店按钮
rep("""    <button class="btn" id="btn-start">\U0001F680 \u5f00\u59cb\u884c\u52a8</button>
    <a class="link" href="index.html">\u2b05 \u56de\u5230\u8dd1\u9177\u8005\u7684\u5929\u53f0</a>
</div>
""",
    """    <p id="start-money">\U0001F4B0 \u91d1\u94b1\uff1a0</p>
    <button class="btn" id="btn-start">\U0001F680 \u5f00\u59cb\u884c\u52a8</button>
    <button class="btn shop-btn" id="btn-shop">\U0001F6D2 \u5546\u5e97</button>
    <a class="link" href="index.html">\u2b05 \u56de\u5230\u8dd1\u9177\u8005\u7684\u5929\u53f0</a>
</div>
""",
    'start-shop-btn')

# 6) CSS：商店样式
rep("""    .map-btn.active { background: linear-gradient(135deg, #ff7e5f, #feb47b); border-color: transparent; font-weight: bold; }
    .link { display: inline-block; margin-top: 16px; color: #9db2d0; text-decoration: none; font-size: 15px; }
""",
    """    .map-btn.active { background: linear-gradient(135deg, #ff7e5f, #feb47b); border-color: transparent; font-weight: bold; }
    .shop-btn { background: linear-gradient(135deg, #ffd93d, #ffb347); color: #5a3d00; }
    #shop .shop-grid { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; max-width: 760px; margin: 8px auto; }
    .shop-item {
        width: 116px;
        padding: 10px 6px;
        border-radius: 14px;
        border: 2px solid rgba(255, 255, 255, 0.25);
        background: rgba(255, 255, 255, 0.08);
        color: #fff;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.2s;
    }
    .shop-item:hover { border-color: #ffd93d; transform: translateY(-3px); }
    .shop-item .price { color: #ffd93d; font-size: 13px; }
    .shop-item .small { font-size: 11px; opacity: 0.8; }
    #shop-money { color: #ffd93d; font-size: 22px; font-weight: bold; }
    #shop-slots { font-size: 14px; opacity: 0.9; margin-top: 8px; }
    .link { display: inline-block; margin-top: 16px; color: #9db2d0; text-decoration: none; font-size: 15px; }
""",
    'shop-css')

# 7) 商店逻辑函数（插在 checkState 之前）
rep("""    var checkState = setInterval(function () {
""",
    """    // \U0001F6D2 \u5546\u5e97\uff1a\u62bd\u79bb\u6210\u529f\u540e\u7269\u8d44\u5356\u94b1\uff0c\u8d2d\u4e70\u6b66\u5668/\u88c5\u5907\uff01
    function showShop(info) {
        document.getElementById('shop-info').textContent = info;
        document.getElementById('shop').style.display = 'flex';
        document.getElementById('over').style.display = 'none';
        document.getElementById('start-money').textContent = '\U0001F4B0 \u91d1\u94b1\uff1a' + money;
        buildShop();
    }
    function buildShop() {
        document.getElementById('shop-money').textContent = money;
        // \u6b66\u5668\u533a
        var wg = document.getElementById('shop-weapons');
        wg.innerHTML = '';
        var wkeys = ['rifle', 'shotgun', 'sniper', 'smg', 'gatling', 'laser', 'knife'];
        for (var i = 0; i < wkeys.length; i++) {
            (function (w) {
                var btn = document.createElement('button');
                btn.className = 'shop-item';
                btn.innerHTML = (WEAPONS[w].emoji || '\U0001F52B') + ' ' + WEAPONS[w].name +
                    '<br><span class="price">' + WEAPON_PRICES[w] + ' \U0001F4B0</span>';
                btn.addEventListener('click', function () { buyWeapon(w); });
                wg.appendChild(btn);
            })(wkeys[i]);
        }
        // \u88c5\u5907\u533a
        var gg = document.getElementById('shop-gear');
        gg.innerHTML = '';
        var gearItems = [
            { key: 'hp', name: '\u2764\ufe0f \u533b\u7597\u5305', desc: '\u5f00\u5c40 +20 \u8840', price: 50 },
            { key: 'bullet', name: '\U0001F4E6 \u5f39\u836f\u5305', desc: '\u5f00\u5c40 +50 \u5b50\u5f39', price: 60 },
            { key: 'armor', name: '\U0001F6E1\ufe0f \u9632\u5f39\u8863', desc: '\u53d7\u4f24 -30%', price: 100 }
        ];
        for (var i = 0; i < gearItems.length; i++) {
            (function (it) {
                var b2 = document.createElement('button');
                b2.className = 'shop-item';
                b2.innerHTML = it.name + '<br><span class="small">' + it.desc + '</span><br><span class="price">' + it.price + ' \U0001F4B0</span>';
                b2.addEventListener('click', function () { buyGear(it); });
                gg.appendChild(b2);
            })(gearItems[i]);
        }
        updateSlotTxt();
    }
    function updateSlotTxt() {
        var s1 = loadout[0] ? WEAPONS[loadout[0]].name : '\u7a7a';
        var s2 = loadout[1] ? WEAPONS[loadout[1]].name : '\u7a7a';
        document.getElementById('shop-slots').textContent =
            '\U0001F52B \u6211\u7684\u67aa\uff1a1.' + s1 + ' | 2.' + s2 +
            '　\u2764\ufe0f+' + gear.hpBonus + '　\U0001F4E6+' + gear.bulletsBonus + '　\U0001F6E1\ufe0f' + (gear.armor ? '\u6709' : '\u65e0');
    }
    function buyWeapon(w) {
        if (money < WEAPON_PRICES[w]) { showMsg('\U0001F4B0 \u94b1\u4e0d\u591f\uff01'); return; }
        money -= WEAPON_PRICES[w];
        saveMoney();
        if (loadout[0] === null || loadout[0] === 'pistol') loadout[0] = w;
        else loadout[1] = w;
        showMsg('\U0001F6D2 \u8d2d\u4e70' + WEAPONS[w].name + '\uff01');
        buildShop();
    }
    function buyGear(it) {
        if (money < it.price) { showMsg('\U0001F4B0 \u94b1\u4e0d\u591f\uff01'); return; }
        money -= it.price;
        saveMoney();
        if (it.key === 'hp') gear.hpBonus += 20;
        else if (it.key === 'bullet') gear.bulletsBonus += 50;
        else gear.armor = true;
        saveGear();
        showMsg('\U0001F6D2 \u8d2d\u4e70' + it.name + '\uff01');
        buildShop();
    }

    var checkState = setInterval(function () {
""",
    'shop-functions')

# 8) endGame：胜利 -> 结算+商店；失败 -> 物资丢失
rep("""    function endGame(win) {
        document.getElementById('over').style.display = 'flex';
        document.getElementById('over-title').textContent = win ? '\U0001F3C6 \u64a4\u79bb\u6210\u529f\uff01' : '\U0001F480 \u88ab\u654c\u4eba\u6253\u8d25\u4e86\u2026';
        document.getElementById('over-score').textContent =
            '\U0001F4B0 \u5f97\u5206\uff1a' + score + ' \u00b7 \U0001F4E6 \u5f00\u7bb1\uff1a' + cratesOpened + ' \u4e2a \u00b7 \U0001F47E \u51fb\u6740\uff1a' + kills + ' \u4e2a';
        state = 'over';
    }
""",
    """    function endGame(win) {
        state = 'over';
        if (win) {
            // \U0001F3C6 \u64a4\u79bb\u6210\u529f\uff1a\u5e26\u51fa\u7684\u7269\u8d44\u5168\u90e8\u5356\u6389\u6362\u94b1\uff01
            loadout = player.weapons.slice();   // \u5e26\u51fa\u53bb\u7684\u67aa\u4fdd\u7559\u7ed9\u4e0b\u4e00\u5c40
            var earnings = cratesOpened * 20 + kills * 30;
            money += earnings;
            saveMoney();
            showShop('\U0001F3C6 \u64a4\u79bb\u6210\u529f\uff01\u672c\u5c40\u7269\u8d44\u5356\u51fa +' + earnings + ' \U0001F4B0');
        } else {
            // \U0001F480 \u5931\u8d25\uff1a\u7269\u8d44\u5168\u4e22\u4e86\u2026
            document.getElementById('over').style.display = 'flex';
            document.getElementById('over-title').textContent = '\U0001F480 \u88ab\u654c\u4eba\u6253\u8d25\u4e86\u2026';
            document.getElementById('over-score').textContent =
                '\u672c\u5c40\u7269\u8d44\u5168\u90e8\u4e22\u5931\uff01\u00b7 \U0001F4B0 \u91d1\u94b1\uff1a' + money +
                ' \u00b7 \U0001F4E6 \u5f00\u7bb1\uff1a' + cratesOpened + ' \u4e2a \u00b7 \U0001F47E \u51fb\u6740\uff1a' + kills + ' \u4e2a';
        }
    }
""",
    'endgame-shop')

# 9) btn-start：隐藏商店面板
rep("""    document.getElementById('btn-start').addEventListener('click', function () {
        resetGame();
        state = 'play';
        document.getElementById('start').style.display = 'none';
        document.getElementById('over').style.display = 'none';
    });
""",
    """    document.getElementById('btn-start').addEventListener('click', function () {
        resetGame();
        state = 'play';
        document.getElementById('start').style.display = 'none';
        document.getElementById('over').style.display = 'none';
        document.getElementById('shop').style.display = 'none';
    });
""",
    'btn-start-hide-shop')

# 10) 商店按钮 & 下一局
rep("""    var checkState = setInterval(function () {
        if (state === 'win') endGame(true);
""",
    """    document.getElementById('btn-shop').addEventListener('click', function () {
        showShop('\U0001F6D2 \u5546\u5e97\uff08\u5c40\u5916\u8d2d\u4e70\u88c5\u5907\u548c\u6b66\u5668\uff09');
    });
    document.getElementById('btn-next').addEventListener('click', function () {
        document.getElementById('shop').style.display = 'none';
        document.getElementById('start').style.display = 'none';
        resetGame();
        state = 'play';
    });

    var checkState = setInterval(function () {
        if (state === 'win') endGame(true);
""",
    'shop-btns')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
