from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Expense, Budget
from .forms import ExpenseForm, BudgetForm
import csv
from datetime import datetime
# Imports específicos de utils modularizados
from .utils.util_dashboard import get_dashboard_context
from .utils.util_expense_list import get_expense_list_context
from .utils.util_crud_operations import (
    get_expense_for_user,
    handle_expense_creation,
    handle_expense_form_update,
    handle_expense_deletion,
    build_add_expense_context,
    build_expense_edit_context,
    build_delete_success_context,
    handle_expense_error_response,
    create_htmx_add_response,
    create_htmx_edit_response,
    create_htmx_delete_response
)


@login_required
def dashboard(request):
    """
    Muestra el dashboard principal con métricas de gastos
    Maneja filtros de período con HTMX
    """
    # Obtener el período seleccionado del filtro
    period = request.GET.get('period', 'current_month')
    
    # Obtener todo el contexto del dashboard usando las funciones auxiliares
    context = get_dashboard_context(request.user, period)
    
    # Si es una petición HTMX, devolver solo las métricas
    if request.headers.get('HX-Request'):
        return render(request, 'expenses/partials/dashboard_metrics.html', context)
    
    return render(request, 'expenses/dashboard.html', context)


@login_required
def expense_list(request):
    """
    Muestra la lista de gastos del usuario con filtros
    Maneja tanto peticiones normales como HTMX
    """
    # Obtener todo el contexto usando las funciones auxiliares
    context = get_expense_list_context(request.user, request.GET)
    
    # ¿Es una petición HTMX? Devolver solo contenido parcial
    if request.headers.get('HX-Request'):
        return render(request, 'expenses/partials/expense_list_content.html', context)
    
    # Petición normal: devolver página completa
    return render(request, 'expenses/expense_list.html', context)


@login_required
def add_expense(request):
    """
    Maneja la creación de nuevos gastos
    Soporta tanto formularios tradicionales como modales HTMX
    """
    if request.method == 'POST':
        # Manejar creación del gasto usando función auxiliar
        expense, form, is_valid = handle_expense_creation(request.POST, request.user)
        
        # Formulario válido: respuesta HTMX con mensaje de éxito
        if is_valid and request.headers.get('HX-Request'):
            return create_htmx_add_response(request, expense)
        
        # Formulario válido: redirect normal
        if is_valid:
            messages.success(request, '¡Gasto agregado exitosamente!')
            return redirect('expenses:dashboard')
        
        # Formulario con errores: mostrar modal HTMX
        if request.headers.get('HX-Request'):
            return render(request, 'expenses/partials/add_expense_modal.html', {
                'form': form
            })
    
    else:
        # Obtener contexto usando función auxiliar
        context = build_add_expense_context()
        
        # Mostrar formulario: modal HTMX o página completa
        if request.headers.get('HX-Request'):
            return render(request, 'expenses/partials/add_expense_modal.html', context)
        
        return render(request, 'expenses/add_expense.html', context)


@login_required
def close_modal(request):
    """
    Vista para cerrar modales HTMX
    """
    return render(request, 'expenses/partials/empty.html')


@login_required
def delete_expense(request, expense_id):
    """
    Elimina un gasto específico del usuario
    Soporta eliminación vía HTMX y peticiones tradicionales
    """
    if request.method == 'DELETE':
        # Manejar eliminación del gasto usando función auxiliar
        expense_data, is_deleted, error_message = handle_expense_deletion(expense_id, request.user)
        
        # Eliminación exitosa: respuesta HTMX con lista actualizada
        if is_deleted and request.headers.get('HX-Request'):
            context = build_delete_success_context(request.user, expense_data, request.GET)
            return create_htmx_delete_response(request, context)
        
        # Eliminación exitosa: redirect normal
        if is_deleted:
            messages.success(request, f'Gasto de €{expense_data["amount"]} eliminado exitosamente')
            return redirect('expenses:expense_list')
        
        # Error en eliminación: manejar respuesta de error
        return handle_expense_error_response(request, error_message)


@login_required
def edit_expense(request, expense_id):
    """
    Permite editar un gasto existente del usuario
    Soporta edición vía modal HTMX y formularios tradicionales
    """
    try:
        # Obtener el gasto usando función auxiliar
        expense = get_expense_for_user(expense_id, request.user)
        
        if request.method == 'POST':
            updated_expense, form, is_valid = handle_expense_form_update(expense, request.POST)
            
            # Formulario válido: respuesta HTMX con actualización de lista
            if is_valid and request.headers.get('HX-Request'):
                context = build_expense_edit_context(request.user, updated_expense, form, request.GET)
                return create_htmx_edit_response(request, context)
            
            # Formulario válido: redirect normal
            if is_valid:
                messages.success(request, f'Gasto de €{updated_expense.amount} actualizado exitosamente')
                return redirect('expenses:expense_list')
            
            # Formulario con errores: mostrar modal HTMX
            if request.headers.get('HX-Request'):
                return render(request, 'expenses/partials/edit_expense_modal.html', {
                    'form': form,
                    'expense': expense,
                    'form_errors': True
                })
            
        else:
            form = ExpenseForm(instance=expense)
            
        # Mostrar formulario: modal HTMX o página completa
        if request.headers.get('HX-Request'):
            return render(request, 'expenses/partials/edit_expense_modal.html', {
                'form': form,
                'expense': expense
            })
        
        return render(request, 'expenses/edit_expense.html', {
            'form': form,
            'expense': expense
        })
        
    except Expense.DoesNotExist:
        return handle_expense_error_response(
            request, 
            'El gasto no existe o no tienes permisos para editarlo'
        )


@login_required
def manage_budget(request):
    """
    Vista sencilla para configurar el presupuesto del usuario
    """
    try:
        budget = Budget.objects.get(user=request.user)
    except Budget.DoesNotExist:
        budget = None
    
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            
            # Respuesta HTMX: recargar dashboard
            if request.headers.get('HX-Request'):
                messages.success(request, 'Presupuesto configurado exitosamente!')
                response = render(request, 'expenses/partials/budget_success.html', {
                    'budget': budget
                })
                response['HX-Trigger'] = 'refreshDashboard'  # Recargar métricas
                return response
            
            messages.success(request, 'Presupuesto configurado exitosamente!')
            return redirect('expenses:dashboard')
    else:
        form = BudgetForm(instance=budget)
    
    # Modal HTMX o página completa
    if request.headers.get('HX-Request'):
        return render(request, 'expenses/partials/budget_modal.html', {
            'form': form,
            'budget': budget
        })
    
    return render(request, 'expenses/budget.html', {
        'form': form,
        'budget': budget
    })


@login_required
def export_expenses_csv(request):
    """
    Exporta los gastos del usuario a formato CSV
    Respeta los filtros activos en la lista de gastos
    """
    # Reutilizar la lógica de filtros de get_expense_list_context
    context = get_expense_list_context(request.user, request.GET)
    expenses = context['expenses']

    # Crear la respuesta HTTP con tipo CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')

    # Nombre del archivo con fecha actual
    filename = f'gastos_{datetime.now().strftime("%Y-%m-%d")}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Agregar BOM para que Excel reconozca UTF-8
    response.write('\ufeff')

    # Crear el writer CSV
    writer = csv.writer(response, delimiter=';')

    # Escribir cabecera
    writer.writerow(['Fecha', 'Categoría', 'Monto (€)', 'Descripción', 'Ubicación'])

    # Escribir datos de gastos
    for expense in expenses:
        writer.writerow([
            expense.date.strftime('%d/%m/%Y'),  # Formato español
            expense.category.name,
            str(expense.amount).replace('.', ','),  # Separador decimal europeo
            expense.description or '',
            expense.location or ''
        ])

    return response



