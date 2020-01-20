from django.template import Library
from django.utils import timezone
import base64
import json
from urllib.parse import quote

register = Library()


@register.filter
def get_expire_days(expire_time):
    if expire_time > timezone.now():
        return (expire_time - timezone.now()).days + 1
    else:
        return 0


@register.filter
def get_vmess_link(node_info, req):
    client_config = {
        "v": "2",
        "ps": node_info.name,
        "add": node_info.server,
        "port": node_info.port,
        "id": str(req.user.user_id),
        "aid": req.user.alter_id,
        "net": node_info.protocol,
        "type": "none",
        "host": node_info.server,
        "path": node_info.path,
        "tls": "tls"
    }
    return "vmess://" + (base64.b64encode(json.dumps(client_config).replace(' ', '').encode('utf-8'))).decode("utf-8")


@register.filter
def get_ios_vmess_link(node_info, req):
    server_str = "auto:%s@%s:%d" % (str(req.user.user_id), node_info.server, node_info.port)
    config_str = 'vmess://' + (base64.b64encode(server_str.encode('utf-8'))).decode("utf-8")
    config_str += '?remarks=%s' % quote(node_info.name, 'utf-8')
    config_str += '&obfsParam=%s' % node_info.server
    config_str += '&path=%s' % node_info.path
    config_str += '&obfs=%s' % 'websocket' if node_info.protocol == 'ws' else 'http2'
    config_str += '&tls=1&peer=&cert=&tfo=1&mux=1'
    return config_str


@register.filter
def get_if_expired(datetime_info):
    return datetime_info < timezone.now()


@register.filter
def get_node_traffic(node_id, nodes_traffic_obj):
    for traffic_obj in nodes_traffic_obj:
        if traffic_obj.node_id == node_id:
            return round(((traffic_obj.upload_traffic + traffic_obj.download_traffic) / 1024 / 1024 / 1024), 2)
    return 0


@register.filter
def get_user_traffic(user_id, users_traffic_obj):
    for traffic_obj in users_traffic_obj:
        if traffic_obj.user_id == user_id:
            return round(((traffic_obj.upload_traffic + traffic_obj.download_traffic) / 1024 / 1024 / 1024), 2)
    return 0
