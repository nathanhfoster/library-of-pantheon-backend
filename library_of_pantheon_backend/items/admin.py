from django.contrib import admin
from .models import Item, Category, ItemAnalytics
from import_export.fields import Field
from import_export.resources import ModelResource
from import_export.admin import ImportExportActionModelAdmin
from import_export.widgets import ManyToManyWidget
from .admin_forms import ItemAdminForm


class ItemResource(ModelResource):
    categories = Field(widget=ManyToManyWidget(Category))

    class Meta:
        model = Item
        import_id_fields = ('id', 'name',)
        fields = ('id', 'name', 'url',
                  'slug', 'categories', 'image_url',
                  'description', 'created_at', 'updated_at',)
        widgets = {'categories': {'field': 'name'}, }


class ItemAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = ItemResource
    form = ItemAdminForm
    list_display = ('id', 'name', 'slug', 'url', 'get_categories', 'published',
                    'created_at', 'updated_at',)
    list_display_links = ('id', 'name',)
    search_fields = ('id', 'name', 'url', 'slug', 'categories__name', 'description',)


class CategoryResource(ModelResource):
    class Meta:
        model = Category
        import_id_fields = ('id', 'name',)
        fields = ('id', 'name', 'created_at', 'updated_at',)
        # widgets = {'categories': {'field': 'name'}}


class CategoryAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = CategoryResource

    list_display = ('id', 'name', 'created_at', 'updated_at',)
    list_display_links = ('id', 'name', )
    search_fields = ('id', 'name',)


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
