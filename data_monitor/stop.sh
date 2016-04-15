ps -axu |grep monitor.py|awk '{print $2}'|head -1|xargs kill -9

