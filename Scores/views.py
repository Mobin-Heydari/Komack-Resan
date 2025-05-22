from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import ServiceScore
from .serializers import ServiceScoreSerializer
from .permissions import ServiceScorePermission  # custom permission per our previous discussion





class ServiceScoreViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing ServiceScore records.

    Endpoints:
      - List:       GET /service-scores/
      - Retrieve:   GET /service-scores/<pk>/
      - Create:     POST /service-scores/create/
      - Update:     PUT/PATCH /service-scores/<pk>/update/
      - Destroy:    DELETE /service-scores/<pk>/delete/

    Permissions are enforced so that:
      • Only a Service Recipient (user_type "SC") can create a score for a Service 
        (and only if that Service’s recepient matches the requesting user).
      • Only an Admin (user_type "AD") or the Service’s recipient can update the score.
      • Only an Admin or the Service’s recipient can delete (destroy) the score.
    """
    permission_classes = [ServiceScorePermission]

    def list(self, request):
        queryset = ServiceScore.objects.all()
        serializer = ServiceScoreSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(ServiceScore, pk=pk)
        self.check_object_permissions(request, instance)
        serializer = ServiceScoreSerializer(instance, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = ServiceScoreSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            response_serializer = ServiceScoreSerializer(instance, context={'request': request})
            return Response({
                'message': 'Score created successfully.',
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        instance = get_object_or_404(ServiceScore, pk=pk)
        self.check_object_permissions(request, instance)
        serializer = ServiceScoreSerializer(instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            response_serializer = ServiceScoreSerializer(instance, context={'request': request})
            return Response({
                'message': 'Score updated successfully.',
                'data': response_serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        instance = get_object_or_404(ServiceScore, pk=pk)
        self.check_object_permissions(request, instance)
        # Additional check for destroy: only Admin or Service recipient can delete the score.
        if not (getattr(request.user, 'user_type', None) == "AD" or instance.service.recepient == request.user):
            return Response(
                {"detail": "You do not have permission to delete this score."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()
        return Response(
            {"message": "Score deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
