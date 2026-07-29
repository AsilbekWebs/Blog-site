from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdate.as_view(), name='profile-update'),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    path('token/refresh/', TokenRefresh.as_view(), name='token-refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]