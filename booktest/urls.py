from django.urls import path, re_path, include
from . import views
app_name = 'booktest'
urlpatterns = [
    re_path('^$', views.index, name="index"),
    # re_path('^(\w+)/$', views.show, name='show'),
    re_path('htmlTest/$', views.htmlTest),
    re_path('csrf1/$', views.csrf1),
    re_path('csrf2/$', views.csrf2),
    re_path('verifyCode/$', views.verifyCode),
    re_path('verifyTest1/$', views.verifyTest1),
    re_path('verifyTest2/$', views.verifyTest2),
    re_path('^yanzheng/$',views.yanzheng, name="yzm"),
    re_path('^yz_home/$',views.yz_home ),

]