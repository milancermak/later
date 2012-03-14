----
WHAT
----

Later is a in-process thread-safe scheduler for Python. It is licensed under the `Simplified BSD license <http://en.wikipedia.org/wiki/BSD_licenses#2-clause_license_.28.22Simplified_BSD_License.22_or_.22FreeBSD_License.22.29>`_.

---
WHY
---

None of the existing python schedulers suited my needs so I had to write my own.

---
HOW
---

Later is really easy to use. In your process, you create an instance of the ``Scheduler`` class. You use only this to interact with the scheduling.

::

    from later import later
    scheduler = later.Scheduler()

The most important methods of ``Scheduler`` are ``add_delayed_job`` and ``add_periodic_job``. Use the first one to trigger a function only once in the future. The later one can be used to schedule the same function in intervals. The only required parameter to these methods is the callable that will be executed in the future.

::

    import functools
    sms_sender = functools.partial(send_sms, "+112345678", "Hello Monty") # assuming send_sms is a function
    scheduler.add_delayed_job(sms_sender, minutes=2) # will send an sms to Monty in 2 minutes
    

You can also pass a ``name`` parameter. This should be a string that acts as an identifier of the scheduled job. Both methods return this string. Additional keyword arguments are ``days``, ``hours``, ``minutes`` and ``seconds``. Use these to schedule the job in an appropriate time in the future. With ``add_periodic_job``, the delay is also used as the period.

::

    cappuccino_maker = functools.partial(make_espresso, cream=True, whipped=True)
    scheduler.add_periodic_job(cappuccino_maker, name="Cappuccino FTW", hours=3) # make a cappuccino every 3 hours


If you want to end the periodic job from *inside*, raise ``later.StopJobException`` in it. This will cause the scheduler to stop any planned executions of the job. See the `examples/` directory in the repo for some more examples on how to use Later.

Because the scheduling is based on the `threading.Timer <http://docs.python.org/library/threading.html#timer-objects>`_ class, keep in mind the execution may not fire in **precisely** the same moment as you specified.

As mentioned earlier, Later is not a persistent scheduler. All jobs are stored in the operating memory. Once you end the python process, the scheduled jobs are lost.
