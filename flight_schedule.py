#!/usr/bin/env python

import os
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

import browser
from event import Event

import pdb

class FlightSchedule(browser.Browser):
    attr_table = { 'reservation | reservationListResourceDisplayFilter' : 'resource',
                   'reservation | reservationListCustomerDisplayFilter:operator' : 'customer',
                }
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
        time.sleep(3)

    def get_schedule(self):
        self.driver.get('https://app.flightschedulepro.com/App/Reservations/')
        time.sleep(5)
        events = []
        soup = BeautifulSoup(self.get_html(), 'html.parser')
        table = soup.find('table').find('tbody')
        for row in table.find_all('tr'):
            event = Event()
            for cell in row.find_all('td'):
                for times in cell.find_all('time'):
                    try:
                        event.push_time(times['datetime'])
                    except KeyError:
                        pass
                try:
                    attr = self.attr_table[cell['ng-bind-html']]
                    if cell.string:
                        value = [cell.string]
                    else:
                        value = list(cell.strings)
                    setattr(event, attr, value)
                except KeyError:
                    pass
            events.append(event)
        return events

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

    #for event in events:
    #    driver.store_event(event)
    for event in driver.get_schedule():
        print(event, '\n')
    if not args.view:
        driver.driver.close()
