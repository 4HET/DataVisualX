import json
import os
import subprocess
import execjs

with open('./rohr.min.js', 'r', encoding='utf-8') as fp:
    js = fp.read()

JS = execjs.compile(js)
sign = JS.call("hhh_token",'https://www.dianping.com?shopId=H8mrf4qzTjyV6sji')
print(sign)
