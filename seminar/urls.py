from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='signout'),
    path('addseminar/', views.addseminar, name='addseminar'),
    path('seminar/<str:pk_test>', views.seminardetails, name='seminardetails'),
    path('organizedseminar/<str:pk_test>',
         views.organizedseminardetails, name='organizedseminardetails'),

    path('myseminar/', views.myseminar, name='myseminar'),
    path('organizedseminar/', views.organizedseminar, name='organizedseminar'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
