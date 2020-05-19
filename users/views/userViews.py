from django.shortcuts import render
from django.http import JsonResponse
from users.models import User
# Create your views here.


def hey(req):
    data = User.objects.all()

    return JsonResponse({"data": "user"})

    # return JsonResponse({"data": data})


def uploadToCloud(req):
    pass


def savePhotoInDb(req, url):
    pass


def uploadPhotos(req):
    pass


def updateMe(req):
    pass


def updatePassword(req):
    pass


def getMe(req):
    pass


def deleteMe(req):
    pass
