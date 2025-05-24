from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer

@api_view(['GET'])
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return Response(UserSerializer(user).data)