from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.simple_tag
def render_packaging_icon(pkg_name):
    """
    Renders a custom SVG icon for vinaigre_de_maroc packaging formats.
    """
    name_lower = pkg_name.lower()
    
    # Extract volume if present
    volume_match = re.search(r'(\d+)\s*(l|ml)?', name_lower)
    volume_num = int(volume_match.group(1)) if volume_match else 0
    volume_unit = volume_match.group(2) if volume_match and volume_match.group(2) else ''
    volume_str = f"{volume_num}{volume_unit.upper()}" if volume_num else ""

    if 'glass' in name_lower or 'verre' in name_lower or 'glass' in name_lower:
        # Glass Bottle
        color_lid = "#b5944b" # Gold/Bronze
        color_glass = "#e8f4f8"
        svg = f"""
        <svg class="pkg-icon-svg" viewBox="0 0 48 48" style="width: 100%; height: 100%;" xmlns="http://www.w3.org/2000/svg">
            <g transform="translate(12, 3)">
                <!-- Cap -->
                <rect x="8" y="1" width="8" height="4" rx="1" fill="{color_lid}" stroke="#7e6328" stroke-width="0.75"/>
                <!-- Neck -->
                <rect x="9" y="5" width="6" height="7" fill="{color_glass}" stroke="#b0d0e0" stroke-width="1.25"/>
                <!-- Body -->
                <path d="M 9,12 C 4,14 1,18 1,24 L 1,38 C 1,40.5 3,42 5,42 L 19,42 C 21,42 23,40.5 23,38 L 23,24 C 23,18 20,14 15,12 Z" fill="{color_glass}" stroke="#b0d0e0" stroke-width="1.75"/>
                <!-- Label -->
                <rect x="4" y="20" width="16" height="12" rx="1.5" fill="#581825" fill-opacity="0.85"/>
                <line x1="7" y1="26" x2="17" y2="26" stroke="#b5944b" stroke-width="1"/>
                <!-- Shine -->
                <path d="M 4,16 L 4,36" stroke="#ffffff" stroke-width="1.25" stroke-linecap="round" fill="none"/>
            </g>
        </svg>
        """
    elif 'ibc' in name_lower:
        # IBC Tank
        svg = """
        <svg class="pkg-icon-svg" viewBox="0 0 48 48" style="width: 100%; height: 100%;" xmlns="http://www.w3.org/2000/svg">
            <g transform="translate(2, 2)">
                <!-- Steel Cage Grid -->
                <rect x="5" y="7" width="34" height="30" rx="3" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.75"/>
                <line x1="5" y1="15" x2="39" y2="15" stroke="#94a3b8" stroke-width="1.25"/>
                <line x1="5" y1="23" x2="39" y2="23" stroke="#94a3b8" stroke-width="1.25"/>
                <line x1="5" y1="31" x2="39" y2="31" stroke="#94a3b8" stroke-width="1.25"/>
                <line x1="13" y1="7" x2="13" y2="37" stroke="#94a3b8" stroke-width="1.25"/>
                <line x1="22" y1="7" x2="22" y2="37" stroke="#94a3b8" stroke-width="1.25"/>
                <line x1="31" y1="7" x2="31" y2="37" stroke="#94a3b8" stroke-width="1.25"/>
                <!-- HDPE Tank -->
                <rect x="7" y="9" width="30" height="26" rx="2" fill="#ffffff" fill-opacity="0.75"/>
                <!-- Cap/Valve -->
                <rect x="19" y="4" width="6" height="3" fill="#581825" />
                <rect x="20" y="34" width="4" height="4" fill="#e11d48" />
                <!-- Pallet base -->
                <rect x="7" y="37" width="30" height="3" fill="#78350f" />
            </g>
        </svg>
        """
    else:
        # PET Bottle / Jug / Plastic Jar / Box fallback
        # Let's render a clean PET Jug SVG
        color_body = "#f0fdf4"
        color_cap = "#581825"
        has_handle = volume_num >= 2 # 2L and 5L PET have handles
        
        svg = f"""
        <svg class="pkg-icon-svg" viewBox="0 0 48 48" style="width: 100%; height: 100%;" xmlns="http://www.w3.org/2000/svg">
            <g transform="translate(10, 4)">
                <!-- Cap -->
                <rect x="8" y="1" width="12" height="5" rx="1" fill="{color_cap}" stroke="#47141e" stroke-width="0.5"/>
                <!-- Body -->
                <path d="M 8,6 L 20,6 L 22,11 L 25,11 C 26.5,11 27,12 27,13.5 L 27,39 C 27,41 25.5,42 24,42 L 4,42 C 2.5,42 1,41 1,39 L 1,13.5 C 1,12 1.5,11 3,11 L 6,11 Z" fill="{color_body}" stroke="#a7f3d0" stroke-width="1.75"/>
        """
        if has_handle:
            svg += f"""
                <!-- Handle -->
                <path d="M 23,15 L 23,28 C 26.5,28 26.5,15 23,15" fill="none" stroke="#a7f3d0" stroke-width="2.5" stroke-linecap="round"/>
            """
        svg += f"""
                <!-- Rib details -->
                <line x1="5" y1="16" x2="23" y2="16" stroke="#a7f3d0" stroke-width="1.25"/>
                <line x1="5" y1="22" x2="23" y2="22" stroke="#a7f3d0" stroke-width="1.25"/>
                <line x1="5" y1="28" x2="23" y2="28" stroke="#a7f3d0" stroke-width="1.25"/>
                <line x1="5" y1="34" x2="23" y2="34" stroke="#a7f3d0" stroke-width="1.25"/>
            </g>
        </svg>
        """
    return mark_safe(svg)
