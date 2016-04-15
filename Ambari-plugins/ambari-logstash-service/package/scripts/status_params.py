#!/usr/bin/env python
from resource_management import *
import sys, os

config = Script.get_config()

logstash_pid_dir = config['configurations']['logstash-bootstrap-env']['logstash_pid_dir']

logstash_pid_file = logstash_pid_dir + '/logstash.pid'