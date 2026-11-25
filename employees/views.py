from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, viewsets, filters, permissions
from .models import Employee
from .serializers import EmployeeSerializer
from .pagination import EmployeePagination


# ==============================================================================
# LEVEL 1: APIView (Manual Control - Steps 7, 8, 9, 10)
# ==============================================================================
class EmployeeListAPIView(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetailAPIView(APIView):
    def get_object(self, id):
        try:
            return Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            return None

    def get(self, request, id):
        employee = self.get_object(id)
        if not employee:
            return Response({"error": f"Employee {id} not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        employee = self.get_object(id)
        if not employee:
            return Response({"error": f"Employee {id} not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        employee = self.get_object(id)
        if not employee:
            return Response({"error": f"Employee {id} not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        employee = self.get_object(id)
        if not employee:
            return Response({"error": f"Employee {id} not found."}, status=status.HTTP_404_NOT_FOUND)
        employee.delete()
        return Response({"message": f"Employee {id} deleted successfully."}, status=status.HTTP_200_OK)


# ==============================================================================
# LEVEL 2 & 3: Generic Views (Step 12)
# ==============================================================================
class EmployeeListCreateGenericView(generics.ListCreateAPIView):
    queryset = Employee.objects.all().order_by('-id')
    serializer_class = EmployeeSerializer


class EmployeeDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'id'


# ==============================================================================
# LEVEL 4: ModelViewSet (The Ultimate DRF Standard - Step 13)
# Poora CRUD cycle sirf ek single class me!
# ==============================================================================
class EmployeeViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    Includes Pagination, Search, Department Filter and Ordering.
    """
    queryset = Employee.objects.all().order_by('-id')
    serializer_class = EmployeeSerializer
    pagination_class = EmployeePagination
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email']
    ordering_fields = ['salary', 'joining_date', 'name']

    def get_queryset(self):
        queryset = super().get_queryset()
        department = self.request.query_params.get('department')
        if department:
            queryset = queryset.filter(department__iexact=department)
        return queryset
