from django import template
from core.models import Order

register = template.Library()


@register.filter
def cart_item_count(user):
        order = Order.objects.filter(user = user, ordered = False)
        if order.exists():
                return order[0].items.count()
        return 0