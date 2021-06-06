from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.home,name='home'),
    path("search/", views.search, name="search"),
    path('optimizationcode/', views.optimizationcode,name='optimizationcode')
    

]