from django import template

register = template.Library()

@register.filter
def status_badge(status_label):
    colors = {
        'Новая': 'primary',
        'Принято в работу': 'warning',
        'Выполнено': 'success',
    }
    return colors.get(status_label, 'secondary')
