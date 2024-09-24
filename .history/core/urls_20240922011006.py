from django.urls import path
from .views import * 
urlpatterns = [
    path('admin/', Index.as_view()),
]
