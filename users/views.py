from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer
import random

@api_view(['GET'])
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return Response(UserSerializer(user).data)

@api_view(['GET'])
def random_user(request):
    count = User.objects.count()
    if count == 0:
        return Response({"error": "No users in DB"})
    random_index = random.randint(0, count - 1)
    user = User.objects.all()[random_index]
    return Response(UserSerializer(user).data)