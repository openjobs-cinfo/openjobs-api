from django.urls import path, include
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from .viewsets import DegreeViewSet, JobViewSet, SkillViewSet, DataOriginViewSet, AddressViewSet, \
    QualificationViewSet, JobRecommendationViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


swagger_view = get_schema_view(
    openapi.Info(
        title="OpenJobs API",
        default_version='v1',
        description="API from OpenJobs project",
    ),
)

router = DefaultRouter()
router.register(r'addresses', AddressViewSet)
router.register(r'degrees', DegreeViewSet)
router.register(r'qualifications', QualificationViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'data_origins', DataOriginViewSet)
router.register(r'auth/users/me', JobRecommendationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.base')),
    path('auth/', include('djoser.urls.jwt')),
    path('doc/', login_required(swagger_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    path('redoc/', login_required(swagger_view.with_ui('redoc', cache_timeout=0)), name='schema-redoc'),
]
