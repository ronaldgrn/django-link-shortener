from django.urls import path
from shortener import views
from django.conf import settings

app_name = "shortener"
urlpatterns = [
    path('<link>/', views.expand, name="expand"),
]

if getattr(settings, 'SHORTENER_ENABLE_TEST_PATH', False):
    urlpatterns.append(path('test/<path:link>', views.test, name="test"))
