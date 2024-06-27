"""
URL configuration for medicine_guide project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from website.views import diseasesClasses, search, search_disease_by_symptoms, calculate_bmi, calculator_child_height, calculate_meldna, term_detail_view
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', diseasesClasses, name='home'),
    path("search/", search, name = "search"),
    path("search_disease_by_symptoms/", search_disease_by_symptoms, name="search_disease_by_symptoms"),
    path("calculate_bmi/", calculate_bmi, name="calculate_bmi"),
    path("calculate_child_height/", calculator_child_height, name="calculator_child_height"),
    path('calculate_meldna/', calculate_meldna, name="calculate_meldna"),
    path('terms/<str:term_name>', term_detail_view, name="term_detail_view")
    #path("get_all_symptoms/", get_all_symptoms, name="get_all_symptoms"),

]
