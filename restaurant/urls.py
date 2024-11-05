from django.urls import path
from .views import (Home, MenuView, MenuByCategoryView)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('<int:pk>/', Home.as_view(), name='home'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('menu/<str:category_name>/', MenuByCategoryView.as_view(), name='menu_by_category')



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
