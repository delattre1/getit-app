from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tagsList/', views.tagsList, name='tagsList'),
    path('tag/<str:tag_>/', views.tag, name='tag')
]
