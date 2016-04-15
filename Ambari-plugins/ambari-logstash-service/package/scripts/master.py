#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, pwd, grp, signal, time, glob
from resource_management import *


reload(sys)
sys.setdefaultencoding('utf8')


class Master(Script):
    #安装软件包
    def install(self, env):
        import params
        import status_params
        snapshot_package = params.logstash_download_url
        
        self.create_linux_user(params.logstash_user, params.logstash_group)
        if params.logstash_user != 'root':
            Execute('cp /etc/sudoers /etc/sudoers.bak')
            Execute('echo "' + params.logstash_user + '    ALL=(ALL)       NOPASSWD: ALL" >> /etc/sudoers')
            Execute('echo Creating ' + params.logstash_log_dir + ' ' + status_params.logstash_pid_dir)

        Directory([status_params.logstash_pid_dir, params.logstash_log_dir],
                  owner=params.logstash_user,
                  group=params.logstash_group,
                  recursive=True
                  )

        Execute('touch ' + params.logstash_log_file, user=params.logstash_user)
        Execute('rm -rf ' + params.logstash_dir, ignore_failures=True)
        Execute('mkdir -p ' + params.logstash_dir)
        Execute('chown -R ' + params.logstash_user + ':' + params.logstash_group + ' ' + params.logstash_dir)

        Execute('echo Installing packages')

        if not os.path.exists(params.temp_file):
            Execute('wget ' + snapshot_package + ' -O ' + params.temp_file + ' -a ' + params.logstash_log_file,
                    user=params.logstash_user)

        Execute('unzip ' + params.temp_file + ' -d ' + params.logstash_install_dir + ' >> ' + params.logstash_log_file,
                user=params.logstash_user)

        self.configure(env)
    #创建用户
    def create_linux_user(self, user, group):
        try:
            pwd.getpwnam(user)
        except KeyError:
            Execute('adduser ' + user)
        try:
            grp.getgrnam(group)
        except KeyError:
            Execute('groupadd ' + group)
    #设置conf和bin目录
    def set_conf_bin(self, env):

        import params
        params.conf_dir = os.path.join(*[params.logstash_install_dir, params.logstash_dirname, 'config'])
        params.bin_dir = os.path.join(*[params.logstash_install_dir, params.logstash_dirname, 'bin'])
    #设置软件所需配置文件名称内容等
    def configure(self, env):
        import params
        import status_params
        env.set_params(params)
        env.set_params(status_params)

        self.set_conf_bin(env)

        logstash_conf = InlineTemplate(params.logstash_conf_content)

        File(format("{params.conf_dir}/logstash.conf"), content=logstash_conf, owner=params.logstash_user,
             group=params.logstash_group)
    #停止服务
    def stop(self, env):
        import params
        import status_params
        self.set_conf_bin(env)
        Execute('cat ' + status_params.logstash_pid_file + '|xargs kill >> ' + params.logstash_log_file,
                user=params.logstash_user)
        Execute('rm ' + status_params.logstash_pid_file)
    #启动服务
    def start(self, env):
        import params
        import status_params
        self.configure(env)
        self.set_conf_bin(env)
        Execute('echo pid file ' + status_params.logstash_pid_file)


        Execute(
            'nohup ' + params.bin_dir + '/logstash -b ' + str(params.logstash_pipeline_batch_size) + ' -w ' + str(
                params.logstash_pipeline_workers) + ' -u ' + str(
                params.logstash_pipeline_batch_delay) + ' -l ' + params.logstash_start_log_file + ' -f ' + params.conf_dir + '/logstash.conf >> ' + params.logstash_log_file + ' 2>&1&',
            user=params.logstash_user)

        Execute("jps -l|grep org.jruby.Main|awk '{print $1}' > " + status_params.logstash_pid_file, user=params.logstash_user)

        Execute('chown ' + params.logstash_user + ':' + params.logstash_group + ' ' + status_params.logstash_pid_file)
    #检查状态查看进程是否存活
    def status(self, env):

        import status_params

        check_process_status(status_params.logstash_pid_file)


if __name__ == "__main__":
    Master().execute()
