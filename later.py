# -*- coding: utf-8 -*-

import threading


# TODO: write in-code documentation


class StopJobException(ValueError):
    pass


class Job(object):

    def __init__(self, fn, delay=0, name=None):
        self.delay = delay
        self.fn = fn
        self.name = name if name else str(id(self))

        self._is_periodic = False
        self._store = None
        self._timer = threading.Timer(self.delay, self)


    def __call__(self):
        try:
            # schedule next call
            if self._is_periodic:
                self._timer = threading.Timer(self.delay, self)
                self._timer.start()

            # execute on the current one
            self.fn()

        except StopJobException:
            if self._is_periodic:
                self._store.remove_job(self.name)

    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.cancel()


class BaseJobStore(object):

    def __init__(self):
        self.jobs = None

    def add_job(self, job):
        raise NotImplementedError

    def has_job(self, name):
        raise NotImplementedError

    def remove_job(self, name):
        raise NotImplementedError


class RAMJobStore(BaseJobStore):

    def __init__(self):
        self.jobs = {}

    def add_job(self, job):
        self.jobs[job.name] = job
        job.start()

    def has_job(self, name):
        return name in self.jobs

    def remove_job(self, name):
        job = self.jobs.pop(name)
        job.stop()


class Scheduler(object):

    def __init__(self):
        self.store = RAMJobStore()

    def _build_job(self, func, name, days, hours, minutes, seconds):
        delay_in_seconds = self._calc_seconds(days, hours, minutes, seconds)
        if delay_in_seconds <= 0:
            raise ValueError("Can't schedule job in the past")
        return Job(func, delay_in_seconds, name)

    def _calc_seconds(self, days, hours, minutes, seconds):
        return seconds + minutes * 60 + hours * 3600 + days * 86400

    def add_delayed_job(self, func, name=None, days=0, hours=0, minutes=0, seconds=0):
        job = self._build_job(func, name, days, hours, minutes, seconds)
        self.store.add_job(job)
        return job

    def add_periodic_job(self, func, name=None, days=0, hours=0, minutes=0, seconds=0):
        job = self._build_job(func, name, days, hours, minutes, seconds)
        job._is_periodic = True
        self.store.add_job(job)
        return job

    def is_job_scheduled(self, job_name):
        return self.store.has_job(job_name)

    def remove_job(self, job):
        self.remove_job_by_name(job.name)

    def remove_job_by_name(self, job_name):
        self.store.remove_job(job_name)

    def stop(self):
        for job_name in self.store.jobs.keys():
            self.store.remove_job(job_name)
