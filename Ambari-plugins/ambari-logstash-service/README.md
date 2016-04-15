#### Ambari logstash 插件

目录结构:
- configuration 提供logstash配置文件，以及一些安装信息的配置文件。
- package/scripts 主要功能脚本，实现界面化安装脚本。
安装logstash信息以及应用: 
- logstash的版本是2.2.2，logstash详细用法[here](https://www.elastic.co/guide/en/logstash/2.2/index.html)
插件启动方法:
- 首先已经安装ambari-server，ambari用法[here](https://cwiki.apache.org/confluence/display/AMBARI/Build+and+install+Ambari+2.2.1+from+Source)
- 把插件目录放到/var/lib/ambari-server/resources/stacks/HDP/{HDP-version}/services下（插件目录名称需要全部大写）
- 最后执行ambari-server setup,在执行ambari-server start 登陆当前ip和8080端口即可访问图形化界面，然后通过图形化界面配置安装信息.
问题反馈:
- 如有问题请联系zhaoxinyanfa@oneapm.com
