#!/usr/bin/env python
from resource_management import *
from resource_management.libraries.script.script import Script
import sys, os, glob

config = Script.get_config()

logstash_user = config['configurations']['logstash-bootstrap-env']['logstash_user']
logstash_group = config['configurations']['logstash-bootstrap-env']['logstash_group']

logstash_log_dir = config['configurations']['logstash-bootstrap-env']['logstash_log_dir']

logstash_log_file = os.path.join(logstash_log_dir, 'logstash-setup.log')

logstash_dirname = 'logstash-2.2.2'

logstash_install_dir = config['configurations']['logstash-bootstrap-env']['logstash.install_dir']

logstash_dir = os.path.join(*[logstash_install_dir, logstash_dirname])

conf_dir = ''
bin_dir = ''

temp_file = '/tmp/' + logstash_dirname + '.zip'

logstash_conf_content = config['configurations']['logstash-conf-env']['content']

logstash_pipeline_workers = config["configurations"]['logstash-start-config']['pipeline-workers']
logstash_pipeline_batch_size = config["configurations"]['logstash-start-config']['pipeline-batch-size']
logstash_pipeline_batch_delay = config["configurations"]['logstash-start-config']['pipeline-batch-delay']
logstash_start_log_file = config["configurations"]['logstash-start-config']['start-log-file']


logstash_download_url = config['configurations']['logstash-bootstrap-env']['logstash_download_url']