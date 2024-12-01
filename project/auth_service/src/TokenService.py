import os
from datetime import timedelta

import jwt
from django.utils import timezone

refresh_secret_key = os.environ.get("REFRESH_TOKEN_SECRET")
access_secret_key = os.environ.get("ACCESS_TOKEN_SECRET")


class TokenService:

    def generate_access_token(username):
        exp = TokenService.create_expiration_date(60 * 24 * 7)
        access_token = jwt.encode(
            {"username": username, "exp": exp}, access_secret_key, algorithm="HS256"
        )
        return access_token, exp

    def generate_refresh_token(username):
        exp = TokenService.create_expiration_date(60 * 24 * 30)
        refresh_token = jwt.encode(
            {"username": username, "exp": exp},
            refresh_secret_key,
            algorithm="HS256",
        )
        return refresh_token, exp

    def create_expiration_date(minutes):
        return timezone.now() + timedelta(minutes=minutes)

    @staticmethod
    def validate_access_token(access_token):
        try:
            decoded_token = jwt.decode(
                access_token, access_secret_key, algorithms=["HS256"]
            )
            return decoded_token["username"]
        except jwt.ExpiredSignatureError:
            return None, "Access token expired"
        except jwt.InvalidTokenError:
            return None, "Invalid access token"

    @staticmethod
    def validate_refresh_token(refresh_token):
        try:
            decoded_token = jwt.decode(
                refresh_token, refresh_secret_key, algorithms=["HS256"]
            )
            return decoded_token["username"]
        except jwt.ExpiredSignatureError:
            return None, "Refresh token expired"
        except jwt.InvalidTokenError:
            return None, "Invalid refresh token"

    def is_mail_token_expired(exp):
        return timezone.now() > exp
