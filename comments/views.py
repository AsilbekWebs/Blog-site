from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from interactions.models import Post
from .models import Comment, Like
from .serializer import CommentSerializer




class CommentListCreateAPIView(APIView):


    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        comments = post.comments.all().order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, post_id):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Izoh qoldirish uchun avval tizimga kiring!"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        post = get_object_or_404(Post, pk=post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailAPIView(APIView):


    def put(self, request, pk):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Tahrirlash uchun tizimga kiring!"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        comment = get_object_or_404(Comment, pk=pk)


        if comment.author != request.user:
            return Response(
                {"detail": "Siz faqat o'zingizning izohingizni tahrirlashingiz mumkin!"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "O'chirish uchun tizimga kiring!"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        comment = get_object_or_404(Comment, pk=pk)


        if comment.author != request.user and comment.post.author != request.user:
            return Response(
                {"detail": "Siz ushbu izohni o'chira olmaysiz!"},
                status=status.HTTP_403_FORBIDDEN
            )

        comment.delete()
        return Response(
            {"detail": "Izoh muvaffaqiyatli o'chirildi."},
            status=status.HTTP_200_OK
        )




class LikeToggleAPIView(APIView):

    def post(self, request, post_id):

        if not request.user.is_authenticated:
            return Response(
                {"detail": "Layk bosish uchun tizimga kiring!"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        post = get_object_or_404(Post, pk=post_id)


        if post.author == request.user:
            return Response(
                {"detail": "O'zingizning postingizga layk bosa olmaysiz!"},
                status=status.HTTP_400_BAD_REQUEST
            )


        like_filter = Like.objects.filter(post=post, user=request.user)

        if like_filter.exists():

            like_filter.delete()
            return Response(
                {"detail": "Layk olib tashlandi.", "liked": False},
                status=status.HTTP_200_OK
            )
        else:
            Like.objects.create(post=post, user=request.user)
            return Response(
                {"detail": "Layk bosildi.", "liked": True},
                status=status.HTTP_201_CREATED
            )