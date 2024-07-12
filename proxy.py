import requests
import threading
import pandas as pd
import concurrent.futures
import time
import random


class Proxies():
    _instance = None

    @staticmethod
    def get_instance():
        if Proxies._instance is None:
            Proxies()
        return Proxies._instance

    def __init__(self):
        if Proxies._instance is not None:
            raise Exception('only one instance can exist')
        else:
            self._id = id(self)
            Proxies._instance = self

        print('loading proxies')
        self.proxy_classes = [FreeProxy(), SLLProxy()]
        self.index = 0
        self.proxies = []
        self.lock = threading.Lock()
        self.time_stamp = time.time()
        self.update()

    def get_proxies(self):
        for p_class in self.proxy_classes:
            self.proxies.extend(p_class.get_proxies())
        random.shuffle(self.proxies)

    def get_proxy(self):
        with self.lock:
            if time.time() - self.time_stamp >= 600:
                self.update()
            if self.index >= len(self.proxies):
                self.index = 0
            proxy = self.proxies[self.index]
            self.index += 1
        return f'http://{proxy["ip"]}:{proxy["port"]}'

    def update(self):
        with self.lock:
            print('update proxies')
            self.proxies = []
            self.get_proxies()
            self.time_stamp = time.time()
            print(f"可用的proxies數量: {len(self.proxies)}")

class Proxy:
    proxies = []
    valid_proxies = []

    def is_valid_proxy(self, proxy):
        try:
            proxy_url = f'http://{proxy["ip"]}:{proxy["port"]}'
            # r = requests.get("https://api.ipify.org",
            #                  proxies={"http": proxy_url, "https": proxy_url}, timeout=3)
            # if r.status_code == 200 and r.text == proxy['ip']:
            #     return proxy
            r = requests.get("https://www.twse.com.tw/", proxies={"http": proxy_url, "https": proxy_url}, timeout=3)
            if r.status_code == 200:
                return proxy
            return None
        except:
            return None

    def check(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(self.is_valid_proxy, proxy)
                       for proxy in self.proxies]
            for f in concurrent.futures.as_completed(results):
                valid_proxy = f.result()
                if valid_proxy:
                    self.valid_proxies.append(valid_proxy)

    def get_proxies(self):
        pass


class FreeProxy(Proxy):
    def get_proxies(self):
        url = 'https://free-proxy-list.net/'
        response = requests.get(url)
        df_list = pd.read_html(response.text)
        df = df_list[0]
        self.proxies = [{
            'ip': df.iloc[i][0],
            'port': str(df.iloc[i][1]),
        } for i in range(len(df))]
        self.check()
        return self.valid_proxies


class SLLProxy(Proxy):
    def get_proxies(self):
        url = 'https://www.sslproxies.org/'
        response = requests.get(url)
        df_list = pd.read_html(response.text, header=0)
        df = df_list[0]
        for i in range(len(df)):
            self.proxies.append({
                'ip': df.iloc[i][0],
                'port': str(df.iloc[i][1]),
            })
        self.check()
        return self.valid_proxies


if __name__ == '__main__':
    p = SLLProxy()
    print(p.get_proxies())
