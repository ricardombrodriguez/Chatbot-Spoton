"""spoton URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('/', views.main_page),
    path('flights', views.get_flights),
    path('flight', views.get_flight),
    path('city', views.get_city),
    path('flights_by_arrival', views.get_flights_by_arrival),
    path('flights_by_departure', views.get_flights_by_departure),
    path('flights_by_departure_arrival', views.get_flights_by_arr_dep),
    path('airports', views.get_airports),
]
