import os
import json
import google.generativeai as genai
import numpy as np
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import auth
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from .models import 用户信息, 游戏帖子, 游戏帖子图片, 评论
from sentence_transformers import SentenceTransformer


def 登录(request):
    错误 = "账号或密码错误"
    无 = " "

    if request.method == "POST":

        username = request.POST.get('USERNAME')
        password = request.POST.get('PASSWORD')

        用户 = auth.authenticate(username=username, password=password)

        if 用户 is not None:
            login(request, 用户)

            # return redirect('../主页')
            return redirect('../聊天')
        else:
            return render(request, '登录界面.html', {

                "ANDSS": 错误

            })












    else:
        return render(request, '登录界面.html', {

            "ANDSS": 无

        })


def generate_verification_code():
    # 生成一个随机的6位数验证码
    verification_code = ''.join(random.choice('0123456789') for _ in range(6))
    return verification_code


from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render
import random


def generate_verification_code():
    # 生成一个随机的6位数验证码
    verification_code = ''.join(random.choice('0123456789') for _ in range(6))
    return verification_code


def 注册(request):
    错误1 = "用户名存在！"
    错误2 = "邮箱已被注册，请登录！"
    无 = " "

    if request.method == "POST":
        username = request.POST['USERNAME']
        password = request.POST['PASSWORD']
        email = request.POST['EMAIL']

        # 如果密码相等
        if password == password:
            # 如果邮箱已存在
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return render(request, '注册界面.html', {
                    "ANDSS": 错误2
                })
            # 如果用户名已经存在
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return render(request, '注册界面.html', {
                    "ANDSS": 错误1
                })
            # 如果都不存在
            else:
                # 生成验证码
                verification_code = generate_verification_code()

                # 将验证码和用户名保存在会话中
                request.session['verification_code'] = verification_code
                request.session['username'] = username
                request.session['password'] = password
                request.session['email'] = email

                # 发送验证码邮件
                subject = '验证码'
                message = f'您正在注册lingo账号，您的验证码是: {verification_code}'
                from_email = 'lingotema@foxmail.com'  # 用你的邮箱替换
                recipient_list = [email]

                # 发送电子邮件
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                return redirect('../验证码')
    else:
        return render(request, '注册界面.html', {
            "ANDSS": 无
        })


def 验证码检测(request):
    if request.method == "POST":
        # 从会话中获取验证码和用户名
        verification_code = request.session.get('verification_code', '')
        username = request.session.get('username', '')
        password = request.session.get('password', '')
        email = request.session.get('email', '')
        验证码 = request.POST['YZM']

        if 验证码 == verification_code:

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            user_login = auth.authenticate(username=username, password=password)
            auth.login(request, user_login)
            user_model = User.objects.get(username=username)
            new_profile = 用户信息.objects.create(用户名=user_model, id_user=user_model.id)
            new_profile.save()
            user_info = 用户信息.objects.get(用户名=request.user)

            user_info.save()

            return redirect('../注册成功')
        else:
            return render(request, '邮箱验证码界面.html', {
                "ANDSS": "验证码错误请重新输入"
            })
    else:
        return render(request, '邮箱验证码界面.html', {
            "ANDSS": " "
        })


def 登录1(request):
    错误 = "账号或密码错误"
    无 = " "

    if request.method == "POST":

        username = request.POST.get('USERNAME')
        password = request.POST.get('PASSWORD')

        用户 = auth.authenticate(username=username, password=password)

        if 用户 is not None:
            login(request, 用户)
            # return redirect('../主页')
            return redirect('../聊天')
        else:
            return render(request, '登录界面.html', {

                "ANDSS": 错误

            })












    else:
        return render(request, '登录界面.html', {

            "ANDSS": "注册成功！请登录"

        })


def 找回密码(request):
    if request.method == "POST":
        邮箱 = request.POST['邮箱']

        错误 = "此邮箱没有注册账号！！！"

        if User.objects.filter(email=邮箱).exists():
            # 生成验证码
            verification_code = generate_verification_code()

            # 将验证码和用户名保存在会话中
            request.session['verification_code'] = verification_code
            # request.session['username'] = username
            # request.session['password'] = password
            request.session['邮箱'] = 邮箱

            # 发送验证码邮件
            subject = '验证码'
            message = f'您正在修改密码，您的验证码是: {verification_code}'
            from_email = 'lingotema@foxmail.com'  # 用你的邮箱替换
            recipient_list = [邮箱]

            # 发送电子邮件
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return redirect('../找回密码2')


        else:
            return render(request, '找回密码.html', {

                "ANDSS": 错误

            })
    return render(request, '找回密码.html', {

        "ANDSS": ""

    })


def 找回密码2(request):
    if request.method == "POST":
        验证码 = request.POST['验证码']

        verification_code = request.session.get('verification_code', '')

        if 验证码 == verification_code:

            return redirect('../找回密码3')


        else:
            return render(request, '找回密码2.html', {

                "ANDSS": "验证码错误！！"
            })

    return render(request, '找回密码2.html', {

        "ANDSS": "  "

    })


def 找回密码3(request):
    if request.method == "POST":
        密码 = request.POST['密码']

        邮箱 = request.session.get('邮箱', '')

        user_to_update = User.objects.get(email=邮箱)
        new_password = 密码
        user_to_update.set_password(new_password)
        user_to_update.save()

        return redirect('../登录')

    else:

        return render(request, '找回密码3.html', {

            "ANDSS": "  "

        })


def 检测(request):
    # 如果session存在并且不为空，说明用户已经登录
    if request.session.exists(request.session.session_key) and not request.session.is_empty():
        # 跳转到用户的主页或者其他页面
        # return redirect('/主页')

        return redirect('../聊天')
    return render(request, '检测客户端设备.html')


"""----------------------------------------------------------------------------------------------------------------------------------"""
"""----------------------------------------------------------------------------------------------------------------------------------"""


def 登录pe(request):
    错误 = "账号或密码错误"
    无 = " "

    if request.method == "POST":

        username = request.POST.get('USERNAME')
        password = request.POST.get('PASSWORD')

        用户 = auth.authenticate(username=username, password=password)

        if 用户 is not None:
            login(request, 用户)
            # return redirect('../主页')
            return redirect('../聊天')
        else:
            return render(request, '登录界面pe.html', {

                "ANDSS": 错误

            })












    else:
        return render(request, '登录界面pe.html', {

            "ANDSS": 无

        })


def 注册pe(request):
    错误1 = "用户名存在！"
    错误2 = "邮箱已被注册，请登录！"
    无 = " "

    if request.method == "POST":
        username = request.POST.get('USERNAME')
        password = request.POST.get('PASSWORD')
        email = request.POST['EMAIL']

        # 如果密码相等
        if password == password:
            # 如果邮箱已存在
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return render(request, '注册界面pe.html', {
                    "ANDSS": 错误2
                })
            # 如果用户名已经存在
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return render(request, '注册界面pe.html', {
                    "ANDSS": 错误1
                })
            # 如果都不存在
            else:
                # 生成验证码
                verification_code = generate_verification_code()

                # 将验证码和用户名保存在会话中
                request.session['verification_code'] = verification_code
                request.session['username'] = username
                request.session['password'] = password
                request.session['email'] = email

                # 发送验证码邮件
                subject = '验证码'
                message = f'您正在注册lingo账号，您的验证码是: {verification_code}'
                from_email = 'lingotema@foxmail.com'  # 用你的邮箱替换
                recipient_list = [email]

                # 发送电子邮件
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                return redirect('../验证码pe')
    else:
        return render(request, '注册界面pe.html', {

            "ANDSS": 无
        })


def 验证码检测pe(request):
    if request.method == "POST":
        # 从会话中获取验证码和用户名
        verification_code = request.session.get('verification_code', '')
        username = request.session.get('username', '')
        password = request.session.get('password', '')
        email = request.session.get('email', '')
        验证码 = request.POST['YZM']

        if 验证码 == verification_code:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            user_login = auth.authenticate(username=username, password=password)
            auth.login(request, user_login)
            user_model = User.objects.get(username=username)
            new_profile = 用户信息.objects.create(用户名=user_model, id_user=user_model.id)
            new_profile.save()
            user_info = 用户信息.objects.get(用户名=request.user)

            return redirect('../注册成功pe')
        else:
            return render(request, '邮箱验证码界面pe.html', {
                "ANDSS": "验证码错误请重新输入"
            })
    else:
        return render(request, '邮箱验证码界面pe.html', {
            "ANDSS": " "
        })


def 登录1pe(request):
    错误 = "账号或密码错误"
    无 = " "

    if request.method == "POST":

        username = request.POST.get('USERNAME')
        password = request.POST.get('PASSWORD')

        用户 = auth.authenticate(username=username, password=password)

        if 用户 is not None:
            login(request, 用户)
            # return redirect('../主页')
            return redirect('../聊天')
        else:
            return render(request, '登录界面pe.html', {

                "ANDSS": 错误

            })












    else:
        return render(request, '登录界面pe.html', {

            "ANDSS": "注册成功！请登录"

        })


def 找回密码pe(request):
    if request.method == "POST":
        邮箱 = request.POST['邮箱']

        if User.objects.filter(email=邮箱).exists():
            # 生成验证码
            verification_code = generate_verification_code()

            # 将验证码和用户名保存在会话中
            request.session['verification_code'] = verification_code
            # request.session['username'] = username
            # request.session['password'] = password
            request.session['邮箱'] = 邮箱

            # 发送验证码邮件
            subject = '验证码'
            message = f'您正在修改密码，您的验证码是: {verification_code}'
            from_email = 'lingotema@foxmail.com'  # 用你的邮箱替换
            recipient_list = [邮箱]

            # 发送电子邮件
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return redirect('../找回密码2pe')


        else:
            return render(request, '找回密码pe.html', {

                "ANDSS": "此邮箱没有注册账号！！！"

            })

    return render(request, '找回密码pe.html', {

        "ANDSS": "  "

    })


def 找回密码2pe(request):
    if request.method == "POST":
        验证码 = request.POST['验证码']

        verification_code = request.session.get('verification_code', '')

        if 验证码 == verification_code:

            return redirect('../找回密码3pe')


        else:
            return render(request, '找回密码2pe.html', {

                "ANDSS": "验证码错误！！"
            })

    return render(request, '找回密码2pe.html', {

        "ANDSS": "  "

    })


def 找回密码3pe(request):
    if request.method == "POST":
        密码 = request.POST['密码']

        邮箱 = request.session.get('邮箱', '')

        user_to_update = User.objects.get(email=邮箱)
        new_password = 密码
        user_to_update.set_password(new_password)
        user_to_update.save()

        return redirect('../登录pe')

    else:

        return render(request, '找回密码3pe.html', {

            "ANDSS": "  "

        })


def 主页函数(request):
    # --------------------------------------------验证是否登录---------------------------------------------------

    # 如果session不存在或者为空，就重定向到登录界面
    if not request.session.exists(request.session.session_key) or request.session.is_empty():
        return redirect('../')
    # 如果session已经过期，就清除session并且重定向到登录界面
    if request.session.get_expiry_age() <= 0:
        request.session.flush()
        return redirect('../')
    # 如果session还有效，就获取当前登录的用户对象，并且进入主页
    用户 = request.user

    # ----------------------------------------------------------------------------------------------------------
    游戏帖子列表 = 游戏帖子.objects.order_by('-日期')[:20]  # 按日期降序排列并获取前6个

    current_user_info = 用户信息.objects.get(用户名=request.user)

    context = {
        'current_user_info': current_user_info,
        '背景': current_user_info.背景图片.url,
        '用户': 用户,
        '游戏帖子列表': 游戏帖子列表
    }

    if request.method == "POST":

        退出 = request.POST.get('退出')
        修改用户名 = request.POST.get('修改用户名')
        改邮箱 = request.POST.get('改邮箱')
        邮箱 = request.POST.get('邮箱')
        密码 = request.POST.get('密码')
        头像1 = request.FILES.get('修改头像')
        背景 = request.FILES.get('修改背景')
        个性签名 = request.POST.get('个性签名')
        帖子 = request.POST.get('帖子类型')
        标题 = request.POST.get('标题')
        正文 = request.POST.get('正文')
        链接 = request.POST.get('链接')
        游戏图片 = request.FILES.getlist('游戏图片')

        if 退出 == "退出":
            logout(request)
            return redirect('../')

        # # 这里tmd有个bug，修不好cnm
        # if 密码 is not None:
        #     current_user = request.user
        #
        #     current_user.set_password(密码)
        #     current_user.save()
        #       open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
        #       context = {
        #     'open_dialog2': open_dialog,
        #            }
        #       return render(request, '网页主页.html', context)

        if 修改用户名 is not None:
            if User.objects.filter(username=修改用户名).exists():
                open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
                context = {
                    'open_dialog': open_dialog,
                }
                return render(request, '网页主页.html', context)
            else:
                current_user = request.user
                current_user.username = 修改用户名
                current_user.save()
                open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
                context = {
                    'open_dialog2': open_dialog,
                }
                return render(request, '网页主页.html', context)

        if 邮箱 is not None:
            if User.objects.filter(email=邮箱).exists():
                open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
                context = {
                    'open_dialog': open_dialog,
                }
                return render(request, '网页主页.html', context)
            else:
                current_user = request.user

                # 修改邮箱为 邮箱啊啊啊啊啊啊啊啊啊啊啊好累
                current_user.email = 邮箱
                current_user.save()
                open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
                context = {
                    'open_dialog2': open_dialog,
                }
                return render(request, '网页主页.html', context)

        # 这里tmd有个bug，修不好cnm
        if 密码 is not None:
            current_user = request.user

            current_user.set_password(密码)
            current_user.save()

            logout(request)
            return redirect('../')

        if 头像1 is not None:
            current_user = request.user
            user_info = 用户信息.objects.get(用户名=current_user)
            original_avatar_path = user_info.头像.path

            # 检查文件名是否等于特定值
            if os.path.basename(original_avatar_path) != 'blank-profile-picture.png':
                # 不等于特定值时，删除原始头像文件
                if default_storage.exists(original_avatar_path):
                    default_storage.delete(original_avatar_path)

            user_info.头像 = 头像1
            user_info.save()
            open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
            context = {
                'open_dialog2': open_dialog,
            }
            return render(request, '网页主页.html', context)

        if 背景 is not None:
            current_user = request.user
            user_info = 用户信息.objects.get(用户名=current_user)
            if user_info.背景图片.name != 'blank-profile-picture.png':
                default_storage.delete(user_info.背景图片.name)
            user_info.背景图片 = 背景
            user_info.save()
            open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
            context = {
                'open_dialog2': open_dialog,
            }
            return render(request, '网页主页.html', context)

        if 个性签名 is not None:
            current_user = request.user
            user_info = 用户信息.objects.get(用户名=current_user)
            user_info.个性签名 = 个性签名
            user_info.save()
            open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
            context = {
                'open_dialog2': open_dialog,
            }
            return render(request, '网页主页.html', context)

        if 帖子 == "游戏":
            # 从表单中获取其他信息

            # 获取当前用户
            current_user = request.user

            # 创建新的帖子对象
            new_post = 游戏帖子(发帖人=current_user, 链接=链接, 标题=标题, 内容=正文, 封面=游戏图片[0])
            new_post.save()
            for 文件 in 游戏图片[1:]:
                游戏图片对象 = 游戏帖子图片(游戏帖子=new_post, 图片=文件)
                游戏图片对象.save()
            open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
            context = {
                'open_dialog4': open_dialog,
            }
            return render(request, '网页主页.html', context)

        open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
        context = {
            'open_dialog3': open_dialog,
        }
        return render(request, '网页主页.html', context)






    else:

        return render(request, '网页主页.html', context)


def 帖子函数(request):
    # --------------------------------------------验证是否登录---------------------------------------------------

    # 如果session不存在或者为空，就重定向到登录界面
    if not request.session.exists(request.session.session_key) or request.session.is_empty():
        return redirect('../')
    # 如果session已经过期，就清除session并且重定向到登录界面
    if request.session.get_expiry_age() <= 0:
        request.session.flush()
        return redirect('../')

    # 如果session还有效，就获取当前登录的用户对象，并且进入主页
    用户 = request.user

    # ----------------------------------------------------------------------------------------------------------
    游戏帖子列表 = 游戏帖子.objects.all()

    游戏帖子列表 = Paginator(游戏帖子列表, 20)
    page_number = request.GET.get('page')
    游戏帖子列表分页 = 游戏帖子列表.get_page(page_number)
    current_user_info = 用户信息.objects.get(用户名=request.user)

    context = {
        'current_user_info': current_user_info,
        '背景': current_user_info.背景图片.url,
        '用户': 用户,
        '游戏帖子列表': 游戏帖子列表分页
    }

    if request.method == "POST":

        退出 = request.POST.get('退出')
        修改用户名 = request.POST.get('修改用户名')
        改邮箱 = request.POST.get('改邮箱')
        邮箱 = request.POST.get('邮箱')
        密码 = request.POST.get('密码')
        头像1 = request.FILES.get('修改头像')
        背景 = request.FILES.get('修改背景')
        个性签名 = request.POST.get('个性签名')
        帖子 = request.POST.get('帖子类型')
        标题 = request.POST.get('标题')
        正文 = request.POST.get('正文')
        链接 = request.POST.get('链接')
        游戏图片 = request.FILES.getlist('游戏图片')

        if 退出 == "退出":
            logout(request)
            return redirect('../')

        # # 这里tmd有个bug，修不好cnm
        # if 密码 is not None:
        #     current_user = request.user
        #
        #     current_user.set_password(密码)
        #     current_user.save()
        #       open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
        #       context = {
        #     'open_dialog2': open_dialog,
        #            }
        #       return render(request, '网页主页.html', context)

        if 修改用户名 is not None:
            if User.objects.filter(username=修改用户名).exists():
                open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
                context = {
                    'open_dialog': open_dialog,
                }
                return render(request, '浏览帖子.html', context)
            else:
                current_user = request.user
                current_user.username = 修改用户名
                current_user.save()
                open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
                context = {
                    'open_dialog2': open_dialog,
                }
                return render(request, '浏览帖子.html', context)

        if 邮箱 is not None:
            if User.objects.filter(email=邮箱).exists():
                open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
                context = {
                    'open_dialog': open_dialog,
                }
                return render(request, '浏览帖子.html', context)
            else:
                current_user = request.user

                # 修改邮箱为 邮箱啊啊啊啊啊啊啊啊啊啊啊好累
                current_user.email = 邮箱
                current_user.save()
                open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
                context = {
                    'open_dialog2': open_dialog,
                }
                return render(request, '浏览帖子.html', context)

        # 这里tmd有个bug，修不好cnm
        if 密码 is not None:
            current_user = request.user

            current_user.set_password(密码)
            current_user.save()

            logout(request)
            return redirect('../')

        if 头像1 is not None:
            current_user = request.user
            user_info = 用户信息.objects.get(用户名=current_user)
            original_avatar_path = user_info.头像.path

            # 检查文件名是否等于特定值
            if os.path.basename(original_avatar_path) != 'blank-profile-picture.png':
                # 不等于特定值时，删除原始头像文件
                if default_storage.exists(original_avatar_path):
                    default_storage.delete(original_avatar_path)

            user_info.头像 = 头像1
            user_info.save()
            open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
            context = {
                'open_dialog2': open_dialog,
            }
            return render(request, '浏览帖子.html', context)

        if 背景 is not None:
            current_user = request.user
            user_info = 用户信息.objects.get(用户名=current_user)
            if user_info.背景图片.name != 'blank-profile-picture.png':
                default_storage.delete(user_info.背景图片.name)
            user_info.背景图片 = 背景
            user_info.save()
            open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
            context = {
                'open_dialog2': open_dialog,
            }
            return render(request, '浏览帖子.html', context)

        if 个性签名 is not None:
            current_user = request.user
            user_info = 用户信息.objects.get(用户名=current_user)
            user_info.个性签名 = 个性签名
            user_info.save()
            open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
            context = {
                'open_dialog2': open_dialog,
            }
            return render(request, '浏览帖子.html', context)

        if 帖子 == "游戏":
            # 从表单中获取其他信息

            # 获取当前用户
            current_user = request.user

            # 创建新的帖子对象
            new_post = 游戏帖子(发帖人=current_user, 链接=链接, 标题=标题, 内容=正文, 封面=游戏图片[0])
            new_post.save()
            for 文件 in 游戏图片[1:]:
                游戏图片对象 = 游戏帖子图片(游戏帖子=new_post, 图片=文件)
                游戏图片对象.save()
            open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
            context = {
                'open_dialog4': open_dialog,
            }
            return render(request, '浏览帖子.html', context)

        open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
        context = {
            'open_dialog3': open_dialog,
        }
        return render(request, '浏览帖子.html', context)






    else:

        return render(request, '浏览帖子.html', context)


def 帖子展示(request):
    # --------------------------------------------验证是否登录---------------------------------------------------

    # 如果session不存在或者为空，就重定向到登录界面
    if not request.session.exists(request.session.session_key) or request.session.is_empty():
        return redirect('../')
    # 如果session已经过期，就清除session并且重定向到登录界面
    if request.session.get_expiry_age() <= 0:
        request.session.flush()
        return redirect('../')

    # 如果session还有效，就获取当前登录的用户对象，并且进入主页
    用户 = request.user

    # ----------------------------------------------------------------------------------------------------------
    游戏帖子列表1 = 游戏帖子.objects.order_by('-日期')[:20]  # 按日期降序排列并获取前6个

    current_user_info = 用户信息.objects.get(用户名=request.user)

    context = {
        'current_user_info': current_user_info,
        '背景': current_user_info.背景图片.url,
        '用户': 用户,
        '游戏帖子列表': 游戏帖子列表1
    }

    if request.method == "POST":

        退出 = request.POST.get('退出')
        修改用户名 = request.POST.get('修改用户名')
        改邮箱 = request.POST.get('改邮箱')
        邮箱 = request.POST.get('邮箱')
        密码 = request.POST.get('密码')
        头像1 = request.FILES.get('修改头像')
        背景 = request.FILES.get('修改背景')
        个性签名 = request.POST.get('个性签名')
        帖子 = request.POST.get('帖子类型')
        标题 = request.POST.get('标题')
        正文 = request.POST.get('正文')
        链接 = request.POST.get('链接')
        游戏图片 = request.FILES.getlist('游戏图片')
        写评论 = request.POST.get('写评论')

        帖子id = request.POST.get('帖子id')
        游戏帖子对象 = 游戏帖子.objects.get(id=帖子id)
        发帖人用户id = 游戏帖子对象.发帖人_id
        游戏图片列表 = 游戏帖子对象.游戏图片.all()

        发帖人 = User.objects.get(id=发帖人用户id)
        发帖人用户信息 = 用户信息.objects.get(用户名=发帖人用户id)

        context = {
            'current_user_info': current_user_info,
            '背景': current_user_info.背景图片.url,
            '用户': 用户,
            '游戏帖子列表': 游戏帖子列表1,
            '帖子': 游戏帖子对象,
            '游戏图片列表': 游戏图片列表,
            '类型': "游戏",
            '发帖人': 发帖人,

            '发帖人用户信息': 发帖人用户信息
        }

        if 退出 == "退出":
            logout(request)
            return redirect('../')

        # # 这里tmd有个bug，修不好cnm
        # if 密码 is not None:
        #     current_user = request.user
        #
        #     current_user.set_password(密码)
        #     current_user.save()
        #       open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
        #       context = {
        #     'open_dialog2': open_dialog,
        #            }
        #       return render(request, '网页主页.html', context)

        if 修改用户名 is not None:
            if User.objects.filter(username=修改用户名).exists():
                open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
                context = {
                    'open_dialog': open_dialog,
                }
                return render(request, '帖子.html', context)
            else:
                current_user = request.user
                current_user.username = 修改用户名
                current_user.save()
                open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
                context = {
                    'open_dialog2': open_dialog,
                }
                return render(request, '帖子.html', context)

        if 邮箱 is not None:
            if User.objects.filter(email=邮箱).exists():
                open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
                context = {
                    'open_dialog': open_dialog,
                }
                return render(request, '帖子.html', context)
            else:
                current_user = request.user

                # 修改邮箱为 邮箱啊啊啊啊啊啊啊啊啊啊啊好累
                current_user.email = 邮箱
                current_user.save()
                open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
                context = {
                    'open_dialog2': open_dialog,
                }
                return render(request, '帖子.html', context)

        # 这里tmd有个bug，修不好cnm
        if 密码 is not None:
            current_user = request.user

            current_user.set_password(密码)
            current_user.save()

            logout(request)
            return redirect('../')

        if 头像1 is not None:
            current_user = request.user
            user_info = 用户信息.objects.get(用户名=current_user)
            original_avatar_path = user_info.头像.path

            # 检查文件名是否等于特定值
            if os.path.basename(original_avatar_path) != 'blank-profile-picture.png':
                # 不等于特定值时，删除原始头像文件
                if default_storage.exists(original_avatar_path):
                    default_storage.delete(original_avatar_path)

            user_info.头像 = 头像1
            user_info.save()
            open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
            context = {
                'open_dialog2': open_dialog,
            }
            return render(request, '帖子.html', context)

        if 背景 is not None:
            current_user = request.user
            user_info = 用户信息.objects.get(用户名=current_user)
            if user_info.背景图片.name != 'blank-profile-picture.png':
                default_storage.delete(user_info.背景图片.name)
            user_info.背景图片 = 背景
            user_info.save()
            open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
            context = {
                'open_dialog2': open_dialog,
            }
            return render(request, '帖子.html', context)

        if 个性签名 is not None:
            current_user = request.user
            user_info = 用户信息.objects.get(用户名=current_user)
            user_info.个性签名 = 个性签名
            user_info.save()
            open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
            context = {
                'open_dialog2': open_dialog,
            }
            return render(request, '帖子.html', context)

        if 帖子 == "游戏":
            # 从表单中获取其他信息

            # 获取当前用户
            current_user = request.user

            # 创建新的帖子对象
            new_post = 游戏帖子(发帖人=current_user, 链接=链接, 标题=标题, 内容=正文, 封面=游戏图片[0])
            new_post.save()
            for 文件 in 游戏图片[1:]:
                游戏图片对象 = 游戏帖子图片(游戏帖子=new_post, 图片=文件)
                游戏图片对象.save()
            open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
            context = {
                'open_dialog4': open_dialog,
            }
            return render(request, '帖子.html', context)
        if 写评论 is not None:
            评论人id = request.POST.get('评论人id')
            comment = 评论()

            # 设置评论属性值
            comment.帖子 = 游戏帖子.objects.get(id=帖子id)  # 使用适当的帖子ID来获取游戏帖子对象
            comment.评论人 = User.objects.get(id=评论人id)  # 使用适当的用户ID来获取用户对象
            comment.点赞数 = 0  # 设置点赞数
            comment.评论 = request.POST.get('写评论')

            评论和用户信息列表 = None
            # 评论人 =None
            try:
                评论列表 = 评论.objects.filter(帖子__id=帖子id)
                评论和用户信息列表 = []

                for 评论对象 in 评论列表:
                    # 获取评论人的用户信息
                    用户信息对象 = 用户信息.objects.get(用户名=评论对象.评论人)

                    # 将评论对象和用户信息对象拼接成一个元组，并添加到新列表666
                    评论和用户信息列表.append((评论对象, 用户信息对象))
                # 评论人id = 评论.评论人
                # 评论人 = User.objects.get(id=评论人id)
            except 评论.DoesNotExist:

                pass

            # 保存评论到数据库
            comment.save()

            return render(request, '帖子.html', {
                'current_user_info': current_user_info,
                '背景': current_user_info.背景图片.url,
                '用户': 用户,
                '游戏帖子列表': 游戏帖子列表1,
                '帖子': 游戏帖子对象,
                '游戏图片列表': 游戏图片列表,
                '类型': "游戏",
                '发帖人': 发帖人,
                '评论和用户信息列表': 评论和用户信息列表,
                # '评论人':评论人,
                '发帖人用户信息': 发帖人用户信息,

                'open_dialog5': True,

            })

        open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
        context = {
            'open_dialog3': open_dialog,

        }
        return render(request, '帖子.html', context)






    elif request.method == "GET":

        帖子id = request.GET.get('id')
        游戏帖子对象 = 游戏帖子.objects.get(id=帖子id)
        发帖人用户id = 游戏帖子对象.发帖人_id
        游戏图片列表 = 游戏帖子对象.游戏图片.all()

        发帖人 = User.objects.get(id=发帖人用户id)
        发帖人用户信息 = 用户信息.objects.get(用户名=发帖人用户id)
        评论和用户信息列表 = None
        # 评论人 =None

        try:
            评论列表 = 评论.objects.filter(帖子__id=帖子id)
            评论和用户信息列表 = []

            for 评论对象 in 评论列表:
                # 获取评论人的用户信息
                用户信息对象 = 用户信息.objects.get(用户名=评论对象.评论人)

                # 将评论对象和用户信息对象拼接成一个元组，并添加到新列表
                评论和用户信息列表.append((评论对象, 用户信息对象))
            # 评论人id = 评论.评论人
            # 评论人 = User.objects.get(id=评论人id)
        except 评论.DoesNotExist:
            # 处理评论不存在的情况
            pass

        return render(request, '帖子.html', {
            'current_user_info': current_user_info,
            '背景': current_user_info.背景图片.url,
            '用户': 用户,
            '游戏帖子列表': 游戏帖子列表1,
            '帖子': 游戏帖子对象,
            '游戏图片列表': 游戏图片列表,
            '类型': "游戏",
            '发帖人': 发帖人,
            '评论和用户信息列表': 评论和用户信息列表,

            '发帖人用户信息': 发帖人用户信息

        })

    open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
    context = {
        'open_dialog3': open_dialog,
    }
    return render(request, '帖子.html', context)


def 设置个人中心(request):
    # --------------------------------------------验证是否登录---------------------------------------------------

    # 如果session不存在或者为空，就重定向到登录界面
    if not request.session.exists(request.session.session_key) or request.session.is_empty():
        return redirect('../')
    # 如果session已经过期，就清除session并且重定向到登录界面
    if request.session.get_expiry_age() <= 0:
        request.session.flush()
        return redirect('../')

    # 如果session还有效，就获取当前登录的用户对象，并且进入主页
    用户 = request.user
    current_user_info = 用户信息.objects.get(用户名=request.user)
    游戏帖子列表 = 游戏帖子.objects.filter(发帖人=request.user)

    per_page = 10  # 每页显示的项目数量
    paginator = Paginator(游戏帖子列表, per_page)

    page_number = request.GET.get('page')
    游戏帖子列表分页 = paginator.get_page(page_number)

    if request.method == "POST":

        用户名 = request.POST.get('修改名')
        邮箱 = request.POST.get('修改邮箱')
        密码 = request.POST.get('修改密码')
        头像1 = request.FILES.get('修改头像')
        背景 = request.FILES.get('修改背景')
        个性签名 = request.POST.get('个性签名')
        删除id = request.POST.get('删除id')

        # ----------------------------------------------------------------------------------------------------------
        if 用户名 is not None:
            if User.objects.filter(username=用户名).exists():
                open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
                context = {
                    'open_dialog': open_dialog,
                    "current_user_info": current_user_info
                }
                return render(request, '个人与设置中心.html', context)
            else:
                current_user = request.user
                current_user.username = 用户名
                current_user.save()
                open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
                context = {
                    'open_dialog2': open_dialog,
                    "current_user_info": current_user_info

                }
                return render(request, '个人与设置中心.html', context)

        if 邮箱 is not None:
            if User.objects.filter(email=邮箱).exists():
                open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
                context = {
                    'open_dialog': open_dialog,
                    "current_user_info": current_user_info
                }
                return render(request, '个人与设置中心.html', context)
            else:
                current_user = request.user

                # 修改邮箱为 邮箱啊啊啊啊啊啊啊啊啊啊啊好累
                current_user.email = 邮箱
                current_user.save()
                open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
                context = {
                    'open_dialog2': open_dialog,
                    "current_user_info": current_user_info
                }
                return render(request, '个人与设置中心.html', context)

        # 这里tmd有个bug，修不好cnm
        if 密码 is not None:
            current_user = request.user

            current_user.set_password(密码)
            current_user.save()

            logout(request)
            return redirect('../')

        if 头像1 is not None:
            current_user = request.user
            user_info = 用户信息.objects.get(用户名=current_user)
            original_avatar_path = user_info.头像.path

            # 检查文件名是否等于特定值
            if os.path.basename(original_avatar_path) != 'blank-profile-picture.png':
                # 不等于特定值时，删除原始头像文件
                if default_storage.exists(original_avatar_path):
                    default_storage.delete(original_avatar_path)

            user_info.头像 = 头像1
            user_info.save()

            open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
            context = {
                'open_dialog2': open_dialog,
                "current_user_info": current_user_info
            }
            return render(request, '个人与设置中心.html', context)

        if 背景 is not None:
            print('背景执行成功')

            current_user = request.user
            user_info = 用户信息.objects.get(用户名=current_user)
            print('背景执行成功')
            if user_info.背景图片.name != 'blank-profile-picture.png':
                default_storage.delete(user_info.背景图片.name)
            user_info.背景图片 = 背景
            user_info.save()
            open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
            context = {
                'open_dialog2': open_dialog,
                "current_user_info": current_user_info
            }
            print('背景执行成功')
            return render(request, '个人与设置中心.html', context)

        if 个性签名 is not None:
            current_user = request.user
            user_info = 用户信息.objects.get(用户名=current_user)
            user_info.个性签名 = 个性签名
            user_info.save()
            open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
            context = {
                'open_dialog2': open_dialog,
            }
            return render(request, '个人与设置中心.html', context)

        if 删除id is not None:
            游戏帖子对象 = get_object_or_404(游戏帖子, id=删除id)
            游戏帖子对象.delete()
            open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
            context = {
                'open_dialog2': open_dialog,
            }
            return render(request, '个人与设置中心.html', context)

        open_dialog = True  # 如果要打开对话框，将其设置为True；否则设置为False
        context = {
            'open_dialog3': open_dialog,
        }
        return render(request, '个人与设置中心.html', context)


    else:
        return render(request, '个人与设置中心.html', {
            "current_user_info": current_user_info,
            '游戏帖子列表': 游戏帖子列表分页
        })


def ai聊天(request):

    if request.method == "GET":
        qwqw = request.user
        用户 = 用户信息.objects.get(id_user=qwqw.id)

        AI模型 = AIModel.objects.filter(user_id=qwqw.id)

        return render(request, 'ai聊天.html', {

            "用户": 用户,
            "AI模型": AI模型

        })

    elif request.method == "POST":

        pass


from django.http import HttpResponse
import time

from .models import AIModel


def 处理(request):
    """=================================================================================================="""
    # 如果session不存在或者为空，就重定向到登录界面
    if not request.session.exists(request.session.session_key) or request.session.is_empty():
        return redirect('../')
    # 如果session已经过期，就清除session并且重定向到登录界面
    if request.session.get_expiry_age() <= 0:
        request.session.flush()
        return redirect('../')

    try:
        用户 = request.user
        print("12312412354")
        AIID = request.POST.get('AIID')
        ai模型 = AIModel.objects.get(aiid=AIID)
        print(ai模型.聊天记录)
        聊天记录 = ai模型.聊天记录
        性格数据 = ai模型.personality_text
        温度 = str(ai模型.温度)
        最大输出字数 = int(ai模型.最大输出字数)
        检索记忆长度 = int(ai模型.检索记忆长度)
        print("12312412354")

        if not AIID:
            # 如果AIID为空，重定向到指定的URL
            return redirect('../聊天/')

        print(AIID)
        聊天记录数组 = json.loads(ai模型.chat_vector_dict)



        if request.method == "POST":
            文本 = request.POST.get('text')

            GOOGLE_API_KEY = ""
            genai.configure(api_key=f"{GOOGLE_API_KEY}", transport="rest")
            # Set up the model
            generation_config = {
                "temperature": float(温度),
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": int(最大输出字数),
            }

            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
            ]

            model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                          generation_config=generation_config,
                                          safety_settings=safety_settings)

            convo = model.start_chat(history=[
            ])

            最大检索长度 = 检索记忆长度

            def get_last_chars(input_string, num_chars=23500 - int(最大检索长度)):
                # 如果字符串长度小于指定的字符数，则返回整个字符串
                # 否则，返回最后num_chars个字符
                return input_string[-num_chars:] if len(input_string) > num_chars else input_string

            # # 示例用法
            # string_to_slice = "这里是你的字符串"
            # last_chars = get_last_chars(string_to_slice)
            # print(last_chars)
            from datetime import datetime

            聊天记录2 = get_last_chars(聊天记录)

            print(文本)

            # convo.send_message(文本)
            # convo.last.text
            print("12312412354")


            # 等待5秒钟
            # 23500/2
            time.sleep(0)
            x = int(ai模型.相似度最高的键的数量)

            if x != 0 and (len(聊天记录) > 23500 - int(最大检索长度)):


                model = SentenceTransformer('DMetaSoul/Dmeta-embedding')


                print("将字典中的字符串键转换为NumPy向量")
                dict_vectors = {key: np.fromstring(key.strip('[]'), sep=', ') for key in 聊天记录数组}
                your_vector = model.encode("人类:" + 文本, normalize_embeddings=True)
                print("ok==>将字典中的字符串键转换为NumPy向量")

                # 计算相似度
                print("计算相似度")
                similarity_scores = {key: your_vector @ value.T for key, value in dict_vectors.items()}
                print("ok==>计算相似度")

                n = float (ai模型.相似度阈值)

                filtered_keys = {key: score for key, score in similarity_scores.items() if score >= n}

                print("寻找相似内容")
                # 提取相似度最高的前x个键
                  # 您想要的相似度最高的键的数量
                top_keys = sorted(filtered_keys, key=filtered_keys.get, reverse=True)[:x]

                # 使用这些键去找对应内容，并拼接成字符串
                result_string = ''.join([聊天记录数组[key] for key in top_keys])
                print("ok==>寻找相似内容")


                print("输出结果")
                # 输出结果
                print(result_string)
                print("ok==>输出结果")

            else:
                result_string = ''


            def get_last_chars2(input_string, num_chars=int(最大检索长度)):
                # 如果字符串长度小于指定的字符数，则返回整个字符串
                # 否则，返回最后num_chars个字符
                return input_string[-num_chars:] if len(input_string) > num_chars else input_string

            检索信息 = get_last_chars2(result_string)

            输入数据 = "当前时间" + str(datetime.now()) + 性格数据 + ("\n由于大语言模型的输入限制，下面是通过RAG从对话历史中检索到的有关聊天记录\n"
                                                                      "") + 检索信息 + "接下来是最近的聊天记录" + 聊天记录2 + "人类" + str(
                datetime.now()) + ":" + 文本 + "\n " + ai模型.AI名字 + ":"
            现在时间 = str(datetime.now())

            convo.send_message(输入数据)

            文字 = convo.last.text

            # 输入数据 = 性格数据 + 聊天记录2 + "人类" + str(datetime.now()) + ":" + 文本 + "\n 香草："

            聊天记录1 = 聊天记录 + "人类" + 现在时间 + ":" + 文本 + " \n "+ ai模型.AI名字 + str(datetime.now()) + ":"  + 文字 + "\n"

            ai模型.聊天记录 = 聊天记录1

            if x != 0:
                
                model = SentenceTransformer('DMetaSoul/Dmeta-embedding')
                embs1 = model.encode("人类" + 现在时间 + ":" + 文本 + " \n " + ai模型.AI名字 + str(datetime.now()) + ":"  + 文字 + "\n",
                                     normalize_embeddings=True)

                print(embs1)

                embs1_tuple = np.array2string(embs1, separator=', ', max_line_width=np.inf)

                聊天记录数组[embs1_tuple] = "人类:" + 文本 + " \n " + ai模型.AI名字 + ":" + 文字 + "\n"

                ai模型.chat_vector_dict = json.dumps(聊天记录数组, ensure_ascii=False)

            ai模型.save()

            print("ok==>")
            # 返回纯文本响应
            print(文字)
            return HttpResponse(文字)




    except Exception as e:

        print("捕获到异常：", e)

        文字 = """<p style="color: red;font-size: 15px;">出现问题！可能是由于敏感内容或者字数受限，请重试！！！(如果没有模型点击左上角创建)</p>"""

        print("ok==>")
        # 返回纯文本响应
        print(文字)
        return HttpResponse(文字)


# genai.configure(api_key="AIzaSyDWiYURphW_ePd6m5dWGc-TV4IYGt3A6UU")


# convo.send_message("你好你是谁")
# print(convo.last.text)


def 创建机器人(request):

    # 如果session不存在或者为空，就重定向到登录界面
    if not request.session.exists(request.session.session_key) or request.session.is_empty():
        return redirect('../')
    # 如果session已经过期，就清除session并且重定向到登录界面
    if request.session.get_expiry_age() <= 0:
        request.session.flush()
        return redirect('../')
    用户 = request.user

    AI名字 = request.POST.get('AI名字')
    要求文本 = request.POST.get('要求文本')
    温度 = request.POST.get('温度')
    最大输出字数 = request.POST.get('最大输出字数')
    检索记忆长度 = request.POST.get('检索记忆长度')
    相似度阈值 = request.POST.get('相似度阈值')
    相似度最高的键的数量 = request.POST.get('相似度最高的键的数量')


    print(AI名字, 要求文本, 温度, 最大输出字数, 检索记忆长度)
    aiid = random.randint(100000, 999999)

    new_record = AIModel(AI名字=AI名字, personality_text=要求文本, 温度=温度, 最大输出字数=最大输出字数,
                         检索记忆长度=检索记忆长度, user_id=用户.id, aiid=aiid, 聊天记录=" ",相似度阈值=相似度阈值,
                         相似度最高的键的数量=相似度最高的键的数量
                         )
    new_record.save()

    return redirect("../聊天/")


def ai删除(request):
    # 如果session不存在或者为空，就重定向到登录界面
    if not request.session.exists(request.session.session_key) or request.session.is_empty():
        return redirect('../')
    # 如果session已经过期，就清除session并且重定向到登录界面
    if request.session.get_expiry_age() <= 0:
        request.session.flush()
        return redirect('../')



    删除id = request.POST.get('删除')
    ai模型 = AIModel.objects.get(aiid=删除id)
    ai模型.delete()
    return redirect("../聊天/")








def ai下载(request):
    # 如果session不存在或者为空，就重定向到登录界面
    if not request.session.exists(request.session.session_key) or request.session.is_empty():
        return redirect('../')
    # 如果session已经过期，就清除session并且重定向到登录界面
    if request.session.get_expiry_age() <= 0:
        request.session.flush()
        return redirect('../')


    下载id = request.POST.get('下载')
    ai模型 = AIModel.objects.get(aiid=下载id)

    response = HttpResponse(ai模型.聊天记录, content_type='text/plain; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="聊天记录_{ai模型.aiid}_{ai模型.AI名字}.txt"'

    return response

def 转跳(request):
    return redirect("../设置个人中心/")




