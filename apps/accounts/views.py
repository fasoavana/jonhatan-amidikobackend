from django.shortcuts import render
from django.contrib.auth import get_user_model

from django.db import transaction

# Create your views here.

from rest_framework import generics, permissions
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


from .permissions import IsAdmin, IsAdminOrModerator
#from .serializers import RegisterSerializer, LoginSerializer, AdminUserSerializer, AdminUserStatusSerializer
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    AdminUserSerializer,
    AdminUserStatusSerializer,
    CustomTokenRefreshSerializer,
    AdminUserRoleSerializer,
)

from .choices import UserRole, UserStatus

User = get_user_model()

class RegisterThrottle(AnonRateThrottle):
    scope = "register"


#class RegisterView(generics.CreateAPIView):
#    serializer_class = RegisterSerializer
#    permission_classes = [permissions.AllowAny]
#    throttle_classes = [RegisterThrottle]

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
            "status": user.status,
        })

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

# Mi afficher liste user reetra
class AdminUserListView(generics.ListAPIView):
    serializer_class = AdminUserSerializer
    #permission_classes = [IsAdmin]
    #permission_classes = [IsAdminOrModerator]

    def get_queryset(self):
        return User.objects.all().order_by("-created_at")

# Mijery liste user specifique via ID
class AdminUserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdmin]

# Mijery status an user (active, suspended, delete) côté admin
# Change le status des utilisateurs 
class AdminUserStatusView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserStatusSerializer
    permission_classes = [IsAdmin]
    #permission_classes = [IsAdminOrModerator]

    def update(self, request, *args, **kwargs):
        user = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data["status"]

        user.status = new_status

        if new_status == "active":
            user.is_active = True
        elif new_status == "suspended":
            user.is_active = True
        elif new_status == "deleted":
            user.is_active = False

        user.save()

        return Response({
            "message": "Statut de l'utilisateur mis à jour.",
            "user": AdminUserSerializer(user).data,
        })

# vérifie que le compte est toujours actif avant d'accepter le renouvellement du token.
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


# Ancien protection compte admin au changement de role
# vue accessible uniquement aux administrateurs. vue empêche un administrateur de modifier son propre rôle
#############################################################
#class AdminUserRoleView(generics.UpdateAPIView):
#    queryset = User.objects.all()
#    serializer_class = AdminUserRoleSerializer
#    permission_classes = [IsAdmin]

#    def update(self, request, *args, **kwargs):
#        user = self.get_object()

#        # Empêcher un administrateur de modifier son propre rôle.
#        if user.id == request.user.id:
#            return Response(
#                {
#                    "detail": "Vous ne pouvez pas modifier votre propre rôle."
#                },
#                status=400,
#            )

#        serializer = self.get_serializer(data=request.data)
#        serializer.is_valid(raise_exception=True)

#        user.role = serializer.validated_data["role"]
#        user.save(update_fields=["role"])

#        return Response({
#            "message": "Rôle de l'utilisateur mis à jour.",
#            "user": AdminUserSerializer(user).data,
#        })
######################################################
# Protection du dernier compte admin dans le cas où il n'y aura plu de compte admin
class AdminUserRoleView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserRoleSerializer
    permission_classes = [IsAdmin]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_role = serializer.validated_data["role"]

        with transaction.atomic():
            user = self.get_object()

            # Empêcher un administrateur de modifier son propre rôle.
            if user.id == request.user.id:
                return Response(
                    {
                        "detail": "Vous ne pouvez pas modifier votre propre rôle."
                    },
                    status=400,
                )

            # Verrouiller les administrateurs actifs pendant la vérification.
            active_admin_ids = list(
                User.objects.select_for_update()
                .filter(
                    role=UserRole.ADMIN,
                    status=UserStatus.ACTIVE,
                    is_active=True,
                )
                .values_list("id", flat=True)
            )

            # Empêcher la rétrogradation du dernier administrateur actif.
            if (
                user.id in active_admin_ids
                and new_role != UserRole.ADMIN
                and len(active_admin_ids) <= 1
            ):
                return Response(
                    {
                        "detail": "Impossible de retirer le rôle du dernier administrateur actif."
                    },
                    status=400,
                )

            user.role = new_role
            user.save(update_fields=["role"])

        return Response({
            "message": "Rôle de l'utilisateur mis à jour.",
            "user": AdminUserSerializer(user).data,
        })
