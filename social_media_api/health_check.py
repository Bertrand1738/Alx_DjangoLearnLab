from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint for AWS Elastic Beanstalk
    """
    return Response({"status": "healthy"}, status=status.HTTP_200_OK)
