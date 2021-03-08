from django.contrib import admin
from django.urls import path
from .views import package_view,create_view,packages_view

urlpatterns = [
    #path('',packages_view),
    #path('<int:code>/', package_view),
    #path('create/',create_view),
]
