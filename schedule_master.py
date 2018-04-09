#!/usr/bin/env python

import os
import browser

import event

class ScheduleMaster(browser.Browser):
    def __init__(self):
        self.userid = os.environ['SM_USERID']
        self.password = os.environ['SM_PASSWORD']
        self.schedule = []
        super().__init__("https://my.schedulemaster.com")

    def login(self):
        for form in self.driver.find_elements_by_tag_name('form'):
            if form.get_attribute('action').split('/')[-1] == 'login.asp':
                userid = form.find_element_by_name('USERID')
                userid.send_keys(self.userid)
                password = form.find_element_by_name('DATA')
                password.send_keys(self.password)
                form.submit()
        
    def get_schedule(self):
        schedule = []
        self.driver.get(self.driver.find_element_by_id('asp_legacy').get_attribute('src'))
        table = self.driver.find_element_by_id('res_table2')
        for button in table.find_elements_by_tag_name('button'):
            attr = button.get_attribute('onMouseOver')
            if attr is not None:
                schedule.append(event.Event().from_sm(attr))
                # schedule.append(attr)
        return schedule

if __name__ == '__main__':
    driver = ScheduleMaster()
    driver.login()
    schedule = driver.get_schedule()
    for event in schedule:
        print(event, '\n')
    driver.driver.close()
