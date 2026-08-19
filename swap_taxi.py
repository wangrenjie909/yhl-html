# -*- coding: utf-8 -*-
import io

path = r'C:\ai\code\yhl-html\index.html'
src = io.open(path, encoding='utf-8').read()

old1 = '<div class="theme-card" id="theme-football">\n                <div class="card-inner">\n                    <div class="card-front">\u26BD \u8db3\u7403</div>\n                    <div class="card-back">\u26BD \u8db3\u7403\u4e3b\u9898<br>\u5236\u4f5c\u4e2d\uff5e</div>\n                </div>\n            </div>'
new1 = '<div class="theme-card" id="theme-taxi">\n                <div class="card-inner">\n                    <div class="card-front">\U0001F695 \u51fa\u79df\u8f66</div>\n                    <div class="card-back">\U0001F695 \u51fa\u79df\u8f66\u4e3b\u9898<br>\u5236\u4f5c\u4e2d\uff5e</div>\n                </div>\n            </div>'

old2 = "document.getElementById('theme-football').addEventListener('click', function () {\n            themeStatus.textContent = '\u26BD \u8db3\u7403\u4e3b\u9898\u6b63\u5728\u5236\u4f5c\u4e2d\uff01\u656c\u8bf7\u671f\u5f85\uff5e';\n        });"
new2 = "document.getElementById('theme-taxi').addEventListener('click', function () {\n            themeStatus.textContent = '\U0001F695 \u51fa\u79df\u8f66\u4e3b\u9898\u6b63\u5728\u5236\u4f5c\u4e2d\uff01\u656c\u8bf7\u671f\u5f85\uff5e';\n        });"

for old, new, name in [(old1, new1, 'card'), (old2, new2, 'js')]:
    assert src.count(old) == 1, '%s match = %d' % (name, src.count(old))
    src = src.replace(old, new)
    print('OK replaced', name)

io.open(path, 'w', encoding='utf-8').write(src)
print('done')
