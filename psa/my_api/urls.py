from django.urls import path
from my_api import views

urlpatterns = [
    path('imports', views.imports, name="imports"),
    path('imports/<int:import_id>/citizens/<int:citizen_id>', views.update_citizen, name="update-citizen"),
    path('imports/<int:import_id>/citizens', views.show_citizens, name="show-all"),
    path('imports/<int:import_id>/citizens/birthdays', views.birthdays, name="birthdays"),
    path('imports/<int:import_id>/towns/stat/percentile/age', views.percentile, name="percentiles")
]