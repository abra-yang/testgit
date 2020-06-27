from django.urls import path,re_path
from .views import reg,login,pub,get
urlpatterns = [
    re_path('^reg$',reg),
    re_path('^login$',login),
    re_path('^pub$',pub),
    re_path('(\d+)',get)
]