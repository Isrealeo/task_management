from django.urls import path
from .views import LoginView, RegisterView, UserViewSet

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name='register'),
    path("users/", UserViewSet.as_view({'get': 'list'}), name="user-list"),
]
