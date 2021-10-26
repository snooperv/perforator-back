from rest_framework import generics
from .serializers import *
from .models import User
from .permission import IsOwnerReadOnly
from rest_framework.permissions import IsAuthenticated


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    permission_classes = (IsOwnerReadOnly, )
