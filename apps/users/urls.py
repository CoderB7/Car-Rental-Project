from django.urls import path
from apps.users.api.views import RegistrationView, LogoutView, UserProfileView, LoginView, RefreshTokenView, OTPVerificationView

 
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='sign_up'),
    path('verify/', OTPVerificationView.as_view(), name='verify-otp'),

    path('login/', LoginView.as_view(), name='login'),
    path('login/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path('logout', LogoutView.as_view()), # not ready yet
]
