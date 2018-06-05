#!/usr/bin/env python

import os
from selenium.webdriver.support.ui import Select

import browser
import sm_event

class ScheduleMaster(browser.Browser):
    def __init__(self, headless = True):
        self.userid = os.environ['SM_USERID']
        self.password = os.environ['SM_PASSWORD']
        self.schedule = []
        super().__init__("https://my.schedulemaster.com", headless = headless)
        self.logger = logging.getLogger(__name__)
        self.logger.info('fetched login page')

    def login(self):
        for form in self.driver.find_elements_by_tag_name('form'):
            if form.get_attribute('action').split('/')[-1] == 'login.asp':
                userid = form.find_element_by_name('USERID')
                userid.send_keys(self.userid)
                password = form.find_element_by_name('DATA')
                password.send_keys(self.password)
                form.submit()
        # switch to iframe
        self.driver.get(self.driver.find_element_by_id('asp_legacy').get_attribute('src'))
        self.userid = self.driver.find_element_by_name('USERID').get_attribute('value')
        self.session = self.driver.find_element_by_name('SESSION').get_attribute('value')
        self.schedule = self.driver.find_element_by_id('res_table2')
        self.username = self.schedule.find_element_by_class_name('InactiveLink').text.split(',')[0]
        self.logger.info('login successful')
        
    def get_schedule(self):
        schedule = []
        for button in self.schedule.find_elements_by_tag_name('button'):
            attr = button.get_attribute('onMouseOver')
            if attr is not None:
                schedule.append(sm_event.SMEvent().from_sm(attr))
        self.logger.info('fetched current schedule')
        return schedule

    def store_event(self, event):
        url = ['https://my.schedulemaster.com/schedlesson.aspx?WINDOW=YES']
        url.append('N_NO={}'.format(self.username))
        url.append('USERID={}'.format(self.userid))
        url.append('SESSION={}'.format(self.session))
        self.driver.get('&'.join(url))
        self.fill_date('ctl00_CPL1_dt_StartDate2', 'ctl00_CPL1_ddl_StartTime2', event.start)
        self.fill_date('ctl00_CPL1_dt_EndDate2', 'ctl00_CPL1_ddl_EndTime2', event.end)
        self.driver.find_element_by_name('ctl00$CPL1$btnMakeSched').click()
        self.logger.info('stored event\n{}'.format(event))

    def fill_date(self, id_date, id_time, value):
        date = self.driver.find_element_by_id(id_date)
        date.clear()
        date.send_keys('{}/{}/{}'.format(value.month, value.day, value.year))
        time = Select(self.driver.find_element_by_id(id_time))
        time.select_by_index(value.hour * 2 + int(value.minute / 30))


if __name__ == '__main__':
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
    driver = ScheduleMaster(not args.view)
    driver.login()
    for event in events:
        driver.store_event(event)
    for event in driver.get_schedule():
        print(event, '\n')
    driver.driver.close()
