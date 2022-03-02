from django.shortcuts import render
from django.db.models import F, ExpressionWrapper, Value, DecimalField
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from store.models import Collection, Customer, OrderItem, Product, Order


def say_hello(request):
    # ExpressionWrapper(F('unit_price')*Count('order'))
    queryset = Product.objects.annotate(
        best_selling=Sum(F('orderitem__quantity')*F('orderitem__unit_price'))
    ).order_by('-best_selling')[:5]
    return render(request, "hello.html", {"name": "Mosh", "orders": list(queryset)})
