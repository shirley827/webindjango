from django.conf.urls import url
from django.template.backends import django
from django.template.context_processors import static
from django.urls import path,include
from myapp import views
from django.views.static import serve
from mysite import settings
from myapp.views import Regist
app_name = 'myapp'


urlpatterns = [
    path(r'', views.index, name='index'),
    url(r'about', views.about, name='about'),
    url(r'index', views.index, name='index'),
    url(r'place_order', views.place_order, name='place'),
    url(r'payorders', views.place_order, name='place'),
    url(r'products', views.products, name='products'),
    url(r'productdetail/<int:prodid>/', views.productdetail, name='products'),
    url(r'login', views.user_login, name='login'),
    url(r'logout', views.user_logout, name='logout'),
    #url(r'logout',views.User_logout.as_view(),name='logout'),
    #url(r'regist', views.regist, name='regist'),
    url(r'regist',views.Regist.as_view(),name='regist'),
    url(r'orders', views.myorder, name='myorder'),
    url(r'<int:cat_no>/',views.detail,name='detail'),
    url(r'upload', views.upload,name='upload'),
    url(r'forgot',views.Forgot,name='Forgot'),
    url(r'^media/(?P<path>.*)$',serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^test',views.test,name='test'),
   ]
