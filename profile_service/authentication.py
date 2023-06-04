import types
from typing import Tuple

import jwt
from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import APIException
from rest_framework import status


class JWTAuthenticationException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = dict()

    def __init__(self, context, status_code=None, detail=None):
        self.default_detail['msg'] = context['msg']
        self.detail = detail or self.default_detail
        self.status_code = status_code or self.status_code

    def get_response(self):
        return self.detail, self.status_code


class JWTAuthentication(BaseAuthentication):
    @staticmethod
    def extract_user_id(access_token: str) -> Tuple:
        try:
            payload = jwt.decode(
                access_token,
                settings.JWT_AUTHENTICATION_KEY,
                settings.JWT_AUTHENTICATION_ALGORITHMS
            )
        except jwt.ExpiredSignatureError:
            return None, _('access token expired')

        except (jwt.InvalidSignatureError, jwt.InvalidTokenError):
            return None, _('invalid token')

        return payload['uid'], None

    def authenticate(self, request):
        try:
            access_token = get_authorization_header(request).split()[1]
        except (AttributeError, IndexError):
            return None

        if not access_token:
            raise JWTAuthenticationException(
                {'msg': _('token not provided or authorization header has invalid structure')}
            )

        user_id, error_message = self.extract_user_id(access_token=access_token)
        if user_id:
            user = types.SimpleNamespace(is_authenticated=True)
            setattr(user, 'id', user_id)
            return user, None

        raise JWTAuthenticationException({'msg': error_message})
