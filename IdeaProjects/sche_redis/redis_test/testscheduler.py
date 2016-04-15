__author__ = 'root'
import unittest
import scheduler
import mock


class MyTestCase(unittest.TestCase):

    @mock.patch('scheduler.getRedisData')
    def testmetric(self,mock_redis):
        metric="abc"
        topic="flink"
        mock_redis.return_value="100"
        value=scheduler.metric(metric,topic)
        #print mock_redis
        self.assertEqual("100", value)
    @mock.patch('scheduler.getRedisData')
    def testmetricRate(self,mock_redis):
        scheduler.metric_dict={}
        metric="abc"
        topic="flink"
        timer=2
        mock_redis.side_effect=['100','200']
        rate1=scheduler.metricRate(metric,topic,timer)
        rate2=scheduler.metricRate(metric,topic,timer)
        #print mock_redis
        self.assertEqual(0, rate1)
        self.assertEqual(50, rate2)

if __name__=="__main__":

    unittest.main()
