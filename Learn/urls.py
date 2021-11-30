from django.urls import path
from django.conf.urls.static import static
from django.conf import  settings


from . import views

urlpatterns = [
    path('login', views.signin, name='login'),
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('register', views.register, name='register'),
    path('sign', views.sign, name='sign'),
    path('logout', views.signout, name='logout'),
    path('course', views.course, name='course'),
    path('search', views.search, name='search'),
    path('addcourse', views.addcourse, name='addcourse'),
    path('savecourse', views.savecourse, name='savecourse'),
    path('r^(?P<cr_id>\d+)/editcourse/$', views.editcourse, name='editcourse'),
    path('r^(?P<cr_id>\d+)/updatecourse/$', views.updatecourse, name='updatecourse'),
    path('r^(?P<cr_id>\d+)/delete/$', views.deletecourse, name='deletecourse'),
    path('r^(?P<cr_id>\d+)/chapter/$', views.chapter, name='chapter'),
    path('r^(?P<cr_id>\d+)/addchapter/$', views.addchapter, name='addchapter'),
    path('r^(?P<cr_id>\d+)/savechapter/$', views.savechapter, name='savechapter'),
    path('r^(?P<ch_id>\d+)/editchapter/$', views.editchapter, name='editchapter'),
    path('r^(?P<ch_id>\d+)/(?P<cr_id>\d+)/updatechapter/$', views.updatechapter, name='updatechapter'),
    path('r^(?P<ch_id>\d+)/(?P<cr_id>\d+)/deletechapter/$', views.deletechapter, name='deletechapter'),
    path('r^(?P<ch_id>\d+)/lesson/$', views.lesson, name='lesson'),
    path('r^(?P<ch_id>\d+)/addlesson/$', views.addlesson, name='addlesson'),
    path('r^(?P<ch_id>\d+)/savelesson/$', views.savelesson, name='savelesson'),
    path('r^(?P<l_id>\d+)/editlesson/$', views.editlesson, name='editlesson'),
    path('r^(?P<l_id>\d+)/(?P<ch_id>\d+)/updatelesson/$', views.updatelesson, name='updatelesson'),
    path('r^(?P<l_id>\d+)/(?P<ch_id>\d+)/deletelesson/$', views.deletelesson, name='deletelesson'),
    path('r^(?P<cr_id>\d+)/listlesson/$', views.listlesson, name='listlesson'),
    path('r^(?P<l_id>\d+)/(?P<ch_id>\d+)/playlesson/$', views.playlesson, name='playlesson'),
    path('stcourse', views.stcourse, name='stcourse'),
]

urlpatterns  += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)