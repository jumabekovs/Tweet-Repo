from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegistrationView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('users/search/', views.SearchViewSet.as_view()),
    path('profile/', MyProfile.as_view()),
    path('feeds/', FeedsView.as_view()),
    path('profile/<str:username>/', ProfileView.as_view()),
    path('profile/<str:username>/followers/', GetFollowersView.as_view(), name='followers'),
    path('profile/<str:username>/followings/', GetFollowingsView.as_view(), name='followings'),
    path('follow/<str:username>/', FollowUserView.as_view()),
]