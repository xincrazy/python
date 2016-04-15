__author__ = 'root'

from pytz import utc
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(1)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = BlockingScheduler(executors=executors, job_defaults=job_defaults, timezone=utc)


def metricRateArithmetic(count, topic, timer, weight=0.5):
    print count, topic, timer, weight


scheduler.add_job(metricRateArithmetic, 'interval', args=(10, 22, 33), seconds=1)

scheduler.start()
