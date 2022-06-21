from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET', 'HEAD'])
def api_root(request, format=None):
    return Response({
        'company departments':
            reverse('department-list', request=request, format=format),
        'employee list':
            reverse('employee-list', request=request, format=format),
        'projects list':
            reverse('project-list', request=request, format=format),
        'current user by token':
            reverse('employee-me', request=request, format=format),
        'auth token for user (only POST method)':
            reverse('login', request=request, format=format),
    })
