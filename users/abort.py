from rest_framework.response import Response


def abort(msg, code=500):
    return Response({"message": msg, "status": code}, status=code)
