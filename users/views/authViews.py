from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers import UserSerializer
from users.models import User
from ..sql import getUserWithId, getUserWithEmail
# Create your views here.


@api_view(["GET"])
def hey(req):
    users = User.objects.raw(getUserWithEmail("user1@gmail.com"))
    ready = UserSerializer(users, many=True)
    print("📌", ready.data)

    return Response(ready.data)


@api_view(["POST"])
def signup(req):
    pass


@api_view(["POST"])
def login(req):
    pass


@api_view(["POST"])
def forgotPassword(req):
    pass


@api_view(["PATCH"])
def resetPassword(req):
    pass
