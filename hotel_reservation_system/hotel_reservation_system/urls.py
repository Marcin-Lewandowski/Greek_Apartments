"""
URL configuration for hotel_reservation_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from reservations.views import HotelList, HotelDetail, ReservationList, ReservationDetail, RoomList, RoomDetail, ReservationPlanningAPIView, Register


from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import LoginView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="API documentation for all available endpoints",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="example@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

class CustomLoginView(LoginView):
    redirect_authenticated_user = True  # Redirects logged in users
    success_url = reverse_lazy('user_profile')  # Redirected after successful login

urlpatterns = [
    # SWAGGER
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('api/v1/', include([
        path('', include('reservations.urls')),
    ])),
    
    
    path('admin/', admin.site.urls),
    path('hotels/', HotelList.as_view(), name='hotel-list'),
    path('hotels/<int:pk>/', HotelDetail.as_view(), name='hotel-detail'),
    path('reservations/', ReservationList.as_view(), name='reservation-list'),
    path('reservations/<int:pk>/', ReservationDetail.as_view(), name='reservation-detail'),
    path('rooms/', RoomList.as_view(), name='room-list'),
    path('rooms/<int:pk>/', RoomDetail.as_view(), name='room-detail'),


    path('register/', Register.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    # path('logout/', ... , name='logout'),
    # path('profile/', ... , name='user_profile'),
    # path('my_reservations/', ... , name='my_reservations'),
    # path('reservation_planning/', ... , name='reservation_planning'),
    path('api/reservation-planning/', ReservationPlanningAPIView.as_view(), name='reservation-planning-api'),
]