from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='content_list'),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.SignInView.as_view(), name="signin"),
    path("profile_edit/", views.ProfileEditView.as_view(), name="profile_edit"),
    path('upload/', views.ContentUploadView.as_view(), name='upload_content'),
    path('post/<uuid:pk>/', views.ContentDetailView.as_view(), name='view_post'),
    path('delete_content/<uuid:content_id>/', views.ContentDeleteView.as_view(), name='content_delete'),
]
