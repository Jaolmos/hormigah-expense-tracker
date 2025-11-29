from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('gastos/', views.expense_list, name='expense_list'),
    path('gastos/exportar-csv/', views.export_expenses_csv, name='export_csv'),
    path('agregar/', views.add_expense, name='add_expense'),
    path('eliminar/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('editar/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('presupuesto/', views.manage_budget, name='manage_budget'),
    path('close-modal/', views.close_modal, name='close_modal'),
] 