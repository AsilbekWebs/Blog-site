from django.urls import path
from .views import CommentListCreateAPIView, CommentDetailAPIView, LikeToggleAPIView

urlpatterns = [
    path('posts/<int:post_id>/comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),


    path('posts/<int:post_id>/like/', LikeToggleAPIView.as_view(), name='like-toggle'),
]