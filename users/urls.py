from django.urls import path
from .views import authViews, userViews


# user.before_request(authController.protect)


urlpatterns = [
    # authViews
    path('auth/', authViews.hey),
    path('auth/signup', authViews.hey),
    path('auth/login', authViews.hey),
    path('auth/forgotPassword', authViews.hey),
    path('auth/resetPassword', authViews.hey),
    # userViews
    path('user/', userViews.hey),
    path('user/uploadPhotos', userViews.uploadPhotos),
    path('user/getMe', userViews.getMe),
    path('user/updateMe', userViews.updateMe),
    path('user/updatePassword', userViews.updatePassword),
    path('user/deleteMe', userViews.deleteMe),
]
