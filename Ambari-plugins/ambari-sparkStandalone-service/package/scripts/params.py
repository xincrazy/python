#!/usr/bin/env python

from resource_management.libraries.script.script import Script
import os


    

config = Script.get_config()


sparkStandalone_dirname = 'spark-1.6.0'


sparkStandalone_install_dir = config['configurations']['spark-bootstrap-env']['sparkStandalone.install_dir']

sparkStandalone_dir = os.path.join(*[sparkStandalone_install_dir,sparkStandalone_dirname])
conf_dir=''
bin_dir=''

sparkStandalone_user = config['configurations']['spark-bootstrap-env']['sparkStandalone_user']
sparkStandalone_group = config['configurations']['spark-bootstrap-env']['sparkStandalone_group']
sparkStandalone_log_dir = config['configurations']['spark-bootstrap-env']['sparkStandalone_log_dir']
sparkStandalone_log_file = os.path.join(sparkStandalone_log_dir,'sparkStandalone-setup.log')



temp_file = '/tmp/' + sparkStandalone_dirname + '.zip'

sparkStandalone_download_url = config['configurations']['spark-bootstrap-env']['sparkStandalone_download_url']
