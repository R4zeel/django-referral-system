from rest_framework import routers
from django.urls import path, include

from .views import UserAuthViewSet, ReferralViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserAuthViewSet, basename='users')
router_v1.register('referrals', ReferralViewSet, basename='referrals')

urlpatterns = [
    path('', include(router_v1.urls)),
]
