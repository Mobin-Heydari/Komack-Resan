from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer





class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"Massage": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, username, *args, **kwargs):
        if request.user.is_staff or request.user.username == username:
            queryset = get_object_or_404(User, username=username)
            serializer = self.get_serializer(queryset)
            return Response(serializer.data)
        else:
            return Response({"Massage": "شما اجازه مشاهده این محتوا را ندارید"}, status=status.HTTP_403_FORBIDDEN)
