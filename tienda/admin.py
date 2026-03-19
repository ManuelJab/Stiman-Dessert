from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Producto


# 1. Recurso para import/export
class ProductoResource(resources.ModelResource):
    class Meta:
        model = Producto
        fields = ('id', 'name', 'description', 'price', 'category', 'is_active', 'is_special')


# 2. Admin correcto
@admin.register(Producto)
class ProductoAdmin(ImportExportModelAdmin):  
    resource_class = ProductoResource
    list_display = ('name', 'price', 'category', 'is_active', 'is_special')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)