from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..abort import abort
from users.models import User
from ..serializers import UserSerializer
from ..useful.jwt import (checkToken)
from ..useful.password import (changedPasswordAfter)
from ..sql import getUserWithId, getUserWithEmail
# Create your views here.

# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDYsImlhdCI6MTU5MDIzOTg5ODE3MiwiZXhwIjoxNTk4MDE1ODk4MTcyfQ.c5Un7ZmVnv5GnfQMk5PuadQIDKi3PGQr0D1C2f5-Yo8


def protect(view_func):
    def wrap(req, *args, **kwargs):
        # 1) Getting token and check of it's there
        if "HTTP_AUTHORIZATION" not in req.META:
            return abort("you are not logged in, please login", 401)

        token = req.META["HTTP_AUTHORIZATION"].split(' ')[1]

        # 2) Verification token
        try:
            decoded = checkToken(token)
        except:
            return abort('wrong or expired token.', 401)

        # 3) Check if user still exists
        result = User.objects.raw(getUserWithId(decoded["id"]))
        ready = UserSerializer(result, many=True)

        if len(ready.data) == 0:
            return abort('The user belonging to this token does no longer exist.', 401)

        user = dict(ready.data[0])

        # 4) Check if user changed password after the token was issued
        if changedPasswordAfter(decoded["iat"], user["password_changed_at"]):
            return abort('User recently changed password! Please log in again.', 401)

        # GRANT ACCESS TO PROTECTED ROUTE
        return view_func(req, user, *args, **kwargs)

    return wrap


@api_view(["PATCH"])
@protect
def updatePassword(req, user):
    pass


@api_view(["GET"])
@protect
def getMe(req, user):
    return Response(user)


@api_view(["PATCH"])
@protect
def updateMe(req, user):
    pass


@api_view(["DELETE"])
@protect
def deleteMe(req, user):
    pass


def uploadToCloud(req):
    pass


def savePhotoInDb(req, url):
    pass


@api_view(["POST"])
@protect
def uploadPhotos(req, user):
    pass
