"""mysiteS18 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include
from django.urls import path
from myapp import views
from django.views.static import serve
from mysite import settings
app_name = 'myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'myapp/', include('myapp.urls')),
    path(r'myapp/products', include('myapp.urls')),
    path(r'myapp/place_order', include('myapp.urls')),
    path(r'myapp/productdetail/<int:prodid>/', views.productdetail),
    path('admin/', admin.site.urls),
    path(r'myapp/<int:cat_no>/',views.detail),
    path(r'myapp/login',views.user_login),
    path(r'myapp/logout', views.user_logout),
    #path(r'myapp/logout',views.User_logout.as_view()),
    path(r'myapp/orders', views.myorder),
    path(r'myapp/payorders', views.place_order),
    #path(r'myapp/regist', views.regist),
    path(r'myapp/regist',views.Regist.as_view()),
    path(r'myapp/upload',views.upload),
    path(r'myapp/forgot',views.Forgot,name='Forgot'),
    url(r'^media/(?P<path>.*)$',serve, {'document_root': settings.MEDIA_ROOT}),
    path(r'myapp/test',views.test,name='test'),
    ]
