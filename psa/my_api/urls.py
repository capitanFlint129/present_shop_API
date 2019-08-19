from django.urls import path
from my_api import views

urlpatterns = [
    path('imports/', views.imports),
]
