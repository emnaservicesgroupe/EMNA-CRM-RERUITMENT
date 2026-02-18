from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CompanyViewSet, CandidateViewSet, dashboard_summary

router = DefaultRouter()
router.register(r"companies", CompanyViewSet, basename="companies")
router.register(r"candidates", CandidateViewSet, basename="candidates")

urlpatterns = [
    path("", include(router.urls)),
    path("dashboard/summary/", dashboard_summary),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
