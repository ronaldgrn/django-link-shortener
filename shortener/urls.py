from django.urls import path

from shortener import views

urlpatterns = [
    path('test/<path:link>', views.test),
    path('<link>/', views.expand),
]
