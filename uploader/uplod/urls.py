from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'uplod'

router = DefaultRouter()
router.register(r'composites', views.CompositeViewSet,basename='composites')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/composites/get_composite_from_path/<path:request_path>',
         views.GetCompositeFromPath.as_view(), name='composites_frompath'),
]
