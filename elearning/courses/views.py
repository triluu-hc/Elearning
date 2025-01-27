from rest_framework import viewsets,status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from .models import Subject,Course, Module, Content, TextContent, VideoContent
from .serializers import (SubjectSerializer,CourseSerializer, ModuleSerializer, ContentSerializer, TextContentSerializer, VideoContentSerializer)
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import  get_object_or_404
from .tasks import send_new_course_email
from django.core.cache import cache
from rest_framework.authentication import TokenAuthentication
    
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Subject.objects.filter(subject_id=self.kwargs['subject_pk'])
    def retrieve(self, request, *args, **kwargs):
        cache_key = f"subject_{kwargs['pk']}"
        cached_subject = cache.get(cache_key)

        if cached_subject:
            return Response(cached_subject, status=status.HTTP_200_OK)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = serializer.data

        cache.set(cache_key, response_data, timeout=3600)

        return Response(response_data)

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)
        #add cache here

    def perform_update(self, serializer):
        instance = serializer.save()
        cache_key = f"subject_{instance.id}"
        cache.delete(cache_key)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        subject_id = instance.id
        self.perform_destroy(instance)

        cache_key = f"subject_{subject_id}"
        cache.delete(cache_key)

        return Response({"message": f"Subject with id {subject_id} deleted successfully"}, status=status.HTTP_200_OK)

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(subject_id=self.kwargs['subject_pk'])

    def perform_create(self, serializer):
        subject = Subject.objects.get(pk=self.kwargs['subject_pk'])
        course = serializer.save(subject=subject)
        send_new_course_email.delay(course.id)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        id = instance.id
        self.perform_destroy(instance)
        return Response({"message": f"Course with id {id} deleted successfully"}, status=status.HTTP_200_OK)

class ModuleViewSet(viewsets.ModelViewSet):
    serializer_class = ModuleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Module.objects.filter(course_id=self.kwargs['course_pk'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['course'] = Course.objects.get(pk=self.kwargs['course_pk'])
        return context



class ContentViewSet(viewsets.ModelViewSet):
    serializer_class = ContentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Content.objects.filter(module_id=self.kwargs['module_pk'])

    def perform_create(self, serializer):
        module = Module.objects.get(pk=self.kwargs['module_pk'])
        serializer.save(module=module)


class TextContentViewSet(viewsets.ModelViewSet):
    serializer_class = TextContentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        module_pk = self.kwargs.get('module_pk')
        # Get all TextContent objects linked to the module via the Content model
        return TextContent.objects.filter(
            id__in=Content.objects.filter(
                module_id=module_pk,
                content_type=ContentType.objects.get_for_model(TextContent)
            ).values_list('object_id', flat=True)
        )
    def perform_create(self, serializer):
        text_content = serializer.save()
        module_pk = self.kwargs.get('module_pk')
        module = get_object_or_404(Module, pk=module_pk)
        content_type = ContentType.objects.get_for_model(TextContent)
        Content.objects.create(
            module=module,
            order=Content.objects.filter(module=module).count() + 1,
            content_type=content_type,
            object_id=text_content.id
        )


class VideoContentViewSet(viewsets.ModelViewSet):
    serializer_class = VideoContentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        video_content = serializer.save()
        module_pk = self.kwargs.get('module_pk')
        module = get_object_or_404(Module, pk=module_pk)
        content_type = ContentType.objects.get_for_model(VideoContent)
        Content.objects.create(
            module=module,
            order=Content.objects.filter(module=module).count() + 1,
            content_type=content_type,
            object_id=video_content.id
        )
