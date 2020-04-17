from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'uplod'

router = DefaultRouter()
router.register(r'composites', views.CompositeViewSet,basename='composites')

urlpatterns = [
    path('api/', include(router.urls)),
]