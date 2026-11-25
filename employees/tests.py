from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Employee


class EmployeeAPITests(APITestCase):
    """
    Automated test suite for Employee Management REST API.
    Covers CRUD operations, validations, permissions, and edge cases.
    """

    def setUp(self):
        # 1. Create a test user for authenticated requests
        self.user = User.objects.create_user(
            username='testadmin',
            email='testadmin@example.com',
            password='testpassword123'
        )

        # 2. Seed an initial employee in test database
        self.employee = Employee.objects.create(
            name='Rajesh Kumar',
            email='rajesh@example.com',
            department='Engineering',
            salary='70000.00',
            joining_date='2026-01-15'
        )

        self.list_url = '/api/employees/'
        self.detail_url = f'/api/employees/{self.employee.id}/'

    # --- READ TESTS ---
    def test_unauthenticated_get_all_employees(self):
        """Public users should be able to view employee list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(response.data['count'], 1)

    def test_get_single_employee_by_id_success(self):
        """Public users should be able to retrieve an employee by valid ID."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Rajesh Kumar')
        self.assertEqual(response.data['email'], 'rajesh@example.com')

    def test_get_single_employee_nonexistent_id_returns_404(self):
        """Querying an invalid employee ID should return 404 Not Found."""
        response = self.client.get('/api/employees/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # --- PERMISSION TESTS ---
    def test_unauthenticated_post_is_forbidden(self):
        """Anonymous user trying to create employee should be rejected with 401/403."""
        payload = {
            'name': 'Intruder',
            'email': 'intruder@example.com',
            'department': 'Hacking',
            'salary': '50000.00',
            'joining_date': '2026-11-25'
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    # --- CREATE TESTS ---
    def test_authenticated_create_employee_success(self):
        """Authenticated user should be able to create a new employee."""
        self.client.force_authenticate(user=self.user)
        payload = {
            'name': 'Priya Nair',
            'email': 'priya.nair@example.com',
            'department': 'Marketing',
            'salary': '65000.00',
            'joining_date': '2026-11-25'
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Priya Nair')
        self.assertEqual(Employee.objects.count(), 2)

    def test_create_employee_duplicate_email_fails(self):
        """Attempting to create an employee with an existing email should fail."""
        self.client.force_authenticate(user=self.user)
        payload = {
            'name': 'Duplicate Person',
            'email': 'rajesh@example.com',  # Same as seeded employee
            'department': 'HR',
            'salary': '40000.00',
            'joining_date': '2026-11-25'
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_create_employee_negative_salary_fails(self):
        """Custom validator should reject salary <= 0."""
        self.client.force_authenticate(user=self.user)
        payload = {
            'name': 'Valid Name',
            'email': 'valid.salary@example.com',
            'department': 'IT',
            'salary': '-1000.00',
            'joining_date': '2026-11-25'
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('salary', response.data)

    # --- UPDATE TESTS ---
    def test_authenticated_patch_salary_success(self):
        """Authenticated user can partially update salary via PATCH."""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url, {'salary': '90000.00'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(str(self.employee.salary), '90000.00')

    # --- DELETE TESTS ---
    def test_authenticated_delete_employee_success(self):
        """Authenticated user can delete an employee."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)

    # --- MODEL TEST ---
    def test_employee_str_representation(self):
        """Model __str__ should return 'Name (Department)'."""
        self.assertEqual(str(self.employee), 'Rajesh Kumar (Engineering)')
