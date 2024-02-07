from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('organizationsignup/', views.organizationsignup,
         name='organizationsignup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='signout'),
    path('addseminar/', views.addseminar, name='addseminar'),
    path('seminar/<str:pk_test>', views.seminardetails, name='seminardetails'),
    path('cancel_registration/<str:pk_test>', views.cancelRegistration, name='cancelRegistration'),
    path('organizedseminar/<str:pk_test>',
         views.organizedseminardetails, name='organizedseminardetails'),

    path('myseminar/', views.myseminar, name='myseminar'),
    path('seminars/', views.seminars, name='seminars'),
    path('organizedseminar/', views.organizedseminar, name='organizedseminar'),
    path('archive/<str:pk_test>', views.seminararchive, name='seminararchive'),
    path('user_info', views.user_info, name='user_info'),
    path('update_info', views.user_info_update, name='user_info_update'),
    path('organization_info', views.organization_info, name='organization_info'),
    path('organization_info_update', views.organization_info_update, name='organization_info_update'),
    path('about', views.about_us, name='about_us'),
    path('update_seminar_details/<str:pk_test>', views.update_seminar_details, name='update_seminar_details'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
