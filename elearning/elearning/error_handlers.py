# error_handlers.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_bad_request(request, exception):
    return Response({'detail': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

def custom_permission_denied(request, exception):
    return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

def custom_not_found(request, exception):
    return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

def custom_server_error(request):
    return Response({'detail': 'A server error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
