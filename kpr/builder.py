"""HTML builder that assembles the complete KPR website."""

from kpr.assets import get_all_images
from kpr.styles import get_css
from kpr.scripts import get_js
from kpr.sections import get_all_sections


def build_kpr_html() -> str:
    """Build and return the complete KPR website HTML document.
    
    Returns a self-contained HTML string with embedded CSS, JS, fonts,
    GSAP, Three.js, and all section content. This is rendered inside
    a Streamlit components.html() iframe.
    """
    images = get_all_images()
    css = get_css()
    sections = get_all_sections(images)
    js = get_js()

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="KPR - Keepers. Keep. Protect. Reimagine. A collective narrative NFT project set in a cyberpunk solarpunk world.">
    <title>KPR — Keepers</title>

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">

    <style>
{css}
    </style>
</head>
<body>
{sections}

    <!-- GSAP + ScrollTrigger -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
    <!-- Three.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r150/three.min.js"></script>

    <script>
{js}
    </script>
</body>
</html>'''

    return html
