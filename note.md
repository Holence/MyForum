本地的static文件无法直接在 DEBUG=False 的时候使用，可以用WhiteNoise

数据库删除后，重新建立数据库可能会缺失自己定义的Model，用`py manage.py migrate --run-syncdb`