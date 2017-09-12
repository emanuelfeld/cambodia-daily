from selenium import webdriver
from config import CHROMEDRIVER_PATH
# from config import DCAP, PHANTOMJS_PATH, 

import random
import sys
import time


def random_pause(mean=10):
    t = mean + random.uniform(-mean / 4, mean / 4)
    return t


if __name__ == "__main__":
    BACKUP_URL = "https://web.archive.org/save/"
    LOOKUP_URL = "https://web.archive.org/web/*/"
    browser = webdriver.Chrome(executable_path = CHROMEDRIVER_PATH)
    # browser = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH, desired_capabilities=DCAP)

    # pipe in URLs from stdin to archive
    for url in sys.stdin:
        url = url.strip()
        if url:
            try:
                browser.get(BACKUP_URL + url)
                message = u"ok\t{url} \u2192 {prefix}{url}".format(url=url, prefix=LOOKUP_URL)
            except Exception as e:
                print(e)
                message = u":(\t{}".format(url)
            print(message)
            time.sleep(random_pause(5))
