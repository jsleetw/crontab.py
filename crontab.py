from time import sleep
from datetime import datetime, timedelta
import gevent

# Some utility classes / functions first
class AllMatch(set):
    """Universal set - match everything"""
    def __contains__(self, item):
        return True

allMatch = AllMatch()


def conv_to_set(obj):  # Allow single integer to be provided
    if isinstance(obj, (int, long)):
        return set([obj])  # Single item
    if not isinstance(obj, set):
        obj = set(obj)
    return obj


# The actual Event class
class Event(object):
    def __init__(self, action, min=allMatch, hour=allMatch,
            day=allMatch, month=allMatch, dow=allMatch,
            args=(), kwargs={}):
        self.mins = conv_to_set(min)
        self.hours = conv_to_set(hour)
        self.days = conv_to_set(day)
        self.months = conv_to_set(month)
        self.dow = conv_to_set(dow)
        self.action = action
        self.args = args
        self.kwargs = kwargs

    def matchtime(self, t):
        """Return True if this event should trigger at the specified datetime"""
        return ((t.minute     in self.mins) and
                (t.hour       in self.hours) and
                (t.day        in self.days) and
                (t.month      in self.months) and
                (t.weekday()  in self.dow))

    def check(self, t):
        print "check!"
        if self.matchtime(t):
            print "yes!"
            self.action(*self.args, **self.kwargs)


class CronTab(object):
    def __init__(self, *events):
        self.events = events

    def run(self):
        t = datetime(*datetime.now().timetuple()[:5])
        while 1:
            for e in self.events:
                e.check(t)

            print t
            t += timedelta(minutes=1)
            print t
            print datetime.now()
            print (t - datetime.now()).seconds
            while datetime.now() < t:
                sleep((t - datetime.now()).seconds)


def test_task():
    """Just an example """
    print "Hello world!"

c = CronTab(
        Event(test_task, 10),
        )

c.run()
