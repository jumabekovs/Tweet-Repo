from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Post, Comment, Tag, Follow
from tweetapp import services as likes_services

User = get_user_model()


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('user',)

    def create(self, validate_data):
        user_follow = validate_data.get('user')
        user_following = self.context['request'].user

        if Follow.objects.filter(user=user_follow, follower=user_following).exists():
            message = 'You are already following'
            raise serializers.ValidationError(message)
        elif user_following.id == user_follow.id:
            message = 'You can not follow yourself'
            raise serializers.ValidationError(message)
        else:
            follow = Follow.objects.create(
                user=user_follow,
                follower=user_following
            )
            return follow


class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d %b %Y', read_only=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), write_only=True, required=False)

    class Meta:
        model = Comment
        fields = ('text', 'parent', 'created_at', 'id', 'author')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        representation['text'] = instance.text
        return representation


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('title', 'slug')


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    tags = serializers.SlugRelatedField(many=True, queryset=Tag.objects.all(), slug_field='slug')
    is_fan = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('text', 'image', 'created_at', 'id', 'tags', 'total_likes', 'is_fan')

    def get_is_fan(self, obj) -> bool:
       
        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)

    def __get_image_url(self, instance):
        request = self.context.get('request')
        if instance.image:
            url = instance.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author_id'] = request.user.id
        print(validated_data['title'])
        title = validated_data['title'].split()
        print(title)
        for word in title:
            if word.startswith('#'):
                if Tag.objects.filter(tag=word).exists():
                    pass
                else:
                    Tag.objects.create(tag=word)
        print(Tag.objects.all())
        post = Post.objects.create(**validated_data)
        return post

    def to_representation(self, instance):
        if 'comments' not in self.fields:
            self.fields['comments'] = CommentSerializer(instance, many=True)
        representation = super().to_representation(instance)
        representation['text'] = instance.text
        representation['author'] = instance.author.email
        representation['image'] = self.__get_image_url(instance)
        representation['likes'] = instance.likes.all().count()
        return representation


class CommentReplySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d %b %Y', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'author', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.user.username
        return representation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']