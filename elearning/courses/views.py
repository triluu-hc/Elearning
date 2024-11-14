from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated
from .models import Course, Module, TextContent, VideoContent
from .serializers import (CourseSerializer, ModuleSerializer, TextContentSerializer, VideoContentSerializer)
from rest_framework.response import Response
from rest_framework.decorators import action
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save()
    def perform_update(self, serializer):
        # Save module with proper course relation
        serializer.save()
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        id = instance.id
        self.perform_destroy(instance)
        return Response({"message": f"Course with id {id} deleted successfully"}, status=status.HTTP_200_OK)

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    def get_queryset(self):
        return Module.objects.filter(course_id=self.kwargs['course_pk'])

    def perform_create(self, serializer):
        course = Course.objects.get(pk=self.kwargs['course_pk'])
        serializer.save(course=course)

    def perform_update(self, serializer):
        # Save module with proper course relation
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        id = instance.id
        self.perform_destroy(instance)
        return Response({"message": f"Module with id {id} deleted successfully"}, status=status.HTTP_200_OK)


class ContentViewSet(viewsets.ViewSet):
    def list(self, request, course_pk=None, module_pk=None):
        # Retrieve all contents (text and video) for a specific module
        text_contents = TextContent.objects.filter(module_id=module_pk)
        video_contents = VideoContent.objects.filter(module_id=module_pk)

        text_serializer = TextContentSerializer(text_contents, many=True)
        video_serializer = VideoContentSerializer(video_contents, many=True)

        return Response(text_serializer.data + video_serializer.data)

    def create(self, request, course_pk=None, module_pk=None):
        # Determine content type in body request and use appropriate serializer
        content_type = request.data.get('content_type')
        module = Module.objects.get(pk=module_pk)

        if content_type == 'text':
            serializer = TextContentSerializer(data=request.data)
        elif content_type == 'video':
            serializer = VideoContentSerializer(data=request.data)
        else:
            return Response({"error": "Invalid content_type. Use 'text' or 'video'."}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save(module=module)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
