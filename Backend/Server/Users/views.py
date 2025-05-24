from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import User, IdCardInFormation
from .serializers import UserSerializer, IdCardInFormationSerializer




class IdCardViewSet(viewsets.ViewSet):
    def list(self, request):
        if request.user.is_staff:
            queryset = IdCardInFormation.objects.all()
            serializer = IdCardInFormationSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"Massage": "شما دسترسی به اطلاعات کارت ملی را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk):
        instance = get_object_or_404(IdCardInFormation, id=pk)
        if request.user.is_staff or request.user == instance.id_card_info:
            serializer = IdCardInFormationSerializer(instance)
            return Response(serializer.data)
        else:
            return Response({"Massage": "شما دسترسی برای دریافت اطلاعات را ندارید"}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk):
        instance = get_object_or_404(IdCardInFormation, id=pk)
        if request.user.is_staff or instance.id_card_info:
            serializer = IdCardInFormationSerializer(instance, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Message": "شما دسترسی برای به‌روزرسانی اطلاعات را ندارید."}, status=status.HTTP_403_FORBIDDEN)



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
