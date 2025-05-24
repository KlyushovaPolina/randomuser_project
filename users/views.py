
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, get_object_or_404, redirect
from .models import User
from .serializers import UserSerializer
import random
import requests

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

@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == 'POST':
        count = int(request.POST.get('count', 0))
        if count > 0:
            url = f'https://randomuser.me/api/?results={count}'
            response = requests.get(url)
            data = response.json()['results']

            for item in data:
                User.objects.create(
                    gender=item['gender'],
                    first_name=item['name']['first'],
                    last_name=item['name']['last'],
                    phone=item['phone'],
                    email=item['email'],
                    location=", ".join([item['location']['city'], item['location']['country']]),
                    picture=item['picture']['thumbnail']
                )
        return redirect('index')

    users = User.objects.all().order_by('-id')
    paginator = Paginator(users, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/index.html', {'page_obj': page_obj})