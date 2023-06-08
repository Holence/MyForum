数据库删除后，重新建立数据库可能会缺失自己定义的Model，用`py manage.py migrate --run-syncdb`

# 用Nginx提供文件

https://www.cnblogs.com/taiyonghai/p/9402734.html
https://wolfx.io/how-to-serve-static-and-media-files-in-nginx

启动
start nginx

修改port和location

检查conf是否正确
nginx -t -c ./conf/nginx.conf

重启
nginx -s reload

快速停止
nginx -s stop

完整有序的关闭
nginx -s quit
