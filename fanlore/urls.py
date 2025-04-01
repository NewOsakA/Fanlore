from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='content_list'),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/<int:user_id>/", views.ProfileView.as_view(),
         name="friend-profile"),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.SignInView.as_view(), name="signin"),

    # Friend
    path('friends/', views.friend.FriendListView.as_view(), name="friends-list"),
    path("friends/add/<int:user_id>/", views.friend.FriendRequestCreateView.as_view(),
         name="add-friend"),
    path("friends/accept/<int:pk>/", views.friend.FriendRequestAcceptView.as_view(),
         name="accept-friend"),
    path("friends/reject/<int:pk>/", views.friend.FriendRequestRejectView.as_view(),
         name="reject-friend"),
    path("friends/remove/<int:user_id>/", views.friend.RemoveFriendView.as_view(),
         name="remove-friend"),
    path("friends/cancel-request/<int:pk>/",
         views.friend.CancelFriendRequestView.as_view(),
         name="cancel-friend-request"),

    path("profile_edit/", views.ProfileEditView.as_view(),
         name="profile_edit"),
    path('profile/bookmarks/', views.BookmarkedPostsView.as_view(),
         name='bookmarked_post'),
    path('content_edit/<uuid:pk>/', views.ContentUpdateView.as_view(),
         name='content_edit'),
    path('upload/', views.ContentUploadView.as_view(), name='upload_content'),
    path('post/<uuid:pk>/', views.ContentDetailView.as_view(),
         name='view_post'),
    path('delete_content/<uuid:content_id>/',
         views.ContentDeleteView.as_view(), name='content_delete'),

    # Event
    path("event/<int:pk>/", views.event.EventDetailView.as_view(),
         name="event-detail"),
    path("event/<int:event_id>/submit/", views.event.EventSubmitView.as_view(),
         name="event-submit"),
    path("events/", views.event.EventListView.as_view(), name="event-list"),
    path("events/create/", views.event.EventCreateView.as_view(),
         name="event-create"),
    path("events/<int:pk>/edit/", views.event.EventUpdateView.as_view(),
         name="event-edit"),
    path("submission/<int:pk>/toggle-reviewed/",
         views.event.ToggleReviewedView.as_view(),
         name="submission-toggle-reviewed"),
    path("event/<int:event_id>/dashboard/",
         views.event.EventCreatorDashboardView.as_view(),
         name="event-creator-dashboard"),

    path("achievement/give/", views.GiveAchievementView.as_view(),
         name="give-achievement"),
    path('toggle-bookmark/', views.ToggleBookmarkView.as_view(),
         name='toggle_bookmark'),
]
