from selenium.webdriver.common.proxy import *
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import os, socket
from qlib.log import show

phantomjs_path = os.popen("which phantomjs").read().strip()
if not phantomjs_path:
    show("install phantomjs first!!")
    sys.exit(1)


SocialKit_cache_max_size = '1000468'
storage_path = '/tmp/'
cookies_path = '/tmp/cookie.txt'

class ProxyNotConnectError(Exception):
    pass


def test_proxy(proxy):
    t,s,p = proxy.split(":")
    s = s[2:]
    p = int(p)
    try:
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((s,p))
    except Exception as e:
        show(e)
        return False
    return True



class FLowNet:
    def __init__(self, proxy=False, load_img=False, random_agent=False,agent=None,**options):
        
        if proxy:
            if not test_proxy(proxy):
                raise ProxyNotConnectError(proxy + " not connected")

        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        if agent:
            dcap["phantomjs.page.settings.userAgent"] = agent

        # dcap['phantomjs.page.settings.resourceTimeout'] = '5000'
        load_image = 'true' if load_img else 'false' 
        timeout = options.get('timeout')

        web_service_args = [
            '--load-images=' + load_image,
        ]

        if proxy:
            proxy_t, proxy_c = proxy.split("//")
            proxy_t = proxy_t[:-1]
            show(proxy_c, proxy_t)
            web_service_args += [
                '--proxy=' + proxy_c,
                '--proxy-type=' + proxy_t,
                '--local-storage-path=' + storage_path,
                '--cookies-file=' + cookies_path,
                '--local-storage-quota=' + str(SocialKit_cache_max_size),
            ]

        self.phantom = webdriver.PhantomJS(phantomjs_path,service_args=web_service_args, desired_capabilities=dcap)
        if timeout:
            self.phantom.set_page_load_timeout(int(timeout))
        self.dcap = dcap

    def go(self, url):
        self.phantom.get(url)

    def __call__(self, selectID, action, *args, save_data=False, **kargs):
        if selectID.strip().startswith("."):
            target = self.phantom.find_element_by_class_name(selectID[1:])
        elif selectID.strip().startswith("#"):
            target = self.phantom.find_element_by_id(selectID[1:])
        else:
            target = self.phantom.find_element_by_tag_name(selectID[1:])
        if hasattr(target, action):
            func = getattr(target, action)
            func(*args, **kargs)
            


