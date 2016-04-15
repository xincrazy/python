__author__ = 'root'
import unittest
import Control
import mock
from Control import changeData


class MyTestCase(unittest.TestCase):

    @mock.patch('Control.changeData.getRedisData')
    def testmetric(self,mock_redis):
        metric="abc"
        topic="flink"
        mock_redis.return_value="100"
        data=changeData()
        value=changeData.metric(data,metric,topic)
        #print mock_redis
        self.assertEqual("100", value)

    @mock.patch('Control.changeData.getRedisData')
    def testmetricRate(self,mock_redis):

        Control.metric_dict={}
        metric="abc"
        topic="flink"
        timer=2
        mock_redis.side_effect=['','100','200']
        data=changeData()
        rate0=changeData.metricRate(data,metric,topic,timer)
        rate1=changeData.metricRate(data,metric,topic,timer)
        rate2=changeData.metricRate(data,metric,topic,timer)

        #print mock_redis
        self.assertEqual(0, rate0)
        self.assertEqual(0, rate1)
        self.assertEqual(50, rate2)

if __name__=="__main__":

    unittest.main()
