from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response

from hatter.serializers import HatOrderSerializer


@api_view(["GET", "POST"])
def healthz(request):
    """
    health endpoint for use in k8s etc
    """
    _ = request  # stop unused request warning
    return Response("alles jut, ne!", status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def order_hat(request) -> Response:
    serializer = HatOrderSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def pact_provider_states(request) -> Response:
    """
    Example Request:

        {
            "consumer": "ColdPerson",
            "state": "cold-person has an account with the hatter",
            "states": [
                "cold-person has an account with the hatter"
            ],
            "params": {}
        }
    """
    state = request.data["state"]

    # Clear previous state data
    User.objects.filter(username="cold-person").delete()

    if state == "cold-person has an account with the hatter":
        # Load credentials from some secret store
        User.objects.create_user(username="cold-person", password="im-a-freezin")
        return Response(status=status.HTTP_200_OK)
    return Response(
        {
            "detail": "unknown fixture",
        },
        status=status.HTTP_400_BAD_REQUEST,
    )
