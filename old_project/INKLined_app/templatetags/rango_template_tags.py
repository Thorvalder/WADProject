from django import template
from INKLined_app.models import Artist

register = template.Library()

@register.inclusion_tag('INKLined_app/artists.html')
def get_artist_list(current_artist=None):
    return {'Artists': Artist.objects.all(),
            'current_artist': current_artist}
