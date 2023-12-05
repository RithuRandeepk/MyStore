"""
URL configuration for Mystore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from api import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import ObtainAuthToken

router=DefaultRouter()
# router.register("api/products",views.ProductViewsetView,basename="products")
router.register("api/products",views.ProductModelViewsetView,basename="products")
router.register("carts",views.CartView,basename="carts")
router.register("users",views.UserModelViewsetView,basename="users")




urlpatterns = [
    path('admin/', admin.site.urls),
    path('reviews/<int:pk>',views.ReviewDeleteView.as_view()),
    path('token/',ObtainAuthToken.as_view()),
    path('products',views.productView.as_view()),
    path('products/<int:id>',views.ProductDetailView.as_view()),
]+router.urls
