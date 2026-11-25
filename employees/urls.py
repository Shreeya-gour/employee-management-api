from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet

# Initialize DefaultRouter
router = DefaultRouter()

# Register ViewSet with router
# URL prefix: 'employees' -> generates /api/employees/ and /api/employees/<pk>/
router.register(r'employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
]
