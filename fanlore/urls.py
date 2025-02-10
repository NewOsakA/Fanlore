from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.SignInView.as_view(), name="signin"),
    path("edit/", views.ProfileUpdateView.as_view(), name="profile_edit"),
    path('upload/', views.ContentUploadView.as_view(), name='upload_content'),
]
