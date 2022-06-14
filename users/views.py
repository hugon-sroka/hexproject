from django.db.models.expressions import OuterRef
from rest_framework import status
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from knox.models import AuthToken
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework import filters, generics, authentication, permissions
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from .serializers import UserProfileSerializerInput, UserProfileSerializerOutput, \
    TokenSerializer, LoginSerializer, ListingSerializer, ImageSerializer, ImgSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from users.permissions import UpdateOwnProfile
from django.contrib.auth import get_user_model
from users.models import UserProfile, Img
from rest_framework.permissions import IsAdminUser



# Create your views here.


def detail_route(methods, permission_classes):
    pass


class UserProfileView(ListAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UserProfileSerializerInput
    queryset = UserProfile.objects.all().order_by('id')
    permission_classes = (UpdateOwnProfile, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('full_name', 'email', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class ImageProfileView(ListAPIView):
    permission_classes = (UpdateOwnProfile,)
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UserProfileSerializerInput

    def filter_queryset(self, queryset):
        filter_backends = [CategoryFilter]

        if 'geo_route' in self.request.query_params:
            filter_backends = [GeoRouteFilter, CategoryFilter]
        elif 'geo_point' in self.request.query_params:
            filter_backends = [GeoPointFilter, CategoryFilter]

        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, view=self)

        return queryset



class CreateUserView(generics.ListCreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UserProfileSerializerInput
    queryset = UserProfile.objects.prefetch_related('img')

    def create(self, request, *args, **kwargs):
        images_list = request.FILES.getlist('img', None)
        data = {
            "title": request.POST.get('title', None),
            }
        _serializer = self.serializer_class(data=data, context={'documents': images_list})
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)  # NOQA
        else:
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, format=None):
        serializer = UserProfileSerializerInput(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class ListImgView(generics.ListAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ListingSerializer
    queryset = UserProfile.objects.all()


class UserDetailView(RetrieveAPIView):
    serializer_class = UserProfileSerializerInput

    def get_authenticate_header(self, request):
        """
        If a request is unauthenticated, determine the WWW-Authenticate
        header to use for 401 responses, if any.
        """
        authenticators = self.get_authenticators()
        if authenticators:
            return authenticators[0].authenticate_header(request)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)



class TokenView(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = TokenSerializer(data=self.request.data,
                                                 context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)

class UserLoginApiView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializerInput
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user















