
from django.contrib.auth import get_user_model
from rest_framework import serializers

################Ancien gestionnaire jwt
#from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

#nouveau gestionnaire jwt*******renouvelement token personnalisé
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.settings import api_settings


from .choices import UserStatus, UserRole

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        trim_whitespace=False,
        style={"input_type": "password"},
    )

    password_confirm = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "password",
            "password_confirm",
        ]
        read_only_fields = ["id"]

    def validate_email(self, value):
        return value.strip().lower()

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({
                "password_confirm": "Les mots de passe ne correspondent pas."
            })

        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")

        # Le rôle et le statut sont imposés par le backend.
        return User.objects.create_user(
            password=password,
            role="user",
            status="active",
            is_active=True,
            **validated_data,
        )
class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        email = attrs.get("email")

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Email ou mot de passe incorrect."
            )

        if user.status != "active":
            raise serializers.ValidationError(
                "Votre compte n'est pas actif."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "Votre compte est désactivé."
            )

        return super().validate(attrs)


class AdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "role",
            "status",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# Gestion status active, suspended, delete pour l'admin (Verification pour etre exact)
class AdminUserStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=UserStatus.choices
    )



###################### Renouvelement token#################################### 
#-Vérifie le refresh token.
#-Identifie l'utilisateur associé.
#-Consulte son statut dans la base de données.
#-Vérifie que son compte est actif.
#-Autorise le renouvellement uniquement si toutes les conditions sont respectées.
class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])

        user_id = refresh.get(api_settings.USER_ID_CLAIM)

        if not user_id:
            raise serializers.ValidationError(
                "Utilisateur introuvable."
            )

        try:
            user = User.objects.get(
                **{api_settings.USER_ID_FIELD: user_id}
            )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Utilisateur introuvable."
            )

        if user.status != UserStatus.ACTIVE or not user.is_active:
            raise serializers.ValidationError(
                "Votre compte n'est pas actif."
            )

        return super().validate(attrs)


###Limite les roles possible par admin, moderator et user
class AdminUserRoleSerializer(serializers.Serializer):
    role = serializers.ChoiceField(
        choices=UserRole.choices
    )



################### modifications des informations des utilisateurs
class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone",
        ]

    def validate_first_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Le prénom ne peut pas être vide."
            )

        return value

    def validate_last_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Le nom ne peut pas être vide."
            )

        return value

    def validate_phone(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Le numéro de téléphone ne peut pas être vide."
            )

        return value

    def validate(self, attrs):
        allowed_fields = set(self.fields.keys())
        submitted_fields = set(self.initial_data.keys())

        forbidden_fields = submitted_fields - allowed_fields

        if forbidden_fields:
            raise serializers.ValidationError({
                field: "Ce champ ne peut pas être modifié ici."
                for field in forbidden_fields
            })

        return attrs