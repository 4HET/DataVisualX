import json
import traceback
from concurrent.futures import ThreadPoolExecutor
import threading
import time

from DataVisualX.static.scripts.get_res_name_and_url import spj, get_csv, list_to_csv, update_log

def th(k):
    try:
        url = json_data[k]
        if spj(url):
            print("{}已经爬取完成".format(k))
            return
        for i in range(1, 5):
            csv_path = 'csv/{}.csv'.format(k)
            list_data = get_csv(url, i)
            list_to_csv(csv_path, list_data)
            print("第{}页已爬取完成".format(i))
        print('{}已经爬取完成'.format(k))
        update_log(url)
        # time.sleep(random.randint(3))
    except Exception as e:
        print(traceback.format_exc())
        return

if __name__ == '__main__':
    with open("./json/city_list.json", encoding="utf-8") as f:
        json_data = json.load(f)
    # if not os.path.exists(csv_path):
    #     os.makedirs(csv_path)
    ks = json_data.keys()
    cnt = 0
    with ThreadPoolExecutor(max_workers=10) as t:  # 创建一个最大容纳数量为5的线程池
        for k in ks:
            t.submit(th, k)