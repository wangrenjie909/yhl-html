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

# 1) 仓库数据 → 24格背包
rep("""    // \U0001F3E0 \u4ed3\u5e93\uff1a\u5e26\u51fa\u53bb\u7684\u4e1c\u897f\u5b58\u8fd9\u91cc\uff08\u67aa/\u7532/\u836f\uff09
    var stash = { guns: [], armor: 0, meds: 0 };
    var runArmor = false, runMeds = 0;   // \u672c\u5c40\u7a7f\u7532\u3001\u7528\u836f
    try { stash = JSON.parse(localStorage.getItem('sdcStash') || 'null') || { guns: [], armor: 0, meds: 0 }; } catch (e) {}
    function saveStash() { try { localStorage.setItem('sdcStash', JSON.stringify(stash)); } catch (e) {} }
""",
    """    // \U0001F3E0 \u4ed3\u5e93\uff1a24\u683c\u80cc\u5305\uff0c\u6bcf\u683c\u653e\u4e00\u4ef6\uff08\u67aa/\u7532/\u5934/\u836f/\u7532\u4fee\uff09
    var INV_SIZE = 24;
    var inv = new Array(INV_SIZE).fill(null);
    var wornArmor = -1, wornHelmet = -1;   // \u672c\u5c40\u7a7f\u7684\u7532/\u5934\u5728 inv \u4e2d\u7684\u4e0b\u6807
    var runMeds = 0;                       // \u672c\u5c40\u7528\u4e86\u51e0\u4e2a\u836f
    function addInv(it) {
        for (var i = 0; i < INV_SIZE; i++) {
            if (!inv[i]) { inv[i] = it; return i; }
        }
        return -1;   // \u80cc\u5305\u6ee1\u4e86
    }
    try {
        var savedInv = JSON.parse(localStorage.getItem('sdcInv') || 'null');
        if (savedInv && savedInv.length === INV_SIZE) {
            inv = savedInv;
        } else {
            var old = JSON.parse(localStorage.getItem('sdcStash') || 'null');
            if (old) {
                for (var g = 0; g < (old.guns || []).length; g++) addInv({ t: 'gun', w: old.guns[g] });
                for (var a = 0; a < (old.armor || 0); a++) addInv({ t: 'armor', d: 3 });
                for (var m = 0; m < (old.meds || 0); m++) addInv({ t: 'med' });
            }
        }
    } catch (e) {}
    // \u65e7\u7248\u672c\u4e70\u8fc7\u7684\u9632\u5f39\u8863\u8fc1\u79fb\u6210\u4e00\u4ef6\u7532
    if (gear.armor) { gear.armor = false; saveGear(); addInv({ t: 'armor', d: 3 }); }
    function saveInv() { try { localStorage.setItem('sdcInv', JSON.stringify(inv)); } catch (e) {} }
""",
    'inv-system')

# 2) 伤害：甲+头盔
rep("                player.hp -= Math.round(12 * ((gear.armor || runArmor) ? 0.7 : 1));\n",
    "                player.hp -= Math.round(12 * ((gear.armor || wornArmor >= 0) ? 0.7 : 1) * (wornHelmet >= 0 ? 0.8 : 1));\n",
    'dmg-12')
rep("                player.hp -= Math.round(9 * ((gear.armor || runArmor) ? 0.7 : 1));\n",
    "                player.hp -= Math.round(9 * ((gear.armor || wornArmor >= 0) ? 0.7 : 1) * (wornHelmet >= 0 ? 0.8 : 1));\n",
    'dmg-9')

# 3) endGame：枪进背包、甲/头扣耐久
rep("""        // \u7a7f\u8fc7\u7684\u7532\u7528\u5b8c\uff1b\u7528\u8fc7\u7684\u836f\u5df2\u6d88\u8017
        if (runArmor) stash.armor = Math.max(0, stash.armor - 1);
        runArmor = false; runMeds = 0;
        saveStash();
        if (win) {
            // \U0001F3C6 \u64a4\u79bb\u6210\u529f\uff1a\u7269\u8d44\u5356\u94b1\uff0c\u5e26\u51fa\u7684\u67aa\u5b58\u8fdb\u4ed3\u5e93\uff01
            for (var ci = 0; ci < player.weapons.length; ci++) {
                if (player.weapons[ci] && player.weapons[ci] !== 'pistol') stash.guns.push(player.weapons[ci]);
            }
            loadout = ['pistol', null];   // \u4e0b\u4e00\u5c40\u91cd\u65b0\u4ece\u4ed3\u5e93\u88c5\u5907
            saveStash();
""",
    """        // \u7a7f\u8fc7\u7684\u7532/\u5934\u6263\u8010\u4e45\uff1b\u7528\u8fc7\u7684\u836f\u5df2\u6d88\u8017
        if (wornArmor >= 0 && inv[wornArmor]) {
            inv[wornArmor].d -= 1;
            if (inv[wornArmor].d <= 0) inv[wornArmor] = null;
        }
        if (wornHelmet >= 0 && inv[wornHelmet]) {
            inv[wornHelmet].d -= 1;
            if (inv[wornHelmet].d <= 0) inv[wornHelmet] = null;
        }
        wornArmor = -1; wornHelmet = -1; runMeds = 0;
        saveInv();
        if (win) {
            // \U0001F3C6 \u64a4\u79bb\u6210\u529f\uff1a\u7269\u8d44\u5356\u94b1\uff0c\u5e26\u51fa\u7684\u67aa\u5b58\u8fdb\u80cc\u5305\uff01
            for (var ci = 0; ci < player.weapons.length; ci++) {
                if (player.weapons[ci] && player.weapons[ci] !== 'pistol') addInv({ t: 'gun', w: player.weapons[ci] });
            }
            loadout = ['pistol', null];   // \u4e0b\u4e00\u5c40\u91cd\u65b0\u4ece\u80cc\u5305\u88c5\u5907
            saveInv();
""",
    'endgame-inv')

# 4) 商店装备列表：加 头盔 + 甲修
rep("""        var gearItems = [
            { key: 'hp', name: '\u2764\ufe0f \u533b\u7597\u5305', desc: '\u5f00\u5c40 +20 \u8840', price: 50 },
            { key: 'bullet', name: '\U0001F4E6 \u5f39\u836f\u5305', desc: '\u5f00\u5c40 +50 \u5b50\u5f39', price: 60 },
            { key: 'armor', name: '\U0001F6E1\ufe0f \u9632\u5f39\u8863', desc: '\u4e00\u4ef6\u7532\uff08\u5b58\u4ed3\u5e93\uff09', price: 100 },
            { key: 'med', name: '\U0001F48A \u836f\u54c1', desc: '\u5b58\u4ed3\u5e93\uff0c\u7528\u4e86\u5f00\u5c40 +20\u8840', price: 40 }
        ];
""",
    """        var gearItems = [
            { key: 'hp', name: '\u2764\ufe0f \u533b\u7597\u5305', desc: '\u5f00\u5c40 +20 \u8840\uff08\u6c38\u4e45\uff09', price: 50 },
            { key: 'bullet', name: '\U0001F4E6 \u5f39\u836f\u5305', desc: '\u5f00\u5c40 +50 \u5b50\u5f39\uff08\u6c38\u4e45\uff09', price: 60 },
            { key: 'armor', name: '\U0001F6E1\ufe0f \u9632\u5f39\u8863', desc: '1\u4ef6\u7532\u8fdb\u80cc\u5305\uff083\u8010\u4e45\uff09', price: 100 },
            { key: 'helmet', name: '\U0001FA96 \u5934\u76d4', desc: '1\u4e2a\u5934\u8fdb\u80cc\u5305\uff083\u8010\u4e45\uff09', price: 80 },
            { key: 'med', name: '\U0001F48A \u836f\u54c1', desc: '1\u4e2a\u836f\u8fdb\u80cc\u5305\uff0c\u7528+20\u8840', price: 40 },
            { key: 'repair', name: '\U0001F9F0 \u7532\u4fee', desc: '\u4fee\u7406\u7532/\u5934\u76d4 +1\u8010\u4e45', price: 30 }
        ];
""",
    'shop-gear-items')
rep("""        if (it.key === 'hp') { gear.hpBonus += 20; saveGear(); }
        else if (it.key === 'bullet') { gear.bulletsBonus += 50; saveGear(); }
        else if (it.key === 'med') { stash.meds++; saveStash(); showMsg('\U0001F6D2 \u8d2d\u4e70\u836f\u54c1\uff01\u5b58\u5165\u4ed3\u5e93'); }
        else { stash.armor++; saveStash(); showMsg('\U0001F6D2 \u8d2d\u4e70\u7532\uff01\u5b58\u5165\u4ed3\u5e93'); }
""",
    """        if (it.key === 'hp') { gear.hpBonus += 20; saveGear(); }
        else if (it.key === 'bullet') { gear.bulletsBonus += 50; saveGear(); }
        else if (it.key === 'armor') { addInv({ t: 'armor', d: 3 }); saveInv(); showMsg('\U0001F6D2 \u8d2d\u4e70\u7532\uff01\u5b58\u5165\u80cc\u5305'); }
        else if (it.key === 'helmet') { addInv({ t: 'helmet', d: 3 }); saveInv(); showMsg('\U0001F6D2 \u8d2d\u4e70\u5934\u76d4\uff01\u5b58\u5165\u80cc\u5305'); }
        else if (it.key === 'med') { addInv({ t: 'med' }); saveInv(); showMsg('\U0001F6D2 \u8d2d\u4e70\u836f\u54c1\uff01\u5b58\u5165\u80cc\u5305'); }
        else if (it.key === 'repair') { addInv({ t: 'repair' }); saveInv(); showMsg('\U0001F6D2 \u8d2d\u4e70\u7532\u4fee\uff01\u5b58\u5165\u80cc\u5305'); }
""",
    'buygear-inv')
rep("""            '　\u2764\ufe0f+' + gear.hpBonus + '　\U0001F4E6+' + gear.bulletsBonus + '　\U0001F6E1\ufe0f\u4ed3\u5e93\u7532x' + stash.armor;
""",
    """            '　\u2764\ufe0f+' + gear.hpBonus + '　\U0001F4E6+' + gear.bulletsBonus + '　\U0001F6E1\ufe0f\u7532x' + (inv.filter(function (x) { return x && x.t === 'armor'; }).length) + '　\U0001FA96\u5934x' + (inv.filter(function (x) { return x && x.t === 'helmet'; }).length);
""",
    'shop-slot-counts')

# 5) 仓库面板 HTML → 格子
rep("""<div class="panel" id="warehouse" style="display:none">
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
""",
    """<div class="panel" id="warehouse" style="display:none">
    <h1>\U0001F3E0 \u4ed3\u5e93</h1>
    <p>\u5e26\u51fa\u6765\u7684\u4e1c\u897f\u90fd\u5b58\u5728\u8fd9\u91cc\uff08\u4e00\u683c\u4e00\u4ef6\uff09\uff01</p>
    <div class="wh-grid" id="wh-grid"></div>
    <p id="wh-loadout"></p>
    <button class="btn" id="btn-wh-close">\u2705 \u5b8c\u6210</button>
    <a class="link" href="index.html">\u2b05 \u56de\u5230\u8dd1\u9177\u8005\u7684\u5929\u53f0</a>
</div>
""",
    'warehouse-html')

# 6) buildWarehouse → 格子版
rep("""    function buildWarehouse() {
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
""",
    """    function buildWarehouse() {
        var grid = document.getElementById('wh-grid');
        grid.innerHTML = '';
        for (var i = 0; i < INV_SIZE; i++) {
            (function (idx) {
                var it = inv[idx];
                var slot = document.createElement('div');
                slot.className = 'wh-slot';
                if (!it) {
                    slot.innerHTML = '<span class="wh-empty">\u00b7</span>';
                } else if (it.t === 'gun') {
                    var equipped = loadout.indexOf(it.w) >= 0;
                    slot.innerHTML = (WEAPONS[it.w].emoji || '\U0001F52B') + '<br><span class="small">' + WEAPONS[it.w].name + (equipped ? ' \u2713' : '') + '</span>';
                    slot.title = '\u70b9\u51fb\u88c5\u5907/\u5378\u4e0b';
                    slot.addEventListener('click', function () {
                        if (equipped) { var k = loadout.indexOf(it.w); if (k >= 0) loadout[k] = null; }
                        else if (loadout[0] === null || loadout[0] === 'pistol') loadout[0] = it.w;
                        else if (loadout[1] === null) loadout[1] = it.w;
                        else { showMsg('\u67aa\u69fd\u6ee1\u4e86\uff01'); return; }
                        buildWarehouse();
                    });
                } else if (it.t === 'armor') {
                    var worn = wornArmor === idx;
                    slot.innerHTML = '\U0001F6E1\ufe0f<br><span class="small">\u7532 ' + it.d + '/' + 3 + (worn ? ' \u7a7f\u4e2d' : '') + '</span>';
                    slot.title = '\u70b9\u51fb\u7a7f\u7532\u51fa\u6218\uff08\u6bcf\u5c40\u8017 1 \u8010\u4e45\uff09';
                    slot.addEventListener('click', function () {
                        if (worn) { wornArmor = -1; }
                        else { wornArmor = idx; showMsg('\U0001F6E1\ufe0f \u672c\u5c40\u7a7f\u7532\uff01'); }
                        buildWarehouse();
                    });
                } else if (it.t === 'helmet') {
                    var wornH = wornHelmet === idx;
                    slot.innerHTML = '\U0001FA96<br><span class="small">\u5934 ' + it.d + '/' + 3 + (wornH ? ' \u6234\u4e2d' : '') + '</span>';
                    slot.title = '\u70b9\u51fb\u6234\u5934\u76d4\u51fa\u6218\uff08\u6bcf\u5c40\u8017 1 \u8010\u4e45\uff09';
                    slot.addEventListener('click', function () {
                        if (wornH) { wornHelmet = -1; }
                        else { wornHelmet = idx; showMsg('\U0001FA96 \u672c\u5c40\u6234\u5934\u76d4\uff01'); }
                        buildWarehouse();
                    });
                } else if (it.t === 'med') {
                    slot.innerHTML = '\U0001F48A<br><span class="small">\u836f</span>';
                    slot.title = '\u70b9\u51fb\u4f7f\u7528\uff1a\u4e0b\u4e00\u5c40\u5f00\u5c40 +20\u8840';
                    slot.addEventListener('click', function () {
                        inv[idx] = null; runMeds++;
                        showMsg('\U0001F48A \u7528\u836f\uff01\u4e0b\u4e00\u5c40\u5f00\u5c40 +20\u8840');
                        saveInv();
                        buildWarehouse();
                    });
                } else if (it.t === 'repair') {
                    slot.innerHTML = '\U0001F9F0<br><span class="small">\u7532\u4fee</span>';
                    slot.title = '\u70b9\u51fb\u4fee\u7406\uff1a\u7ed9\u4e00\u4ef6\u7532/\u5934\u76d4 +1\u8010\u4e45';
                    slot.addEventListener('click', function () {
                        for (var j = 0; j < INV_SIZE; j++) {
                            if (inv[j] && (inv[j].t === 'armor' || inv[j].t === 'helmet') && inv[j].d < 3) {
                                inv[j].d++;
                                var name = inv[j].t === 'armor' ? '\u7532' : '\u5934\u76d4';
                                inv[idx] = null;
                                saveInv();
                                showMsg('\U0001F9F0 \u4fee\u7406\u5b8c\u6210\uff01' + name + ' +1\u8010\u4e45');
                                buildWarehouse();
                                return;
                            }
                        }
                        showMsg('\U0001F9F0 \u6ca1\u6709\u9700\u8981\u4fee\u7406\u7684\u7532/\u5934\u76d4');
                    });
                }
                grid.appendChild(slot);
            })(i);
        }
        var s1 = loadout[0] ? WEAPONS[loadout[0]].name : '\u7a7a';
        var s2 = loadout[1] ? WEAPONS[loadout[1]].name : '\u7a7a';
        document.getElementById('wh-loadout').textContent =
            '\U0001F392 \u51fa\u6218\u88c5\u5907\uff1a1.' + s1 + ' | 2.' + s2 +
            (wornArmor >= 0 ? ' \U0001F6E1\ufe0f\u7a7f\u7532' : '') + (wornHelmet >= 0 ? ' \U0001FA96\u6234\u5934' : '') +
            (runMeds > 0 ? ' \U0001F48Ax' + runMeds : '');
    }
""",
    'build-warehouse')

# 7) CSS：格子样式
rep("""    #shop-slots { font-size: 14px; opacity: 0.9; margin-top: 8px; }
    .link { display: inline-block; margin-top: 16px; color: #9db2d0; text-decoration: none; font-size: 15px; }
""",
    """    #shop-slots { font-size: 14px; opacity: 0.9; margin-top: 8px; }
    .wh-grid { display: grid; grid-template-columns: repeat(6, 64px); gap: 6px; justify-content: center; margin: 12px auto; }
    .wh-slot {
        width: 64px; height: 64px;
        border-radius: 10px;
        border: 2px solid rgba(255, 255, 255, 0.2);
        background: rgba(255, 255, 255, 0.06);
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        font-size: 20px;
        cursor: pointer;
        transition: all 0.15s;
    }
    .wh-slot:hover { border-color: #ffd93d; transform: scale(1.05); }
    .wh-slot .small { font-size: 10px; opacity: 0.9; }
    .wh-slot .wh-empty { color: rgba(255, 255, 255, 0.25); }
    .link { display: inline-block; margin-top: 16px; color: #9db2d0; text-decoration: none; font-size: 15px; }
""",
    'wh-css')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
