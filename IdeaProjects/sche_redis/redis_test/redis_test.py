__author__ = 'zhaoxin'

import threading
import time
import redis
from oneapm_ci_sdk import statsd

count_total=0
old_total=0


def counter_traffic_total_func(topic):
    global count_total
    global old_total
    global thread_model
    global r
    print topic
    total=r.get('alertevent.traffic.total.'+topic)
    timestamp_total=time.time()
    print("alertevent.traffic.total "+str(timestamp_total)+" "+total+" topic:"+topic)
    statsd.gauge("alertevent.traffic.total",total,tags=[topic+":http"])
    if count_total > 0:
        old_total=total
        timestamp_total_rate=time.time()
        total_rate=(int(total)-int(old_total))/3
        print("alertevent.traffic_rate.total "+str(timestamp_total_rate)+" "+str(total_rate)+" topic:"+topic)
        statsd.gauge("alertevent.traffic_rate.total",total_rate,tags=[topic+":http"])
    print(count_total)
    thread_model = threading.Timer(3,counter_traffic_total_func,("flink",))
    thread_model.start()
    count_total=count_total+1



if __name__ == "__main__":
    r=redis.Redis(host='10.128.7.125',port=6379,db=0)
    thread_model = threading.Timer(3,counter_traffic_total_func,("flink",))
    thread_model.start()