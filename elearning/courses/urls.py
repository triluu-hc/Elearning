from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, ModuleViewSet, TextContentViewSet, VideoContentViewSet

# Set up router for all viewsets
router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'modules', ModuleViewSet)
router.register(r'text-content', TextContentViewSet)
router.register(r'video-content', VideoContentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
