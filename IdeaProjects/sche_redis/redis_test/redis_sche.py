__author__ = 'root'

import threading
import time
import redis
from oneapm_ci_sdk import statsd


#def timer_start():
#    t = threading.Timer(5,counter_traffic_total_func)
#    t.start()

def counter_traffic_total_func(topic):
    global count_total
    global old_total
    global thread_model_total
    total=r.get('alertevent.traffic.total.'+topic)
    timestamp_total=time.time()
    print("alertevent.traffic.total "+str(timestamp_total)+" "+total+" topic:"+topic)
    statsd.gauge("alertevent.traffic.total",total,tags=[topic+":http"])
    if count_total > 0:
        old_total=total
        timestamp_total_rate=time.time()
        total_rate=(int(total)-int(old_total))/5
        print("alertevent.traffic_rate.total "+str(timestamp_total_rate)+" "+str(total_rate)+" topic"+topic)
        statsd.gauge("alertevent.traffic_rate.total",total_rate,tags=[topic+":http"])
    print(count_total)
    thread_model_total = threading.Timer(5,counter_traffic_total_func,("flink",))
    thread_model_total.start()
    count=count_total+1

def counter_traffic_processed_func(topic):
    global count_process
    global old_process
    global thread_model_process
    process=r.get('alertevent.traffic.processed.'+topic)
    timestamp_process=time.time()
    print("alertevent.traffic.processed "+str(timestamp_process)+" "+process+" topic:"+topic)
    statsd.gauge("alertevent.traffic.processed",process,tags=[topic+":http"])
    if count_process > 0:
        old_process=process
        timestamp_process_rate=time.time()
        process_rate=(int(process)-int(old_process))/5
        print("alertevent.traffic.rate.processed "+str(timestamp_process_rate)+" "+str(process_rate)+" topic:"+topic)
        statsd.gauge("alertevent.traffic.rate.processed",process_rate,tags=[topic+":http"])
    print(count_process)
    thread_model_process = threading.Timer(5,counter_traffic_processed_func,("flink",))
    thread_model_process.start()
    count_process=count_process+1

def counter_traffic_jsonexception_func(topic):
    global thread_model_jsonexception
    jsonexception=r.get('alertevent.traffic.jsonexception.'+topic)
    timestamp_process=time.time()
    print("alertevent.traffic.jsonexception. "+str(timestamp_process)+" "+jsonexception+" topic:"+topic)
    statsd.gauge("alertevent.traffic.jsonexception",jsonexception,tags=[topic+":http"])
    thread_model_jsonexception = threading.Timer(5,counter_traffic_jsonexception_func,("flink",))
    thread_model_jsonexception.start()

def counter_traffic_checkfailure_func(topic):
    global thread_model_checkfailure
    checkfailure=r.get('alertevent.traffic.checkfailure.'+topic)
    timestamp_process=time.time()
    print("alertevent.traffic.checkfailure "+str(timestamp_process)+" "+checkfailure+" topic:"+topic)
    statsd.gauge("alertevent.traffic.checkfailure",checkfailure,tags=[topic+":http"])
    thread_model_checkfailure = threading.Timer(5,counter_traffic_checkfailure_func,("flink",))
    thread_model_checkfailure.start()

def counter_traffic_rulemissing_func(topic):
    global thread_model_rulemissing
    rulemissing=r.get('alertevent.traffic.rulemissing.'+topic)
    timestamp_process=time.time()
    print("alertevent.traffic.rulemissing "+str(timestamp_process)+" "+rulemissing+" topic:"+topic)
    statsd.gauge("alertevent.traffic.rulemissing",rulemissing,tags=[topic+":http"])
    thread_model_rulemissing = threading.Timer(5,counter_traffic_rulemissing_func,("flink",))
    thread_model_rulemissing.start()

if __name__ == "__main__":
    count_total=0
    old_total=0
    count_process=0
    old_process=0
    r=redis.Redis(host='10.128.7.125',port=6379,db=0)
    thread_model_total = threading.Timer(5,counter_traffic_total_func,("flink",))
    thread_model_total.start()
    thread_model_process = threading.Timer(5,counter_traffic_processed_func,("flink",))
    thread_model_process.start()
    thread_model_jsonexception = threading.Timer(5,counter_traffic_jsonexception_func,("flink",))
    thread_model_jsonexception.start()
    thread_model_checkfailure = threading.Timer(5,counter_traffic_checkfailure_func,("flink",))
    thread_model_checkfailure.start()
    thread_model_rulemissing = threading.Timer(5,counter_traffic_rulemissing_func,("flink",))
    thread_model_rulemissing.start()