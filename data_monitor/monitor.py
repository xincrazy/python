from __future__ import division

import ConfigParser
from pytz import utc
from oneapm_ci_sdk import statsd
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import redis
import logging
from logging.handlers import TimedRotatingFileHandler


class Data():
    def getRedisData(self, count, topic):
        r = redis.StrictRedis(host=host, port=port, db=0, password=user)
        data = r.get(count + ":" + topic)
        return data

    def metric(self, count, topic):
        metric = self.getRedisData(count, topic)
        if metric is None:
            metric = "0"
            logger.info("maybe the topic" + topic + " not exist could not get the " + count)
        print(count + ";" + topic + ";" + metric + "\n")
        logger.info("metric:" + count.replace(':', '.') + ",topic:" + topic + ",value:" + metric)
        statsd.gauge(count.replace(':', '.'), metric, tags=[topic + ":http"])
        return metric

    def metricRateArithmetic(self, count, topic, timer):
        global weight
        metric = self.getRedisData(count, topic)
        if metric is None:
            metric = "0"
            logger.info("maybe the topic" + topic + "not exist could not get the " + count)
        print(count + ";" + topic + ";" + metric + "\n")
        logger.info("metric:" + count.replace(':', '.') + ",topic:" + topic + ",value:" + metric)
        statsd.gauge(count.replace(':', '.'), metric, tags=[topic + ":http"])
        if metric != '':
            old_metric = metric_dict.get(count + ":" + topic, metric)
            rate = round((int(metric) - int(old_metric)) / timer, 2)
            print(count + " rate;" + topic + ";" + str(rate) + "\n")
            send_rate = rate_dict.get(count + ":" + topic, 0)
            rate_stable = weight * rate + (1 - weight) * send_rate
            logger.info("metric:" + count.replace(':', '.') + ".rate_send,topic:" + topic + ",value:" + str(send_rate))
            logger.info("metric:" + count.replace(':', '.') + ".rate,topic:" + topic + ",value:" + str(rate))
            logger.info("metric:" + count.replace(':', '.') + ".rate_stable,topic:" + topic + ",value:" + str(rate_stable))
            statsd.gauge(count.replace(':', '.') + ".rate", rate_stable, tags=[topic + ":http"])
            metric_dict[count + ":" + topic] = metric
            rate_dict[count + ":" + topic] = rate_stable
            return rate
        else:
            rate = 0
            return rate

    def metricRate(self, count, topic, timer):
        metric = self.getRedisData(count, topic)
        if metric is None:
            metric = "0"
            logger.info("maybe the topic" + topic + "not exist could not get the " + count)
        print(count + ";" + topic + ";" + metric + "\n")
        logger.info("metric:" + count.replace(':', '.') + ",topic:" + topic + ",value:" + metric)
        statsd.gauge(count.replace(':', '.'), metric, tags=[topic + ":http"])
        if metric != '':
            old_metric = metric_dict.get(count + ":" + topic, metric)
            rate = round((int(metric) - int(old_metric)) / timer, 2)
            print(count + " rate;" + topic + ";" + str(rate) + "\n")
            logger.info("metric:" + count.replace(':', '.') + ".rate,topic:" + topic + ",value:" + str(rate))
            statsd.gauge(count.replace(':', '.') + ".rate", rate, tags=[topic + ":http"])
            metric_dict[count + ":" + topic] = metric
            return rate
        else:
            rate = 0
            return rate


if __name__ == "__main__":

    logFilePath = "logs/monitor.log"
    logger = logging.getLogger("Monitor")

    logger.setLevel(logging.INFO)

    handler = TimedRotatingFileHandler(logFilePath,
                                       when="D",
                                       interval=1,
                                       backupCount=7)
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    cf = ConfigParser.ConfigParser()
    cf.read('resource.ini')
    host = cf.get('db', 'db_host')
    port = cf.getint('db', 'db_port')
    user = cf.get('db', 'db_user')
    thread = cf.getint('concurrent', 'thread')
    timer = cf.getint('concurrent', 'timer')
    topics = cf.get('topics', 'topics')
    counts_rate = cf.get('countNameNeedRate', 'name')
    counts = cf.get('countName', 'name')
    counts_rate_Arithmetic = cf.get('countNameNeedRateArithmetic', 'name')
    weight = cf.get('arithmetic', 'weight')
    topic_list = topics.split(',')
    count_rate_Arithmetic_list = counts_rate_Arithmetic.split(',')
    count_rate_list = counts_rate.split(',')
    count_list = counts.split(',')
    metric_dict = {}
    rate_dict = {}
    executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(thread)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }

    scheduler = BlockingScheduler(executors=executors, job_defaults=job_defaults, timezone=utc)

    data = Data()

    if count_rate_Arithmetic_list[0] != "":
        for k in [(i, j) for i in count_rate_Arithmetic_list for j in topic_list]:
            print k
            scheduler.add_job(data.metricRateArithmetic, 'interval', args=(k[0], k[1], timer), seconds=timer)

    if count_rate_list[0] != "":
        for m in [(i, j) for i in count_rate_list for j in topic_list]:
            print m
            scheduler.add_job(data.metricRate, 'interval', args=(m[0], m[1], timer), seconds=timer)

    if count_list[0] != "":
        for l in [(i, j) for i in count_list for j in topic_list]:
            print l
            scheduler.add_job(data.metric, 'interval', args=(l[0], l[1]), seconds=timer)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
