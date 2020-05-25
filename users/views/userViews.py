from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..abort import abort
from users.models import User
from ..serializers import UserSerializer
from ..useful.jwt import (checkToken, signToken)
from ..useful.password import (
    changedPasswordAfter, hashPassword, comparePasswords)
from ..sql import getUserWithId, getUserWithEmail, updateResetPassword, updateUserEmail, updateUserName, updatUserPhoto, deleteUser
import time
from cloudinary.utils import cloudinary_url
from cloudinary.uploader import upload

# Create your views here.


def createSendToken(user):
    token = signToken(user["id"])
    # remove password from output
    del user["password"]
    del user["password_changed_at"]
    del user["password_reset_token"]
    del user["password_reset_expires"]

    return Response({"token": token, "user": user}, status=200)


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
    data = req.data
    if "currentPassword" not in data or "newPassword" not in data:
        return abort("please enter the needed data!", 400)

    if not comparePasswords(user["password"], data["currentPassword"]):
        return abort('Your current password is wrong', 401)

    hashed = hashPassword(data["newPassword"])
    nowDate = int(round(time.time() * 1000))

    # 4) update changes to db
    with connection.cursor() as cursor:
        cursor.execute(updateResetPassword(user["id"], hashed, nowDate))

    # send the token
    return createSendToken(user)


@api_view(["GET"])
@protect
def getMe(req, user):
    del user["password"]
    del user["password_changed_at"]
    del user["password_reset_token"]
    del user["password_reset_expires"]
    return Response(user)


@api_view(["PATCH"])
@protect
def updateMe(req, user):
    data = req.data
    if "password" in data:
        return abort('please use updatePassowrd endpoint to update the password.', 400)

    if "email" not in data and "name" not in data:
        return abort('update at least one data.', 400)

    if "email" in data:
        with connection.cursor() as cursor:
            cursor.execute(updateUserEmail(user["id"], data["email"]))
    if "name" in data:
        with connection.cursor() as cursor:
            cursor.execute(updateUserName(user["id"], data["name"]))

    # get the same new user
    result = User.objects.raw(getUserWithId(user["id"]))
    ready = UserSerializer(result, many=True)
    nUser = dict(ready.data[0])
    del nUser["password"]
    del nUser["password_changed_at"]
    del nUser["password_reset_token"]
    del nUser["password_reset_expires"]
    return Response(nUser)


@api_view(["DELETE"])
@protect
def deleteMe(req, user):
    # update changes to db
    with connection.cursor() as cursor:
        cursor.execute(deleteUser(user["id"]))

    return abort("deleted successfully!", 200)


def uploadToCloud(req):
    file_to_upload = req.FILES['file']
    if file_to_upload:
        upload_result = upload(file_to_upload)
        photo_url = cloudinary_url(upload_result['public_id'],
                                   format="jpg",
                                   crop="fill",
                                   width=500,
                                   height=500)
        return photo_url

    return abort('photo couldnt upload to the cloud, try later', 400)


def savePhotoInDb(user, url):
    if url:
        user["photo"] = url[0]
        with connection.cursor() as cursor:
            cursor.execute(updatUserPhoto(user["id"], url[0]))
        return url
    return abort('photo couldnt be saved in the db', 400)


@api_view(["POST"])
@protect
def uploadPhotos(req, user):
    url = uploadToCloud(req)
    savePhotoInDb(user, url)
    return Response({"url": url, "msg": "photo uploeded successfully!"}, status=200)
