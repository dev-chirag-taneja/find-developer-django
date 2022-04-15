from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from users.models import Profile
from .serializers import RegistrationSerializer, ProfileSerializers 

# Register User
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get profiles   
@api_view()
def profiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializers(profiles, many=True)
    return Response(serializer.data)
    
# Get, Put, Delete profile 
@api_view(['GET', 'PUT', 'DELETE'])  
@permission_classes([IsAuthenticated])
def profile(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    
    if request.method == 'GET':
        serializer = ProfileSerializers(profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProfileSerializers(profile, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if request.user.is_superuser:
            profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            context = {'message':'Permission Denied!'}
            return Response(context, status=status.HTTP_403_FORBIDDEN)  


