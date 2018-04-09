#!/usr/bin/env python3
import re
from datetime import datetime

class Event:
    fields = ('who', 'start', 'end', 'resource', 'comment', 'email', 'mobile', 'error')

    ''' Create event from Schedule Master string'''
    @classmethod
    def from_sm(cls, event_string):
        prefix_start = 'Strt: '
        prefix_end = 'End: '
        prefix_resource = 'Lesson: '
        prefix_comment = 'Comment:'
        prefix_mobile = 'mobile: '
        re_mobile = re.compile(r'[\d-]+')
        re_email = re.compile(r'[\w.-]+@[\w.-]+')
        event = cls()
        for name in cls.fields:
            setattr(event, name, None)
        try:
            event_string = re.sub(r'^ddrivetip\(\'', '', event_string)
            event_string = re.sub(r'\',\d+\);\s*$', '', event_string)
            event_list = event_string.split('<br>')
            event.who = event_list.pop(0)
            for el in event_list:
                if el[:len(prefix_start)] == prefix_start:
                    event.start = event.decode_date(el[len(prefix_start):])
                elif el[:len(prefix_end)] == prefix_end:
                    event.end = event.decode_date(el[len(prefix_end):])
                elif el[:len(prefix_resource)] == prefix_resource:
                    event.resource = el[len(prefix_resource):]
                elif re.match(re_email, el):
                    event.email = el.strip()
                elif el[:len(prefix_comment)] == prefix_comment:
                    event.comment = el[len(prefix_comment):]
                elif el[:len(prefix_mobile)] == prefix_mobile and re.match(re_mobile, el[len(prefix_mobile):]):
                    event.mobile = el[len(prefix_mobile):]
        except Exception as ex:
            event.error = ex
        return event

    @staticmethod
    def decode_date(date_string):
        fmt = '%a %m/%d/%y %H:%M'
        return datetime.strptime(date_string, fmt)

    def __str__(self):
        rep = []
        for field in self.fields:
            value = getattr(self, field)
            if value is not None:
                rep.append('{}: {}'.format(field, value))
        return '\n'.join(rep)
            
if __name__ == '__main__':
    events = ['''ddrivetip('Fang, Gan <br>Strt: Sun 04/08/18 09:30<br>End: Sun 04/08/18 12:00<br>Lesson: 122DZ<br>Local<br>fanggan2012@gmail.com <br>mobile: 614-886-4354<br>Comment:Club & SR20 Initial',250);'''
,
'''ddrivetip('Daniel, Thomas <br>Strt: Sun 04/08/18 13:00<br>End: Sun 04/08/18 18:00<br>cfi@thomas-daniel.com <br>hm: 65-529-3078 <br>mobile: 650-279-3429',250);''' ]

    import pdb
    # pdb.set_trace()
    for event_string in events:
        event = Event().from_sm(event_string)
        print(event, '\n')
