from django.contrib import admin
from django.urls import path
from article.views import ArticleListCreateAPIView,ArticleDetailUpdateDeleteAPIView
from user.views import *

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
   openapi.Info(
      title="Shiranka API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.blahblahblah.com/policies/terms/",
      contact=openapi.Contact(email="nosuchemail@mail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
#    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('articles/',ArticleListCreateAPIView.as_view(),name='article-list'),
    path('articles/<int:pk>/',ArticleDetailUpdateDeleteAPIView.as_view(),name='article-detail'),
    path('register/',UserCreateAPIView.as_view(),name='user-create'),
    path('user-verify/',VerifyEmail.as_view(),name='verify-email'),
    path('login/',UserLoginAPIView.as_view(),name='user-login'),
    path('request-reset-email/',RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/',PasswordTokenCheckAPIView.as_view(),name='password-reset'),
    path('password-reset-complete/',SetNewPasswordAPIView.as_view(),name='password-reset-complete'),
    path('user-profile/<int:pk>/',UserDetailDestroyAPIView().as_view(),name='user-detail'),

]
