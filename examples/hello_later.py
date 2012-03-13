# -*- coding: utf-8 -*-

import functools
import later


def hello_world():
    print "Hello spam"

def greetings(name):
    print "Greetings %s" % name

def main():
    scheduler = later.Scheduler()
    scheduler.add_delayed_job(hello_world, seconds=1)

    hi_jack = functools.partial(greetings, "Jack")
    scheduler.add_delayed_job(hi_jack, seconds=2)

if __name__ == '__main__':
    main()
