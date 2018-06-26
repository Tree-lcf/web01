from . import views
from django.urls import path
from django.contrib.auth.views import login

app_name = 'users'
urlpatterns = [
    # 主页
    path('login/', login, {'template_name': '../templates/users/login.html'}, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]


