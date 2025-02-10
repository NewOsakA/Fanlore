from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.CustomLoginView.as_view(), name="login"),
    path("edit/", views.ProfileUpdateView.as_view(), name="profile_edit"),
]
