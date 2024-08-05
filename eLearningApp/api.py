# Import necessary modules
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view,action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from .models import *
from .serializers import *

    
@api_view(['GET', 'POST', 'DELETE'])

def user(request, pk=None):
    """
    List all users.
    ---
    operationId: manageUsers
    """
    
    if request.method == 'GET':
        if pk is not None:
            user_instance = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(user_instance)
            return Response(serializer.data)
        else:
            return Response({"detail": "pk is required for GET request"}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        
        data = request.data
        
        # Remove institution from data if it exists and save it for later use
        institution = data.pop('institution', None)
        
        data['username'] = data['email']
        user_serializer = UserSerializer(data=data)
        # app_serializer = AppUserSerializer(AppUser, data=data)
        
        if user_serializer.is_valid():
           
            user = get_user_model().objects.create_user( 
                email=user_serializer.validated_data['email'],
                password=data['password'],
                first_name=user_serializer.validated_data['first_name'],
                last_name=user_serializer.validated_data['last_name'],
                username=user_serializer.validated_data['email']
            )
            
            institution_id = Institution.objects.get(name=institution).id
            app_user_data = {
                    'user': user.id,
                    'institution': institution_id
                }
            app_user_serializer = AppUserSerializer(data=app_user_data)
            if app_user_serializer.is_valid():
                app_user_serializer.save()
            else:
                return Response(app_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if pk is not None:
            user = User.objects.get(pk=pk)
            app_user = AppUser.objects.get(user=user)
            app_user.delete()
            user.delete()
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "pk is required for DELETE request"}, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET'])
def users(request):
    """
    List all users.
    ---
    operationId: listAllUsers
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
