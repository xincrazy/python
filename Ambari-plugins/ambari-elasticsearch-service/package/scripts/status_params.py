#!/usr/bin/env python
from resource_management import *
import sys, os

config = Script.get_config()

es_pid_dir = config['configurations']['es-bootstrap-env']['es_pid_dir']
es_pid_file = es_pid_dir + '/elasticsearch.pid'

