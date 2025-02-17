from django.urls import path
from .views import dashboard, place_list

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('places/', place_list, name='place_list'),
]
