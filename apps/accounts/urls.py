
from django.urls import path

#from rest_framework_simplejwt.views import (
#    TokenObtainPairView,
#    TokenRefreshView,
#)
from rest_framework_simplejwt.views import TokenObtainPairView

#from .views import MeView, RegisterView, LoginView, AdminUserListView, AdminUserDetailView
from .views import (
    LoginView,
    MeView,
    RegisterView,
    AdminUserListView,
    AdminUserDetailView,
    AdminUserStatusView,
    AdminUserRoleView,
    CustomTokenRefreshView,
)


app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),

    path("login/", LoginView.as_view(), name="login"),

    #path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),

    path("me/", MeView.as_view(), name="me"),

    path("admin/users/", AdminUserListView.as_view(), name="admin_users"),

    path("admin/users/<int:pk>/", AdminUserDetailView.as_view(), name="admin_user_detail"),

    path("admin/users/<int:pk>/status/", AdminUserStatusView.as_view(), name="admin_user_status"), #modification de statut

    path("admin/users/<int:pk>/role/", AdminUserRoleView.as_view(), name="admin_user_role"), #modification de role
]
