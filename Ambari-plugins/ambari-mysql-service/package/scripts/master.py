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
        snapshot_package = params.mysql_download_url

        self.create_linux_user(params.mysql_user, params.mysql_group)
        if params.mysql_user != 'root':
            Execute('cp /etc/sudoers /etc/sudoers.bak')
            Execute('echo "' + params.mysql_user + '    ALL=(ALL)       NOPASSWD: ALL" >> /etc/sudoers')
            Execute('echo Creating ' + params.mysql_log_dir + ' ' + status_params.mysql_pid_dir)

        Directory([status_params.mysql_pid_dir, params.mysql_log_dir, params.mysql_data_dir],
                  owner=params.mysql_user,
                  group=params.mysql_group,
                  recursive=True
                  )

        Execute('touch ' + params.mysql_log_file, user=params.mysql_user)
        Execute('rm -rf ' + params.mysql_dir, ignore_failures=True)
        Execute('mkdir -p ' + params.mysql_dir)
        Execute('chown -R ' + params.mysql_user + ':' + params.mysql_group + ' ' + params.mysql_dir)

        Execute('echo Installing packages')

        if not os.path.exists(params.temp_file):
            Execute('wget ' + snapshot_package + ' -O ' + params.temp_file + ' -a ' + params.mysql_log_file,
                    user=params.mysql_user)

        # Execute('unzip ' + params.temp_file + ' -d ' + params.mysql_install_dir + ' >> ' + params.mysql_log_file,
        #        user=params.mysql_user)

        Execute(
            'tar xvf ' + params.temp_file + ' -C ' + params.mysql_install_dir + '/' + params.mysql_dirname + ' --strip-components=1 >> ' + params.mysql_log_file,
            user=params.mysql_user)

        self.set_conf_bin(env)

        Execute(params.conf_dir + "/scripts/mysql_install_db --user=" + params.mysql_user + " --basedir=" + params.mysql_dir + " --datadir=" + params.mysql_data_dir)

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

    # 设置conf和bin目录
    def set_conf_bin(self, env):

        import params
        params.conf_dir = os.path.join(*[params.mysql_install_dir, params.mysql_dirname])
        params.bin_dir = os.path.join(*[params.mysql_install_dir, params.mysql_dirname, 'bin'])

    # 设置软件所需配置文件名称内容等
    def configure(self, env):
        import params
        import status_params
        env.set_params(params)
        env.set_params(status_params)

        self.set_conf_bin(env)

        mysql_conf = InlineTemplate(params.mysql_conf_content)

        File(format("{params.conf_dir}/my.cnf"), content=mysql_conf, owner=params.mysql_user,
             group=params.mysql_group)

    # 停止服务
    def stop(self, env):
        import params
        import status_params
        self.set_conf_bin(env)
        Execute('cat ' + status_params.mysql_pid_file + '|xargs kill >> ' + params.mysql_log_file,
                user=params.mysql_user)
        Execute('rm ' + status_params.mysql_pid_file)

    # 启动服务
    def start(self, env):
        import params
        import status_params
        self.configure(env)
        self.set_conf_bin(env)
        Execute('echo pid file ' + status_params.mysql_pid_file)

        #Must cd the mysql install dir

        Execute(
            "cd "+params.mysql_dir+"&& nohup " + params.bin_dir+"/mysqld_safe --defaults-file=" + params.conf_dir + "/my.cnf >>" + params.mysql_log_file + " 2>&1&",
            user=params.mysql_user)

        #Execute('chown ' + params.mysql_user + ':' + params.mysql_group + ' ' + status_params.mysql_pid_file)

    # 检查状态查看进程是否存活
    def status(self, env):

        import status_params

        check_process_status(status_params.mysql_pid_file)


if __name__ == "__main__":
    Master().execute()
