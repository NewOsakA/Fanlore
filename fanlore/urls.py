from django.urls import path

from . import views

app_name = 'fanlore'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    ]
