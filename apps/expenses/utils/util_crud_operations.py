"""
Utilidades para operaciones CRUD y respuestas HTMX

Este módulo contiene funciones especializadas en:
- Operaciones CRUD (Create, Read, Update, Delete)
- Respuestas HTMX especializadas
- Manejo de errores consistente
- Context builders para diferentes operaciones
"""

from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from django.db.models import Sum
from django.conf import settings
import requests
from ..models import Expense, Budget

def get_expense_for_user(expense_id, user):
    """
    Obtiene un gasto específico verificando que pertenece al usuario
    
    Args:
        expense_id: ID del gasto
        user: Usuario actual
    
    Returns:
        Expense: Objeto del gasto o None si no existe/no pertenece al usuario
    
    Raises:
        Expense.DoesNotExist: Si el gasto no existe o no pertenece al usuario
    """
    try:
        return Expense.objects.get(id=expense_id, user=user)
    except Expense.DoesNotExist:
        raise Expense.DoesNotExist("El gasto no existe o no tienes permisos para acceder a él")


def handle_expense_creation(form_data, user):
    """
    Maneja la creación de un nuevo gasto con los datos del formulario
    
    Args:
        form_data: Datos POST del formulariomonthly_limit
        user: Usuario actual
    
    Returns:
        tuple: (expense, form, is_valid)
    """
    from ..forms import ExpenseForm
    
    form = ExpenseForm(form_data)
    
    if form.is_valid():
        expense = form.save(commit=False)
        expense.user = user
        expense.save()
        
        # Verificar alerta de presupuesto del 90%
        check_budget_alert(user)
        
        return expense, form, True
    
    return None, form, False


def handle_expense_form_update(expense, form_data):
    """
    Maneja la actualización de un gasto con los datos del formulario
    
    Args:
        expense: Instancia del gasto a actualizar
        form_data: Datos POST del formulario
    
    Returns:
        tuple: (updated_expense, form, is_valid)
    """
    from ..forms import ExpenseForm
    
    form = ExpenseForm(form_data, instance=expense)
    
    if form.is_valid():
        updated_expense = form.save()
        return updated_expense, form, True
    
    return expense, form, False


def handle_expense_deletion(expense_id, user):
    """
    Maneja la eliminación segura de un gasto
    
    Args:
        expense_id: ID del gasto a eliminar
        user: Usuario actual
    
    Returns:
        tuple: (expense_data, is_deleted, error_message)
    """
    try:
        # Obtener el gasto usando función auxiliar existente
        expense = get_expense_for_user(expense_id, user)
        
        # Guardar datos para el mensaje de confirmación
        expense_data = {
            'amount': expense.amount,
            'category_name': expense.category.name,
            'description': expense.description or 'Sin descripción',
            'date': expense.date
        }
        
        # Eliminar el gasto
        expense.delete()
        
        return expense_data, True, None
        
    except Expense.DoesNotExist:
        return None, False, 'El gasto no existe o no tienes permisos para eliminarlo'


def build_add_expense_context(form=None):
    """
    Construye el contexto para el formulario de agregar gasto
    
    Args:
        form: Formulario (nuevo o con errores)
    
    Returns:
        dict: Context para el template
    """
    from ..forms import ExpenseForm
    
    if form is None:
        form = ExpenseForm()
    
    return {
        'form': form
    }


def build_expense_edit_context(user, expense, form, request_params):
    """
    Construye el contexto para mostrar después de una edición exitosa
    
    Args:
        user: Usuario actual
        expense: Gasto actualizado
        form: Formulario usado
        request_params: Parámetros GET de la petición
    
    Returns:
        dict: Context actualizado con mensaje de éxito
    """
    # Importar aquí para evitar imports circulares
    from .util_expense_list import get_expense_list_context
    
    # Obtener contexto actualizado de la lista
    context = get_expense_list_context(user, request_params)
    
    # Agregar información específica de la edición
    context.update({
        'edit_success': True,
        'expense_data': {
            'amount': expense.amount,
            'category_name': expense.category.name,
            'description': expense.description or 'Sin descripción',
            'date': expense.date
        },
        'edit_message': 'Gasto actualizado exitosamente'
    })
    
    return context


def build_delete_success_context(user, expense_data, request_params):
    """
    Construye el contexto para mostrar después de una eliminación exitosa
    
    Args:
        user: Usuario actual
        expense_data: Datos del gasto eliminado
        request_params: Parámetros GET de la petición
    
    Returns:
        dict: Context actualizado con mensaje de éxito
    """
    # Importar aquí para evitar imports circulares
    from .util_expense_list import get_expense_list_context
    
    # Obtener contexto actualizado de la lista
    context = get_expense_list_context(user, request_params)
    
    # Agregar información específica de la eliminación
    context.update({
        'delete_success': True,
        'expense_data': expense_data,
        'delete_message': 'Gasto eliminado exitosamente'
    })
    
    return context


def handle_expense_error_response(request, error_message):
    """
    Maneja respuestas de error de forma consistente
    
    Args:
        request: Objeto request de Django
        error_message: Mensaje de error a mostrar
    
    Returns:
        HttpResponse: Respuesta apropiada según el tipo de petición
    """
    if request.headers.get('HX-Request'):
        return render(request, 'expenses/partials/delete_error.html', {
            'error': error_message
        })
    
    messages.error(request, error_message)
    return redirect('expenses:expense_list')


def create_htmx_add_response(request, expense):
    """
    Crea respuesta HTMX para creación exitosa que actualiza contenido automáticamente
    
    Args:
        request: Objeto request de Django
        expense: Gasto creado exitosamente
    
    Returns:
        HttpResponse: Respuesta con mensaje de éxito y triggers para actualización
    """
    response = render(request, 'expenses/partials/expense_success.html', {
        'expense': expense,
        'message': '¡Gasto agregado exitosamente!'
    })
    
    # Agregar triggers para actualizar contenido automáticamente
    # - refreshExpenseList: actualiza la lista si está visible
    # - refreshDashboard: actualiza métricas del dashboard si está visible
    response['HX-Trigger-After-Settle'] = 'refreshExpenseList, refreshDashboard'
    
    return response


def create_htmx_edit_response(request, context):
    """
    Crea respuesta HTMX para edición exitosa con trigger para cerrar modal
    
    Args:
        request: Objeto request de Django
        context: Context para el template
    
    Returns:
        HttpResponse: Respuesta con header HX-Trigger-After-Swap
    """
    response = render(request, 'expenses/partials/expense_list_content.html', context)
    response['HX-Trigger-After-Swap'] = 'closeEditModal'
    return response


def create_htmx_delete_response(request, context):
    """
    Crea respuesta HTMX para eliminación exitosa
    
    Args:
        request: Objeto request de Django
        context: Context para el template
    
    Returns:
        HttpResponse: Respuesta con lista actualizada
    """
    return render(request, 'expenses/partials/expense_list_content.html', context)


def check_budget_alert(user):
    """
    Verifica si el usuario ha alcanzado o superado el 90% de su presupuesto
    y envía webhook a n8n si es necesario
    
    Args:
        user: Usuario actual
    """
    
    try:
        # Obtener el presupuesto del usuario
        budget = Budget.objects.get(user=user)
        
        # Solo proceder si tiene alertas habilitadas
        if not budget.email_alerts_enabled:
            return
        
        # Calcular gastos del mes actual
        now = timezone.now()
        current_month_expenses = Expense.objects.filter(
            user=user,
            date__year=now.year,
            date__month=now.month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Calcular porcentaje
        percentage = (current_month_expenses / budget.monthly_limit) * 100
        
        # Verificar si alcanzó o superó el 90%
        if percentage >= 90:
            send_webhook_to_n8n(user, budget, current_month_expenses, percentage)
            
    except Budget.DoesNotExist:
        # Usuario no tiene presupuesto configurado
        pass


def send_webhook_to_n8n(user, budget, current_spending, percentage):
    """
    Envía webhook a n8n con los datos de alerta de presupuesto
    
    Args:
        user: Usuario que superó el límite
        budget: Objeto Budget del usuario
        current_spending: Gasto actual del mes
        percentage: Porcentaje usado del presupuesto
    """
    
    # Construir URL del webhook específico
    # Usar URL interna para comunicación Docker, fallback a URL base
    base_url = getattr(settings, 'N8N_INTERNAL_URL', settings.N8N_BASE_URL)
    webhook_url = f"{base_url}/webhook/budget-alert"
    
    payload = {
        'user_id': user.id,
        'user_name': user.get_full_name() or user.username,
        'user_email': user.email,
        'budget_limit': float(budget.monthly_limit),
        'current_spending': float(current_spending or 0),
        'percentage': round(float(percentage), 2),
        'alert_type': 'budget_90_percent',
        'message': f'Has alcanzado el {percentage:.1f}% de tu presupuesto mensual',
        'timestamp': timezone.now().isoformat()
    }
    
    try:
        # Headers con Bearer Token para autenticación
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.N8N_WEBHOOK_TOKEN}'
        }
        
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=10,  # Timeout de 10 segundos
            headers=headers
        )
        
        # Log del resultado (opcional)
        if response.status_code == 200:
            print(f"[SUCCESS] Webhook enviado exitosamente para {user.username}")
        else:
            print(f"[WARNING] Error en webhook: {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        # No fallar si el webhook falla - solo logging
        print(f"[ERROR] Error enviando webhook: {e}")
        pass 