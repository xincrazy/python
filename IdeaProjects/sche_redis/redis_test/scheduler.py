__author__ = 'root'

import ConfigParser
from pytz import utc
from oneapm_ci_sdk import statsd
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import redis
import logging



def metric(count,topic):
    metric=getRedisData(count,topic)
    print(count+";"+topic+";"+metric+"\n")
    logging.debug("metric:"+count.replace(':','.')+",topic:"+topic+",value:"+metric)
    statsd.gauge(count.replace(':','.'),metric,tags=[topic+":http"])
    return metric

def metricRate(count,topic,timer):

    metric=getRedisData(count,topic)
    print(count+";"+topic+";"+metric+"\n")
    logging.debug("metric:"+count.replace(':','.')+",topic:"+topic+",value:"+metric)
    statsd.gauge(count.replace(':','.'),metric,tags=[topic+":http"])
    if metric!=None:
        old_metric=metric_dict.get(count+":"+topic,metric)
        rate=(int(metric)-int(old_metric))/timer
        print(count+" rate;"+topic+";"+str(rate)+"\n")
        logging.debug("metric:"+count.replace(':','.')+".rate,topic:"+topic+",value:"+str(rate))
        statsd.gauge(count.replace(':','.')+".rate",rate,tags=[topic+":http"])
        metric_dict[count+":"+topic]=metric
    return rate

def getRedisData(count,topic):
    r=redis.StrictRedis(host=host,port=port,db=0,password=user)
    data=r.get(count+":"+topic)
    return data



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='myapp.log',
                        filemode='w')
    metric_dict={}
    cf = ConfigParser.ConfigParser()
    cf.read('resource.ini')
    host=cf.get('db','db_host')
    port=cf.getint('db','db_port')
    user=cf.get('db','db_user')
    thread=cf.getint('concurrent','thread')
    timer=cf.getint('concurrent','timer')
    topics=cf.get('topics','topics')
    counts_rate=cf.get('countNameNeedRate','name')
    counts=cf.get('countName','name')
    topic_list=topics.split(',')
    count_rate_list=counts_rate.split(',')
    count_list=counts.split(',')

    executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(thread)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }

    scheduler = BlockingScheduler(executors=executors,job_defaults=job_defaults, timezone=utc)

    for k in [(i,j) for i in count_rate_list for j in topic_list]:
        print k
        scheduler.add_job(metricRate,'interval',args=(k[0],k[1],timer),seconds=timer)

    for l in [(i,j) for i in count_list for j in topic_list]:
        print l
        scheduler.add_job(metric,'interval',args=(l[0],l[1]),seconds=timer)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):

        scheduler.shutdown()