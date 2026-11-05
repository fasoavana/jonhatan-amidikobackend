from rest_framework_simplejwt.authentication import JWTAuthentication

from .choices import UserStatus


class CustomJWTAuthentication(JWTAuthentication):

    def get_user(self, validated_token):
        user = super().get_user(validated_token)

        if user.status != UserStatus.ACTIVE:
            from rest_framework.exceptions import AuthenticationFailed

            raise AuthenticationFailed(
                "Votre compte n'est pas actif."
            )

        if not user.is_active:
            from rest_framework.exceptions import AuthenticationFailed

            raise AuthenticationFailed(
                "Votre compte est désactivé."
            )

        return user