from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from v2rayui.forms import ServerNodeForm
from v2rayui.models import User, Node
from django.conf import settings
from django.utils import timezone


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
                                server=form_data.cleaned_data["server_addr"],
                                port=int(form_data.cleaned_data["server_port"]),
                                protocol=form_data.cleaned_data["protocol"],
                                path=form_data.cleaned_data["path"],
                                inbound_tag=form_data.cleaned_data["inbound_tag"],
                                enable=True if form_data.cleaned_data["is_enable"] == 'True' else False,
                                grpc_host=form_data.cleaned_data["grpc_host"],
                                grpc_port=int(form_data.cleaned_data["grpc_port"]),
                                country=form_data.cleaned_data["country"],
                                info=form_data.cleaned_data["info"])
            return HttpResponseRedirect(reverse("servernode"))
    form = ServerNodeForm()
    try:
        nodes = Node.objects.filter()
    except Node.DoesNotExist:
        nodes = []
    return render(request, "server-nodes.html", {"page": "server_node", "nodes": nodes, "form": form})


def users(request):
    """用户管理页面"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if not request.user.is_superuser:
        return HttpResponseNotFound()
    try:
        users = User.objects.filter().order_by("-date_joined")
    except User.DoesNotExist:
        users = []
    return render(request, "users.html", {"page": "users", "users": users})
