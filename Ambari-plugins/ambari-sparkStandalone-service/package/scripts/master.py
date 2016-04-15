#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, pwd, grp, signal, time, glob
from resource_management import *

reload(sys)
sys.setdefaultencoding('utf8')


class Master(Script):
    # 安装软件包
    def install(self, env):

        import params
        import status_params

        snapshot_package = params.sparkStandalone_download_url

        self.create_linux_user(params.sparkStandalone_user, params.sparkStandalone_group)
        if params.sparkStandalone_user != 'root':
            Execute('cp /etc/sudoers /etc/sudoers.bak')
            Execute('echo "' + params.sparkStandalone_user + '    ALL=(ALL)       NOPASSWD: ALL" >> /etc/sudoers')
            Execute('echo Creating ' + params.sparkStandalone_log_dir + ' ' + status_params.sparkStandalone_pid_dir)

        Directory([status_params.sparkStandalone_pid_dir, params.sparkStandalone_log_dir],
                  owner=params.sparkStandalone_user,
                  group=params.sparkStandalone_group,
                  recursive=True
                  )

        Execute('touch ' + params.es_log_file, user=params.es_user)
        Execute('rm -rf ' + params.es_dir, ignore_failures=True)
        Execute('mkdir -p ' + params.es_dir)
        Execute('chown -R ' + params.es_user + ':' + params.es_group + ' ' + params.es_dir)

        Execute('echo Installing packages')

        if not os.path.exists(params.temp_file):
            Execute('wget ' + snapshot_package + ' -O ' + params.temp_file + ' -a ' + params.es_log_file,
                    user=params.es_user)

        Execute('unzip ' + params.temp_file + ' -d ' + params.es_install_dir + ' >> ' + params.es_log_file,
                user=params.es_user)

        self.configure(env)

    # 创建用户
    def create_linux_user(self, user, group):
        try:
            pwd.getpwnam(user)
        except KeyError:
            Execute('adduser ' + user)
        try:
            grp.getgrnam(group)
        except KeyError:
            Execute('groupadd ' + group)

    # 设置软件所需配置文件名称内容等

    def configure(self, env):
        import params
        import status_params
        env.set_params(params)
        env.set_params(status_params)

        self.set_conf_bin(env)

        es_properties = InlineTemplate(params.es_properties_content)

        File(format("{params.conf_dir}/elasticsearch.yml"), content=es_properties, owner=params.es_user,
             group=params.es_group)

        es_logging = InlineTemplate(params.es_logging_content)

        File(format("{params.conf_dir}/logging.yml"), content=es_logging, owner=params.es_user,
             group=params.es_group)

    # 停止服务
    def stop(self, env):
        import params
        import status_params
        self.set_conf_bin(env)
        Execute('cat ' + status_params.es_pid_file + '|xargs kill >> ' + params.es_log_file, user=params.es_user)

    # 启动服务
    def start(self, env):
        import params
        import status_params
        self.configure(env)
        self.set_conf_bin(env)
        Execute('echo pid file ' + status_params.es_pid_file)
        Execute(params.bin_dir + '/elasticsearch -d -p ' + status_params.es_pid_file + '>> ' + params.es_log_file,
                user=params.es_user)

        Execute('chown ' + params.es_user + ':' + params.es_group + ' ' + status_params.es_pid_file)

    # 检查状态查看进程是否存活
    def status(self, env):

        import status_params

        check_process_status(status_params.es_pid_file)

    # 设置conf和bin目录
    def set_conf_bin(self, env):

        import params
        params.conf_dir = os.path.join(*[params.es_install_dir, params.es_dirname, 'config'])
        params.bin_dir = os.path.join(*[params.es_install_dir, params.es_dirname, 'bin'])


if __name__ == "__main__":
    Master().execute()
