from django.template import Library
from django.utils import timezone
import base64

register = Library()


@register.filter
def get_expire_days(expire_time):
    if expire_time > timezone.now():
        return (expire_time - timezone.now()).days + 1
    else:
        return 0


@register.filter
def get_vmss_base64(node_info, req):
    client_config = str({
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
    })
    return (base64.b64encode(client_config.encode('utf-8'))).decode("utf-8")


@register.filter
def get_if_expired(datetime_info):
    return datetime_info < timezone.now()
