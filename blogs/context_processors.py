from assignments.models import SocialLink

from .models import Category


def get_categories(request):
    return dict(
        categories=Category.objects.all().order_by("-created_at"),
    )


def get_social_links(request):
    return dict(
        social_links=SocialLink.objects.all(),
    )
