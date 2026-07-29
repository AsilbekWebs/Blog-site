from rest_framework import serializers
from .models import Post
from comments.serializer import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')


    likes_count = serializers.SerializerMethodField()


    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'author_username',
            'title',
            'content',
            'likes_count',
            'comments',
            'created_at',
            'updated_at'
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()