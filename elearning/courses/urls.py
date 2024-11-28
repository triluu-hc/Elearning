# courses/urls.py
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from rest_framework_nested import routers
from .views import (
    SubjectViewSet,
    CourseViewSet,
    ModuleViewSet,
    ContentViewSet,
    TextContentViewSet,
    VideoContentViewSet,
)

# Main router
router = routers.DefaultRouter()
router.register(r'subjects', SubjectViewSet, basename='subject')

# Nested routers
subjects_router = routers.NestedDefaultRouter(router, r'subjects', lookup='subject')
subjects_router.register(r'courses', CourseViewSet, basename='subject-courses')

courses_router = routers.NestedDefaultRouter(subjects_router, r'courses', lookup='course')
courses_router.register(r'modules', ModuleViewSet, basename='course-modules')

modules_router = routers.NestedDefaultRouter(courses_router, r'modules', lookup='module')

# Register specific content routes before the general 'contents' route
modules_router.register(r'textcontents', TextContentViewSet, basename='module-textcontents')
modules_router.register(r'videocontents', VideoContentViewSet, basename='module-videocontents')
modules_router.register(r'contents', ContentViewSet, basename='module-contents')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(subjects_router.urls)),
    path('', include(courses_router.urls)),
    path('', include(modules_router.urls)),
]
