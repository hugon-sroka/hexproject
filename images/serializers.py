from rest_framework import serializers
from users.models import Img, UserProfile


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Img

        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': True}}


class ImageDetailSerializer(ImageSerializer):

    class Meta(ImageSerializer.Meta):
        fields = ImageSerializer.Meta.fields + ['image']


