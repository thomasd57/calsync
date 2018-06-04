#!/usr/bin/env python

import os
from selenium.webdriver.support.ui import Select

import browser
import event

class FlightSchedule(browser.Browser):
    def __init__(self, headless = True):
        self.userid = os.environ['FS_USERID']
        self.password = os.environ['FS_PASSWORD']
        self.schedule = []
        super().__init__("https://app.flightschedulepro.com/Account/Login", headless = headless)
        self.logger = logging.getLogger(__name__)
        self.logger.info('fetched login page')

    def login(self):
        userid = self.driver.find_element_by_id('username')
        userid.send_keys(self.userid)
        password = self.driver.find_element_by_id('password')
        password.send_keys(self.password)
        submit = self.driver.find_element_by_tag_name('button')
        submit.click()
        self.logger.info('login successful')

    def get_schedule(self):
        self.driver.get('https://app.flightschedulepro.com/App/Reservations/')

if __name__ == '__main__':
    import time
    import argparse
    import json
    import logging
    parser = argparse.ArgumentParser(description = 'Access Schedule Master')
    parser.add_argument('-v', '--view', help = 'See browser window, by default headless', action = 'store_true')
    parser.add_argument('-e', '--event', help = 'Create new events from json file')
    parser.add_argument('-l', '--log_level', help = 'logging level', choices = ('DEBUG', 'INFO', 'WARNING', 'ERROR'), default = 'ERROR')
    args = parser.parse_args()
    logging.basicConfig(format = '%(levelname)s: %(message)s', level = getattr(logging, args.log_level))
    events = []
    if args.event:
        events = json.load(open(args.event))
    driver = FlightSchedule(not args.view)
    driver.login()
    time.sleep(10)
    with open('reservations.html', 'w') as fp:
        fp.write(driver.get_html())

    #for event in events:
    #    driver.store_event(event)
    #for event in driver.get_schedule():
    #    print(event, '\n')
    if not args.view:
        driver.driver.close()
