from rest_framework import generics, status, viewsets, mixins, permissions
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

# from account.models import User
# from .mixins import LikedMixin # misused
from .models import Post, Comment, Tag, Follow
from .permissions import IsPostAuthor
from .serializers import PostSerializer, CommentSerializer, TagSerializer, FollowSerializer, UserSerializer


class MyPaginations(PageNumberPagination):
    page_size = 5


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class TagFilter(filters.FilterSet):
    title = CharFilterInFilter(field_name='tags__title')

    class Meta:
        model = Post
        fields = ('tags',)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsPostAuthor]
    pagination_class = MyPaginations

    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        if self.action in ['create', 'my_tweet']:
            permissions = [IsAuthenticated, ]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthenticated, IsPostAuthor]
        else:
            permissions = []
        return [permission() for permission in permissions]

    @action(detail=False, methods=['get'])
    def my_tweet(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddCommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsPostAuthor]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        if self.action in ['create', 'own']:
            permissions = [IsAuthenticated, ]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthenticated, IsPostAuthor]
        else:
            permissions = []
        return [permission() for permission in permissions]

    @action(detail=False, methods=['get'])
    def my_tweet(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteCommentView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsPostAuthor, ]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class FollowerList(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class LikeAndUnlike(APIView):

    def get(self, request, format=None, post_id=None):
        post = Post.objects.get(pk=post_id)
        user = self.request.user
        if user.is_authenticated:
            if user in post.likes.all():
                like = False
                post.likes.remove(user)
            else:
                like = True
                post.likes.add(user)

        context = {'like': like}
        return Response(context)


class LikedMe(APIView):

    def get(self, request, format=None, post_id=None):
        post = Post.objects.get(pk=post_id)
        likers = post.likes.all()
        serializer = UserSerializer(likers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetComments(APIView):

    def get(self, request, format=None, post_id=None):
        post = Post.objects.get(pk=post_id)
        comments = Comment.objects.filter(post_id=post_id, parent__isnull=True)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetHashtagsView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer