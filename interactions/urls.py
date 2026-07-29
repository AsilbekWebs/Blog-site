from django.urls import path
from .views import PostListCreateAPIView, PostDetailAPIView

urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(), name='comments-list-create'),
    path('posts/<int:pk>/', PostDetailAPIView.as_view(), name='comments-detail-update-delete'),
]