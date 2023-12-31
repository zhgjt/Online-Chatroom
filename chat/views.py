from django.http import JsonResponse
from django.shortcuts import render, redirect
from chat.models import *
from datetime import datetime
from django.core import serializers


# Create your views here.

# 登录API
def log(request):
    if request.method == "GET":
        return render(request, 'log.html')
    else:
        print("post方法")
        print(request.POST)
        uid = request.POST.get("uid")
        pwd = request.POST.get("pwd")
        # 如果输入的账号或密码为空，跳转到登录界面，重新输入
        if uid == '' or pwd == '':
            return render(request, 'log.html')

        # 如果输入的用户名不存在，跳转到登录界面重新输入
        if not User.objects.filter(uid=uid):
            return render(request, 'log.html')

        # 如果密码不正确
        if User.objects.get(uid=uid).pwd != pwd:
            return render(request, 'log.html')

        # 登录成功
        print("登录成功")
        # 修改用户表的登陆时间
        time = datetime.now()
        obj = User.objects.get(uid=uid)
        User.objects.filter(uid=uid).update(this_time=time, last_time=obj.last_time)
        request.session["info"] = {'uid': uid}
        # 设置session的生命周期为24小时
        request.session.set_expiry(60 * 60 * 24)
        return redirect('/index/')


# 注册API
def signup(request):
    if request.method == "GET":
        return render(request, 'signup.html')
    else:
        print(request.POST)
        uid = request.POST.get("uid")
        pwd = request.POST.get("pwd")
        # 如果输入的账号或密码为空，跳转到注册界面，重新输入
        if uid == '' or pwd == '':
            return render(request, 'signup.html')

        # 如果数据库中没有等于uid的用户名，保存到数据库
        if not User.objects.filter(uid=uid).first():
            print("没有")
            time = datetime.now()
            user = User(uid=uid, pwd=pwd, this_time=time, last_time=time)
            user.save()
            return render(request, 'log.html')
        # 注册失败，跳转到注册界面，重新输入
        return render(request, 'signup.html')


def index(request):
    uid = request.session['info']["uid"]
    gid = request.GET.get("gid")
    objs = Websocket.objects.filter(uid=uid)
    list = []
    for obj in objs:
        list.append(obj.gid)
    return render(request, 'index.html', {"uid": uid, "gid": gid, "list": list})


def can_bejoin(request):
    gid = request.GET.get("gid")

    # 如果房间号为空
    if gid == "":
        return JsonResponse({"status": False, "msg": "房间号不能为空！"})


# 根据gid获取聊天室的聊天记录,如果24小时内用户加入过该群聊，返回上次登录到目前为止的数据
def get_msg(request):
    print("session_key------------>")
    uid = request.session['info']['uid']
    session_key = request.session.session_key + uid
    gid = request.GET.get('gid')
    obj = Message.objects.filter(gid=gid, uid=uid, session_key=session_key).first()
    print(uid)
    print(gid)
    if obj:
        # last_time = User.objects.get(uid=uid).last_time
        queryset = serializers.serialize("json", Message.objects.filter(gid=gid))
        print("这里在传送数据------------------------------------------------------------------------------->")
        return JsonResponse({"status": True, "queryset": queryset})
    else:
        return JsonResponse({"status": False})


# 存储消息到数据库
def storage_msg(request):
    uid = request.session['info']['uid']
    gid = request.GET.get('gid')
    msg = request.GET.get('msg')
    # 同一个浏览器登录同一个账号，发送过去的session_key是相同的
    session_key = request.session.session_key + uid
    time = datetime.now()
    message = Message(uid=uid, msg=msg, time=time, gid=gid, session_key=session_key)
    message.save()
    return JsonResponse({"status": True})


def get_websocket(request):
    uid = request.session["info"]["uid"]
    objs = Websocket.objects.filter(uid=uid)
    if not objs:
        return JsonResponse({"status": False})
    queryset = serializers.serialize("json", objs)
    all = Websocket.objects.all()
    allws = serializers.serialize("json", all)
    return JsonResponse({"status": True, "queryset": queryset})

def get_allwebsocket(request):
    all = Websocket.objects.all()
    if not all:
        return JsonResponse({"status": False})
    allws = serializers.serialize("json", all)
    return JsonResponse({"status": True, "allws": allws})


def add_websocket(request):
    uid = request.GET.get("uid")
    gid = request.GET.get("gid")
    key = uid + gid
    wb = Websocket(key=key, uid=uid, gid=gid)
    wb.save()
    return JsonResponse({"status": True})


def delete_websocket(request):
    uid = request.GET.get("uid")
    gid = request.GET.get("gid")
    key = uid + gid
    Websocket.objects.filter(uid=uid, gid=gid).delete()
    return JsonResponse({"status": True})


def test(request):
    return render(request, 'test.html')
