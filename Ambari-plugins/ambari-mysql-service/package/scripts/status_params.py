#!/usr/bin/env python
from resource_management import *
import sys, os

config = Script.get_config()

mysql_pid_dir = config['configurations']['mysql-bootstrap-env']['mysql_pid_dir']

mysql_pid_file = mysql_pid_dir + "/mysql.pid"