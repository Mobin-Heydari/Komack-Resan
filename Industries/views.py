from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import IndustryCategory, Industry
from .serializers import IndustryCategorySerializer, IndustrySerializer




class IndustryCategoryViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        queryset = IndustryCategory.objects.all()
        serializer = IndustryCategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug, *args, **kwargs):
        category = get_object_or_404(IndustryCategory, slug=slug)
        serializer = IndustryCategorySerializer(category)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.user.is_staff:
            serializer = IndustryCategorySerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "شما اجازه ایجاد این محتوا را ندارید."},
                status=status.HTTP_403_FORBIDDEN
            )

    def update(self, request, slug, *args, **kwargs):
        if request.user.is_staff:
            category = get_object_or_404(IndustryCategory, slug=slug)
            serializer = IndustryCategorySerializer(category, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "شما اجازه ویرایش این محتوا را ندارید."},
                status=status.HTTP_403_FORBIDDEN
            )

    def destroy(self, request, slug, *args, **kwargs):
        if request.user.is_staff:
            category = get_object_or_404(IndustryCategory, slug=slug)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"error": "شما اجازه حذف این محتوا را ندارید."},
                status=status.HTTP_403_FORBIDDEN
            )


class IndustryViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        queryset = Industry.objects.all()
        serializer = IndustrySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug, *args, **kwargs):
        industry = get_object_or_404(Industry, slug=slug)
        serializer = IndustrySerializer(industry)
        return Response(serializer.data)

    def create(self, request, category_slug, *args, **kwargs):
        if request.user.is_staff:
            category = get_object_or_404(IndustryCategory, slug=category_slug)
            serializer = IndustrySerializer(
                data=request.data,
                context={'request': request, 'category_slug': category.slug}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "شما اجازه ایجاد این محتوا را ندارید."},
                status=status.HTTP_403_FORBIDDEN
            )

    def update(self, request, slug, category_slug=None, *args, **kwargs):
        if request.user.is_staff:
            industry = get_object_or_404(Industry, slug=slug)
            
            category = industry.category
            
            if category_slug:
                category = get_object_or_404(IndustryCategory, slug=category_slug)

            serializer = IndustrySerializer(
                industry, 
                data=request.data, 
                context={'request': request, 'category_slug': category.slug}
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "شما اجازه ویرایش این محتوا را ندارید."},
                status=status.HTTP_403_FORBIDDEN
            )


    def destroy(self, request, slug, *args, **kwargs):
        if request.user.is_staff:
            industry = get_object_or_404(Industry, slug=slug)
            industry.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"error": "شما اجازه حذف این محتوا را ندارید."},
                status=status.HTTP_403_FORBIDDEN
            )
            
