from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from airplain_app.serializers import RegisterSerializer, UserSerializer


# Create your views here.


@api_view(['POST'])
def sign_up(request):
    serializer = RegisterSerializer(data=request.data, many=False)
    if serializer.is_valid(raise_exception=True):
        new_user = serializer.create(serializer.validated_data)
        return Response(data=UserSerializer(instance=new_user, many=False).data)