from django import template

register = template.Library()

@register.filter(name='file_url')
def file_url(obj):
    """Return the external link or the storage URL of an uploaded PDF."""
    if obj.external_file_url:
        return obj.external_file_url
    return obj.file_url.url if obj.file_url else ''
