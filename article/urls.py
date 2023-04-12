from django.urls import path

from . import views

urlpatterns = [
    # path('test/', views.test, name='test'),
    path('', views.index, name='index'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    path('categories/<int:pk>/', views.category, name='category'),
    path('tags/<int:pk>/', views.tag, name='tag'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('create/', views.create, name='create'),
    path('update/<int:pk>/', views.update, name='update'),
]