from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..abort import abort
from users.models import User
from ..serializers import UserSerializer

from ..useful.password import (hashPassword, comparePasswords,
                               changedPasswordAfter,
                               createPasswordResetToken, cryptToken)
from ..useful.jwt import (signToken, checkToken)

from ..sql import (insertUser, getUserWithId,
                   getUserWithEmail, getUserByResetToken,
                   updateUserEmail, updateUserName,
                   updateUserPassResetData, updatUserPhoto,
                   updateResetPassword)

from ..useful.mail import Mailer
import time

# Create your views here.


@api_view(["GET"])
def hey(req):
    users = User.objects.raw(getUserWithEmail("user1@gmail.com"))
    ready = UserSerializer(users, many=True)
    print("📌", ready.data)

    return Response(ready.data)


def createSendToken(user):
    token = signToken(user["id"])
    # remove password from output
    del user["password"]
    return Response({"token": token, "user": user}, status=200)


@api_view(["POST"])
def signup(req):
    data = req.data

    if ("email" not in data or "password" not in data or "name" not in data):
        return abort('please provide a name, email and password', 400)

    newUser = {
        "name": data["name"],
        "email": data["email"],
        "password": hashPassword(data["password"])
    }

    # insert the new user
    result = User.objects.raw(insertUser(newUser))
    ready = UserSerializer(result, many=True)

    # get the same new user
    user = dict(ready.data[0])
    return createSendToken(user)


@api_view(["POST"])
def login(req):
    # 1) Check if email and password exist
    data = req.data
    if ("email" not in data or "password" not in data):
        return abort('please provide an email and password', 400)

    # 2) Check if user exists
    result = User.objects.raw(getUserWithEmail(data["email"]))
    ready = UserSerializer(result, many=True)

    if len(ready.data) == 0:
        return abort('no user with this email', 400)

    user = dict(ready.data[0])

    # 3) check password is correct
    if not comparePasswords(user["password"], data["password"]):
        return abort('the password you enterd is wrong, please try again', 400)

    # 4) If everything ok, send token to client
    return createSendToken(user)


@api_view(["POST"])
def forgotPassword(req):
    pass


@api_view(["PATCH"])
def resetPassword(req):
    pass
