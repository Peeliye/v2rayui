from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from . import admin
from . import apis

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('register', views.register, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('tutorial/<str:system>', views.tutorial, name='tutorial'),
    path('client', views.client, name='client'),
    path('invitecode', views.invite_code, name='invitecode'),
    path('changepassword', views.change_password, name='changepassword'),

    # Admin only
    path('nodes', admin.server_node, name='servernode'),
    path('users', admin.users, name='users'),
    path('reopen_invite_code/<str:invite_code>', admin.reopen_invite_code, name='reopen_invite_code'),
    path('delete_invite_code/<str:invite_code>', admin.delete_invite_code, name='delete_invite_code'),

    # APIs
    path('userapi', apis.user_api, name='userapi'),
    path('trafficapi', apis.traffic_api, name='trafficapi'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
