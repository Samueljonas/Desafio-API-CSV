from django.urls import path
from . import views

#logica das paginas
urlpatterns = [
    path('', views.home, name ='home'),
    path('states/', views.state_list, name='state_list'),
    path('cities/', views.city_list, name='city_list', ),
    path('districts/', views.district_list, name='district_list'),
    path('companies/', views.company_list, name='company_list')
]

