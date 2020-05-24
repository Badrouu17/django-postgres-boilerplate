from django.urls import path
from .views import authViews, userViews


# user.before_request(authController.protect)


urlpatterns = [
    # authViews
    path('auth/signup', authViews.signup),
    path('auth/login', authViews.login),
    path('auth/forgotPassword', authViews.forgotPassword),
    path('auth/resetPassword/<token>', authViews.resetPassword),
    # userViews
    path('user/getMe', userViews.getMe),
    path('user/updateMe', userViews.updateMe),
    path('user/updatePassword', userViews.updatePassword),
    path('user/uploadPhotos', userViews.uploadPhotos),
    path('user/deleteMe', userViews.deleteMe),
]
