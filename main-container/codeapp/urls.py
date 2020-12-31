from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.home,name='home'),
    path('code/', views.code,name='code'),
    path('test/', views.test,name='test'),
    path('optimizationcode/', views.optimizationcode,name='optimizationcode')
    

]