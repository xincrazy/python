#!/usr/bin/env python
# -*- coding: utf-8 -*-
from resource_management import *
from resource_management.libraries.script.script import Script
import sys, os, glob
import getVersion




config = Script.get_config()

mysql_user = config['configurations']['mysql-bootstrap-env']['mysql_user']
mysql_group = config['configurations']['mysql-bootstrap-env']['mysql_group']

mysql_log_dir = config['configurations']['mysql-bootstrap-env']['mysql_log_dir']

mysql_log_file = os.path.join(mysql_log_dir, 'mysql-setup.log')

mysql_dirname ='mysql-5.6.29'

mysql_install_dir = config['configurations']['mysql-bootstrap-env']['mysql.install_dir']

mysql_dir = os.path.join(*[mysql_install_dir, mysql_dirname])

conf_dir = ''
bin_dir = ''

temp_file = '/tmp/' + mysql_dirname + '.zip'

mysql_conf_content = config['configurations']['mysql-bootstrap-env']['content']


mysql_download_url = config['configurations']['mysql-bootstrap-env']['mysql_download_url']

mysql_data_dir = config['configurations']['mysql-bootstrap-env']['mysql_data_dir']