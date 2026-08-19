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

# 1) mapOpen 变量
rep("    var state = 'start';\n    var extractT = 0;\n",
    "    var state = 'start';\n    var extractT = 0;\n    var mapOpen = false;   // \U0001F5FA \u5c40\u5185\u5730\u56fe\u662f\u5426\u6253\u5f00\n",
    'mapopen-var')

# 2) M 键开/关大地图
rep("        if (k === 'e' || k === 'f') tryPickup();\n",
    "        if (k === 'e' || k === 'f') tryPickup();\n        if (k === 'm' && state === 'play') mapOpen = !mapOpen;\n",
    'key-m')

# 3) 手机地图按钮
rep("        <button class=\"tbtn\" id=\"btn-pickup\">\u270B</button>\n",
    "        <button class=\"tbtn\" id=\"btn-pickup\">\u270B</button>\n        <button class=\"tbtn\" id=\"btn-map\">\U0001F5FA\ufe0f</button>\n",
    'touch-map')
rep("    document.getElementById('btn-pickup').addEventListener('click', tryPickup);\n",
    "    document.getElementById('btn-pickup').addEventListener('click', tryPickup);\n    document.getElementById('btn-map').addEventListener('click', function () { if (state === 'play') mapOpen = !mapOpen; });\n",
    'touch-map-js')

# 4) resetGame 关地图
rep("        setupMap();\n        crates = []; enemies = []; bullets = []; drops = []; fx = []; enemyShots = [];\n",
    "        setupMap();\n        mapOpen = false;\n        crates = []; enemies = []; bullets = []; drops = []; fx = []; enemyShots = [];\n",
    'reset-mapopen')

# 5) 地图开着时暂停
rep("        if (state === 'play') update(1 / 60);\n",
    "        if (state === 'play' && !mapOpen) update(1 / 60);\n",
    'pause-map')

# 6) 画小地图 + 大地图（在鼠标准星之前）
rep("""        // \U0001F3AF \u9f20\u6807\u51c6\u661f
        if (mouse.on) {
""",
    """        // \U0001F5FA \u5c0f\u5730\u56fe\uff08\u4e00\u76f4\u663e\u793a\uff1a\u9632\u533a + \u64a4\u79bb\u70b9 + \u73a9\u5bb6\uff0c\u4e0d\u663e\u793a\u654c\u4eba\uff09
        if (state === 'play') drawMinimap();
        // \U0001F5FA \u5927\u5730\u56fe\uff08\u6309 M \u5f00\u5173\uff09
        if (mapOpen) drawBigMap();

        // \U0001F3AF \u9f20\u6807\u51c6\u661f
        if (mouse.on) {
""",
    'call-maps')

# 7) 新增 drawMinimap / drawBigMap 函数（放在 draw() 之后、loop() 之前）
rep("""    function loop() {
        if (state === 'play' && !mapOpen) update(1 / 60);
""",
    """    // \U0001F5FA \u5c0f\u5730\u56fe\uff1a\u53f3\u4e0a\u89d2\u5e38\u9a7b\uff08\u9632\u533a\u6a59\u8272 / \u64a4\u79bb\u70b9\u7eff\u8272 / \u73a9\u5bb6\u767d\u8272\uff0c\u4e0d\u663e\u793a\u654c\u4eba\uff09
    function drawMinimap() {
        var mw = 190, mh = 150;
        var mx = W - mw - 12, my = 56;
        ctx.fillStyle = 'rgba(0,0,0,0.55)';
        ctx.fillRect(mx - 6, my - 6, mw + 12, mh + 12);
        ctx.strokeStyle = 'rgba(255,255,255,0.35)';
        ctx.lineWidth = 1;
        ctx.strokeRect(mx - 6, my - 6, mw + 12, mh + 12);
        var sc = Math.min(mw / MAPW, mh / MAPH);
        var ox = mx + (mw - MAPW * sc) / 2;
        var oy = my + (mh - MAPH * sc) / 2;
        // \u9632\u533a\uff08\u623f\u95f4\uff09
        ctx.fillStyle = 'rgba(255,170,90,0.85)';
        for (var i = 0; i < buildings.length; i++) {
            var b = buildings[i];
            ctx.fillRect(ox + b.x * sc, oy + b.y * sc, Math.max(2, b.w * sc), Math.max(2, b.h * sc));
        }
        // \u64a4\u79bb\u70b9
        ctx.fillStyle = 'rgba(80,220,120,0.95)';
        ctx.beginPath();
        ctx.arc(ox + extract.x * sc, oy + extract.y * sc, 5, 0, Math.PI * 2);
        ctx.fill();
        // \u73a9\u5bb6\uff08\u4e0d\u663e\u793a\u654c\u4eba\uff01\uff09
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(ox + player.x * sc, oy + player.y * sc, 4, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = 'rgba(255,255,255,0.6)';
        ctx.font = '11px sans-serif';
        ctx.textAlign = 'left';
        ctx.fillText('\U0001F5FA\ufe0f \u5730\u56fe\uff08M\uff09', mx, my + mh + 14);
    }

    // \U0001F5FA \u5927\u5730\u56fe\uff08\u6309 M \u6253\u5f00\uff09
    function drawBigMap() {
        ctx.fillStyle = 'rgba(8,10,14,0.92)';
        ctx.fillRect(0, 0, W, H);
        var mw = Math.min(W - 60, 900), mh = Math.min(H - 130, 620);
        var mx = (W - mw) / 2, my = (H - mh) / 2 + 8;
        ctx.fillStyle = 'rgba(20,24,32,0.96)';
        ctx.fillRect(mx, my, mw, mh);
        ctx.strokeStyle = 'rgba(255,255,255,0.4)';
        ctx.lineWidth = 2;
        ctx.strokeRect(mx, my, mw, mh);
        var sc = Math.min(mw / MAPW, mh / MAPH);
        var ox = mx + (mw - MAPW * sc) / 2;
        var oy = my + (mh - MAPH * sc) / 2;
        // \u7f51\u683c
        ctx.strokeStyle = 'rgba(255,255,255,0.08)';
        ctx.lineWidth = 1;
        for (var gx = 0; gx <= MAPW; gx += 200) { ctx.beginPath(); ctx.moveTo(ox + gx * sc, oy); ctx.lineTo(ox + gx * sc, oy + MAPH * sc); ctx.stroke(); }
        for (var gy = 0; gy <= MAPH; gy += 200) { ctx.beginPath(); ctx.moveTo(ox, oy + gy * sc); ctx.lineTo(ox + MAPW * sc, oy + gy * sc); ctx.stroke(); }
        // \u9632\u533a
        ctx.fillStyle = 'rgba(255,170,90,0.8)';
        for (var i = 0; i < buildings.length; i++) {
            var b = buildings[i];
            ctx.fillRect(ox + b.x * sc, oy + b.y * sc, Math.max(2, b.w * sc), Math.max(2, b.h * sc));
        }
        // \u64a4\u79bb\u70b9 + \u6587\u5b57
        ctx.fillStyle = 'rgba(80,220,120,0.95)';
        ctx.beginPath();
        ctx.arc(ox + extract.x * sc, oy + extract.y * sc, 7, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#7CFC9A';
        ctx.font = 'bold 14px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('\U0001F681 \u64a4\u79bb\u70b9', ox + extract.x * sc, oy + extract.y * sc - 12);
        // \u73a9\u5bb6
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(ox + player.x * sc, oy + player.y * sc, 6, 0, Math.PI * 2);
        ctx.fill();
        ctx.font = '12px sans-serif';
        ctx.fillText('\u6211', ox + player.x * sc, oy + player.y * sc - 10);
        // \u6807\u9898
        ctx.fillStyle = '#ff8e3c';
        ctx.font = 'bold 22px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('\U0001F5FA\ufe0f ' + currentMap.name, W / 2, my - 6);
        ctx.fillStyle = 'rgba(255,255,255,0.7)';
        ctx.font = '14px sans-serif';
        ctx.fillText('\u9632\u533a\u6a59\u8272 \u00b7 \u64a4\u79bb\u70b9\u7eff\u8272 \u00b7 \u4e0d\u663e\u793a\u654c\u4eba \u00b7 \u6309 M \u5173\u95ed', W / 2, my + mh + 28);
    }

    function loop() {
        if (state === 'play' && !mapOpen) update(1 / 60);
""",
    'map-functions')

# 8) 玩法说明：加 M 键
rep("        <li>\U0001F47E \u8fd1\u6218\u654c\u4eba\u51b2\u8138 \u00b7 \U0001F916 <b>\u8fdc\u7a0b\u654c\u4eba</b>\u4f1a\u671d\u4f60\u5c04\u51fb\uff0c\u6ce8\u610f\u8eb2\u5b50\u5f39\uff01</li>\n",
    "        <li>\U0001F47E \u8fd1\u6218\u654c\u4eba\u51b2\u8138 \u00b7 \U0001F916 <b>\u8fdc\u7a0b\u654c\u4eba</b>\u4f1a\u671d\u4f60\u5c04\u51fb\uff0c\u6ce8\u610f\u8eb2\u5b50\u5f39\uff01</li>\n        <li>\U0001F5FA\ufe0f \u6309 <b>M</b> \u770b\u5730\u56fe\uff1a\u663e\u793a\u9632\u533a\u548c\u64a4\u79bb\u70b9\uff08\u4e0d\u663e\u793a\u654c\u4eba\uff09</li>\n",
    'instructions-m')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
