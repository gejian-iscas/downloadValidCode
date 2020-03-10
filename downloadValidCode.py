import time
import os

base_url = 'https://www.creditease.cn/servlet/validateCodeServlet?'
for i in range(500):
    t = time.time()
    now_time = int(round(t*1000))
    url = base_url+str(now_time)
    file_name = "pics/" + str(i) + ".jpg"
    os.popen('curl -o %s %s'%(file_name, url))
    print("%d finished."%i)
