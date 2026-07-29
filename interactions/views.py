from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Post
from .serializer import PostSerializer



class PostListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
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