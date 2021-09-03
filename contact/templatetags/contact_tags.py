from django import template
from contact.forms import ContactForm

"""создадим темлейттег который будет рендерить нашу форму на всех странциах где мы её укажем"""

register = template.Library()


@register.inclusion_tag("contact/tags/form.html")  # для inclusion_tag нужно указать нашу касватомную  html, которую мы будем вставлять в нужный template
def contact_form():
    return {"contact_form": ContactForm()}