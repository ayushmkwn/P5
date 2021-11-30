from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('registration',views.registration, name="registration"),
    path('login',views.loggin, name="login"),
    path('logout',views.loggout, name="logout"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('userInfo', views.user_information, name='userInfo')
]