from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('seminar/<str:pk_test>', views.seminardetails, name='seminardetails'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
