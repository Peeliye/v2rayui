import json
from django.http import HttpResponseNotFound, JsonResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from v2rayui.models import User, UserTraffic, Node, NodeTraffic


def check_node(node_id, api_key):
    try:
        node = Node.objects.filter(node_id=node_id, api_key=api_key)
        if node:
            return True
        else:
            return False
    except Exception:
        return False


def user_api(request):
    """用户信息获取API"""
    node_id = request.headers.get('Nodeid', None)
    api_key = request.headers.get('Apikey', None)
    if node_id and api_key:
        if check_node(node_id, api_key):
            result_dict = {'users': []}
            try:
                db_users = User.objects.filter()
            except User.DoesNotExist:
                db_users = []
            for user in db_users:
                if not user.is_superuser:
                    if not user.is_free:
                        if user.expire_at < timezone.now():
                            continue
                result_dict['users'].append({
                    'user_id': str(user.user_id),
                    'username': user.username,
                    'level': user.level,
                    'alter_id': user.alter_id
                })
            return JsonResponse(result_dict, json_dumps_params={"ensure_ascii": False})
    return HttpResponseNotFound()


@csrf_exempt
def traffic_api(request):
    """用户或节点流量处理"""
    if request.method == 'POST':
        node_id = request.headers.get('Nodeid', None)
        api_key = request.headers.get('Apikey', None)
        if node_id and api_key:
            year_month = timezone.now().strftime('%Y-%m')
            try:
                post_dict = json.loads(request.body)
            except Exception:
                return HttpResponseServerError()
            if post_dict:
                try:
                    node_traffic, is_created = NodeTraffic.objects.get_or_create(node_id=node_id, year_month=year_month)
                    node_traffic.upload_traffic += post_dict['node']['uplink']
                    node_traffic.download_traffic += post_dict['node']['downlink']
                    node_traffic.save()
                except Exception:
                    return HttpResponseServerError()
                try:
                    for user_id, traffic_obj in post_dict['users'].items():
                        user_obj, is_create = UserTraffic.objects.get_or_create(user_id=user_id, year_month=year_month)
                        user_obj.upload_traffic += traffic_obj.get('uplink', 0)
                        user_obj.download_traffic += traffic_obj.get('downlink', 0)
                        user_obj.save()
                except Exception:
                    return HttpResponseServerError()
            return JsonResponse({'status': 'ok'})
    return HttpResponseNotFound()
