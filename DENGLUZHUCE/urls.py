from django.shortcuts import render
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# Create your views here.


urlpatterns = [

    path('', views.检测),

    # pc端
    path('登录/', views.登录),
    path('注册/', views.注册),
    path('验证码/', views.验证码检测),
    path('注册成功/', views.登录1),
    path('找回密码/', views.找回密码),
    path('找回密码2/', views.找回密码2),
    path('找回密码3/', views.找回密码3),



    path('登录pe/', views.登录pe),
    path('注册pe/', views.注册pe),
    path('验证码pe/', views.验证码检测pe),
    path('注册成功pe/', views.登录1pe),
    path('找回密码pe/', views.找回密码pe),
    path('找回密码2pe/', views.找回密码2pe),
    path('找回密码3pe/', views.找回密码3pe),

    path('主页/', views.主页函数),
    path('游戏/', views.帖子函数),
    path('帖子/', views.帖子展示),
    path('设置个人中心/', views.设置个人中心),
    path('处理/', views.处理),


    #ai聊天
    path('创建机器人/', views.创建机器人),
    path('聊天/',views.ai聊天),
    path('删除/',views.ai删除),
    path('聊天记录/',views.ai下载),
    path('转跳/',views.转跳),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
