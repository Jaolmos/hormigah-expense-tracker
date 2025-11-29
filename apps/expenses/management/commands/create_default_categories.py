"""
Comando de gestión de Django para crear categorías predeterminadas
Uso: python manage.py create_default_categories
"""
from django.core.management.base import BaseCommand
from apps.expenses.models import Category


class Command(BaseCommand):
    help = 'Crea categorías predeterminadas de gastos si no existen'

    def handle(self, *args, **options):
        """
        Crea las categorías predeterminadas basadas en las de producción
        """
        # Definición de categorías con los mismos nombres y colores de producción
        default_categories = [
            {
                'name': 'Café y Bebidas',
                'icon': '☕',
                'color': '#880514',
                'description': 'Café, té y otras bebidas'
            },
            {
                'name': 'Compras Impulsivas',
                'icon': '🛍️',
                'color': '#FF8680',
                'description': 'Compras no planificadas y caprichos'
            },
            {
                'name': 'Delivery y Restaurantes',
                'icon': '🍕',
                'color': '#FF8633',
                'description': 'Pedidos a domicilio y comidas en restaurantes'
            },
            {
                'name': 'Entretenimiento',
                'icon': '🎵',
                'color': '#C27940',
                'description': 'Ocio, música, cine y diversión'
            },
            {
                'name': 'Otros',
                'icon': '📌',
                'color': '#712421',
                'description': 'Gastos varios sin categoría específica'
            },
            {
                'name': 'Salud y Cuidados',
                'icon': '💊',
                'color': '#F757E3',
                'description': 'Medicamentos, farmacia y cuidado personal'
            },
            {
                'name': 'Suscripciones',
                'icon': '📡',
                'color': '#F737E3',
                'description': 'Servicios de suscripción mensual y pagos recurrentes'
            },
            {
                'name': 'Transporte y Movilidad',
                'icon': '🚕',
                'color': '#50CAD0',
                'description': 'Taxi, uber, transporte público y gasolina'
            },
        ]

        # Contador de categorías creadas
        created_count = 0
        existing_count = 0

        self.stdout.write(self.style.SUCCESS('\n🚀 Iniciando creación de categorías predeterminadas...\n'))

        for category_data in default_categories:
            # Verificar si la categoría ya existe (por nombre)
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'icon': category_data['icon'],
                    'color': category_data['color'],
                    'description': category_data['description']
                }
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'  ✅ Creada: {category.icon} {category.name} ({category.color})')
                )
            else:
                existing_count += 1
                self.stdout.write(
                    self.style.WARNING(f'  ⏭️  Ya existe: {category.icon} {category.name}')
                )

        # Resumen final
        self.stdout.write(self.style.SUCCESS(f'\n📊 Resumen:'))
        self.stdout.write(self.style.SUCCESS(f'  • Categorías creadas: {created_count}'))
        self.stdout.write(self.style.WARNING(f'  • Categorías existentes: {existing_count}'))
        self.stdout.write(self.style.SUCCESS(f'  • Total de categorías: {Category.objects.count()}\n'))
        
        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS('✨ ¡Categorías predeterminadas creadas exitosamente!\n')
            )
        else:
            self.stdout.write(
                self.style.WARNING('ℹ️  Todas las categorías ya existían.\n')
            )

