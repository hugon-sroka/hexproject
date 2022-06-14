from django.shortcuts import render

# Create your views here.
from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import (
UserProfile
)

from images.serializers import ImageSerializer, ImageDetailSerializer

class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageDetailSerializer
    queryset = UserProfile.objects.all()


    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        image = self.get_object()
        serializer = self.get_serializer(image, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == 'list':
            return ImageSerializer
        return self.serializer_class

