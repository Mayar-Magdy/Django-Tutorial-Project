from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from tutorial.quickstart import views



router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet),
router.register(r'UsersApi' , views.UserViewSet_one , basename='UsersApi'),
router.register(r'groupsApi', views.GroupViewSet_One ,  basename='GroupsApi') 

urlpatterns = [
    path("", include(router.urls)), # authentication for the browsable API
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
