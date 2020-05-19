from django.shortcuts import render
from django.http import JsonResponse
from users.models import User
# Create your views here.


def hey(req):
    data = User.objects.all()

    return JsonResponse({"data": "auth"})

    # return JsonResponse({"data": data})
