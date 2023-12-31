from django.db import models

# Create your models here.
#消息表
class Message(models.Model):
    uid = models.CharField(max_length=20, verbose_name="用户名")
    msg = models.CharField(max_length=1024, verbose_name="消息")
    time = models.DateTimeField(auto_now_add=True,verbose_name="时间")
    gid = models.CharField(max_length=20, verbose_name="房间号")
    session_key = models.CharField(max_length=80, verbose_name="sessionid")

#用户表
class User(models.Model):
    uid = models.CharField(max_length=20, verbose_name="用户名")
    pwd = models.CharField(max_length=255, verbose_name="密码")
    this_time = models.DateTimeField(verbose_name="本次登录时间")
    last_time = models.DateTimeField(verbose_name="上次登录时间")

#websocket连接表
class Websocket(models.Model):
    key = models.CharField(max_length=80, verbose_name="websocket连接")
    uid = models.CharField(max_length=20, verbose_name="用户名")
    gid = models.CharField(max_length=20, verbose_name="房间号")