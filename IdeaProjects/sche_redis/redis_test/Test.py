__author__ = 'lifei'

import threading
import time



from pytz import utc
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor



def collect(str):
    time.sleep(3)
    print(str)

def thin():
    time.sleep(3)
    print("caiji2")

def zhaoxin():
    time.sleep(3)
    print('zhaoxin')


def lifei():
    time.sleep(3)
    print('lifei')

if __name__ == "__main__":

    executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(1)
    }
    job_defaults = {
    'coalesce': False,
    'max_instances': 3
    }
    #scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults, timezone=utc)
    scheduler = BlockingScheduler(executors=executors,job_defaults=job_defaults, timezone=utc)

    scheduler.add_job(collect,'interval',args=('woca',),seconds=5)
    scheduler.add_job(thin,'interval',seconds=5)
    scheduler.add_job(zhaoxin,'interval',seconds=5)
    scheduler.add_job(lifei,'interval',seconds=5)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):

        scheduler.shutdown()

