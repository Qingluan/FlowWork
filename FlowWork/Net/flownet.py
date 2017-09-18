from selenium.webdriver.common.proxy import *
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os, socket
from qlib.log import show
from bs4 import BeautifulSoup as BS

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
    keys = Keys
    def __init__(self, url, proxy=False, load_img=False, random_agent=False,agent=None,**options):
        
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
        self.datas = []
        self.go(url)

    def go(self, url):
        self.phantom.get(url)

    def _wait(self, selector, timeout=7):
        try:
            if '.' in selector:
                wait = WebDriverWait(self.phantom,timeout).until(
                    EC.presence_of_element_located((By.CLASS_NAME,selector[1:])))
            elif '#' in selector:
                wait = WebDriverWait(self.phantom,timeout).until(
                    EC.presence_of_element_located((By.ID,selector[1:])))
            else:
                wait = WebDriverWait(self.phantom,timeout).until(
                    EC.presence_of_element_located((By.TAG_NAME,selector)))
        except Exception as e:
            self.screenshot('debug')
            raise e

    def save_tmp(self, key=None):
        if self.phantom.current_url in self.datas:
            self.datas[self.phantom.current_url].append(self.phantom.page_source)
        else:
            self.datas[self.phantom.current_url] = [self.phantom.page_source]

    def screenshot(self, *names):
        if len(names) > 0:
            self.phantom.get_screenshot_as_file('/tmp/' + names[0]+".png")
        else:
            self.phantom.get_screenshot_as_file('/tmp/one.png')

    def do(self, selectID, *args, save_screen=True,save_data=False, wait=None, clear=False, callback=None,**kargs):
        """
        css select mode :
            div .
        """
        selectID = selectID.strip()
        if '>' in selectID:
            self._wait(selectID.split(">")[-1])
        else:
            self._wait(selectID)
        res = None
        target = self.find(selectID)
        
        if len(args) == 1:
            if clear:
                target.clear()    
            target.send_keys(args[0])
        elif len(args) == 0:
            target.click()
        else:
            raise Exception("no such operator!!")


        if wait:
            if isinstance(wait, str):
                self._wait(wait)
            elif isinstance(wait, int):
                time.sleep(wait)
            else:
                show("unknow wait type: (only: int, str)", color='red')

        if callback:
            callback(self.phantom.page_source)

        if save_data:
            if isinstance(save_data, bool):
                self.save_tmp()
            elif isinstance(save_data, str):
                # a fliter ...
                pass
        if save_screen:
            self.screenshot(self.phantom.current_url)

        return self

    def find(self, selectID):
        selectIDs = selectID.split(">")
        target = self.phantom
        targets = []
        l = len(selectIDs)
        for no, SLE in enumerate(selectIDs):
            try:
                if SLE.startswith("."):
                    if ':' in SLE:
                        n, i = SLE[1:].split(':')
                        # show(n,i)
                        target = target.find_elements_by_class_name(n)[int(i)]
                    else:
                        target = target.find_element_by_class_name(SLE[1:])
                elif SLE.startswith("#"):
                    if ':' in SLE:
                        n, i = SLE[1:].split(':')
                        # show(n,i)
                        target = target.find_elements_by_id(n)[int(i)]
                    else:
                        target = target.find_element_by_id(SLE[1:])
                else:
                    if ':' in SLE:
                        n, i = SLE.split(':')
                        # show(n,i)
                        target = target.find_elements_by_tag_name(n)[int(i)]
                    else:
                        target = target.find_element_by_tag_name(SLE)
            except NoSuchElementException as e:
                show("can not found , continue", e)
                if no == l-1:
                    raise e
                continue
        return target
    
    def html(self):
        return self.phantom.page_source




