from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class HealthCheckView(APIView):
    """
    A simple API view for health checking.
    Always returns a 200 OK response.
    """

    def get(self, request, *args, **kwargs):
        return Response({"status": "healthy"}, status=status.HTTP_200_OK)
