from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def home(request):

    data = {
        "project": "COGNIVEX AI",
        "message": "Welcome to Cognivex AI Backend!",
        "status": "Backend is running successfully",
        "version": "1.0"
    }

    return Response(data)


# Create your views here.
