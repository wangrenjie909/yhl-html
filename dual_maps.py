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

# 1) 世界定义 → 双地图系统
rep("""    // ---- 世界 ----
    var MAPW = 2000, MAPH = 1400;
    var T = 16;                       // 墙厚
    var DW = 64;                      // 门宽
    var buildings = [
        { x: 300, y: 250, w: 220, h: 160 },
        { x: 700, y: 140, w: 200, h: 180 },
        { x: 150, y: 620, w: 240, h: 170 },
        { x: 760, y: 520, w: 200, h: 160 },
        { x: 420, y: 470, w: 160, h: 140 },
        { x: 170, y: 930, w: 240, h: 180 },
        { x: 660, y: 910, w: 200, h: 160 },
        { x: 1050, y: 300, w: 240, h: 170 },
        { x: 1250, y: 650, w: 200, h: 190 },
        { x: 1000, y: 1000, w: 260, h: 170 },
        { x: 1450, y: 1000, w: 200, h: 170 }
    ];
    var extract = { x: 1760, y: 1240, r: 95 };

    // 每栋楼的墙面（底部留门）
    var wallRects = [];
    (function () {
        for (var i = 0; i < buildings.length; i++) {
            var b = buildings[i];
            wallRects.push({ x: b.x, y: b.y, w: b.w, h: T });
            wallRects.push({ x: b.x, y: b.y + b.h - T, w: (b.w - DW) / 2, h: T });
            wallRects.push({ x: b.x + (b.w + DW) / 2, y: b.y + b.h - T, w: (b.w - DW) / 2, h: T });
            wallRects.push({ x: b.x, y: b.y, w: T, h: b.h });
            wallRects.push({ x: b.x + b.w - T, y: b.y, w: T, h: b.h });
        }
    })();
""",
    """    // ---- 世界：双地图（城市 / 沙漠）----
    var T = 16;                       // 墙厚
    var DW = 64;                      // 门宽
    var MAPS = {
        city: {
            name: '\u57ce\u5e02\u5730\u56fe',
            W: 2600, H: 1800,
            ground: '#14171d', wall: '#39414f', floor: '#232936',
            extract: { x: 2300, y: 1620, r: 95 },
            buildings: [
                { x: 300, y: 250, w: 220, h: 160 },
                { x: 700, y: 140, w: 200, h: 180 },
                { x: 150, y: 620, w: 240, h: 170 },
                { x: 760, y: 520, w: 200, h: 160 },
                { x: 420, y: 470, w: 160, h: 140 },
                { x: 170, y: 930, w: 240, h: 180 },
                { x: 660, y: 910, w: 200, h: 160 },
                { x: 1050, y: 300, w: 240, h: 170 },
                { x: 1250, y: 650, w: 200, h: 190 },
                { x: 1000, y: 1000, w: 260, h: 170 },
                { x: 1450, y: 1000, w: 200, h: 170 },
                { x: 300, y: 1300, w: 200, h: 170 },
                { x: 1600, y: 250, w: 230, h: 160 },
                { x: 1900, y: 600, w: 200, h: 180 }
            ]
        },
        desert: {
            name: '\u6c99\u6f20\u5730\u56fe',
            W: 3400, H: 2400,
            ground: '#1d1810', wall: '#4c4030', floor: '#2e2618',
            extract: { x: 3050, y: 2150, r: 100 },
            buildings: [
                { x: 350, y: 300, w: 260, h: 190 },
                { x: 850, y: 180, w: 220, h: 170 },
                { x: 200, y: 800, w: 280, h: 200 },
                { x: 900, y: 700, w: 240, h: 180 },
                { x: 500, y: 1200, w: 220, h: 190 },
                { x: 1100, y: 1100, w: 280, h: 200 },
                { x: 250, y: 1650, w: 260, h: 190 },
                { x: 900, y: 1600, w: 240, h: 180 },
                { x: 1500, y: 400, w: 280, h: 190 },
                { x: 1800, y: 900, w: 240, h: 200 },
                { x: 1500, y: 1400, w: 260, h: 190 },
                { x: 2100, y: 1700, w: 280, h: 200 },
                { x: 2500, y: 300, w: 260, h: 190 },
                { x: 2600, y: 800, w: 240, h: 200 },
                { x: 2400, y: 1300, w: 280, h: 190 }
            ]
        }
    };
    var currentMap = MAPS.city;
    var MAPW = currentMap.W, MAPH = currentMap.H;
    var buildings = currentMap.buildings;
    var extract = currentMap.extract;

    // 每栋楼的墙面（底部留门）
    var wallRects = [];
    function setupMap() {
        MAPW = currentMap.W; MAPH = currentMap.H;
        buildings = currentMap.buildings;
        extract = currentMap.extract;
        wallRects = [];
        for (var i = 0; i < buildings.length; i++) {
            var b = buildings[i];
            wallRects.push({ x: b.x, y: b.y, w: b.w, h: T });
            wallRects.push({ x: b.x, y: b.y + b.h - T, w: (b.w - DW) / 2, h: T });
            wallRects.push({ x: b.x + (b.w + DW) / 2, y: b.y + b.h - T, w: (b.w - DW) / 2, h: T });
            wallRects.push({ x: b.x, y: b.y, w: T, h: b.h });
            wallRects.push({ x: b.x + b.w - T, y: b.y, w: T, h: b.h });
        }
    }
    setupMap();
""",
    'dual-maps')

# 2) 敌人：18个（9近战+9远程）
rep("""        // 12 \u4e2a\u654c\u4eba\uff1a6 \u8fd1\u6218\uff08\U0001F47E\uff09+ 6 \u8fdc\u7a0b\uff08\U0001F916\uff09\uff0c\u51fa\u751f\u70b9\u9644\u8fd1\u4e0d\u5237\u602a\uff01
        for (var i = 0; i < 12; i++) {
""",
    """        // 18 \u4e2a\u654c\u4eba\uff1a9 \u8fd1\u6218\uff08\U0001F47E\uff09+ 9 \u8fdc\u7a0b\uff08\U0001F916\uff09\uff0c\u51fa\u751f\u70b9\u9644\u8fd1\u4e0d\u5237\u602a\uff01
        for (var i = 0; i < 18; i++) {
""",
    'enemies-18')
rep("            enemies.push({ x: x, y: y, hp: 100, wander: Math.random() * 6.28, ranged: i >= 6, shotCd: 1.5 + Math.random() });\n",
    "            enemies.push({ x: x, y: y, hp: 100, wander: Math.random() * 6.28, ranged: i >= 9, shotCd: 1.5 + Math.random() });\n",
    'ranged-9')

# 3) 开箱数量按地图变大（外面箱子 10 -> 16）
rep("""        for (var i = 0; i < 10; i++) {
            var x, y, tries = 0;
            do { x = 120 + Math.random() * (MAPW - 240); y = 120 + Math.random() * (MAPH - 240); tries++; }
            while (rectHit(x, y, 18) && tries < 60);
            crates.push({ x: x, y: y });
        }
""",
    """        for (var i = 0; i < 16; i++) {
            var x, y, tries = 0;
            do { x = 120 + Math.random() * (MAPW - 240); y = 120 + Math.random() * (MAPH - 240); tries++; }
            while (rectHit(x, y, 18) && tries < 60);
            crates.push({ x: x, y: y });
        }
""",
    'crates-16')

# 4) resetGame：调用 setupMap + HUD 18
rep("""        crates = []; enemies = []; bullets = []; drops = []; fx = []; enemyShots = [];
        spawnCrates(); spawnEnemies();
""",
    """        setupMap();
        crates = []; enemies = []; bullets = []; drops = []; fx = []; enemyShots = [];
        spawnCrates(); spawnEnemies();
""",
    'reset-setupmap')
rep("        document.getElementById('ene').textContent = '12';\n",
    "        document.getElementById('ene').textContent = '18';\n",
    'hud-ene-18')

# 5) 地图选择按钮
rep("""    <button class="btn" id="btn-start">\U0001F680 \u5f00\u59cb\u884c\u52a8</button>
    <a class="link" href="index.html">\u2b05 \u56de\u5230\u8dd1\u9177\u8005\u7684\u5929\u53f0</a>
</div>

<div class="panel" id="over" style="display:none">
""",
    """    <div id="map-choice">
        <button class="map-btn active" data-map="city">\U0001F3D9\ufe0f \u57ce\u5e02\u5730\u56fe</button>
        <button class="map-btn" data-map="desert">\U0001F3DC\ufe0f \u6c99\u6f20\u5730\u56fe</button>
    </div>
    <button class="btn" id="btn-start">\U0001F680 \u5f00\u59cb\u884c\u52a8</button>
    <a class="link" href="index.html">\u2b05 \u56de\u5230\u8dd1\u9177\u8005\u7684\u5929\u53f0</a>
</div>

<div class="panel" id="over" style="display:none">
""",
    'map-btns-html')

# 6) CSS：地图按钮
rep("""    .btn:hover { transform: scale(1.06); }
    .link { display: inline-block; margin-top: 16px; color: #9db2d0; text-decoration: none; font-size: 15px; }
""",
    """    .btn:hover { transform: scale(1.06); }
    #map-choice { display: flex; gap: 14px; margin-top: 16px; flex-wrap: wrap; justify-content: center; }
    .map-btn {
        padding: 12px 26px;
        font-size: 16px;
        border-radius: 22px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        background: rgba(255, 255, 255, 0.08);
        color: #fff;
        cursor: pointer;
        transition: all 0.2s;
    }
    .map-btn:hover { border-color: #ff8e3c; }
    .map-btn.active { background: linear-gradient(135deg, #ff7e5f, #feb47b); border-color: transparent; font-weight: bold; }
    .link { display: inline-block; margin-top: 16px; color: #9db2d0; text-decoration: none; font-size: 15px; }
""",
    'map-btn-css')

# 7) JS：选地图
rep("""    document.getElementById('btn-switch').addEventListener('click', switchWeapon);
    document.getElementById('btn-pickup').addEventListener('click', tryPickup);
""",
    """    document.getElementById('btn-switch').addEventListener('click', switchWeapon);
    document.getElementById('btn-pickup').addEventListener('click', tryPickup);

    // \U0001F3D9 \u9009\u5730\u56fe\uff01
    var mapBtns = document.querySelectorAll('.map-btn');
    for (var i = 0; i < mapBtns.length; i++) {
        (function (b) {
            b.addEventListener('click', function () {
                currentMap = MAPS[b.getAttribute('data-map')];
                setupMap();
                for (var j = 0; j < mapBtns.length; j++) {
                    mapBtns[j].classList.toggle('active', mapBtns[j] === b);
                }
                showMsg('\U0001F5FA\ufe0f \u9009\u62e9\u4e86' + currentMap.name);
            });
        })(mapBtns[i]);
    }
""",
    'map-select-js')

# 8) 画：地图主题色
rep("""    function draw() {
        ctx.fillStyle = '#14171d';
        ctx.fillRect(0, 0, W, H);
""",
    """    function draw() {
        ctx.fillStyle = currentMap.ground;
        ctx.fillRect(0, 0, W, H);
""",
    'draw-ground')
rep("""        for (var i = 0; i < buildings.length; i++) {
            var b = buildings[i];
            ctx.fillStyle = '#39414f';
            ctx.fillRect(b.x, b.y, b.w, b.h);
            ctx.fillStyle = '#232936';
            ctx.fillRect(b.x + T, b.y + T, b.w - 2 * T, b.h - 2 * T);
            // \u95e8\uff08\u5e95\u90e8\u7f3a\u53e3\uff09
            ctx.fillStyle = '#232936';
""",
    """        for (var i = 0; i < buildings.length; i++) {
            var b = buildings[i];
            ctx.fillStyle = currentMap.wall;
            ctx.fillRect(b.x, b.y, b.w, b.h);
            ctx.fillStyle = currentMap.floor;
            ctx.fillRect(b.x + T, b.y + T, b.w - 2 * T, b.h - 2 * T);
            // \u95e8\uff08\u5e95\u90e8\u7f3a\u53e3\uff09
            ctx.fillStyle = currentMap.floor;
""",
    'draw-map-colors')

# 9) 初始 HUD 敌人 18
rep("    <span>\U0001F47E <span id=\"ene\">12</span></span>\n",
    "    <span>\U0001F47E <span id=\"ene\">18</span></span>\n",
    'hud-html-ene')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
