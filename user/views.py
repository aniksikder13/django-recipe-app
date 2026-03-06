from rest_framework import generics, permissions
from user.serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserCreateView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [AllowAny]


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user