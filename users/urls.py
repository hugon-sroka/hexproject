from django.urls import path
from users.views import (UserProfileView,
                         UserDetailView,
                         UserLoginApiView,
                         ManageUserView,
                         CreateUserView,
                         ListImgView,
                         ImageProfileView)




urlpatterns = [
    path('', UserProfileView.as_view(), name='usero'),
    path('users/create/', CreateUserView.as_view(), name='create'),
    path('users/<int:pk>/', UserDetailView.as_view()),
    path('users/login/', UserLoginApiView.as_view(), name='token'),
    path('users/me/', ManageUserView.as_view(), name='me'),
    path('users/list', ListImgView.as_view(), name ='list-img'),
    path('users/image', ImageProfileView.as_view(), name='img')
]
