from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

# from tweetapp.models import Post
# from tweetapp.serializers import PostSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirmation = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirmation')

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email already exist')
        return email

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirmation = validated_data.get('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError('Your passwords did not match, please try again!')
        return validated_data

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        image = validated_data.get('image')
        user = User.objects.create_user(email, password, image)
        user.is_active = True
        user.save()
        # send_activation_email(user.email, user.activation_code)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            print(user)
            if not user:
                msg = _('Unable to log in with this credentials!')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Please provide your "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        validated_data['user'] = user
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'image', 'id', 'followers', 'followings') # should import and add Post from tweetapp

    def to_representation(self, instance):
        # representation = super().to_representation(instance)
        # if instance.followers.all().count() > 0:
        #     followings_object_list = instance.followers.filter(follower=instance)
        #     followings_list = [follow.user.email for follow in followings_object_list]
        #     representation['followings'] = followings_list
        # if instance.followings.all().count() > 0:
        #     followers_object_list = instance.followings.filter(user=instance)
        #     followers_list = [follow.follower.email for follow in followers_object_list]
        #     representation['followers'] = followers_list
        representation = super().to_representation(instance) # short way
        # representation['posts'] = PostSerializer(instance.posts.all(), many=True, context=self.context).data # need to add this
        representation['followers'] = instance.followers.count()
        representation['followings'] = instance.followings.count()

        return representation


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


