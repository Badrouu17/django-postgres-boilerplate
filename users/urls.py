from django.urls import path
from .views import authViews, userViews


# user.before_request(authController.protect)


urlpatterns = [
    # authViews
    path('auth/', authViews.hey),
    # userViews
    path('user/', userViews.hey),
    path('user/uploadPhotos', userViews.uploadPhotos),
    path('user/getMe', userViews.getMe),
    path('user/updateMe', userViews.updateMe),
    path('user/updatePassword', userViews.updatePassword),
    path('user/deleteMe', userViews.deleteMe),
]
