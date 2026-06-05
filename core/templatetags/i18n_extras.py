from django import template
from django.urls import translate_url as django_translate_url, reverse
from django.utils.translation import override as lang_override
import urllib.parse

register = template.Library()

@register.simple_tag(takes_context=True)
def translate_url(context, lang_code):
    """
    Returns the current page URL translated to the given language code.
    For detail pages, it retrieves the translated slug to create clean internationalized URLs.
    """
    request = context.get('request')
    if request is None:
        return '/{}/'.format(lang_code)

    resolver_match = getattr(request, 'resolver_match', None)
    if resolver_match and 'slug' in (resolver_match.kwargs or {}):
        url_name = resolver_match.url_name
        current_slug = resolver_match.kwargs['slug']

        try:
            if url_name == 'product_detail':
                from core.models import Product
                from django.db.models import Q
                obj = Product.objects.filter(
                    Q(slug=current_slug) | Q(slug_fr=current_slug) |
                    Q(slug_ar=current_slug) | Q(slug_es=current_slug) |
                    Q(slug_it=current_slug)
                ).first()
                if obj:
                    translated_slug = _get_slug_for_lang(obj, lang_code)
                    with lang_override(lang_code):
                        res = reverse('product_detail', kwargs={'slug': translated_slug})
                        return urllib.parse.quote(res, safe='/=&?%#+')

            elif url_name == 'blog_detail':
                from core.models import BlogPost
                from django.db.models import Q
                obj = BlogPost.objects.filter(
                    Q(slug=current_slug) | Q(slug_fr=current_slug) |
                    Q(slug_ar=current_slug) | Q(slug_es=current_slug) |
                    Q(slug_it=current_slug)
                ).first()
                if obj:
                    translated_slug = _get_slug_for_lang(obj, lang_code)
                    with lang_override(lang_code):
                        res = reverse('blog_detail', kwargs={'slug': translated_slug})
                        return urllib.parse.quote(res, safe='/=&?%#+')
        except Exception:
            pass

    # Default: translate static URL paths
    current_url = request.get_full_path()
    translated = django_translate_url(current_url, lang_code)
    return urllib.parse.quote(translated, safe='/=&?%#+')


def _get_slug_for_lang(obj, lang_code):
    clean_lang = lang_code.lower().replace('-', '_')
    slug = getattr(obj, f'slug_{clean_lang}', None)
    if slug:
        return slug
    slug = getattr(obj, 'slug_en', None)
    if slug:
        return slug
    return obj.slug


@register.filter
def url_encode_path(value):
    if not value:
        return ""
    return urllib.parse.quote(value, safe='/')


@register.filter
def translate_field(obj, field_name):
    """
    Returns the dynamic translated value of a field.
    Usage: {{ product|translate_field:'name' }}
    """
    from django.utils.translation import get_language
    lang = get_language()
    clean_lang = lang.lower().replace('-', '_')

    # Try target language field (e.g. name_fr)
    val = getattr(obj, f"{field_name}_{clean_lang}", None)
    if val:
        return val

    # Fallback to English field (e.g. name_en)
    val = getattr(obj, f"{field_name}_en", None)
    if val:
        return val

    # Base fallback
    return getattr(obj, field_name, "")
