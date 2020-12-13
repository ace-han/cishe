from django.urls import include, path
from rest_framework.routers import DefaultRouter

from cishe.api.fev1.comment.views import CommentViewSet


router = DefaultRouter()

router.register("comments", CommentViewSet, "comment")


urlpatterns = [
    path("", include(router.urls, "")),
]
