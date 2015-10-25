from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import auth, sites
import django_comments
from app01 import models

# Create your views here.
def acc_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username,password=password)
    print username,password
    if user is not None:
        auth.login(request,user)
        content = '''
        welcome %s !!!
        <a href='/logout/'>Logout</a>
        ''' % user.username
        return HttpResponseRedirect('/')
    else:
        return render_to_response('login.html')


def logout_view(request):
    user = request.user
    auth.logout(request)
    return HttpResponse("<b>%s</b> Logged out! <a href='/login/'>Re-Login</a>" % user)


def Login(request):
    return render_to_response('login.html')


#@login_required
def index(request):

    bbs_list = models.BBS.objects.all()
    bbs_categories = models.Category.objects.all()
    return render_to_response('index.html', {'bbs_list':bbs_list,
                                             'user':request.user,
                                             'bbs_category':bbs_categories,
                                             'cata_id':0,
                                             })


def bbs_detail(request, bbs_id):
    bbs = models.BBS.objects.get(id=bbs_id)
    print '--->', bbs
    return render_to_response('bbs_detail.html', {'bbs_obj':bbs, 'user':request.user})


def sub_comment(request):
    print request.POST
    bbs_id=request.POST.get('bbs_id')
    comment = request.POST.get('comment_content')

    django_comments.models.Comment.objects.create(
        content_type_id = 7,
        object_pk = bbs_id,
        site_id = 1,
        user = request.user,
        comment = comment,

    )
    return HttpResponseRedirect('/detail/%s' % bbs_id)


def bbs_pub(request):
    return render_to_response('bbs_pub.html')


def bbs_sub(request):
    print ',==>', request.POST.get('content')
    # category_id = models.Category.objects.get('category_id')
    title = request.POST.get('title')
    summary = request.POST.get('summary')
    content = request.POST.get('content')
    author = models.BBS_user.objects.get(user__username=request.user)
    models.BBS.objects.create(
        category_id = 1,
        title = title,
        summary = summary,
        content = content,
        author = author,
        view_count = 1,
        ranking = 1,
    )

    return HttpResponse('yes.')


def category(request, cata_id):
    bbs_list = models.BBS.objects.filter(category__id=cata_id)
    bbs_categories = models.Category.objects.all()
    return render_to_response('index.html', {'bbs_list':bbs_list,
                                             'user':request.user,
                                             'bbs_category':bbs_categories,
                                             'cata_id':int(cata_id),
                                             })

