from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'department', 'salary', 'joining_date']
        read_only_fields = ['id']

    def validate_name(self, value):
        """Field-level validation: Name must have at least 2 characters."""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        return value.strip()

    def validate_salary(self, value):
        """Field-level validation: Salary must be greater than zero."""
        if value <= 0:
            raise serializers.ValidationError("Salary must be a positive number greater than 0.")
        return value

    def validate_email(self, value):
        """Field-level validation: Email must be lowercase and unique."""
        normalized_email = value.strip().lower()
        # In update (PUT/PATCH), exclude current employee's own record from duplicate check
        employee_id = self.instance.id if self.instance else None
        if Employee.objects.filter(email__iexact=normalized_email).exclude(id=employee_id).exists():
            raise serializers.ValidationError("An employee with this email already exists.")
        return normalized_email
