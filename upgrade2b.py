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

# 1) 敌人循环：爬2楼 + 同层可见 + 同层子弹
rep("""        // \U0001F47E \u654c\u4eba\uff08\u8fd1\u6218\u51b2\u8138 / \u8fdc\u7a0b\u5c04\u51fb\uff09
        for (var i = 0; i < enemies.length; i++) {
            var e = enemies[i];
            var d = Math.sqrt((e.x - player.x) * (e.x - player.x) + (e.y - player.y) * (e.y - player.y));
            var es = (e.ranged ? 100 : 130) * dt;
            var mx = 0, my = 0;
            var los = (player.floor === 2) ? false : hasLOS(e.x, e.y, player.x, player.y);   // \U0001F441 \u73a9\u5bb6\u57282\u697c\uff0c\u5730\u9762\u654c\u4eba\u770b\u4e0d\u5230\uff01
            if (e.ranged) {
                // \U0001F916 \u8fdc\u7a0b\u654c\u4eba\uff1a\u770b\u4e0d\u5230\u5c31\u5148\u51b2\u51fa\u6765\uff0c\u770b\u5230\u624d\u5f00\u706b\uff01
                if (!los) {
                    // \u88ab\u5899\u6321\u4f4f\u4e86\uff1a\u4e0d\u6253\u67aa\uff0c\u8d70\u8fd1\u73a9\u5bb6\u627e\u89c6\u89d2
                    mx = (player.x - e.x) / d * es * 1.2;
                    my = (player.y - e.y) / d * es * 1.2;
                    e.shotCd = 0.15;   // \u5feb\u901f\u91cd\u65b0\u68c0\u6d4b
                } else if (d < 240 && d > 0.01) {
                    mx = -(player.x - e.x) / d * es;
                    my = -(player.y - e.y) / d * es;
                } else if (d > 340) {
                    mx = (player.x - e.x) / d * es;
                    my = (player.y - e.y) / d * es;
                } else {
                    e.wander += dt;
                    mx = Math.cos(e.wander) * es * 0.4;
                    my = Math.sin(e.wander) * es * 0.4;
                }
                if (los && d < 480 && e.shotCd <= 0) {
                    e.shotCd = 1.6 + Math.random() * 0.6;
                    var ea = Math.atan2(player.y - e.y, player.x - e.x);
                    enemyShots.push({ x: e.x, y: e.y, vx: Math.cos(ea) * 260, vy: Math.sin(ea) * 260, life: 2.4 });
                }
                if (e.shotCd > 0) e.shotCd -= dt;
            } else {
                // \U0001F47E \u8fd1\u6218\u654c\u4eba\uff1a\u51b2\u8138\uff01
                if (d < 280 && d > 0.01) {
                    mx = (player.x - e.x) / d * es;
                    my = (player.y - e.y) / d * es;
                } else {
                    e.wander += dt;
                    mx = Math.cos(e.wander) * es * 0.5;
                    my = Math.sin(e.wander) * es * 0.5;
                }
            }
            // \U0001F9F1 \u654c\u4eba\u4e5f\u78b0\u58c1\uff01\uff08\u4e0d\u80fd\u7a7f\u5899\uff09
            if (!rectHit(e.x + mx, e.y, 14)) e.x += mx;
            if (!rectHit(e.x, e.y + my, 14)) e.y += my;
            e.x = Math.max(20, Math.min(MAPW - 20, e.x));
            e.y = Math.max(20, Math.min(MAPH - 20, e.y));
            if (d < 36 && player.hitCd <= 0) {
""",
    """        // \U0001F47E \u654c\u4eba\uff08\u53ef\u4ee5\u722c\u4e0a\u623f\u5b502\u697c\uff01\u9505\u5854\u4e0a\u4e0d\u53bb\uff09
        for (var i = 0; i < enemies.length; i++) {
            var e = enemies[i];
            var d = Math.sqrt((e.x - player.x) * (e.x - player.x) + (e.y - player.y) * (e.y - player.y));
            var es = (e.ranged ? 100 : 130) * dt;
            var mx = 0, my = 0;
            var sameFloor = (player.floor === e.floor);
            var los = sameFloor && hasLOS(e.x, e.y, player.x, player.y);
            if (player.floor === 2 && player.bIdx >= 0 && e.floor === 1) {
                // \U0001FA9C \u654c\u4eba\u8981\u722c\u5230\u73a9\u5bb6\u7684 2 \u697c\uff01\uff08\u9760\u8fd1\u623f\u5b50\u5c31\u722c\u4e0a\u53bb\uff09
                var sb = buildings[player.bIdx];
                if (sb.has2) {
                    var scx = sb.x + sb.w / 2, scy = sb.y + sb.h / 2;
                    var sdd = Math.sqrt((scx - e.x) * (scx - e.x) + (scy - e.y) * (scy - e.y));
                    if (sdd < 240 && sdd > 0.01) {
                        // \u5df2\u7ecf\u9760\u8fd1\u623f\u5b50\uff1a\u76f4\u63a5\u722c\u4e0a 2 \u697c\uff01
                        e.floor = 2; e.bIdx = player.bIdx;
                        e.x = sb.x + sb.w / 2 + (Math.random() - 0.5) * 60;
                        e.y = sb.y + T + 40 + Math.random() * 40;
                    } else {
                        mx = (scx - e.x) / sdd * es;
                        my = (scy - e.y) / sdd * es;
                    }
                }
            } else if (e.floor === 2) {
                if (player.floor === 2 && player.bIdx === e.bIdx && d > 0.01) {
                    // \u540c\u5728\u8fd9\u680b\u697c\u9876\uff1a\u8ffd\u73a9\u5bb6\uff01
                    mx = (player.x - e.x) / d * es;
                    my = (player.y - e.y) / d * es;
                } else {
                    // \u73a9\u5bb6\u4e0d\u5728\u697c\u4e0a\u4e86\uff1a\u4e0b\u697c
                    e.floor = 1; e.bIdx = -1;
                }
            } else if (e.ranged) {
                // \U0001F916 \u8fdc\u7a0b\uff08\u540c\u5c42\u624d\u4fdd\u6301\u8ddd\u79bb\u5f00\u706b\uff09
                if (!los) {
                    mx = (player.x - e.x) / d * es * 1.2;
                    my = (player.y - e.y) / d * es * 1.2;
                    e.shotCd = 0.15;
                } else if (d < 240 && d > 0.01) {
                    mx = -(player.x - e.x) / d * es;
                    my = -(player.y - e.y) / d * es;
                } else if (d > 340) {
                    mx = (player.x - e.x) / d * es;
                    my = (player.y - e.y) / d * es;
                } else {
                    e.wander += dt;
                    mx = Math.cos(e.wander) * es * 0.4;
                    my = Math.sin(e.wander) * es * 0.4;
                }
                if (los && d < 480 && e.shotCd <= 0) {
                    e.shotCd = 1.6 + Math.random() * 0.6;
                    var ea = Math.atan2(player.y - e.y, player.x - e.x);
                    enemyShots.push({ x: e.x, y: e.y, vx: Math.cos(ea) * 260, vy: Math.sin(ea) * 260, life: 2.4, f: e.floor, b: e.bIdx });
                }
                if (e.shotCd > 0) e.shotCd -= dt;
            } else {
                // \U0001F47E \u8fd1\u6218\uff1a\u51b2\u8138\uff01
                if (d < 280 && d > 0.01) {
                    mx = (player.x - e.x) / d * es;
                    my = (player.y - e.y) / d * es;
                } else {
                    e.wander += dt;
                    mx = Math.cos(e.wander) * es * 0.5;
                    my = Math.sin(e.wander) * es * 0.5;
                }
            }
            // \U0001F9F1 \u79fb\u52a8 + \u697c\u5c42\u8fb9\u754c
            if (e.floor === 2 && e.bIdx >= 0) {
                var eb = buildings[e.bIdx];
                e.x = Math.max(eb.x + T + 4, Math.min(eb.x + eb.w - T - 4, e.x + mx));
                e.y = Math.max(eb.y + T + 4, Math.min(eb.y + eb.h - T - 4, e.y + my));
            } else {
                if (!rectHit(e.x + mx, e.y, 14)) e.x += mx;
                if (!rectHit(e.x, e.y + my, 14)) e.y += my;
            }
            e.x = Math.max(20, Math.min(MAPW - 20, e.x));
            e.y = Math.max(20, Math.min(MAPH - 20, e.y));
            if (sameFloor && d < 36 && player.hitCd <= 0) {
""",
    'enemy-climb')

# 2) 敌人子弹：同层才打中；2楼的子弹忽略自己楼的墙
rep("""        // \U0001F9E8 \u654c\u4eba\u7684\u5b50\u5f39\uff01
        for (var i = enemyShots.length - 1; i >= 0; i--) {
            var sh = enemyShots[i];
            sh.x += sh.vx * dt; sh.y += sh.vy * dt;
            sh.life -= dt;
            if (sh.life <= 0 || rectHit(sh.x, sh.y, 4)) { enemyShots.splice(i, 1); continue; }
            var d2 = Math.sqrt((sh.x - player.x) * (sh.x - player.x) + (sh.y - player.y) * (sh.y - player.y));
            if (d2 < 22 && player.hitCd <= 0 && player.floor === 1) {   // 2\u697c\u65f6\u5730\u9762\u5b50\u5f39\u6253\u4e0d\u5230\u4f60\uff01
""",
    """        // \U0001F9E8 \u654c\u4eba\u7684\u5b50\u5f39\uff01\uff08\u540c\u4e00\u5c42\u624d\u80fd\u6253\u4e2d\u4f60\uff09
        for (var i = enemyShots.length - 1; i >= 0; i--) {
            var sh = enemyShots[i];
            sh.x += sh.vx * dt; sh.y += sh.vy * dt;
            sh.life -= dt;
            var hitWall2 = (sh.f === 2 && sh.b >= 0) ? (function () {
                for (var wi = 0; wi < wallRects.length; wi++) {
                    if (wallRects[wi].b === sh.b) continue;
                    var r2 = wallRects[wi];
                    var cx2 = Math.max(r2.x, Math.min(sh.x, r2.x + r2.w));
                    var cy2 = Math.max(r2.y, Math.min(sh.y, r2.y + r2.h));
                    var ddx = sh.x - cx2, ddy = sh.y - cy2;
                    if (ddx * ddx + ddy * ddy < 16) return true;
                }
                return false;
            })() : rectHit(sh.x, sh.y, 4);
            if (sh.life <= 0 || hitWall2) { enemyShots.splice(i, 1); continue; }
            var d2 = Math.sqrt((sh.x - player.x) * (sh.x - player.x) + (sh.y - player.y) * (sh.y - player.y));
            if (d2 < 22 && player.hitCd <= 0 && sh.f === player.floor) {   // \u540c\u4e00\u5c42\u624d\u6253\u5f97\u5230\uff01
""",
    'enemyshot-floor2')

# 3) 玩家子弹：也能打 BOSS！
rep("""            if (b.life <= 0 || hitWall) {
                bullets.splice(i, 1);
            } else if (hitEnemy >= 0) {
""",
    """            if (b.life <= 0 || hitWall) {
                bullets.splice(i, 1);
            } else if (boss && boss.hp > 0) {
                var bd = Math.sqrt((boss.x - b.x) * (boss.x - b.x) + (boss.y - b.y) * (boss.y - b.y));
                if (bd < 32) {
                    boss.hp -= b.dmg;
                    fx.push({ x: b.x, y: b.y, r: 6, t: 0 });
                    bullets.splice(i, 1);
                    if (boss.hp <= 0) killBoss();
                }
            } else if (hitEnemy >= 0) {
""",
    'bullet-boss')

# 4) 刀：也能砍 BOSS（伤害80）
rep("""                    if (md2 < 95 && diff < 1.0) {
                        me.hp -= wg.dmg;   // \U0001F52A \u5148\u6263\u8840\uff01\u514d\u8d39\u5200\u8d34 2 \u5200\u624d\u80fd\u780d\u6b7b\uff01
                        fx.push({ x: me.x, y: me.y, r: 6, t: 0 });
                        if (me.hp <= 0) killEnemy(mi);
                        else showMsg('\U0001F52A \u780d\u4e2d\u654c\u4eba\uff01');
                    }
""",
    """                    if (md2 < 95 && diff < 1.0) {
                        me.hp -= wg.dmg;   // \U0001F52A \u5148\u6263\u8840\uff01\u514d\u8d39\u5200\u8d34 2 \u5200\u624d\u80fd\u780d\u6b7b\uff01
                        fx.push({ x: me.x, y: me.y, r: 6, t: 0 });
                        if (me.hp <= 0) killEnemy(mi);
                        else showMsg('\U0001F52A \u780d\u4e2d\u654c\u4eba\uff01');
                    }
                }
                if (boss && boss.hp > 0) {
                    var bkd = Math.sqrt((boss.x - player.x) * (boss.x - player.x) + (boss.y - player.y) * (boss.y - player.y));
                    var bka = Math.abs(Math.atan2(boss.y - player.y, boss.x - player.x) - player.dir);
                    if (bka > Math.PI) bka = Math.PI * 2 - bka;
                    if (bkd < 100 && bka < 1.0) {
                        boss.hp -= 80;   // \U0001F52A \u5200\u5bf9 BOSS \u4f24\u5bb3 80
                        fx.push({ x: boss.x, y: boss.y, r: 6, t: 0 });
                        showMsg('\U0001F52A \u780d\u4e2d BOSS\uff01');
                        if (boss.hp <= 0) killBoss();
                    }
                }
""",
    'knife-boss')

# 5) BOSS 更新（插在敌人子弹循环前）
rep("""        // \U0001F9E8 \u654c\u4eba\u7684\u5b50\u5f39\uff01\uff08\u540c\u4e00\u5c42\u624d\u80fd\u6253\u4e2d\u4f60\uff09
""",
    """        // \U0001F479 BOSS\uff01\uff08\u5730\u9762\u5de8\u53d8\u6012\uff0c\u53ea\u5728\u5730\u9762\uff09
        if (boss && boss.hp > 0) {
            var bd = Math.sqrt((boss.x - player.x) * (boss.x - player.x) + (boss.y - player.y) * (boss.y - player.y));
            var bs = 70 * dt;
            var bmx = 0, bmy = 0;
            if (bd > 200 && bd > 0.01) {
                bmx = (player.x - boss.x) / bd * bs;
                bmy = (player.y - boss.y) / bd * bs;
            } else if (bd < 90 && bd > 0.01) {
                bmx = -(player.x - boss.x) / bd * bs;
                bmy = -(player.y - boss.y) / bd * bs;
            } else {
                boss.wander += dt;
                bmx = Math.cos(boss.wander) * bs * 0.3;
                bmy = Math.sin(boss.wander) * bs * 0.3;
            }
            if (!rectHit(boss.x + bmx, boss.y, 20)) boss.x += bmx;
            if (!rectHit(boss.x, boss.y + bmy, 20)) boss.y += bmy;
            boss.x = Math.max(20, Math.min(MAPW - 20, boss.x));
            boss.y = Math.max(20, Math.min(MAPH - 20, boss.y));
            // \U0001F479 \u6247\u5f62\u5c04\u51fb\uff13\u53d1\uff01
            if (player.floor === 1 && bd < 520 && boss.shotCd <= 0) {
                boss.shotCd = 2.0;
                var ba = Math.atan2(player.y - boss.y, player.x - boss.x);
                for (var bk = -1; bk <= 1; bk++) {
                    enemyShots.push({ x: boss.x, y: boss.y, vx: Math.cos(ba + bk * 0.2) * 210, vy: Math.sin(ba + bk * 0.2) * 210, life: 2.4, f: 1, b: -1 });
                }
            }
            if (boss.shotCd > 0) boss.shotCd -= dt;
            // \U0001F479 \u8fd1\u8eab\u649e\u4eba
            if (player.floor === 1 && bd < 42 && player.hitCd <= 0) {
                player.hp -= Math.round(18 * ((gear.armor || wornArmor >= 0) ? 0.7 : 1) * (wornHelmet >= 0 ? 0.8 : 1));
                player.hitCd = 0.8;
                showMsg('\U0001F479 BOSS \u649e\u4f60\uff01');
                document.getElementById('hpbar').style.width = (Math.max(0, player.hp) / maxHp * 100) + '%';
                document.getElementById('hpnum').textContent = Math.max(0, player.hp);
                if (player.hp <= 0) { player.hp = 0; state = 'lose'; }
            }
            // \U0001F479 \u8840\u6761
            document.getElementById('bossbar-wrap').style.display = 'flex';
            document.getElementById('bossfill').style.width = (Math.max(0, boss.hp) / boss.maxHp * 100) + '%';
            document.getElementById('bosshp').textContent = Math.max(0, boss.hp);
        } else {
            document.getElementById('bossbar-wrap').style.display = 'none';
        }

        // \U0001F9E8 \u654c\u4eba\u7684\u5b50\u5f39\uff01\uff08\u540c\u4e00\u5c42\u624d\u80fd\u6253\u4e2d\u4f60\uff09
""",
    'boss-update')

# 6) killBoss 函数（放在 killEnemy 后）
rep("""    // \U0001F52B \u5207\u67aa\uff1aQ / 1 / 2
""",
    """    // \U0001F479 \u51fb\u8d25 BOSS\uff1a\u5927\u5956\u52b1\uff01
    function killBoss() {
        if (!boss) return;
        dropWeaponPickup(boss.x, boss.y);
        dropWeaponPickup(boss.x + 22, boss.y + 22);
        drops.push({ x: boss.x - 22, y: boss.y + 10 });
        score += 200; kills++;
        showMsg('\U0001F479 \u51fb\u8d25 BOSS\uff01+200\u5206\uff0c\u7206\u51fa 2 \u628a\u67aa\u548c\u5b50\u5f39\uff01');
        boss = null;
        document.getElementById('bossbar-wrap').style.display = 'none';
    }

    // \U0001F52B \u5207\u67aa\uff1aQ / 1 / 2
""",
    'killboss')

# 7) 画：哨塔 + BOSS + 3楼楼顶
rep("""        // \U0001F4E6 \u7bb1\u5b50
        ctx.font = '26px sans-serif';
        ctx.textAlign = 'center';
        for (var i = 0; i < crates.length; i++) {
            ctx.fillText('\U0001F4E6', crates[i].x, crates[i].y + 9);
        }
""",
    """        // \U0001F3DC\ufe0f \u9505\u5854\uff08\u76f4\u63a5\u4e0a3\u697c\uff01\uff09
        for (var ti = 0; ti < towers.length; ti++) {
            var tw = towers[ti];
            ctx.fillStyle = 'rgba(70, 60, 40, 0.92)';
            ctx.fillRect(tw.x, tw.y, tw.w, tw.h);
            ctx.strokeStyle = '#8a7a55';
            ctx.lineWidth = 3;
            ctx.strokeRect(tw.x, tw.y, tw.w, tw.h);
            ctx.fillStyle = 'rgba(255,255,255,0.75)';
            ctx.font = 'bold 13px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('\u26F0\ufe0f 3\u697c', tw.x + tw.w / 2, tw.y + tw.h / 2 + 4);
            ctx.font = '18px sans-serif';
            ctx.fillText('\U0001FA9C', tw.x + tw.w / 2, tw.y + tw.h + 34);
        }

        // \U0001F4E6 \u7bb1\u5b50
        ctx.font = '26px sans-serif';
        ctx.textAlign = 'center';
        for (var i = 0; i < crates.length; i++) {
            ctx.fillText('\U0001F4E6', crates[i].x, crates[i].y + 9);
        }
""",
    'draw-towers')

rep("""            ctx.fillStyle = '#ffd93d';
            ctx.font = 'bold 12px sans-serif';
            ctx.fillText(Math.max(0, e.hp), e.x, e.y - 42);
        }
""",
    """            ctx.fillStyle = '#ffd93d';
            ctx.font = 'bold 12px sans-serif';
            ctx.fillText(Math.max(0, e.hp), e.x, e.y - 42);
        }

        // \U0001F479 BOSS
        if (boss && boss.hp > 0) {
            ctx.font = '48px sans-serif';
            ctx.fillText('\U0001F479', boss.x, boss.y + 16);
            ctx.fillStyle = '#333';
            ctx.fillRect(boss.x - 40, boss.y - 46, 80, 8);
            ctx.fillStyle = '#ff2d55';
            ctx.fillRect(boss.x - 40, boss.y - 46, 80 * Math.max(0, boss.hp / boss.maxHp), 8);
            ctx.fillStyle = '#ffd93d';
            ctx.font = 'bold 13px sans-serif';
            ctx.fillText('\U0001F479 ' + Math.max(0, boss.hp), boss.x, boss.y - 56);
        }
""",
    'draw-boss')

rep("""            ctx.fillText('\U0001FA9C', bb.x + T + 24, bb.y + T + 40);   // \u697c\u68af\u53e3
        }

        // \U0001F3C3 \u73a9\u5bb6\uff08\u62ff\u67aa\u5c0f\u4eba\uff09
""",
    """            ctx.fillText('\U0001FA9C', bb.x + T + 24, bb.y + T + 40);   // \u697c\u68af\u53e3
        }
        // \u26F0\ufe0f \u9505\u5854\u9876 3 \u697c\uff08\u9ad8\u5904\uff0c\u80fd\u6253\u5230\u4e0b\u9762\u4e00\u5207\uff09
        if (player.floor === 3 && player.tIdx >= 0) {
            var ttw = towers[player.tIdx];
            ctx.fillStyle = 'rgba(120, 100, 60, 0.9)';
            ctx.fillRect(ttw.x + 6, ttw.y + 6, ttw.w - 12, ttw.h - 12);
            ctx.strokeStyle = '#c8a86a';
            ctx.lineWidth = 3;
            ctx.strokeRect(ttw.x + 6, ttw.y + 6, ttw.w - 12, ttw.h - 12);
            ctx.fillStyle = 'rgba(255,255,255,0.9)';
            ctx.font = 'bold 14px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('\u26F0\ufe0f \u9505\u5854 3\u697c', ttw.x + ttw.w / 2, ttw.y + ttw.h / 2 + 4);
            ctx.font = '16px sans-serif';
            ctx.fillText('\U0001FA9C', ttw.x + ttw.w / 2, ttw.y + 28);
        }

        // \U0001F3C3 \u73a9\u5bb6\uff08\u62ff\u67aa\u5c0f\u4eba\uff09
""",
    'draw-tower-top')

# 8) BOSS 血条 HTML + CSS
rep("""<div id="msg"></div>
""",
    """<div id="msg"></div>
<div id="bossbar-wrap" style="display:none">
    <span>\U0001F479 BOSS</span>
    <div class="bar" id="bossbar"><div id="bossfill" style="width:100%"></div></div>
    <span id="bosshp">500</span>
</div>
""",
    'bossbar-html')

rep("""    #hud .bar div { height: 100%; background: linear-gradient(90deg, #ff7e5f, #ff5d5d); border-radius: 8px; transition: width 0.2s; }
""",
    """    #hud .bar div { height: 100%; background: linear-gradient(90deg, #ff7e5f, #ff5d5d); border-radius: 8px; transition: width 0.2s; }
    #bossbar-wrap {
        position: fixed;
        top: 52px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 15px;
        color: #ff5d7a;
        background: rgba(0, 0, 0, 0.6);
        padding: 6px 14px;
        border-radius: 12px;
        z-index: 10;
    }
    #bossbar-wrap .bar { width: 220px; height: 12px; }
    #bossbar-wrap .bar div { background: linear-gradient(90deg, #ff2d55, #ff7a3c); }
""",
    'bossbar-css')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('PART 2 done')
