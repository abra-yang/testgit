from django.shortcuts import render
from django.http import HttpRequest,HttpResponse,HttpResponseBadRequest,JsonResponse
import simplejson
from .models import User,Title,Content
import bcrypt
import jwt
import  datetime
import math
from django.conf import settings
# Create your views here.

def reg(request:HttpRequest):
    payload = simplejson.loads(request.body)
    user = User()
    try:
        user.name = payload['name']
        user.email = payload['email']
        password = payload['password'].encode()
        user.password =bcrypt.hashpw(password,bcrypt.gensalt()).decode()
        user.save()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest('databases error',status=401)
    return HttpResponse(payload)

AUTH_EXPRIE = 60 * 60 * 8
KEY = 'cth$ib-7-1d_ptx%%g^t2qbtcw-if3m+&qqpe@o6p!*igpbeb-'
def gen_token(user_id):
    return jwt.encode({'user_id':user_id,'exp':int(datetime.datetime.now().timestamp()+AUTH_EXPRIE)},KEY).decode()


def auth(fn):
    def _wrapper(request):
        try:
            token = request.META['HTTP_JWT']
            payload = jwt.decode(token,KEY)

            user = User.objects.filter(pk=payload['user_id']).first()
            if user:
                request.user = user
                ret = fn(request)
                return ret
            else:
                raise  Exception
        except Exception as e:
            return HttpResponse('用户不合法')
    return  _wrapper
def login(request:HttpRequest):
    payload = simplejson.loads(request.body)
    try:
        password = payload['password']
        email = payload['email']
        user = User.objects.filter(email=email).first()
        if user:
            if bcrypt.checkpw(password.encode(),user.password.encode()):
                token = gen_token(user.id)
                res = JsonResponse({'token':token,'userinfo':{'user_id':user.id,'email':user.email,'name':user.name}})
                res.set_cookie('jwt',token)
                return res
            else:
                raise Exception
        else:
            raise Exception
    except Exception as e:
        print(e)
        return HttpResponseBadRequest('参数错误',status=401)
@auth
def pub(request:HttpRequest):
    payload = simplejson.loads(request.body)
    try:
        t = Title()
        t.title = payload['title']
        t.uid = request.user.id
        t.save()
        c = Content()
        c.content = payload['content']
        c.tid = t.tid
        c.save()
    except Exception as e :
        print(e)
        return HttpResponseBadRequest('发布文章不成功')
    return JsonResponse({'status':'sucess'})


def get(request,id):
    try:
        t = Title.objects.filter(pk=id).first()
        if t:
            c = Content.objects.filter(tid=t.tid).first()
            return JsonResponse({
                'title':t.title,
                'content':c.content,
                'auther':t.uid,
                'postdate':t.postdate.timestamp()
            })
        else:
            raise  Exception
    except Exception as e:
        print(e)
        return HttpResponseBadRequest('文章不存在')

def checksth(d,name,default,typy_fn,check_fn):
    try :
        result = typy_fn(d.get(name,default))
        result = check_fn(result,default)
    except:
        result = default
    return result


def getall(requets:HttpRequest):
    page = checksth(requets.GET,'page',1,int,lambda page,default: page if page > 0 else default)
    size = checksth(requets.GET,'size',20,int,lambda size,default: size if size > 100 or size < 0 else default )
    start = (page-1) * size
    ts = Title.objects.order_by('-tid')
    count = ts.count()
    ts = ts[start:start+size]
    ret = {'titles':[{'tid':t.tid,'title':t.title,'postdate':t.postdate.timestamp(),'uid':t.uid} for t in ts],'pageinfo':{'page':page,'count':count,'size':size,'pagecount':math.ceil(count/size)}}
    return JsonResponse(ret)
