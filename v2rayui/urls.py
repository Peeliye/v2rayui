from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from . import admin

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
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
