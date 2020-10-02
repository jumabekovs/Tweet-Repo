from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import generics
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .utils import SendMailUtil
from .models import User
from account.serializers import RegisterSerializer, LoginSerializer, UserSerializer, SearchSerializer, FollowSerializer
from tweetapp.permissions import IsProfileOwner
from tweetapp.views import MyPaginations


class RegistrationView(APIView):
    def post(self, request):
        user = request.data
        serializer = RegisterSerializer(data=user)
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        token = RefreshToken.for_user(user).access_token

        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
        email_body = 'Hi, ' + user.username + ' Use link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}
        SendMailUtil.send_email(data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Successfully signed up', status=status.HTTP_201_CREATED)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Successfully logged out', status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]


class MyProfile(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None, pk=None):
        username = self.request.user.username
        query = get_user_model().objects.get(username=username)
        serializer = UserSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)



class SearchViewSet(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = SearchSerializer
    lookup_field = 'username'
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(email__icontains=search)
        return queryset


class FeedsView(APIView):
    permission_classes = [IsAuthenticated, ]
    pagination_class = MyPaginations

    def get(self, request, format=None, pk=None):
        user = self.request.user
        followings = user.followings.all()
        print(followings)
        posts = Post.objects.filter(user__in=followings)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None, username=None):
        to_user = get_user_model().objects.get(username=username)
        from_user = self.request.user
        follow = None
        if from_user != to_user:
            if from_user in to_user.followers.all():
                follow = False
                from_user.followings.remove(to_user)
                to_user.followers.remove(from_user)

            else:
                follow = True
                from_user.followings.add(to_user)
                to_user.followers.add(from_user)
        else:
            raise Exception('You cant follow yourself')
        context = {'follow': follow}
        return Response(context)


class GetFollowersView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        username = self.kwargs['username']
        queryset = get_user_model().objects.get(username=username).followers.all()
        return queryset


class GetFollowingsView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        username = self.kwargs['username']
        queryset = get_user_model().objects.get(username=username).followings.all()
        return queryset