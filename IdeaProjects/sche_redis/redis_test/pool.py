__author__ = 'zhaoxin'

import threading
import threadpool
import telnetlib
import time
import redis

def timer_start(topic):
    t = threading.Timer(5,counter_traffic_processed_func,(topic,))
    t.start()

def counter_traffic_processed_func(topic):
    global count_process
    global old_process
    process=r.get('alertevent.traffic.processed.'+topic)
    timestamp_process=time.time()
    print("alertevent.traffic.processed "+str(timestamp_process)+" "+process+" topic:"+topic)
    #statsd.gauge("alertevent.traffic.processed",process,tags=[topic+":http"])
    if count_process > 0:
        old_process=process
        timestamp_process_rate=time.time()
        process_rate=(int(process)-int(old_process))/5
        print("alertevent.traffic.rate.processed "+str(timestamp_process_rate)+" "+str(process_rate)+" topic:"+topic)
        #statsd.gauge("alertevent.traffic.rate.processed",process_rate,tags=[topic+":http"])
    print(count_process)
    timer_start()
    count_process=count_process+1





def metricRate(count,topic):
    global flag
    global old_metric
    metric=r.get(count+":"+topic)
    print(count+";"+topic+";"+metric+"\n")
    print flag
    if flag > 0:
        old_metric=metric
        rate=(int(metric)-int(old_metric))/5
        print(count+"rate;"+topic+";"+str(rate)+"\n")
    flag=flag+1
    t = threading.Timer(5,metricRate,('counter:traffic.total','flink-in'))
    t.start()


flag=0
old_metric=0

r=redis.Redis(host='10.128.7.125',port=6379,password='zhaoxin')

t = threading.Timer(5,metricRate,('counter:traffic.total','flink-in'))
t.start()