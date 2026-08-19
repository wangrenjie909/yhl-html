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

# 1) 仓库数据（localStorage 保存）
rep("    var WEAPON_PRICES = { rifle: 100, shotgun: 150, sniper: 200, smg: 120, gatling: 300, laser: 180, knife: 80 };\n",
    """    var WEAPON_PRICES = { rifle: 100, shotgun: 150, sniper: 200, smg: 120, gatling: 300, laser: 180, knife: 80 };

    // \U0001F3E0 \u4ed3\u5e93\uff1a\u5e26\u51fa\u53BB\u7684\u4E1C\u897F\u5B58\u8FD9\u91CC\uff08\u67AA/\u7532/\u836F\uff09
    var stash = { guns: [], armor: 0, meds: 0 };
    var runArmor = false, runMeds = 0;   // \u672C\u5C40\u7A7F\u7532\u3001\u7528\u836F
    try { stash = JSON.parse(localStorage.getItem('sdcStash') || 'null') || { guns: [], armor: 0, meds: 0 }; } catch (e) {}
    function saveStash() { try { localStorage.setItem('sdcStash', JSON.stringify(stash)); } catch (e) {} }
""",
    'stash-vars')

# 2) resetGame：开局应用 仓库装备 + 用药加血
rep("""        player.x = 200; player.y = 200;
        player.hp = 100 + gear.hpBonus;
        player.bullets = 30 + gear.bulletsBonus;
        player.weapons = loadout.slice(); player.weaponSlot = 0;
""",
    """        player.x = 200; player.y = 200;
        player.hp = 100 + gear.hpBonus + runMeds * 20;   // \u7528\u836F\uff1a\u5F00\u5C40+\u8840
        player.bullets = 30 + gear.bulletsBonus;
        player.weapons = loadout.slice(); player.weaponSlot = 0;
""",
    'reset-warehouse')

# 3) 防弹衣减伤：仓库穿甲也算
rep("                player.hp -= Math.round(12 * (gear.armor ? 0.7 : 1));\n",
    "                player.hp -= Math.round(12 * ((gear.armor || runArmor) ? 0.7 : 1));\n",
    'armor-12-wh')
rep("                player.hp -= Math.round(9 * (gear.armor ? 0.7 : 1));\n",
    "                player.hp -= Math.round(9 * ((gear.armor || runArmor) ? 0.7 : 1));\n",
    'armor-9-wh')

# 4) endGame：带出的枪进仓库、甲消耗、装备归零
rep("""    function endGame(win) {
        state = 'over';
        if (win) {
            // \U0001F3C6 \u64a4\u79bb\u6210\u529f\uff1a\u5e26\u51fa\u7684\u7269\u8d44\u5168\u90e8\u5356\u6389\u6362\u94b1\uff01
            loadout = player.weapons.slice();   // \u5e26\u51fa\u53bb\u7684\u67aa\u4fdd\u7559\u7ed9\u4e0b\u4e00\u5c40
            var earnings = cratesOpened * 20 + kills * 30;
            money += earnings;
            saveMoney();
            showShop('\U0001F3C6 \u64a4\u79bb\u6210\u529f\uff01\u672c\u5c40\u7269\u8d44\u5356\u51fa +' + earnings + ' \U0001F4B0');
        } else {
""",
    """    function endGame(win) {
        state = 'over';
        // \u7A7F\u8FC7\u7684\u7532\u7528\u5B8C\uff1b\u7528\u8FC7\u7684\u836F\u5DF2\u6D88\u8017
        if (runArmor) stash.armor = Math.max(0, stash.armor - 1);
        runArmor = false; runMeds = 0;
        saveStash();
        if (win) {
            // \U0001F3C6 \u64A4\u79BB\u6210\u529F\uff1A\u7269\u8D44\u5356\u94B1\uff0C\u5E26\u51FA\u7684\u67AA\u5B58\u8FDB\u4ED3\u5E93\uff01
            for (var ci = 0; ci < player.weapons.length; ci++) {
                if (player.weapons[ci] && player.weapons[ci] !== 'pistol') stash.guns.push(player.weapons[ci]);
            }
            loadout = ['pistol', null];   // \u4E0B\u4E00\u5C40\u91CD\u65B0\u4ECE\u4ED3\u5E93\u88C5\u5907
            saveStash();
            var earnings = cratesOpened * 20 + kills * 30;
            money += earnings;
            saveMoney();
            showShop('\U0001F3C6 \u64A4\u79BB\u6210\u529F\uff01\u672C\u5C40\u7269\u8D44\u5356\u51FA +' + earnings + ' \U0001F4B0\uff08\u5E26\u7684\u67AA\u5DF2\u5B58\u5165\u4ED3\u5E93\U0001F3E0\uff09');
        } else {
""",
    'endgame-stash')

# 5) 商店装备：防弹衣/药品 进仓库
rep("""        var gearItems = [
            { key: 'hp', name: '\u2764\ufe0f \u533b\u7597\u5305', desc: '\u5f00\u5c40 +20 \u8840', price: 50 },
            { key: 'bullet', name: '\U0001F4E6 \u5f39\u836f\u5305', desc: '\u5f00\u5c40 +50 \u5b50\u5f39', price: 60 },
            { key: 'armor', name: '\U0001F6E1\ufe0f \u9632\u5f39\u8863', desc: '\u53d7\u4f24 -30%', price: 100 }
        ];
""",
    """        var gearItems = [
            { key: 'hp', name: '\u2764\ufe0f \u533b\u7597\u5305', desc: '\u5f00\u5c40 +20 \u8840', price: 50 },
            { key: 'bullet', name: '\U0001F4E6 \u5f39\u836f\u5305', desc: '\u5f00\u5c40 +50 \u5b50\u5f39', price: 60 },
            { key: 'armor', name: '\U0001F6E1\ufe0f \u9632\u5f39\u8863', desc: '\u4e00\u4ef6\u7532\uff08\u5b58\u4ed3\u5e93\uff09', price: 100 },
            { key: 'med', name: '\U0001F48A \u836f\u54c1', desc: '\u5b58\u4ed3\u5e93\uff0c\u7528\u4e86\u5f00\u5c40 +20\u8840', price: 40 }
        ];
""",
    'shop-gear-items')
rep("""        if (it.key === 'hp') gear.hpBonus += 20;
        else if (it.key === 'bullet') gear.bulletsBonus += 50;
        else gear.armor = true;
        saveGear();
""",
    """        if (it.key === 'hp') { gear.hpBonus += 20; saveGear(); }
        else if (it.key === 'bullet') { gear.bulletsBonus += 50; saveGear(); }
        else if (it.key === 'med') { stash.meds++; saveStash(); showMsg('\U0001F6D2 \u8d2d\u4e70\u836f\u54c1\uff01\u5b58\u5165\u4ed3\u5e93'); }
        else { stash.armor++; saveStash(); showMsg('\U0001F6D2 \u8d2d\u4e70\u7532\uff01\u5b58\u5165\u4ed3\u5e93'); }
""",
    'buygear-stash')
rep("""            '　\u2764\ufe0f+' + gear.hpBonus + '　\U0001F4E6+' + gear.bulletsBonus + '　\U0001F6E1\ufe0f' + (gear.armor ? '\u6709' : '\u65e0');
""",
    """            '　\u2764\ufe0f+' + gear.hpBonus + '　\U0001F4E6+' + gear.bulletsBonus + '　\U0001F6E1\ufe0f\u4ed3\u5e93\u7532x' + stash.armor;
""",
    'shop-slot-armor')

# 6) 仓库面板 HTML（插在 shop 面板前）
rep("""<div class="panel" id="shop" style="display:none">
""",
    """<div class="panel" id="warehouse" style="display:none">
    <h1>\U0001F3E0 \u4ed3\u5e93</h1>
    <p>\u5e26\u51fa\u6765\u7684\u4e1c\u897f\u90fd\u5b58\u5728\u8fd9\u91cc\uff01</p>
    <p style="font-size:14px;opacity:0.8">\U0001F52B \u67aa\u68f0\uff08\u70b9\u51fb\u88c5\u5907 / \u5378\u4e0b\uff09</p>
    <div class="shop-grid" id="wh-guns"></div>
    <p style="font-size:14px;opacity:0.8">\U0001F6E1\ufe0f \u7532 x<span id="wh-armor">0</span>　\U0001F48A \u836f x<span id="wh-meds">0</span></p>
    <div class="shop-grid" id="wh-gear"></div>
    <p id="wh-loadout"></p>
    <button class="btn" id="btn-wh-close">\u2705 \u5b8c\u6210</button>
    <a class="link" href="index.html">\u2b05 \u56de\u5230\u8dd1\u9177\u8005\u7684\u5929\u53f0</a>
</div>

<div class="panel" id="shop" style="display:none">
""",
    'warehouse-html')

# 7) 主页 + 商店：加 仓库 按钮
rep("""    <button class="btn shop-btn" id="btn-shop">\U0001F6D2 \u5546\u5e97</button>
    <a class="link" href="index.html">\u2b05 \u56de\u5230\u8dd1\u9177\u8005\u7684\u5929\u53f0</a>
</div>
""",
    """    <button class="btn shop-btn" id="btn-shop">\U0001F6D2 \u5546\u5e97</button>
    <button class="btn" id="btn-wh">\U0001F3E0 \u4ed3\u5e93</button>
    <a class="link" href="index.html">\u2b05 \u56de\u5230\u8dd1\u9177\u8005\u7684\u5929\u53f0</a>
</div>
""",
    'start-wh-btn')
rep("""    <button class="btn shop-btn" id="btn-back">\u2b05 \u8fd4\u56de\u4e3b\u754c\u9762</button>
    <a class="link" href="index.html">\u2b05 \u56de\u5230\u8dd1\u9177\u8005\u7684\u5929\u53f0</a>
</div>
""",
    """    <button class="btn shop-btn" id="btn-back">\u2b05 \u8fd4\u56de\u4e3b\u754c\u9762</button>
    <button class="btn" id="btn-wh-shop">\U0001F3E0 \u4ed3\u5e93</button>
    <a class="link" href="index.html">\u2b05 \u56de\u5230\u8dd1\u9177\u8005\u7684\u5929\u53f0</a>
</div>
""",
    'shop-wh-btn')

# 8) 仓库逻辑（插在 btn-shop 监听前）
rep("""    document.getElementById('btn-shop').addEventListener('click', function () {
""",
    """    // \U0001F3E0 \u4ed3\u5e93\uff1a\u88c5\u5907\u67aa / \u7a7f\u7532 / \u7528\u836f
    var whFrom = 'start';
    function showWarehouse() {
        buildWarehouse();
        document.getElementById('warehouse').style.display = 'flex';
    }
    function buildWarehouse() {
        // \u67aa
        var g = document.getElementById('wh-guns');
        g.innerHTML = '';
        for (var i = 0; i < stash.guns.length; i++) {
            (function (w) {
                var equipped = loadout.indexOf(w) >= 0;
                var btn = document.createElement('button');
                btn.className = 'shop-item';
                btn.innerHTML = (WEAPONS[w].emoji || '\U0001F52B') + ' ' + WEAPONS[w].name +
                    '<br><span class="small">' + (equipped ? '\u5df2\u88c5\u5907 \u2713' : '\u70b9\u51fb\u88c5\u5907') + '</span>';
                btn.addEventListener('click', function () {
                    if (equipped) {
                        var k = loadout.indexOf(w);
                        if (k >= 0) loadout[k] = null;
                    } else {
                        if (loadout[0] === null || loadout[0] === 'pistol') loadout[0] = w;
                        else if (loadout[1] === null) loadout[1] = w;
                        else { showMsg('\u67aa\u69fd\u6ee1\u4e86\uff01'); return; }
                    }
                    buildWarehouse();
                });
                g.appendChild(btn);
            })(stash.guns[i]);
        }
        // \u7532 / \u836f
        var gg = document.getElementById('wh-gear');
        gg.innerHTML = '';
        var bA = document.createElement('button');
        bA.className = 'shop-item';
        bA.innerHTML = '\U0001F6E1\ufe0f \u7a7f\u7532\u51fa\u6218' + (runArmor ? '\uff08\u5df2\u7a7f\uff09' : '') + '<br><span class="small">\u7532 x' + stash.armor + '</span>';
        bA.addEventListener('click', function () {
            if (runArmor) { runArmor = false; }
            else if (stash.armor > 0) { runArmor = true; showMsg('\U0001F6E1\ufe0f \u672c\u5c40\u7a7f\u7532\uff01\u53d7\u4f24\u51cf\u5c11'); }
            else showMsg('\U0001F3E0 \u4ed3\u5e93\u91cc\u6ca1\u6709\u7532\uff01\u53bb\u5546\u5e97\u4e70');
            buildWarehouse();
        });
        gg.appendChild(bA);
        var bM = document.createElement('button');
        bM.className = 'shop-item';
        bM.innerHTML = '\U0001F48A \u7528\u836f' + (runMeds > 0 ? '\uff08\u5df2\u7528' + runMeds + '\uff09' : '') + '<br><span class="small">\u5f00\u5c40+20\u8840 \u00b7 \u836f x' + stash.meds + '</span>';
        bM.addEventListener('click', function () {
            if (stash.meds > 0) { stash.meds--; runMeds++; saveStash(); showMsg('\U0001F48A \u7528\u836f\uff01\u4e0b\u4e00\u5c40\u5f00\u5c40 +20\u8840'); }
            else showMsg('\U0001F3E0 \u4ed3\u5e93\u91cc\u6ca1\u6709\u836f\uff01\u53bb\u5546\u5e97\u4e70');
            buildWarehouse();
        });
        gg.appendChild(bM);
        document.getElementById('wh-armor').textContent = stash.armor;
        document.getElementById('wh-meds').textContent = stash.meds;
        var s1 = loadout[0] ? WEAPONS[loadout[0]].name : '\u7a7a';
        var s2 = loadout[1] ? WEAPONS[loadout[1]].name : '\u7a7a';
        document.getElementById('wh-loadout').textContent =
            '\U0001F392 \u51fa\u6218\u88c5\u5907\uff1a1.' + s1 + ' | 2.' + s2 +
            (runArmor ? ' \U0001F6E1\ufe0f\u7a7f\u7532' : '') + (runMeds > 0 ? ' \U0001F48Ax' + runMeds : '');
    }
    document.getElementById('btn-wh').addEventListener('click', function () { whFrom = 'start'; showWarehouse(); });
    document.getElementById('btn-wh-shop').addEventListener('click', function () { whFrom = 'shop'; showWarehouse(); });
    document.getElementById('btn-wh-close').addEventListener('click', function () {
        document.getElementById('warehouse').style.display = 'none';
        if (whFrom === 'shop') {
            document.getElementById('shop').style.display = 'flex';
            buildShop();
        } else {
            document.getElementById('start').style.display = 'flex';
            document.getElementById('start-money').textContent = '\U0001F4B0 \u91d1\u94b1\uff1a' + money;
        }
    });

    document.getElementById('btn-shop').addEventListener('click', function () {
""",
    'warehouse-logic')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
