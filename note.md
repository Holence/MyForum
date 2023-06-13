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

# Docker部署

部署在docker里用两个image，一个是django，一个是nginx，放在同一个compose中：用volumes共享staticfiles和media文件夹，nginx的内部端口为80，外部端口为8000，django的内部端口是8080，没有外部端口，让根网址的路由映射到django接管，根网址加上static和media的路由还是由nginx接管。

删除无用的
docker system prune

createsuperuser
docker exec -it blog python ./manage.py createsuperuser --noinput

Backup
docker run --rm --volumes-from nginx -v $(pwd):/backup ubuntu tar cvf /backup/backup.tar app/
