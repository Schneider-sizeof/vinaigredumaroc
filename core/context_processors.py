from django.conf import settings as django_settings
from .models import SiteSettings, HeroMedia

def site_settings(request):
    settings = SiteSettings.objects.first()
    if not settings:
        settings = SiteSettings(
            site_name='Vinaigre du Maroc',
            phone='+212 5 35 12 34 56',
            email='export@vinaigredemaroc.com',
            address='Quartier Industriel Bensouda, Fès 30000, Morocco'
        )

    # Build hero media lookup: { 'home': <HeroMedia>, 'about': <HeroMedia>, ... }
    hero_backgrounds = {}
    for hero in HeroMedia.objects.all():
        hero_backgrounds[hero.page] = hero

    return {
        'site_settings': settings,
        'LANGUAGES': django_settings.LANGUAGES,
        'SITE_URL': django_settings.SITE_URL,
        'hero_backgrounds': hero_backgrounds,
    }
