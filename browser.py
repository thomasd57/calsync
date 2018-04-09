from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Browser:
    def __init__(self, url = None):
        options = webdriver.firefox.options.Options()
        options.set_headless()
        self.driver = webdriver.Firefox(options = options)
        self.driver.implicitly_wait(10)
        if url is not None:
            self.driver.get(url)
