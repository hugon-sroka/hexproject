from django.dispatch.dispatcher import receiver
import json
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.conf import settings
from rest_framework.exceptions import ValidationError

from users.models import Img, UserProfile


#class for user serializer

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Img
        fields = ['img']
        read_only_fields = ['id']


class UserProfileSerializerInput(serializers.ModelSerializer):
    """Serializer for the user object input data"""
    img = ImageSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ['full_name', 'email', 'password', 'is_enterprise', 'is_premium', 'img']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 7}}

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        images_list = validated_data.pop('img')
        user_obj = UserProfile.objects.create(**validated_data)
        for image_list in images_list:
            Img.objects.create(user_obj, **image_list)
        return validated_data


    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)




    def update(self, instance, validated_data):
            password = validated_data.pop('password', None)
            user = super().update(instance, validated_data)

            if password:
                user.set_password(password)
                user.save()
            return user

    def get_images(self, image):
        return ImageSerializer(image.pics.all(), many=True).data


class TokenSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request = self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with given credentials')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs

class UserProfileSerializerOutput(serializers.ModelSerializer):


    class Meta:
        model = get_user_model()
        fields = ('email', 'full_name', 'password', 'list')
        extra_kwargs =  {'password': {'write_only': True, 'min_length': 7}}

    def create(self, validated_data):
            """Create and return a user with encrypted password"""
            user = get_user_model().objects.create_user(**validated_data)
            return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials Passed.')



class ImageDetailSerializer(ImageSerializer):
    class Meta(ImageSerializer.Meta):
        fields = ImageSerializer.Meta.fields + ['image']

class UserImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['full_name', 'image']
        read_only_fields = ['full_name']
        extra_kwargs = {'image': {'required': 'True'}}

class ModelListField(serializers.ListField):
    def to_representation(self, data):
        """
        List of object instances -> List of dicts of primitive datatypes.
        """
        return [self.child.to_representation(item) if item is not None else None for item in data.all()]

class ListingSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)
    class Meta:
        model = UserProfile
        fields = ['id','full_name','email', 'images']

class ImgSerializer(serializers.ModelSerializer):

    class Meta:
        model = Img
        fields = '__all__'





# class PremiumCustomRegistrationSerializer(RegisterSerializer):
#     fullname_pm = serializers.PrimaryKeyRelatedField(read_only=True, )  # by default allow_null = False
#     email = serializers.EmailField(required=True)
#     image = serializers.ImageField(required=True)
#
#     def get_cleaned_data(self):
#         data = super(PremiumCustomRegistrationSerializer, self).get_cleaned_data()
#         extra_data = {
#             'fullname_pm': self.validated_data.get('fullname_en', ''),
#             'email': self.validated_data.get('email', ''),
#             'image': self.validated_data.get('image', ''),
#         }
#         data.update(extra_data)
#         return data
#
#     def save(self, request):
#         user = super(PremiumCustomRegistrationSerializer, self).save(request)
#         user.is_premium = True
#         user.save()
#         fullname_pm = Premium(premium=user, email=self.cleaned_data.get('email'),
#                             image=self.cleaned_data.get('image'))
#         fullname_pm.save()
#         return user
#
#
# class BasicCustomRegistrationSerializer(RegisterSerializer):
#     fullname_bs = serializers.PrimaryKeyRelatedField(read_only=True, )  # by default allow_null = False
#     email = serializers.EmailField(required=True)
#     image = serializers.ImageField(required=True)
#
#     def get_cleaned_data(self):
#         data = super(BasicCustomRegistrationSerializer, self).get_cleaned_data()
#         extra_data = {
#             'fullname_bs': self.validated_data.get('fullname_bs', ''),
#             'email': self.validated_data.get('email', ''),
#             'image': self.validated_data.get('image', ''),
#         }
#         data.update(extra_data)
#         return data
#
#     def save(self, request):
#         user = super(BasicCustomRegistrationSerializer, self).save(request)
#         user.is_basic = True
#         user.save()
#         fullname_bs = Basic(basic=user, email=self.cleaned_data.get('email'),
#                         image=self.cleaned_data.get('image'))
#         fullname_bs.save()
#         return user
#
# class EnterpriseCustomRegistrationSerializer(RegisterSerializer):
#     def get_cleaned_data(self):
#         data = super(EnterpriseCustomRegistrationSerializer, self).get_cleaned_data()
#         extra_data = {
#             'fullname_en': self.validated_data.get('fullname_en', ''),
#             'email': self.validated_data.get('email', ''),
#             'image': self.validated_data.get('image', ''),
#         }
#         data.update(extra_data)
#         return data
#
#     def save(self, request):
#         user = super(EnterpriseCustomRegistrationSerializer, self).save(request)
#         user.is_enterprise = True
#         user.save()
#         fullname_en = Enterprise(enterprise=user, email=self.cleaned_data.get('email'),
#                         image=self.cleaned_data.get('image'))
#         fullname_en.save()
#         return user

    class UserDetailsSerializer(serializers.ModelSerializer):
        """
        User model w/o password
        """

        class Meta:
            model = UserProfile
            fields = ('pk', 'full_name', 'email', 'image', 'result')
            read_only_fields = ('email',)


