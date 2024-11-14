from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, ModuleViewSet, ContentViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

# Custom URL patterns for nested relationships
module_list = ModuleViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

module_detail = ModuleViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

content_list = ContentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})


urlpatterns = [
    path('', include(router.urls)),
    # Nested URLs for Modules under Courses
    path('courses/<int:course_pk>/modules/', module_list, name='module-list'),
    path('courses/<int:course_pk>/modules/<int:pk>/', module_detail, name='module-detail'),

    # Nested URLs for Text Content under Modules
    path('courses/<int:course_pk>/modules/<int:module_pk>/contents/', content_list, name='module-contents'),
    
]
