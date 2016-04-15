__author__ = 'root'
import unittest
import monitor
import mock
from monitor import Data


class TestMonitor(unittest.TestCase):

    @mock.patch('monitor.Data.getRedisData')
    def testmetric(self,mock_redis):
        metric="abc"
        topic="flink"
        mock_redis.return_value="100"
        data=Data()
        value=Data.metric(data,metric,topic)
        #print mock_redis
        self.assertEqual("100", value)

    @mock.patch('monitor.Data.getRedisData')
    def testmetricRate(self,mock_redis):

        monitor.metric_dict={}
        metric="abc"
        topic="flink"
        timer=2
        mock_redis.side_effect=['','100','200']
        data=Data()
        rate0=Data.metricRate(data,metric,topic,timer)
        rate1=Data.metricRate(data,metric,topic,timer)
        rate2=Data.metricRate(data,metric,topic,timer)

        #print mock_redis
        self.assertEqual(0, rate0)
        self.assertEqual(0, rate1)
        self.assertEqual(50, rate2)

if __name__=="__main__":

    unittest.main()
