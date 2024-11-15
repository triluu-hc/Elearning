from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated
from .models import Subject,Course, Module, Content, TextContent, VideoContent
from .serializers import (SubjectSerializer,CourseSerializer, ModuleSerializer, ContentSerializer, TextContentSerializer, VideoContentSerializer)
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

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
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def contents(self, request, pk=None):
        module = self.get_object()
        contents = module.contents.all()
        serializer = ContentSerializer(contents, many=True, context={'request': request})
        return Response(serializer.data)


class ContentViewSet(viewsets.ViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Content.objects.filter(module__course__owner=user)

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