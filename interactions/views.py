from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Post
from .serializer import PostSerializer



class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100



class PostListCreateAPIView(APIView):

    def get(self, request):
        posts = Post.objects.all().prefetch_related('comments', 'likes').order_by('-created_at')


        search_query = request.query_params.get('search', None)
        if search_query:
            posts = posts.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(author__username__icontains=search_query)
            )


        author_id = request.query_params.get('author', None)
        if author_id:
            posts = posts.filter(author_id=author_id)

        
        paginator = CustomPagination()
        paginated_posts = paginator.paginate_queryset(posts, request)

        if paginated_posts is not None:
            serializer = PostSerializer(paginated_posts, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Post yaratish uchun tizimga kiring!"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if post.author != request.user:
            return Response(
                {"detail": "Siz faqat o'zingizning postingizni tahrirlashingiz mumkin!"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if post.author != request.user:
            return Response(
                {"detail": "Siz faqat o'zingizning postingizni o'chira olasiz!"},
                status=status.HTTP_403_FORBIDDEN
            )

        post.delete()
        return Response(
            {"detail": "Post muvaffaqiyatli o'chirildi."},
            status=status.HTTP_200_OK
        )