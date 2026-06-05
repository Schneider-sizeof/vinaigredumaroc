from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def render_certification_icon(cert_code):
    """
    Renders a premium custom SVG logo for certification boards (BRCGS, IFS, HALAL, KOSHER, FDA).
    """
    code = cert_code.upper()

    if code == 'BRCGS' or code == 'BRC':
        # BRCGS Shield Logo
        svg = """
        <svg class="cert-icon-svg" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" style="width: 100%; height: 100%;">
            <path d="M50 12 L82 22 L82 52 C82 70 68 82 50 88 C32 82 18 70 18 52 L18 22 L50 12 Z" fill="#581825" stroke="#FFFFFF" stroke-width="1.5"/>
            <path d="M40 52 L47 59 L63 43" stroke="#b5944b" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
            <text x="50" y="36" fill="#FFFFFF" font-family="'Inter', 'Outfit', sans-serif" font-weight="900" font-size="12" text-anchor="middle" letter-spacing="0.5">BRCGS</text>
        </svg>
        """
    elif code == 'IFS':
        # IFS Food Logo
        svg = """
        <svg class="cert-icon-svg" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" style="width: 100%; height: 100%;">
            <circle cx="50" cy="50" r="42" fill="#0b3c2a" stroke="#FFFFFF" stroke-width="1.5"/>
            <path d="M38 52 L46 60 L64 42" stroke="#b5944b" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
            <text x="50" y="32" fill="#FFFFFF" font-family="'Inter', 'Outfit', sans-serif" font-weight="900" font-size="14" text-anchor="middle">IFS</text>
            <text x="50" y="78" fill="#FFFFFF" font-family="'Inter', 'Outfit', sans-serif" font-weight="bold" font-size="9" text-anchor="middle" letter-spacing="1">FOOD</text>
        </svg>
        """
    elif code == 'HALAL':
        # Clean green circular Halal certification stamp (with Arabic and English text)
        svg = """
        <svg class="cert-icon-svg" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" style="width: 100%; height: 100%;">
            <circle cx="50" cy="50" r="42" fill="#1e4620" stroke="#FFFFFF" stroke-width="1.5"/>
            <circle cx="50" cy="50" r="36" stroke="#b5944b" stroke-width="1.25" stroke-dasharray="3,3"/>
            <text x="50" y="47" fill="#FFFFFF" font-family="'Inter', 'Outfit', 'Amiri', sans-serif" font-weight="900" font-size="22" text-anchor="middle">حلال</text>
            <text x="50" y="70" fill="#b5944b" font-family="'Inter', 'Outfit', sans-serif" font-weight="900" font-size="10.5" text-anchor="middle" letter-spacing="1">HALAL</text>
        </svg>
        """
    elif code == 'KOSHER':
        # Blue circle with bold circular 'K' Kosher symbol
        svg = """
        <svg class="cert-icon-svg" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" style="width: 100%; height: 100%;">
            <circle cx="50" cy="50" r="42" fill="#0d3b66" stroke="#FFFFFF" stroke-width="1.5"/>
            <circle cx="50" cy="46" r="21" stroke="#b5944b" stroke-width="2"/>
            <text x="50" y="54" fill="#FFFFFF" font-family="'Inter', 'Outfit', sans-serif" font-weight="900" font-size="23" text-anchor="middle">K</text>
            <text x="50" y="78" fill="#FFFFFF" font-family="'Inter', 'Outfit', sans-serif" font-weight="bold" font-size="8" text-anchor="middle" letter-spacing="1.5">KOSHER</text>
        </svg>
        """
    elif code == 'FDA':
        # Official-looking gray/blue rectangular FDA Registered facility badge
        svg = """
        <svg class="cert-icon-svg" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" style="width: 100%; height: 100%;">
            <rect x="12" y="12" width="76" height="76" rx="10" fill="#333333" stroke="#FFFFFF" stroke-width="1.5"/>
            <text x="50" y="47" fill="#FFFFFF" font-family="'Inter', 'Outfit', sans-serif" font-weight="900" font-size="26" text-anchor="middle">FDA</text>
            <line x1="22" y1="57" x2="78" y2="57" stroke="#b5944b" stroke-width="1.5"/>
            <text x="50" y="73" fill="#b5944b" font-family="'Inter', 'Outfit', sans-serif" font-weight="bold" font-size="7.5" text-anchor="middle" letter-spacing="0.75">REGISTERED</text>
        </svg>
        """
    else:
        # Standard fallback medal
        svg = """
        <svg class="cert-icon-svg" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" style="width: 100%; height: 100%;">
            <circle cx="50" cy="50" r="42" fill="#581825" stroke="#FFFFFF" stroke-width="1.5"/>
            <path d="M40 52 L47 59 L63 43" stroke="#b5944b" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        """

    return mark_safe(svg)
