from django.contrib import admin
from django.urls import path,include
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('schedule.urls')),
    path('', views.home, name='home'),
]
