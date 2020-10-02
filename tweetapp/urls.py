from django.urls import path

from . import views

urlpatterns = [
    path('addcomment/<int:pk>/', AddCommentView.as_view()),
    path('deletecomment/<int:pk>/', DeleteCommentView.as_view()),
    path('comments/<int:post_id>/', GetComments.as_view()),
    path('like/<int:post_id>/', LikeAndUnlike.as_view()),
    path('likedme/<int:post_id>/', LikedMe.as_view()),
    path('hashtags/', GetHashtagsView.as_view()),
    path('followers/', FollowerList.as_view()),
]




