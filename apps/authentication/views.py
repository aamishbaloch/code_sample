from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.serializers import UserSerializer, UserTokenSerializer
from libs.authentication import UserAuthentication
from libs.custom_exceptions import (
    InvalidInputDataException,
    InvalidCredentialsException,
    UserExistsException,
    UserNotAllowedException,
    UserDoesNotExistsException,
    VerificationException,
    InvalidVerificationCodeException)

User = get_user_model()


class RegistrationView(APIView):
    """
    View for registering a new user to your system.

    **Example requests**:

        POST /auth/register/
    """

    @transaction.atomic()
    def post(self, request):
        if not User.is_exists(request.data['email']):
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.generate_code_for_user()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            raise InvalidInputDataException(str(serializer.errors))
        raise UserExistsException()


class LoginView(APIView):
    """
    View for login a user to your system.

    **Example requests**:

        POST /auth/login/
    """
    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(email=email, password=password)
        if user:
            if user.verified and user.active:
                serializer = UserTokenSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise UserNotAllowedException()
        else:
            raise InvalidCredentialsException()


class LogoutView(APIView):
    """
    View for logout a user to your system.

    **Example requests**:

        POST /auth/logout/
    """

    authentication_classes = (UserAuthentication,)

    def post(self, request):
        # any operation want to perform at logout
        return Response({}, status=status.HTTP_200_OK)


class VerificationView(APIView):
    """
    View for verifying a user to your system.

    **Example requests**:

        POST /auth/verify/
    """

    def post(self, request):
        code = request.data.get('code', None)
        email = request.data.get('email', None)

        user = User.objects.filter(email=email).first()

        if user.verification_code:
            if user.verification_code == code:
                user.verified = True
                user.save(update_fields=['verified'])
                return Response({}, status=status.HTTP_200_OK)
        raise InvalidVerificationCodeException()


class ForgotPasswordView(APIView):
    """
    View for creating forgot code of user.

    **Example requests**:

        POST /auth/forgot_password/
    """
    def post(self, request):
        email = request.data.get('email', None)

        try:
            user = User.objects.get(email=email)
            if user.verified:
                code = User.generate_code_for_user(user)
                return Response({}, status=status.HTTP_200_OK)
            raise VerificationException()
        except User.DoesNotExist:
            raise UserDoesNotExistsException()


class ChangePasswordView(APIView):
    """
    View for changing password with code.

    **Example requests**:

        POST /auth/password/change/
    """
    def post(self, request):
        code = request.data.get('code', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        try:
            user = User.objects.get(email=email)
            if user.verified:
                if user.verification_code == code:
                    user.set_password(password)
                    user.save()
                    return Response({}, status=status.HTTP_200_OK)
                raise InvalidVerificationCodeException()
            raise VerificationException()
        except User.DoesNotExist:
            raise UserDoesNotExistsException()
