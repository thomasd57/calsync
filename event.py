#!/usr/bin/env python3
from datetime import datetime

class Event:
    def __init__(self, start = None, end = None, customer = None, resource = None):
        self.start = start
        self.end = end
        self.customer = customer
        self.resource = resource

    @staticmethod
    def dt_from_str(dt):
        dt = datetime.strptime(dt[:16], '%Y-%m-%dT%H:%M')
        return dt

    def push_time(self, tm):
        dt = self.dt_from_str(tm)
        if self.start:
            if self.end:
                raise Exception("push time beyond end (" + tm + ")")
            self.end = dt
        else:
            self.start = dt

    def __str__(self):
        return ','.join([str(self.start), str(self.end), '|'.join(self.customer), '|'.join(self.resource)])
