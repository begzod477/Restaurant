from django.urls import path
from .views import (Home, MenuView, MenuByCategoryView, Booking, Detail)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('<int:pk>/', Home.as_view(), name='home'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('menu/<str:category_name>/', MenuByCategoryView.as_view(), name='menu_by_category'),
    path('booking/', Booking.as_view(), name='booking' ),
    path('food_detail/<int:id>/', Detail.as_view(), name='food_detail')




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
