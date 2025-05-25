from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import (
    ServiceProviderProfile,
    ServiceRecipientProfile,
    AdminProfile,
    SupportProfile,
    OwnerProfile,
)
from .serializers import (
    ServiceProviderProfileSerializer,
    ServiceRecipientProfileSerializer,
    AdminProfileSerializer,
    SupportProfileSerializer,
    OwnerProfileSerializer,
)



class ServiceProviderProfileViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    lookup_field = 'user__username'


    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            queryset = ServiceProviderProfile.objects.all()
            serializer = ServiceProviderProfileSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "شما اجازه مشاهده این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )


    def retrieve(self, request, user__username, *args, **kwargs):
        if request.user.is_staff or request.user.username == user__username:
            profile = get_object_or_404(ServiceProviderProfile, user__username=user__username)
            serializer = ServiceProviderProfileSerializer(profile)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "شما اجازه مشاهده این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )


    def update(self, request, user__username, *args, **kwargs):
        if request.user.is_staff or request.user.username == user__username:
            profile = get_object_or_404(ServiceProviderProfile, user__username=user__username)
            serializer = ServiceProviderProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "شما اجازه ویرایش این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )


class ServiceRecipientProfileViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    lookup_field = 'user__username'


    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            queryset = ServiceRecipientProfile.objects.all()
            serializer = ServiceRecipientProfileSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "شما اجازه مشاهده این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )


    def retrieve(self, request, user__username, *args, **kwargs):
        if request.user.is_staff or request.user.username == user__username:
            profile = get_object_or_404(ServiceRecipientProfile, user__username=user__username)
            serializer = ServiceRecipientProfileSerializer(profile)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "شما اجازه مشاهده این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )


    def update(self, request, user__username, *args, **kwargs):
        if request.user.is_staff or request.user.username == user__username:
            profile = get_object_or_404(ServiceRecipientProfile, user__username=user__username)
            serializer = ServiceRecipientProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "شما اجازه ویرایش این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )


class AdminProfileViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    lookup_field = 'user__username'


    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            queryset = AdminProfile.objects.all()
            serializer = AdminProfileSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "شما اجازه مشاهده این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )


    def retrieve(self, request, user__username, *args, **kwargs):
        if request.user.is_staff or request.user.username == user__username:
            profile = get_object_or_404(AdminProfile, user__username=user__username)
            serializer = AdminProfileSerializer(profile)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "شما اجازه مشاهده این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )


    def update(self, request, user__username, *args, **kwargs):
        if request.user.is_staff or request.user.username == user__username:
            profile = get_object_or_404(AdminProfile, user__username=user__username)
            serializer = AdminProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "شما اجازه ویرایش این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )



class SupportProfileViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    lookup_field = 'user__username'

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            queryset = SupportProfile.objects.all()
            serializer = SupportProfileSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "شما اجازه مشاهده این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )


    def retrieve(self, request, user__username, *args, **kwargs):
        if request.user.is_staff or request.user.username == user__username:
            profile = get_object_or_404(SupportProfile, user__username=user__username)
            serializer = SupportProfileSerializer(profile)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "شما اجازه مشاهده این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )


    def update(self, request, user__username, *args, **kwargs):
        if request.user.is_staff or request.user.username == user__username:
            profile = get_object_or_404(SupportProfile, user__username=user__username)
            serializer = SupportProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "شما اجازه ویرایش این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )
        


class OwnerProfileViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    lookup_field = 'user__username'

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            queryset = OwnerProfile.objects.all()
            serializer = OwnerProfileSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "شما اجازه مشاهده این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )


    def retrieve(self, request, user__username, *args, **kwargs):
        if request.user.is_staff or request.user.username == user__username:
            profile = get_object_or_404(OwnerProfile, user__username=user__username)
            serializer = OwnerProfileSerializer(profile)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "شما اجازه مشاهده این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )


    def update(self, request, user__username, *args, **kwargs):
        if request.user.is_staff or request.user.username == user__username:
            profile = get_object_or_404(OwnerProfile, user__username=user__username)
            serializer = OwnerProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "شما اجازه ویرایش این محتوا را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )
