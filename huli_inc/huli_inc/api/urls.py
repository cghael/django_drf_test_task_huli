from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from core.views import (
    UserActivationView,
    UserProfileViewSet,
    UserRegisterView,
    UserViewSet
)


router = DefaultRouter()
router.register(
    'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('registration/',
         UserRegisterView.as_view(),
         name='user-registration'),
    path('registration/activate/<user_id64>/<token>',
         UserActivationView.as_view(),
         name='user-activation'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(
        'users/me/',
        UserProfileViewSet.as_view({'get': 'retrieve'}),
        name='user-profile'
    ),
]

urlpatterns += router.urls
