from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from django.db.utils import IntegrityError
from rest_framework.authtoken.models import Token

from .serializers import (PhoneUserSerializer,
                          PhoneVerificationSerializer,
                          UserProfileSerializer,
                          ReferralSerializer)
from users.models import PhoneUser, PhoneVerification


class UserAuthViewSet(viewsets.ModelViewSet):
    queryset = PhoneUser.objects.all()
    serializer_class = UserProfileSerializer
    http_method_names = ('get', 'post')

    @action(
        methods=['POST'],
        detail=False,
        url_path='get_verify_code'
    )
    def register_phone(self, request):
        serializer = PhoneUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        verification_code = get_random_string(4, '0123456789')
        try:
            PhoneVerification.objects.create(
                phone_number=request.data['phone_number'],
                verification_code=verification_code
            )
        except IntegrityError:
            PhoneVerification.objects.filter(
                phone_number=request.data['phone_number'],
            ).update(
                verification_code=verification_code
            )
        return Response(
            {
                'verification_code': verification_code,
                'user': request.data['phone_number']
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=False,
        url_path='auth'
    )
    def get_phone_verification(self, request):
        serializer = PhoneVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = PhoneUser.objects.filter(
            phone_number=request.data['phone_number']
        )
        if user.exists():
            token, created = Token.objects.get_or_create(user=user.first())
            return Response(
                {'auth_token': str(token)}, status=status.HTTP_200_OK
            )
        invite_token = get_random_string(6)
        new_user = PhoneUser.objects.create(
            phone_number=request.data['phone_number'],
            invite_token=invite_token
        )
        token, created = Token.objects.get_or_create(user=new_user)
        return Response(
            {'auth_token': str(token)}, status=status.HTTP_201_CREATED
        )


class ReferralViewSet(viewsets.ModelViewSet):
    queryset = PhoneUser.objects.all()
    serializer_class = ReferralSerializer
    http_method_names = ['get', 'post']

    @action(
        methods=['POST'],
        detail=False,
        url_path='referral_code'
    )
    def enter_referral_code(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
