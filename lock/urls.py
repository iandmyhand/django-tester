from django.conf.urls import url

from lock.views import TestLockViewSet

urlpatterns = [
    url(regex=r'^test-lock/$',
        view=TestLockViewSet.as_view(), name='test-lock'),
]
