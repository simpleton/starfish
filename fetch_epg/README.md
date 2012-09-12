EPG fetch
==========

this preject is fetching EPG in cntv webpage and save in redis for our weever project

## environment##
1. python

we use 2.7.3 version

2. webpy

3. redis

4. uwsgi

   http://projects.unbit.it/uwsgi/wiki/Install
   
it better not use apt-get, it will install the quite old version
just download the sourcecode and install

## GET interface##

`domain/epg/list?date=yyyy-mm-dd&channel=cctv1`

return json format date

	{
		date:xxx,
		channel:xxx,
		total_size:xxx,
		list:[{name:xxx, time:xx:xx, cover:xxx},
			  {....................},
			  .....]
	}

`domain/epg/showing`

	{
		total_size:xxx,
		current_time:xxx,
		list:[{name:xxx, time:mm:ss, channel:xxx, cover_url:xxx},
		       ........]
	}

`domain/epg/show?clocktime=mm:ss&daytime=yyyy-mm-dd`

	{
		total_size:xxx,
		query_time:xxx,
		list:[{name:xxx ,time:mm:ss, channel:xxx, cover_url:xxx},
		      ...........]
	}
	
#### 部署方式 ####

1. 安装webserver,设置端口转发

如果是apache,那么把如下内容copy到apache2.conf底部

**并enable proxy.conf proxy_http.load**
enable只需建立ln即可，从mods-avaliable 到mod-enables

	ProxyPass /epg http://127.0.0.1:9100 
	
	ProxyPassReverse /epg http://127.0.0.1:9100
	
http//127.0.0.1:9090是starfishd接收请求的url,

若要修改请修改daemon.sh内相关参数,
**如果部署在不同的机器请注意修改ip**

