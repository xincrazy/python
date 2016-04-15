#!/usr/bin/env python

from resource_management.libraries.script.script import Script
import os


    

config = Script.get_config()


es_dirname = 'elasticsearch-2.1.1'
    

es_install_dir = config['configurations']['es-bootstrap-env']['es.install_dir']

es_dir = os.path.join(*[es_install_dir,es_dirname])
conf_dir=''
bin_dir=''

nifi_boostrap_content = config['configurations']['es-bootstrap-env']['content']
es_user = config['configurations']['es-bootstrap-env']['es_user']
es_group = config['configurations']['es-bootstrap-env']['es_group']
es_log_dir = config['configurations']['es-bootstrap-env']['es_log_dir']
es_log_file = os.path.join(es_log_dir,'es-setup.log')


es_properties_content = config['configurations']['elasticsearch_yml']['content']

es_logging_content = config['configurations']['logging_yml']['content']

temp_file = '/tmp/' + es_dirname + '.zip'

es_download_url = config['configurations']['es-bootstrap-env']['es_download_url']
