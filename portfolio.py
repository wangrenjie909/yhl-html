# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\ai\code\yhl-html\index.html'
src = io.open(path, encoding='utf-8').read()
n0 = len(src)

def rep(old, new, name, count=1):
    global src
    assert src.count(old) == count, '%s match = %d' % (name, src.count(old))
    src = src.replace(old, new)
    print('OK', name)

# 1) 作品集网格 + 卡片浮起发光
rep("""        /* \U0001F5BC\ufe0f \u4f5c\u54c1\u96c6 */
        #works .work-grid {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
            margin-top: 10px;
        }
        .work-card {
            width: 240px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 14px;
            color: #fff;
            text-decoration: none;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .work-card:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        }
""",
    """        /* \U0001F5BC\ufe0f \u4f5c\u54c1\u96c6 */
        #works .work-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            max-width: 880px;
            margin: 10px auto 0;
        }
        .work-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 14px;
            color: #fff;
            cursor: pointer;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .work-card:hover {
            transform: translateY(-8px) scale(1.02);   /* \U0001F500 \u6d6e\u8d77 + \u653e\u5927 */
            box-shadow: 0 15px 35px rgba(255, 126, 95, 0.45);   /* \u53D1\u5149\uff01 */
        }
        @media (max-width: 640px) {
            #works .work-grid { grid-template-columns: 1fr; }
        }
""",
    'works-css')

# 2) 搜打撤卡片缩略图背景
rep("        .thumb-moto { background: linear-gradient(135deg, #0f0c29, #302b63); }\n",
    "        .thumb-moto { background: linear-gradient(135deg, #0f0c29, #302b63); }\n        .thumb-sdc { background: linear-gradient(135deg, #0f2027, #2c5364); }\n",
    'thumb-sdc')

# 3) 灯箱样式
rep("        .work-card p { font-size: 13px; opacity: 0.9; margin: 0; line-height: 1.5; }\n        /* \U0001F4EE \u8054\u7cfb\u6211 */\n",
    """        .work-card p { font-size: 13px; opacity: 0.9; margin: 0; line-height: 1.5; }
        /* \U0001F4E1 \u706f\u7bb1\uff08\u70b9\u51fb\u5361\u7247\u5168\u5c4f\u67e5\u770b\uff09 */
        .lightbox {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.92);
            z-index: 9999;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        .lightbox.active { display: flex; }
        .lightbox-content { padding: 30px; max-width: 540px; }
        .lightbox-emoji { font-size: 110px; margin-bottom: 6px; }
        .lightbox-content h3 { font-size: 28px; margin: 10px 0; }
        .lightbox-content p { font-size: 16px; opacity: 0.9; line-height: 1.8; }
        .lightbox-close {
            position: absolute;
            top: 16px;
            right: 28px;
            color: #fff;
            font-size: 44px;
            cursor: pointer;
            opacity: 0.9;
        }
        .lightbox-close:hover { opacity: 1; transform: scale(1.15); }
        /* \U0001F4EE \u8054\u7cfb\u6211 */
""",
    'lightbox-css')

# 4) 作品集 HTML：3 个卡片
rep("""    <section id="works">
        <h2>\U0001F5BC\ufe0f \u6211\u7684\u4f5c\u54c1\u96c6</h2>
        <div class="work-grid">
            <a class="work-card" href="index.html">
                <div class="work-thumb thumb-rooftop">\U0001F3D9\ufe0f</div>
                <h3>\u8dd1\u9177\u8005\u7684\u5929\u53f0</h3>
                <p>\u6211\u7684\u4e3b\u9875\uff1a\u8dd1\u9177\u5c0f\u6e38\u620f\u3001\u97f3\u4e50\u64ad\u653e\u5668\u3001\u70ab\u9177\u89c6\u9891\u3001\u8868\u60c5\u96e8\u9b54\u6cd5\uff01</p>
            </a>
            <a class="work-card" href="moto.html">
                <div class="work-thumb thumb-moto">\U0001F3CD\ufe0f</div>
                <h3>\u6469\u6258\u98de\u9a70</h3>
                <p>\u6469\u6258\u8f66\u7f51\u9875\uff1a90\u00b0\u5f2f\u9053\u7ade\u901f\u300111\u79cd\u54c1\u724c\u89e3\u9501\u3001\u8d2d\u8f66 + \u6210\u5c31\u7cfb\u7edf\uff01</p>
            </a>
        </div>
    </section>
""",
    """    <section id="works">
        <h2>\U0001F5BC\ufe0f \u6211\u7684\u4f5c\u54c1\u96c6</h2>
        <p class="intro">\u70b9\u51fb\u5361\u7247\u5168\u5c4f\u67e5\u770b\uff01</p>
        <div class="work-grid">
            <div class="work-card" data-emoji="\U0001F3D9\ufe0f" data-title="\u8dd1\u9177\u8005\u7684\u5929\u53f0" data-href="index.html" data-desc="\u6211\u7684\u4e3b\u9875\uff1a\u8dd1\u9177\u5c0f\u6e38\u620f\u3001\u97f3\u4e50\u64ad\u653e\u5668\u3001\u70ab\u9177\u89c6\u9891\u3001\u8868\u60c5\u96e8\u9b54\u6cd5\uff01" onclick="openLightbox(this)">
                <div class="work-thumb thumb-rooftop">\U0001F3D9\ufe0f</div>
                <h3>\u8dd1\u9177\u8005\u7684\u5929\u53f0</h3>
                <p>\u6211\u7684\u4e3b\u9875\uff1a\u8dd1\u9177\u5c0f\u6e38\u620f\u3001\u97f3\u4e50\u3001\u89c6\u9891\u3001\u8868\u60c5\u96e8\uff01</p>
            </div>
            <div class="work-card" data-emoji="\U0001F3CD\ufe0f" data-title="\u6469\u6258\u98de\u9a70" data-href="moto.html" data-desc="\u6469\u6258\u8f66\u7ade\u901f\u6e38\u620f\uff1a\u771f90\u00b0\u5f2f\u9053\u3001\u5934\u76d4/\u98d8\u79fb/\u6781\u901f\u3001\u54c1\u724c\u89e3\u9501 + \u6210\u5c31\u7cfb\u7edf\uff01" onclick="openLightbox(this)">
                <div class="work-thumb thumb-moto">\U0001F3CD\ufe0f</div>
                <h3>\u6469\u6258\u98de\u9a70</h3>
                <p>\u771f90\u00b0\u5f2f\u9053\u7ade\u901f\u3001\u98d8\u79fb\u3001\u6781\u901f\u3001\u54c1\u724c\u89e3\u9501\uff01</p>
            </div>
            <div class="work-card" data-emoji="\U0001F525" data-title="\u641c\u6253\u64a4" data-href="sdc.html" data-desc="\u641c\u8d44\u6e90 \u00b7 \u6253\u654c\u4eba \u00b7 \u64a4\u79bb\uff01\u53cc\u5730\u56fe\u3001\u591a\u67aa\u68f0+\u5200\u3001\u8fdc\u7a0b\u654c\u4eba\u3001\u4ed3\u5e93\u3001\u5546\u5e97\u3001\u91d1\u94b1\u7cfb\u7edf\uff01" onclick="openLightbox(this)">
                <div class="work-thumb thumb-sdc">\U0001F525</div>
                <h3>\u641c\u6253\u64a4</h3>
                <p>\u641c\u8d44\u6e90 \u00b7 \u6253\u654c\u4eba \u00b7 \u64a4\u79bb\uff01\u5b8c\u6574\u751f\u5b58\u5c0f\u6e38\u620f\uff01</p>
            </div>
        </div>
    </section>
""",
    'works-html')

# 5) 灯箱 HTML
rep("    <div id=\"rain\"></div>\n",
    """    <!-- \U0001F4E1 \u706f\u7bb1 -->
    <div class="lightbox" id="lightbox" onclick="closeLightbox()">
        <span class="lightbox-close" onclick="closeLightbox()">\u2715</span>
        <div class="lightbox-content" onclick="event.stopPropagation()">
            <div class="lightbox-emoji" id="lb-emoji">\U0001F3D9\ufe0f</div>
            <h3 id="lb-title"></h3>
            <p id="lb-desc"></p>
            <a id="lb-link" class="magic-btn" href="#" target="_blank">\U0001F680 \u6253\u5f00\u4f5c\u54c1</a>
        </div>
    </div>

    <div id="rain"></div>
""",
    'lightbox-html')

# 6) 灯箱 JS
rep("""            setTimeout(function () { contactBtn.textContent = '\U0001F680 \u53d1\u9001'; }, 2000);
        });
""",
    """            setTimeout(function () { contactBtn.textContent = '\U0001F680 \u53d1\u9001'; }, 2000);
        });

        // \U0001F4E1 \u706f\u7bb1\uff1a\u70b9\u51fb\u5361\u7247\u5168\u5c4f\u67e5\u770b + \u8be6\u60c5\uff01
        function openLightbox(card) {
            document.getElementById('lb-emoji').textContent = card.getAttribute('data-emoji');
            document.getElementById('lb-title').textContent = card.getAttribute('data-title');
            document.getElementById('lb-desc').textContent = card.getAttribute('data-desc');
            document.getElementById('lb-link').href = card.getAttribute('data-href');
            document.getElementById('lightbox').classList.add('active');
        }
        function closeLightbox() {
            document.getElementById('lightbox').classList.remove('active');
        }
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') closeLightbox();
        });
""",
    'lightbox-js')

assert len(src) != n0
io.open(path, 'w', encoding='utf-8').write(src)
print('done')
