# -*- coding: utf-8 -*-
import io

path = r'C:\ai\code\yhl-html\index.html'
src = io.open(path, encoding='utf-8').read()

old = '<h2 id="about">\U0001F4D6 \u5173\u4e8e\u6211</h2>\n    <p class="intro">\u6211\u662f\u4e00\u540d\u57ce\u5e02\u8dd1\u9177\u7231\u597d\u8005\uff01\u559c\u6b22\u5728\u9ad8\u697c\u4e4b\u95f4\u7a7f\u68ad\uff0c\u7ffb\u8d8a\u6bcf\u4e00\u9053\u969c\u788d\uff0c\u5728\u6a59\u7ea2\u8272\u7684\u5915\u9633\u4e0b\u5954\u8dd1\u3002\u6b22\u8fce\u5e38\u6765\u6211\u7684\u5929\u53f0\u5750\u5750\uff01\U0001F604</p>'

new = old + '\n\n    <h3 class="skills-title">\U0001F3AF \u6211\u7684\u6280\u80fd</h3>\n    <div class="skills">\n        <span class="badge">\U0001F9F1 HTML</span>\n        <span class="badge">\U0001F3A8 CSS</span>\n        <span class="badge">\u26A1 JavaScript</span>\n        <span class="badge">\U0001F3C3 \u8dd1\u9177</span>\n        <span class="badge">\U0001F3AE \u6e38\u620f\u5236\u4f5c</span>\n    </div>'

assert src.count(old) == 1, 'match count = %d' % src.count(old)
src = src.replace(old, new)
io.open(path, 'w', encoding='utf-8').write(src)
print('OK added skill badges')
