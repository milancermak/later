# -*- coding: utf-8 -*-

import datetime
import functools
import later


def timestamp_to_file(filename):
    with open(filename, "a") as f:
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        f.write(timestamp + "\n")

def main():
    try:
        scheduler = later.Scheduler()

        timestamper = functools.partial(timestamp_to_file, "timestamps.txt")
        scheduler.add_periodic_job(timestamper, "timestamper", seconds=2)
    except KeyboardInterrupt:
        scheduler.stop()

if __name__ == '__main__':
    main()
