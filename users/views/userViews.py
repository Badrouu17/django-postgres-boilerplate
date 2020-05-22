from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers import UserSerializer
from users.models import User
from ..sql import getUserWithId, getUserWithEmail
from ..abort import abort
# Create your views here.


@api_view(["GET"])
def hey(req):
    # return abort("try later")
    users = User.objects.raw(getUserWithEmail("user1@gmail.com"))
    ready = UserSerializer(users, many=True)
    print("📌", ready.data)

    return Response(ready.data)


def uploadToCloud(req):
    pass


def savePhotoInDb(req, url):
    pass


@api_view(["POST"])
def uploadPhotos(req):
    pass


@api_view(["PATCH"])
def updateMe(req):
    pass


@api_view(["PATCH"])
def updatePassword(req):
    pass


@api_view(["GET"])
def getMe(req):
    pass


@api_view(["DELETE"])
def deleteMe(req):
    pass
