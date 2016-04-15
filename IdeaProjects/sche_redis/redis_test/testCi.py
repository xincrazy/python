__author__ = 'root'

from oneapm_ci_sdk import statsd
import time
import random
import redis

if __name__=="__main__":
    i=0
    while(True):
        time.sleep(5)
        r=redis.StrictRedis(host='10.128.7.125',port=6379,db=0,password='zhaoxin')
        r.set('counter:traffic.total:flink-in',i)
        r.set('counter:traffic.total:alert-flink-in2',i)
        #statsd.gauge("counter:traffic.total",i,tags=["flink-in:http"])
        i=i+20
        print i