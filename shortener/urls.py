from django.urls import path

from shortener import views

urlpatterns = [
    path('', views.index),
    path('<link>/', views.expand),
]
