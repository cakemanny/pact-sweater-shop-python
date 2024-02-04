from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def healthz(request):
    """
    health endpoint for use in k8s etc
    """
    _ = request  # stop unused request warning
    return Response("alles jut, ne!", status=status.HTTP_200_OK)
