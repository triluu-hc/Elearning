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

class TextContentViewSet(viewsets.ModelViewSet):
    serializer_class = TextContentSerializer

    def get_queryset(self):
        return TextContent.objects.filter(module_id=self.kwargs['module_pk'])

    def perform_create(self, serializer):
        module = Module.objects.get(pk=self.kwargs['module_pk'])
        serializer.save(module=module)

class VideoContentViewSet(viewsets.ModelViewSet):
    serializer_class = VideoContentSerializer

    def get_queryset(self):
        return VideoContent.objects.filter(module_id=self.kwargs['module_pk'])

    def perform_create(self, serializer):
        module = Module.objects.get(pk=self.kwargs['module_pk'])
        serializer.save(module=module)