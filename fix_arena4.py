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

# 1) 先建决斗场，再放塔（塔就能避开场地！）
rep("""        // \u9AD8\u578B\u573A\u6C99\u9505\u5854\uff1a\u6BCF\u5C40\u968F\u673A\u4F4D\u7F6E\uff01
        towers = [];
        for (var ti = 0; ti < 5; ti++) {
""",
    """        // \U0001F479 BOSS \u4E13\u5C5E\u573A\u5730\uff08\u5148\u5EFA\u573A\u5730\uff0C\u5854\u624D\u80FD\u907F\u5F00\u5B83\uff09
        var ax, ay, tries3 = 0;
        do {
            ax = 350 + Math.random() * (MAPW - 700);
            ay = 350 + Math.random() * (MAPH - 700);
            tries3++;
        } while ((rectHit(ax, ay, 240) || Math.sqrt((ax - 200) * (ax - 200) + (ay - 200) * (ay - 200)) < 500 ||
                  Math.sqrt((ax - extract.x) * (ax - extract.x) + (ay - extract.y) * (ay - extract.y)) < extract.r + 340) && tries3 < 90);
        arena = { x: ax, y: ay, r: 210, gateAng: Math.PI / 2, gateHalf: 0.45, locked: false };

        // \u9AD8\u578B\u573A\u6C99\u9505\u5854\uff1a\u6BCF\u5C40\u968F\u673A\u4F4D\u7F6E\uff01
        towers = [];
        for (var ti = 0; ti < 5; ti++) {
""",
    'arena-first')

# 2) 删掉原来后面重复的场地生成块
rep("""        // \U0001F479 BOSS \u4E13\u5C5E\u573A\u5730
        var ax, ay, tries3 = 0;
        do {
            ax = 350 + Math.random() * (MAPW - 700);
            ay = 350 + Math.random() * (MAPH - 700);
            tries3++;
        } while ((rectHit(ax, ay, 240) || Math.sqrt((ax - 200) * (ax - 200) + (ay - 200) * (ay - 200)) < 500 ||
                  Math.sqrt((ax - extract.x) * (ax - extract.x) + (ay - extract.y) * (ay - extract.y)) < extract.r + 340) && tries3 < 90);
        arena = { x: ax, y: ay, r: 210, gateAng: Math.PI / 2, gateHalf: 0.45, locked: false };
        spawnCrates(); spawnEnemies();
""",
    """        spawnCrates(); spawnEnemies();
""",
    'arena-moved')

# 3) BOSS：玩家不在场地里就不开枪、不撞人！
rep("""        // \U0001F479 BOSS\uff01\uff08\u5730\u9762\u5de8\u53d8\u6012\uff0c\u53ea\u5728\u5730\u9762\uff09
        if (boss && boss.hp > 0) {
            var bd = Math.sqrt((boss.x - player.x) * (boss.x - player.x) + (boss.y - player.y) * (boss.y - player.y));
""",
    """        // \U0001F479 BOSS\uff01\uff08\u5730\u9762\u5de8\u53d8\u6012\uff0c\u53ea\u5728\u5730\u9762\uff09
        if (boss && boss.hp > 0) {
            var bd = Math.sqrt((boss.x - player.x) * (boss.x - player.x) + (boss.y - player.y) * (boss.y - player.y));
            var pInArena = arena ? Math.sqrt((player.x - arena.x) * (player.x - arena.x) + (player.y - arena.y) * (player.y - arena.y)) < arena.r : false;
""",
    'pInArena-var')

rep("""            if (player.floor === 1 && bd < 520 && boss.shotCd <= 0) {
                boss.shotCd = 2.0;
""",
    """            if (player.floor === 1 && pInArena && bd < 520 && boss.shotCd <= 0) {
                boss.shotCd = 2.0;
""",
    'boss-shoot-inside')

rep("""            if (player.floor === 1 && bd < 42 && player.hitCd <= 0) {
                player.hp -= Math.round(18 * ((gear.armor || wornArmor >= 0) ? 0.7 : 1) * (wornHelmet >= 0 ? 0.8 : 1));
""",
    """            if (player.floor === 1 && pInArena && bd < 42 && player.hitCd <= 0) {
                player.hp -= Math.round(18 * ((gear.armor || wornArmor >= 0) ? 0.7 : 1) * (wornHelmet >= 0 ? 0.8 : 1));
""",
    'boss-hit-inside')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
