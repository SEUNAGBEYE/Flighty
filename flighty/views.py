"""Homepage view"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes((AllowAny, ))
def index(request): #pylint: disable=unused-arguments, bad-option-value
    """Handles /api/v1 request

        Args:
            request (request object): Django request object
        Returns:
            JSON: Welcome to Flighty
    """

    content = {'message': 'Welcome to Fligty'}
    return Response(content)
