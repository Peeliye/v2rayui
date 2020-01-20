from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from v2rayui.forms import ServerNodeForm, UserEditForm
from v2rayui.models import User, UserTraffic, Node, NodeTraffic, InviteCode
from django.conf import settings
import datetime
import random
import uuid
import string


def get_random_key():
    max_count = 10
    while max_count > 0:
        key_length = 32
        random_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(key_length))
        try:
            api_key_result = Node.objects.get(api_key=random_key)
        except Node.DoesNotExist:
            api_key_result = None
        if api_key_result:
            max_count -= 1
            continue
        else:
            return random_key
    return str(uuid.uuid4())


def server_node(request):
    """服务器节点管理页面"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if not request.user.is_superuser:
        return HttpResponseNotFound()
    if request.method == 'POST':
        form_data = ServerNodeForm(request.POST)
        if form_data.is_valid():
            Node.objects.create(name=form_data.cleaned_data["node_name"],
                                api_key=get_random_key(),
                                server=form_data.cleaned_data["server_addr"],
                                port=int(form_data.cleaned_data["server_port"]),
                                protocol=form_data.cleaned_data["protocol"],
                                path=form_data.cleaned_data["path"],
                                enable=True if form_data.cleaned_data["is_enable"] == 'True' else False,
                                country=form_data.cleaned_data["country"],
                                total_traffic=int(form_data.cleaned_data["total_traffic"]) if form_data.cleaned_data.get("total_traffic") else 0,
                                comment=form_data.cleaned_data["comment"])
            return HttpResponseRedirect(reverse("servernode"))
    form = ServerNodeForm()
    try:
        nodes = Node.objects.filter()
    except Node.DoesNotExist:
        nodes = []
    try:
        nodes_traffic = NodeTraffic.objects.filter(year_month=timezone.now().strftime('%Y-%m'))
    except NodeTraffic.DoesNotExist:
        nodes_traffic = []
    return render(request, "server-nodes.html", {"page": "server_node", "nodes": nodes, "nodes_traffic": nodes_traffic, "form": form})


def users(request):
    """用户管理页面"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if not request.user.is_superuser:
        return HttpResponseNotFound()
    if request.method == 'POST':
        form_data = UserEditForm(request.POST)
        if form_data.is_valid():
            try:
                user = User.objects.get(user_id=form_data.cleaned_data.get('user_id'))
            except Exception:
                return HttpResponseServerError()
            try:
                if form_data.cleaned_data.get('expire_at'):
                    user.expire_at = form_data.cleaned_data['expire_at']
                if form_data.cleaned_data.get('total_traffic') or form_data.cleaned_data.get('total_traffic') == 0:
                    user.total_traffic = int(form_data.cleaned_data['total_traffic'])
                if form_data.cleaned_data.get('invite_code_num'):
                    user.invite_code_num = int(form_data.cleaned_data['invite_code_num'])
                if form_data.cleaned_data.get('level'):
                    user.level = int(form_data.cleaned_data['level'])
                if form_data.cleaned_data.get('is_free'):
                    user.is_free = True if form_data.cleaned_data['is_free'] == 'True' else False
                if form_data.cleaned_data.get('alter_id'):
                    user.alter_id = int(form_data.cleaned_data['alter_id'])
                if form_data.cleaned_data.get('password'):
                    user.set_password(form_data.cleaned_data['password'])
                user.save()
            except Exception:
                return HttpResponseServerError()
            return HttpResponseRedirect(reverse("users"))
    form = UserEditForm()
    try:
        users = User.objects.filter().order_by("-date_joined")
    except User.DoesNotExist:
        users = []
    try:
        users_traffic = UserTraffic.objects.filter(year_month=timezone.now().strftime('%Y-%m'))
    except UserTraffic.DoesNotExist:
        users_traffic = []
    return render(request, "users.html", {"page": "users", "users": users, "users_traffic": users_traffic, "form": form})


def reopen_invite_code(request, invite_code):
    """重新打开已过期的邀请码"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if not request.user.is_superuser:
        return HttpResponseNotFound()
    if not invite_code:
        return HttpResponseNotFound()
    try:
        invite_code = InviteCode.objects.get(code=invite_code)
        if invite_code.is_used:
            return HttpResponseServerError()
        invite_code.expired_at = timezone.now() + datetime.timedelta(days=settings.INVITE_CODE_EXPIRE_DAYS)
        invite_code.save()
    except Exception:
        return HttpResponseServerError()
    return HttpResponseRedirect(reverse("invitecode"))


def delete_invite_code(request, invite_code):
    """删除邀请码"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if not request.user.is_superuser:
        return HttpResponseNotFound()
    if not invite_code:
        return HttpResponseNotFound()
    try:
        invite_code = InviteCode.objects.get(code=invite_code)
        invite_code.delete()
    except Exception:
        return HttpResponseServerError()
    return HttpResponseRedirect(reverse("invitecode"))
