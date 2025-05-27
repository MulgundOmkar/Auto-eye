from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('index', views.index, name='index'),
        path('registration', views.registration, name='registration'),
    path('extract_text/', views.extract_text, name='extract_text'),
    path('getin/', views.getin, name='getin'),
    path('', views.home, name='home'),
    path('available_slot', views.available_slot, name='available_slot'),


]
