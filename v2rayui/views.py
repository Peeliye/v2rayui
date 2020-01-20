from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from v2rayui.forms import LoginForm, RegisterForm, ChangePasswordForm, InviteCodeForm
from v2rayui.models import User, InviteCode, Node, UserTraffic
from django.conf import settings
from django.utils import timezone
import datetime
import random
import string
import uuid


def global_settings(request):
    return {"ENABLE_USER_INVITATION": settings.ENABLE_USER_INVITATION}


def get_random_code():
    max_count = 10
    while max_count > 0:
        n = random.randint(8, 16)
        random_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))
        try:
            invite_code_result = InviteCode.objects.get(code=random_code)
        except InviteCode.DoesNotExist:
            invite_code_result = None
        if invite_code_result:
            max_count -= 1
            continue
        else:
            return random_code
    return str(uuid.uuid4())


def index(request):
    """首页跳转"""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        return HttpResponseRedirect(reverse("login"))


def user_login(request):
    """用户登录函数"""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dashboard"))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("dashboard"))
        return render(request, "login.html", {"form": form, "failed": True})
    else:
        form = LoginForm()
        return render(request, "login.html", {"form": form})


def user_logout(request):
    """用户登出函数"""
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    """用户注册函数"""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dashboard"))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                invite_code = InviteCode.objects.get(code=form.cleaned_data["invite_code"], is_used=False)
            except InviteCode.DoesNotExist:
                invite_code = None
            if invite_code:
                if invite_code.expired_at < timezone.now():
                    return render(request, "register.html", {"form": form, "failed": True, "reason": "邀请码已过期，请输重新获取邀请码"})
            else:
                return render(request, "register.html", {"form": form, "failed": True, "reason": "邀请码无效，请输入正确的邀请码"})
            try:
                user_check = User.objects.get(username=form.cleaned_data["username"])
            except User.DoesNotExist:
                user_check = None
            if user_check:
                return render(request, "register.html", {"form": form, "failed": True, "reason": "用户名已存在，请使用另外一个用户名"})
            new_user = User.objects.create_user(username=form.cleaned_data["username"],
                                                password=form.cleaned_data["password"],
                                                level=invite_code.user_level,
                                                is_free=invite_code.is_free,
                                                expire_at=invite_code.user_expired_at,
                                                inviter_name=invite_code.username)
            invite_code.is_used = True
            invite_code.save()
            user = authenticate(username=form.cleaned_data["username"],
                                password=form.cleaned_data["password"])
            login(request, user)
            return HttpResponseRedirect(reverse("dashboard"))
        return render(request, "register.html", {"form": form, "failed": True, "reason": "未知错误，请稍后重试注册"})
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form": form})


def dashboard(request):
    """首页展示函数"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    try:
        nodes = Node.objects.filter(enable=True)
    except Node.DoesNotExist:
        nodes = []
    try:
        traffic_obj, is_created = UserTraffic.objects.get_or_create(user_id=request.user.user_id, year_month=timezone.now().strftime('%Y-%m'))
        traffic = round(((traffic_obj.upload_traffic + traffic_obj.download_traffic) / 1024 / 1024 / 1024), 2)
    except Exception:
        traffic = 0
    return render(request, "dashboard.html", {"page": "dashboard", "nodes": nodes, "traffic": traffic})


def tutorial(request, system):
    """教程展示函数"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if system.lower() == "android":
        return render(request, "tutorial-android.html", {"page": "android", "clients": settings.CLIENTS})
    elif system.lower() == 'ios':
        return render(request, "tutorial-ios.html", {"page": "ios", "clients": settings.CLIENTS})
    elif system.lower() == "windows":
        return render(request, "tutorial-windows.html", {"page": "windows", "clients": settings.CLIENTS})
    elif system.lower() == "macos":
        return render(request, "tutorial-macos.html", {"page": "macos", "clients": settings.CLIENTS})
    else:
        return HttpResponseNotFound()


def client(request):
    """客户端下载页面"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "client.html", {"page": "client", "clients": settings.CLIENTS})


def invite_code(request):
    """邀请码管理页面"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if not settings.ENABLE_USER_INVITATION:
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse("dashboard"))
    if request.method == 'POST':
        form_data = InviteCodeForm(request.POST)
        if form_data.is_valid():
            if request.user.is_superuser:
                InviteCode.objects.create(code=get_random_code(),
                                          mark=form_data.cleaned_data["invite_code_mark"],
                                          username=request.user.username,
                                          is_free=True if form_data.cleaned_data["is_free"] == 'True' else False,
                                          user_level=int(form_data.cleaned_data["user_level"]),
                                          user_expired_at=form_data.cleaned_data["user_expired_at"] if form_data.cleaned_data.get(
                                              "user_expired_at") else timezone.now() + datetime.timedelta(days=settings.DEFAULT_USER_EXPIRE_DAYS),
                                          expired_at=timezone.now() + datetime.timedelta(days=settings.INVITE_CODE_EXPIRE_DAYS))
            elif request.user.invite_code_num > 0:
                InviteCode.objects.create(code=get_random_code(),
                                          mark=form_data.cleaned_data["invite_code_mark"],
                                          username=request.user.username,
                                          user_expired_at=timezone.now() + datetime.timedelta(days=settings.DEFAULT_USER_EXPIRE_DAYS),
                                          expired_at=timezone.now() + datetime.timedelta(days=settings.INVITE_CODE_EXPIRE_DAYS))
                request.user.invite_code_num -= 1
                request.user.save()
            return HttpResponseRedirect(reverse("invitecode"))
    form = InviteCodeForm()
    try:
        invite_codes = InviteCode.objects.filter(username=request.user.username).order_by("-created_at")
    except InviteCode.DoesNotExist:
        invite_codes = []

    user_invite_codes = []
    try:
        user_invite_codes = InviteCode.objects.filter(~Q(username=request.user.username)).order_by("-created_at")
    except InviteCode.DoesNotExist:
        user_invite_codes = []
    return render(request, "invite-code.html",
                  {"page": "invite_code", "form": form, "invite_codes": invite_codes, "user_invite_codes": user_invite_codes})


def change_password(request):
    """用户修改密码页面"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if request.user.check_password(form.cleaned_data["old_password"]):
                request.user.set_password(form.cleaned_data["new_password"])
                request.user.save()
                return render(request, "change_password.html", {"page": "change_password",
                                                                "form": form,
                                                                "msg": "修改密码成功！请刷新页面后重新登录"})
            else:
                return render(request, "change_password.html", {"page": "change_password",
                                                                "form": form,
                                                                "msg": "原密码错误，请重新输入"})
        return render(request, "change_password.html", {"page": "change_password",
                                                        "form": form,
                                                        "msg": "出现未知错误，请稍后重试。。。"})
    else:
        form = ChangePasswordForm()
        return render(request, "change_password.html", {"page": "change_password", "form": form})
