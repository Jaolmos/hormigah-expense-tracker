"""
Tests para la funcionalidad de exportación CSV

Cubre la vista export_expenses_csv con diferentes escenarios
"""
import pytest
import csv
from io import StringIO
from datetime import date, timedelta
from decimal import Decimal
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.expenses.models import Category, Expense


@pytest.mark.django_db
class TestExportCSV:
    """Tests para la exportación de gastos a CSV"""

    def setup_method(self):
        """Configuración inicial para cada test"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            password="otherpass123"
        )
        self.category = Category.objects.create(
            name="Test Category",
            color="#FF0000"
        )

    def test_export_csv_requires_login(self):
        """Test que export_csv requiere autenticación"""
        response = self.client.get(reverse('expenses:export_csv'))
        assert response.status_code == 302  # Redirect a login
        assert '/admin/login/' in response.url or '/login/' in response.url

    def test_export_csv_without_filters(self):
        """Test exportación CSV sin filtros (todos los gastos)"""
        self.client.login(username="testuser", password="testpass123")

        # Crear gastos del usuario
        Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('25.50'),
            description="Café matutino",
            location="Starbucks",
            date=date.today()
        )
        Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('10.00'),
            description="Snack",
            location="",
            date=date.today() - timedelta(days=1)
        )

        # Crear gasto de otro usuario (no debe aparecer)
        Expense.objects.create(
            user=self.other_user,
            category=self.category,
            amount=Decimal('100.00'),
            description="Otro usuario",
            date=date.today()
        )

        response = self.client.get(reverse('expenses:export_csv'))

        assert response.status_code == 200
        assert response['Content-Type'] == 'text/csv; charset=utf-8'

        # Verificar nombre de archivo
        content_disposition = response['Content-Disposition']
        assert 'attachment' in content_disposition
        assert 'gastos_' in content_disposition
        assert '.csv' in content_disposition

        # Parsear CSV
        content = response.content.decode('utf-8-sig')  # utf-8-sig para BOM
        csv_reader = csv.reader(StringIO(content), delimiter=';')
        rows = list(csv_reader)

        # Verificar cabecera
        assert rows[0] == ['Fecha', 'Categoría', 'Monto (€)', 'Descripción', 'Ubicación']

        # Verificar datos (2 gastos del usuario autenticado)
        assert len(rows) == 3  # Header + 2 gastos

        # Verificar que no incluye gastos de otro usuario
        descriptions = [row[3] for row in rows[1:]]
        assert 'Otro usuario' not in descriptions

    def test_export_csv_format_european(self):
        """Test formato CSV europeo (delimitador, decimal, fecha)"""
        self.client.login(username="testuser", password="testpass123")

        Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('123.45'),
            description="Test",
            location="Location",
            date=date(2025, 11, 29)
        )

        response = self.client.get(reverse('expenses:export_csv'))
        content = response.content.decode('utf-8-sig')
        csv_reader = csv.reader(StringIO(content), delimiter=';')
        rows = list(csv_reader)

        # Verificar fila de datos
        data_row = rows[1]

        # Formato fecha: DD/MM/YYYY
        assert data_row[0] == '29/11/2025'

        # Separador decimal: coma
        assert data_row[2] == '123,45'

        # Delimitador: punto y coma (ya verificado por csv.reader delimiter)
        assert len(data_row) == 5

    def test_export_csv_with_period_filter(self):
        """Test exportación con filtro de período"""
        self.client.login(username="testuser", password="testpass123")

        today = date.today()

        # Gasto de hoy (dentro del mes actual)
        Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('10.00'),
            description="Este mes",
            date=today
        )

        # Gasto de hace 60 días (fuera del mes actual)
        Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('20.00'),
            description="Mes anterior",
            date=today - timedelta(days=60)
        )

        # Exportar con filtro "current_month"
        response = self.client.get(
            reverse('expenses:export_csv'),
            {'period': 'current_month'}
        )

        content = response.content.decode('utf-8-sig')
        csv_reader = csv.reader(StringIO(content), delimiter=';')
        rows = list(csv_reader)

        # Solo debe aparecer el gasto del mes actual
        assert len(rows) == 2  # Header + 1 gasto
        assert rows[1][3] == 'Este mes'

    def test_export_csv_with_category_filter(self):
        """Test exportación con filtro de categoría"""
        self.client.login(username="testuser", password="testpass123")

        category2 = Category.objects.create(
            name="Other Category",
            color="#00FF00"
        )

        # Gasto con category original
        Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('10.00'),
            description="Category 1",
            date=date.today()
        )

        # Gasto con category2
        Expense.objects.create(
            user=self.user,
            category=category2,
            amount=Decimal('20.00'),
            description="Category 2",
            date=date.today()
        )

        # Exportar filtrando por category original
        response = self.client.get(
            reverse('expenses:export_csv'),
            {'category': self.category.id}
        )

        content = response.content.decode('utf-8-sig')
        csv_reader = csv.reader(StringIO(content), delimiter=';')
        rows = list(csv_reader)

        # Solo debe aparecer el gasto de category 1
        assert len(rows) == 2  # Header + 1 gasto
        assert rows[1][1] == 'Test Category'
        assert rows[1][3] == 'Category 1'

    def test_export_csv_with_amount_filter(self):
        """Test exportación con filtro de monto mínimo/máximo"""
        self.client.login(username="testuser", password="testpass123")

        # Gastos con diferentes montos
        Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('5.00'),
            description="Bajo",
            date=date.today()
        )
        Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('15.00'),
            description="Medio",
            date=date.today()
        )
        Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('25.00'),
            description="Alto",
            date=date.today()
        )

        # Exportar con filtro de monto: min=10, max=20
        response = self.client.get(
            reverse('expenses:export_csv'),
            {'min_amount': '10', 'max_amount': '20'}
        )

        content = response.content.decode('utf-8-sig')
        csv_reader = csv.reader(StringIO(content), delimiter=';')
        rows = list(csv_reader)

        # Solo debe aparecer el gasto "Medio"
        assert len(rows) == 2  # Header + 1 gasto
        assert rows[1][3] == 'Medio'
        assert rows[1][2] == '15,00'

    def test_export_csv_with_combined_filters(self):
        """Test exportación con múltiples filtros combinados"""
        self.client.login(username="testuser", password="testpass123")

        today = date.today()

        # Gasto que cumple todos los filtros
        Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('15.00'),
            description="Match",
            date=today
        )

        # Gasto que NO cumple (monto fuera de rango)
        Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('50.00'),
            description="No match - monto",
            date=today
        )

        # Exportar con filtros combinados
        response = self.client.get(
            reverse('expenses:export_csv'),
            {
                'period': 'current_month',
                'category': self.category.id,
                'min_amount': '10',
                'max_amount': '20'
            }
        )

        content = response.content.decode('utf-8-sig')
        csv_reader = csv.reader(StringIO(content), delimiter=';')
        rows = list(csv_reader)

        # Solo debe aparecer el gasto que cumple todos los filtros
        assert len(rows) == 2  # Header + 1 gasto
        assert rows[1][3] == 'Match'

    def test_export_csv_utf8_bom(self):
        """Test encoding UTF-8 con BOM para Excel"""
        self.client.login(username="testuser", password="testpass123")

        # Crear gasto con caracteres especiales
        Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('10.00'),
            description="Café con ñ y tildes: áéíóú",
            location="España",
            date=date.today()
        )

        response = self.client.get(reverse('expenses:export_csv'))

        # Verificar Content-Type
        assert response['Content-Type'] == 'text/csv; charset=utf-8'

        # Verificar BOM (Byte Order Mark) al inicio del archivo
        content_bytes = response.content
        assert content_bytes[:3] == b'\xef\xbb\xbf'  # UTF-8 BOM

        # Decodificar y verificar caracteres especiales
        content = response.content.decode('utf-8-sig')
        assert 'Café con ñ y tildes: áéíóú' in content
        assert 'España' in content

    def test_export_csv_filename_with_date(self):
        """Test nombre archivo con fecha actual"""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(reverse('expenses:export_csv'))

        content_disposition = response['Content-Disposition']

        # Verificar formato: attachment; filename="gastos_YYYY-MM-DD.csv"
        assert 'attachment' in content_disposition
        assert 'filename="gastos_' in content_disposition
        assert '.csv"' in content_disposition

        # Extraer fecha del nombre
        today_str = date.today().strftime('%Y-%m-%d')
        assert f'gastos_{today_str}.csv' in content_disposition

    def test_export_csv_empty_optional_fields(self):
        """Test exportación con campos opcionales vacíos"""
        self.client.login(username="testuser", password="testpass123")

        # Gasto sin descripción ni ubicación
        Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('10.00'),
            description='',
            location='',
            date=date.today()
        )

        response = self.client.get(reverse('expenses:export_csv'))
        content = response.content.decode('utf-8-sig')
        csv_reader = csv.reader(StringIO(content), delimiter=';')
        rows = list(csv_reader)

        data_row = rows[1]

        # Campos vacíos deben ser strings vacíos, no None
        assert data_row[3] == ''  # Descripción
        assert data_row[4] == ''  # Ubicación

    def test_export_csv_only_user_expenses(self):
        """Test que solo exporta gastos del usuario autenticado"""
        self.client.login(username="testuser", password="testpass123")

        # Gastos del usuario autenticado
        Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('10.00'),
            description="Mi gasto 1",
            date=date.today()
        )
        Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('20.00'),
            description="Mi gasto 2",
            date=date.today()
        )

        # Gastos de otro usuario
        Expense.objects.create(
            user=self.other_user,
            category=self.category,
            amount=Decimal('100.00'),
            description="Gasto ajeno 1",
            date=date.today()
        )
        Expense.objects.create(
            user=self.other_user,
            category=self.category,
            amount=Decimal('200.00'),
            description="Gasto ajeno 2",
            date=date.today()
        )

        response = self.client.get(reverse('expenses:export_csv'))
        content = response.content.decode('utf-8-sig')
        csv_reader = csv.reader(StringIO(content), delimiter=';')
        rows = list(csv_reader)

        # Solo deben aparecer los 2 gastos del usuario autenticado
        assert len(rows) == 3  # Header + 2 gastos

        descriptions = [row[3] for row in rows[1:]]
        assert 'Mi gasto 1' in descriptions
        assert 'Mi gasto 2' in descriptions
        assert 'Gasto ajeno 1' not in descriptions
        assert 'Gasto ajeno 2' not in descriptions


# =============================================================================
# CÓMO EJECUTAR ESTOS TESTS
# =============================================================================
"""
Para ejecutar los tests de exportación CSV, usa estos comandos:

** SI USAS DOCKER (recomendado), añade 'docker compose exec web' antes de cada comando **

1. Ejecutar TODOS los tests de este archivo:
   docker compose exec web pytest apps/expenses/tests/test_export_csv.py -v

2. Ejecutar solo tests de formato:
   docker compose exec web pytest apps/expenses/tests/test_export_csv.py::TestExportCSV::test_export_csv_format_european -v

3. Ejecutar solo tests de filtros:
   docker compose exec web pytest apps/expenses/tests/test_export_csv.py -k "filter" -v

4. Ejecutar con cobertura:
   docker compose exec web pytest apps/expenses/tests/test_export_csv.py --cov=apps.expenses.views -v

5. Ejecutar todos los tests de expenses:
   docker compose exec web pytest apps/expenses/tests/ -v

6. Ejecutar con output detallado:
   docker compose exec web pytest apps/expenses/tests/test_export_csv.py -v -s

** SI NO USAS DOCKER, añade '--ds=config.settings' a cada comando **

Ejemplo sin Docker:
   pytest --ds=config.settings apps/expenses/tests/test_export_csv.py -v

Tests cubren:
✓ Autenticación requerida
✓ Exportación sin filtros
✓ Formato europeo (delimitador ;, decimal ,, fecha DD/MM/YYYY)
✓ Encoding UTF-8 con BOM
✓ Nombre de archivo con fecha
✓ Filtros: período, categoría, monto
✓ Filtros combinados
✓ Solo gastos del usuario autenticado
✓ Campos opcionales vacíos
"""
