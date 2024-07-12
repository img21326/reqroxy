import requests
from fake_useragent import UserAgent
import time
from .proxy import Proxies 
ua = UserAgent()


NEED_TO_RETRY = "0"
NEED_TO_RETRY_WITH_COUNT = "1"


class MaxRetryError(BaseException):
    pass

class Req:

    @staticmethod
    def get(url, params=None, use_proxy = False, custom_retry_func=None, retry=0):
        if retry > 30:
            raise MaxRetryError
        if use_proxy:
            proxy_url = Proxies.get_instance().get_proxy()
            proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
        else:
            proxies = None
        try:
            r = requests.get(
                f'{url}', params=params, headers={'User-Agent': ua.random}, proxies=proxies, timeout=5)
            if custom_retry_func != None:
                retry_func_result = custom_retry_func(r)
                if retry_func_result == NEED_TO_RETRY:
                    return Req.get(url, params=params, use_proxy=use_proxy, custom_retry_func=custom_retry_func, retry=retry)
                elif retry_func_result == NEED_TO_RETRY_WITH_COUNT:
                    return Req.get(url, params=params, use_proxy=use_proxy, custom_retry_func=custom_retry_func, retry=retry+1)
            return r
        # except requests.exceptions.ProxyError:
        #     time.sleep(3) 
        #     return Req.get(url, params=params, use_proxy=use_proxy, custom_retry_func=custom_retry_func, retry=retry+1)
        # except requests.exceptions.Timeout:
        #     time.sleep(3) 
        #     return Req.get(url, params=params, use_proxy=use_proxy, custom_retry_func=custom_retry_func, retry=retry+1)
        # except requests.exceptions.SSLError:
        #     time.sleep(3) 
        #     return Req.get(url, params=params, use_proxy=use_proxy, custom_retry_func=custom_retry_func, retry=retry+1)
        # except requests.exceptions.ConnectionError:
        #     time.sleep(3) 
        #     return Req.get(url, params=params, use_proxy=use_proxy, custom_retry_func=custom_retry_func, retry=retry+1)
        except Exception as e:
            # time.sleep(3) 
            print(f'url: {url}, params: {params}, use_proxy: {use_proxy}, custom_retry_func: {custom_retry_func}, retry: {retry}, error: {e}')
            return Req.get(url, params=params, use_proxy=use_proxy, custom_retry_func=custom_retry_func, retry=retry+1)

    @staticmethod
    def post(url, params=None, use_proxy=None, custom_retry_func=None, retry=0, **kwargs):
        if retry > 10:
            raise MaxRetryError
        if use_proxy:
            proxy_url = Proxies.get_instance().get_proxy()
            proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
        else:
            proxies = None
        try:
            r = requests.post(
                f'{url}', params=params, headers={'User-Agent': ua.random}, proxies=proxies, timeout=10, **kwargs)
            if custom_retry_func != None:
                retry_func_result = custom_retry_func(r)
                if retry_func_result == NEED_TO_RETRY:
                    return Req.post(url, params=params, use_proxy=use_proxy, custom_retry_func=custom_retry_func, retry=retry, **kwargs)
                elif retry_func_result == NEED_TO_RETRY_WITH_COUNT:
                    return Req.post(url, params=params, use_proxy=use_proxy, custom_retry_func=custom_retry_func, retry=retry+1, **kwargs)
            return r
        except requests.exceptions.ProxyError:
            time.sleep(3) 
            return Req.post(url, params=params, use_proxy=use_proxy, custom_retry_func=custom_retry_func, retry=retry+1, **kwargs)
        except requests.exceptions.Timeout:
            time.sleep(3) 
            return Req.post(url, params=params, use_proxy=use_proxy, custom_retry_func=custom_retry_func, retry=retry+1, **kwargs)
        except requests.exceptions.SSLError:
            time.sleep(3) 
            return Req.post(url, params=params, use_proxy=use_proxy, custom_retry_func=custom_retry_func, retry=retry+1, **kwargs)
