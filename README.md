starfish
========

依赖的资源

server:
1.uwsgi http://projects.unbit.it/uwsgi/wiki/Install
2.web.py
3.redis & redis-py
web:
1.jquery
2.jquery-ui, jquery.sha1

部署方式:
安装webserver,设置端口转发
如果是apache,那么把如下内容copy到httpd.conf底部

ProxyPass /starfish http://127.0.0.1:9090
ProxyPassReverse /starfish http://127.0.0.1:9090

http//127.0.0.1:9090是starfishd接收请求的url,
若要修改请修改daemon.sh内相关参数,
如果部署在不同的机器请注意修改ip

/starfish是webserver对外公开的starfishd请求的url,
这个url同时接收手机以及web请求,
参考index.html中的$.starfishd_url设置.

www中的内容是本系统的web页面, 请按照webserver的正常部署方式部署.
