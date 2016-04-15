#!/usr/bin/env python
from resource_management import *
import sys, os

config = Script.get_config()

sparkStandalone_pid_dir = config['configurations']['spark-bootstrap-env']['sparkStandalone_pid_dir']
sparkStandalone_pid_file = sparkStandalone_pid_dir + '/sparkStandalone.pid'

