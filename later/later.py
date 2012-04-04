# -*- coding: utf-8 -*-

import threading


# TODO: write in-code documentation


class StopJobException(ValueError):
    pass


class Job(object):

    def __init__(self, fn, delay, name):
        self.fn = fn
        self.delay = delay
        self.name = name if name else str(id(self))

        self.is_periodic = False
        self.timer = threading.Timer(self.delay, self)

    def __call__(self):
        try:
            # schedule next call
            if self.is_periodic:
                self.timer = threading.Timer(self.delay, self)
                self.timer.start()

            # execute on the current one
            self.fn()

        except StopJobException:
            if self.is_periodic:
                self.stop()
                self.is_periodic = False

    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.cancel()


class JobStore(object):

    def __init__(self):
        self.jobs = {}
        self.rw_lock = threading.Lock()

    def add_job(self, job):
        with self.rw_lock:
            if self.has_job(job.name):
                self.remove_job(job.name)
            self.jobs[job.name] = job
            job.start()

    def has_job(self, name):
        return name in self.jobs

    def purge(self):
        with self.rw_lock:
            for job_name in self.jobs.keys():
                job = self.jobs.pop(job_name)
                job.stop()

    def remove_job(self, name):
        with self.rw_lock:
            if self.has_job(name):
                job = self.jobs.pop(name)
                job.stop()


class Scheduler(object):

    def __init__(self):
        self.store = JobStore()

    def _build_job(self, func, name, days, hours, minutes, seconds):
        delay_in_seconds = seconds + minutes * 60 + hours * 3600 + days * 86400
        if delay_in_seconds <= 0:
            raise ValueError("Can't schedule job in the past")
        return Job(func, delay_in_seconds, name)

    def _job_name(self, job):
        if isinstance(job, Job):
            return job.name
        elif isinstance(job, basestring):
            return job
        else:
            raise ValueError("Expected string or instance of Job, got %s instead" % type(job))

    def add_delayed_job(self, func, name=None, days=0, hours=0, minutes=0, seconds=0):
        job = self._build_job(func, name, days, hours, minutes, seconds)
        self.store.add_job(job)
        return job.name

    def add_periodic_job(self, func, name=None, days=0, hours=0, minutes=0, seconds=0):
        job = self._build_job(func, name, days, hours, minutes, seconds)
        job.is_periodic = True
        self.store.add_job(job)
        return job.name

    def is_job_scheduled(self, job_name):
        return self.store.has_job(job_name)

    def remove_job(self, job_inst_or_name):
        job_name = self._job_name(job_inst_or_name)
        self.store.remove_job(job_name)

    def stop(self):
        self.store.purge()
