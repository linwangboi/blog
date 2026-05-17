
from assignments.models import SocialLink

from .models import Category


def get_categories(request):
    return dict(
        categories=Category.objects.all(),
    )

def get_social_links(request):
    return dict(
        social_links=SocialLink.objects.all(),
    )