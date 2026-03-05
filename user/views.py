from rest_framework import generics
from user.serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny


class UserCreateView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [AllowAny]
