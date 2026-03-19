from decimal import Decimal
from collections import defaultdict

from django.db import connection
from django.db.utils import ProgrammingError
from django.conf import settings

from .models import Producto


def cart_summary(request):

    if request.path.startswith('/admin'):
        return {}

    default_context = {
        'cart_count': 0,
        'cart_total': Decimal('0.00'),
        'productos_por_categoria': {},
        'postres_especiales': []
    }

    try:
        table_name = Producto._meta.db_table
        if table_name not in connection.introspection.table_names():
            return default_context

        cart = request.session.get('cart', {}) or {}
        cart_count = sum(cart.values()) if cart else 0

        return {
            **default_context,
            'cart_count': cart_count,
        }

    except (ProgrammingError, Exception):
        return default_context


def branding(request):
    return {
        'project_name': getattr(settings, 'PROJECT_NAME', 'Sweet House'),
        'support_email': getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@sweethouse.local'),
    }