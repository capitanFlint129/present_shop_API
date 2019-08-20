from django.urls import path
from my_api import views

urlpatterns = [
    path('imports', views.imports),
    path('imports/<int:import_id>/citizen/<int:citizen_id>', views.update_citizen),
    path('imports/<int:import_id>/citizen', views.show_citizens)
]