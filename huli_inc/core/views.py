from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsAdminOrReadOnly, IsSelf
from core.serializers import CustomUserSerializer
from core.tasks import send_confirmation_email
from core.utils import (
    check_activation_token,
    create_activation_link,
    decode_user_id
)


User = get_user_model()


class ListCreateUpdateView(mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.ListModelMixin,
                           # mixins.DestroyModelMixin,  # TODO del
                           viewsets.GenericViewSet):
    pass


class UserViewSet(ListCreateUpdateView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdminOrReadOnly, )


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsSelf, )

    def get_object(self):
        return self.request.user


class UserRegisterView(APIView):
    def __create_user(self, validated_data):
        user = User.objects.create(
            username=validated_data.get('username', ''),
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user

    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = self.__create_user(serializer.validated_data)
            activation_link = create_activation_link(request, user)
            send_confirmation_email.apply_async(
                args=(user.email, activation_link)
            )
            return Response(
                {'Please check your email for activate link '
                 'to confirm and complete the registration.'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class UserActivationView(APIView):
    def get(self, request, user_id64, token):
        try:
            user_id = decode_user_id(user_id64)
        except(TypeError, ValueError, OverflowError):
            return Response({'Activation link is invalid!'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, pk=user_id)
        if check_activation_token(user, token):
            user.is_active = True
            user.save()
            return Response(
                {'Thank you for your email confirmation. '
                 'Now you can login your account.'},
                status=status.HTTP_201_CREATED
            )
        return Response({'Activation link is invalid!'},
                        status=status.HTTP_400_BAD_REQUEST)
