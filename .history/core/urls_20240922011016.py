from django.urls import path
from .views import * 
urlpatterns = [
    path('admin/', IndexView.as_view(), name='index'),
]
