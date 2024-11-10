from django.urls import include, path
from src import views

urlpatterns = [
    path('auth/signin/', views.signin),
    path('auth/signup/', views.signup),
    path('auth/intra/', views.intra),
    path('auth/intra-callback/', views.intraCallback),
    path('auth/signout/', views.signout),
    path('auth/refresh-token/', views.refreshToken),
    path('auth/validate-token/', views.validate_token),
    path('auth/retry-verify-account/', views.retry_verification_account),
    path('auth/access-token-by-username/', views.get_accesstoken_by_username),
    path('auth/verify-account/<str:verify_token>/', views.verifyAccount),
    # path('auth/reset-password/', views.deneme),
    # path('auth/forgot-password/', views.deneme),
]
