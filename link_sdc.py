# -*- coding: utf-8 -*-
import io

path = r'C:\ai\code\yhl-html\index.html'
src = io.open(path, encoding='utf-8').read()

old1 = '<div class="card-front">\u641c\u6253\u64a4</div>\n                    <div class="card-back">\u641c\u6253\u64a4\u4e3b\u9898<br>\u5236\u4f5c\u4e2d\uff5e</div>'
new1 = '<div class="card-front">\u641c\u6253\u64a4</div>\n                    <div class="card-back">\u641c\u6253\u64a4\u7f51\u9875<br>\u70b9\u6211\u8fdb\u5165\uff01</div>'

old2 = "document.getElementById('theme-taxi').addEventListener('click', function () {\n            themeStatus.textContent = '\u641c\u6253\u64a4\u4e3b\u9898\u6b63\u5728\u5236\u4f5c\u4e2d\uff01\u656c\u8bf7\u671f\u5f85\uff5e';\n        });"
new2 = "document.getElementById('theme-taxi').addEventListener('click', function () {\n            window.location.href = 'sdc.html';   // \U0001F525 \u641c\u6253\u64a4\uff1a\u641c\u8d44\u6e90\u00b7\u6253\u654c\u4eba\u00b7\u64a4\u79bb\uff01\n        });"

for old, new, name in [(old1, new1, 'card'), (old2, new2, 'js')]:
    assert src.count(old) == 1, '%s match = %d' % (name, src.count(old))
    src = src.replace(old, new)
    print('OK replaced', name)

io.open(path, 'w', encoding='utf-8').write(src)
print('done')
