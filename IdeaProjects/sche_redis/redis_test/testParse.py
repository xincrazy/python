__author__ = 'root'

import ConfigParser

cf = ConfigParser.ConfigParser()

cf.read('a.ini')

s=cf.sections()

print s

o=cf.options('db')

print o

value=cf.get('db','db_host')

topics=cf.get('topics','topics')
counts=cf.get('countName','name')
topic_list=topics.split(',')
count_list=counts.split(',')
print topic_list,count_list

for k in [(i,j) for i in topic_list for j in count_list]:
    print k[0]