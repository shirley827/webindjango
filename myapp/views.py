from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.core.mail import send_mail
from django.views.generic import View
from mysite import settings
from .models import Category, Product, Client, Order, Clientavatar
from .forms import OrderForm, InterestForm,ClientForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
# Create your views here.
def Forgot(request):
    if request.method == 'POST':
        email = request.POST.get('email',None)
        username = request.POST.get('username',None)
        temail = Client.objects.get(username=username).email
        password = Client.objects.get(username=username).password
        if email == temail:
            Client.objects.filter(username=username,password=password).update(password='abcd1234')
            info = 'Change you info sucessful please check the new one in your email.'
            send_mail('Hello','abcd1234.',settings.EMAIL_FROM,[email],fail_silently=False)
            return HttpResponse(info)
        else:
            info = 'Your email is wrong'
            return HttpResponse(info)
    else:
        return render(request,'myapp/fogpaswd.html')

class Regist(View):
    def get(self,request):
        form=ClientForm()
        return render(request,'myapp/regist.html',{'form':form})
    def post(self,request):
        form=ClientForm(request.POST)
        if form.is_valid():
            user=form.save()
            msg='regist sucess'
            return render(request,'myapp/regist.html',{'form':form,'msg':msg})
        else:
            msg='failed'
            return render(request,'myapp/regist.html',{'form':form,'msg':msg})
'''
def regist(request):
    if request.method == 'POST':
        form=ClientForm(request.POST)
        if form.is_valid():
            user=form.save()
            msg='regist sucess'
            return render(request,'myapp/regist.html',{'form':form,'msg':msg})
        else:
            msg='regist failed'
            return render(request,'myapp/regist.html',{'form':form,'msg':msg})
    else:
        form=ClientForm()
        return render(request,'myapp/regist.html',{'form':form})
'''
def index(request):

    time = request.session.get('last_login', False)
    cat_list = Category.objects.all().order_by('id')[:10]
    if time:
        statu = 1
        return render(request, 'myapp/test1.html', {'statu':statu,'cat_list': cat_list,'time':time})
    else:
        return render(request,'myapp/test1.html',{'cat_list': cat_list,'time':time})

def detail(request,cat_no):
    catinfo = Category.objects.filter(id=cat_no)

    pro_list = Product.objects.filter(category_id=cat_no)
    sql_dic = {'catinfo':catinfo,'pro_list':pro_list}
    return render(request,'myapp/detail0.html',{'catinfo':catinfo,'pro_list':pro_list})

def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prodlist': prodlist})


def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                order.product.stock=order.product.stock-order.num_units
                Product.objects.filter(name=order.product).update(stock=order.product.stock)
                order.save()
                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'myapp/order_response.html', {'msg': msg})

    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist})


def productdetail(request,prodid):
    msg = ''
    proinfo = get_object_or_404(Product, id=prodid)
    if request.method == 'POST':
        #interest = request.POST['interested']
        #num= request.POST['quantity']
        #addtion = request.POST['Additional Comments']
        form = InterestForm(request.POST)

        if form.is_valid():
            if form.interested:
                proinfo.interested+=1
                Product.objects.filter(id = prodid).update(interested=proinfo.interested)
                msg = 'Information has been updated'
                return render(request, 'myapp/productdetail.html', {'form':form,'msg': msg, 'proinfo': proinfo})
            else:
                msg = 'Not interested'
                return render(request, 'myapp/productdetail.html', {'form':form,'msg':msg,'proinfo':proinfo})

        else:
            msg='Not passed the validation'
            return render(request, 'myapp/productdetail.html', {'form': form, 'msg': msg, 'proinfo': proinfo})
    else:
        msg = "Get not Post"
        form=InterestForm
        return render(request, 'myapp/productdetail.html', {'form':form,'msg':msg,'proinfo':proinfo})

def about(request):

        visit = int(request.COOKIES.get('about_visits','0'))
        response = render_to_response('myapp/about.html', {'visit': visit})
        visit = visit+1
        response.set_cookie('about_visits',visit,max_age=300)
        visit = str(visit)
        return  response

@login_required()
def upload(request):
    if request.method == 'POST':
        #imageform = UploadForm(request.POST,request.FILES,instance=request.user)
       # if imageform.is_valid():
            username = request.POST.get('username')
            avatar = request.FILES.get('avatar')
            avatarinfo = Clientavatar.objects.filter(username=username)
            if avatarinfo:
                    avatarinfo.delete()
                    Clientavatar.objects.create(username=username,avatar=avatar)
                #image=Client(username=username,avatar=request.FILES.get('avatar'))
                #image.save()
                    clientinfo = Client.objects.get(username=username)
                    avatarinfo = Clientavatar.objects.get(username=username)
                    return render(request,'myapp/userinfo.html',{'clientinfo':clientinfo,'avatarinfo':avatarinfo})
            else:
                    Clientavatar.objects.create(username=username,avatar=avatar)
                    clientinfo = Client.objects.get(username=username)
                    avatarinfo = Clientavatar.objects.get(username=username)
                    return render(request, 'myapp/userinfo.html', {'clientinfo': clientinfo, 'avatarinfo': avatarinfo})
    else:
        return render(request,'myapp/upload.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        response = HttpResponseRedirect(reverse('myapp:myorder'))
        #usernamecook = request.COOKIES.get('username',)
        #number = request.COOKIES.get('about_visits','0')

        #if usernamecook:
            #if number !=0 :
               # number = int(number)+1
        #else:
            #number = 0
        if user:
            if user.is_active:
                time = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
                #response.set_cookie('username',username)
                response.set_cookie('about_visits',0,max_age=300)
                request.session['is_login']=True
                request.session['username']=username
                request.session.set_expiry(3600)
                request.session['last_login']=time
                login(request, user)
                return response
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))


def myorder(request):
    is_login=request.session.get('is_login',False)
    response=HttpResponseRedirect(reverse('myapp:login'))
    if is_login:
        username = request.session.get('username', '')
        clientinfo = Client.objects.get(username=username)
        orders = Order.objects.filter(client=clientinfo)
        return render(request,'myapp/myorder.html',{'orders':orders})
    else:
        return response


def test(request):
    time = request.session.get('last_login', False)
    cat_list = Category.objects.all().order_by('id')[:10]
    if time:
        statu = 1
        firstname = request.session.get('username',)
        return render(request, 'myapp/test1.html', {'firstname':firstname,'statu': statu, 'cat_list': cat_list, 'time': time})
    else:
        return render(request, 'myapp/test1.html', {'cat_list': cat_list, 'time': time})