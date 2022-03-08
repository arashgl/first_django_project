from django.db.models import Count
from django.contrib import admin
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = "Inventory"
    parameter_name = "inventory"

    def lookups(self, request, model_admin):
        return [("<10", "Low"), ("=>10", "Normal")]

    def queryset(self, request, queryset):
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)
        elif self.value() == "=>10":
            return queryset.filter(inventory__gte=10)


@admin.register(models.Collection)
class AdminCollection(admin.ModelAdmin):
    list_display = ["title", "prodcut_count"]
    search_fields = ["title"]

    @admin.display(ordering="prodcut_count")
    def prodcut_count(self, collection):
        url = reverse("admin:store_product_changelist") + "?" + \
            urlencode({"collection__id": str(collection.id)})
        return format_html("<a href='{}'>{}</a>", url, collection.prodcut_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(prodcut_count=Count("products"))


@admin.register(models.Product)
class AdminProduct(admin.ModelAdmin):
    autocomplete_fields = ["collection"]
    prepopulated_fields = {"slug": ["title"]}
    actions = ["clear_inventory"]
    list_display = ["title", "unit_price",
                    "inventory_status", "collection_title"]
    list_editable = ["unit_price"]
    ordering = ["title"]
    list_per_page = 10
    list_select_related = ["collection"]
    list_filter = ["collection", "last_update", InventoryFilter]
    search_fields = ["title"]

    @admin.display(ordering="collection")
    def collection_title(self, Product):
        return Product.collection.title

    @admin.display(ordering="inventory")
    def inventory_status(self, Product):
        if Product.inventory < 10:
            return "Low"
        return "OK"

    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request, f"{updated_count} products updated successfully")


@admin.register(models.Customer)
class AdminCustomer(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership", "order_count"]
    list_editable = ["membership"]
    list_per_page = 10
    ordering = ["first_name", "last_name"]
    search_fields = ["first_name__istartswith", "last_name__istartswith"]

    @admin.display(ordering="order_count")
    def order_count(self, order):
        url = reverse("admin:store_order_changelist") + "?" + \
            urlencode({"customer__id": order.id})
        return format_html("<a href='{}'>{}</a>", url, order.order_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(order_count=Count("order"))


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ["product"]
    model = models.OrderItem
    extra = 1
    min_num = 1
    max_num = 100


@admin.register(models.Order)
class AdminOrder(admin.ModelAdmin):
    autocomplete_fields = ["customer"]
    inlines = [OrderItemInline]
    list_display = ["id", "placed_at", "customer"]
