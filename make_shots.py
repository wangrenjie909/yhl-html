# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
import os

os.chdir(r'C:\ai\code\yhl-html')

shots = {
    'index.html': 'shot_home.png',
    'moto.html': 'shot_moto.png',
    'sdc.html': 'shot_sdc.png',
}

with sync_playwright() as p:
    b = p.chromium.launch()
    for page_file, out in shots.items():
        page = b.new_page(viewport={'width': 1280, 'height': 900})
        page.goto('file:///C:/ai/code/yhl-html/' + page_file)
        page.wait_for_timeout(2500)
        page.screenshot(path=os.path.join(os.getcwd(), out))
        page.close()
        print('saved', out)
    b.close()
print('ALL DONE')
