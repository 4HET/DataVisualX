import os
import subprocess
import execjs

with open('./v1.js', 'r', encoding='utf-8') as fp:
    js = fp.read()

JS = execjs.compile(js)
sign = JS.call("func","hhh")
print(sign)
# signature = subprocess.getoutput('node v1.js')