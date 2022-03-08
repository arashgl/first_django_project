from django.contrib import admin
from store.models import Product
from tags.models import TaggedItem
from store.admin import AdminProduct
from django.contrib.contenttypes.admin import GenericTabularInline


class TagInLine(GenericTabularInline):
    autocomplete_fields = ["tag"]
    model = TaggedItem


class CustomAdminProduct(AdminProduct):
    inlines = [TagInLine]


admin.site.unregister(Product)
admin.site.register(Product, CustomAdminProduct)
