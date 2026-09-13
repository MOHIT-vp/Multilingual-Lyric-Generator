"""SVG icon definitions and image asset utilities for KPR website."""

import base64
import os

# ---------------------------------------------------------------------------
# SVG Icons
# ---------------------------------------------------------------------------

ICON_KPR_MARK = '''<svg viewBox="0 0 39 39" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M0 0H15.6V15.6H0V0Z" fill="currentColor"/>
  <path d="M0 23.4H15.6V39H0V23.4Z" fill="currentColor"/>
  <path d="M23.4 0H39V15.6H23.4V0Z" fill="currentColor"/>
  <path d="M19.5 19.5L39 39H23.4L15.6 31.2V23.4L19.5 19.5Z" fill="currentColor"/>
</svg>'''

ICON_KPR_WORDMARK = '''<svg viewBox="0 0 200 30" fill="none" xmlns="http://www.w3.org/2000/svg">
  <text x="0" y="24" font-family="'Inter','ABCWhytePlus',sans-serif" font-weight="800" font-size="28" letter-spacing="-2" fill="currentColor">KEEPERS</text>
</svg>'''

ICON_HAMBURGER = '''<svg width="27" height="6" viewBox="0 0 27 6" fill="none" xmlns="http://www.w3.org/2000/svg">
  <line y1="0.5" x2="27" y2="0.5" stroke="currentColor"/>
  <line y1="5.5" x2="27" y2="5.5" stroke="currentColor"/>
</svg>'''

ICON_CLOSE = '''<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
  <line x1="1" y1="1" x2="19" y2="19" stroke="currentColor" stroke-width="1"/>
  <line x1="19" y1="1" x2="1" y2="19" stroke="currentColor" stroke-width="1"/>
</svg>'''

ICON_ARROW_DOWN = '''<svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M7 1V13M7 13L1 7M7 13L13 7" stroke="currentColor" stroke-width="1"/>
</svg>'''

ICON_ARROW_UP = '''<svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M7 13V1M7 1L1 7M7 1L13 7" stroke="currentColor" stroke-width="1"/>
</svg>'''

ICON_SCROLL_ARROW = '''<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
  <line x1="3" y1="3" x2="17" y2="17" stroke="currentColor" stroke-width="1"/>
  <line x1="17" y1="7" x2="17" y2="17" stroke="currentColor" stroke-width="1"/>
  <line x1="7" y1="17" x2="17" y2="17" stroke="currentColor" stroke-width="1"/>
</svg>'''

ICON_PLAY = '''<svg width="60" height="60" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="30" cy="30" r="28" stroke="currentColor" stroke-width="1.5" fill="none"/>
  <polygon points="24,18 42,30 24,42" fill="currentColor"/>
</svg>'''

ICON_CROSSHAIR = '''<svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="20" cy="20" r="8" stroke="currentColor" stroke-width="1" fill="none"/>
  <line x1="20" y1="0" x2="20" y2="12" stroke="currentColor" stroke-width="1"/>
  <line x1="20" y1="28" x2="20" y2="40" stroke="currentColor" stroke-width="1"/>
  <line x1="0" y1="20" x2="12" y2="20" stroke="currentColor" stroke-width="1"/>
  <line x1="28" y1="20" x2="40" y2="20" stroke="currentColor" stroke-width="1"/>
</svg>'''

ICON_CONSOLE = '''<svg width="20" height="16" viewBox="0 0 20 16" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="0.5" y="0.5" width="19" height="15" rx="1" stroke="currentColor" fill="none"/>
  <polyline points="3,5 7,8 3,11" stroke="currentColor" stroke-width="1" fill="none"/>
  <line x1="9" y1="11" x2="15" y2="11" stroke="currentColor" stroke-width="1"/>
</svg>'''

ICON_DOUBLE_ARROW = '''<svg width="16" height="12" viewBox="0 0 16 12" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M0 6L5 0V12L0 6Z" fill="currentColor"/>
  <path d="M6 6L11 0V12L6 6Z" fill="currentColor"/>
</svg>'''

ICON_OPENSEA = '''<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="10" cy="10" r="9" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M5 11L10 6L12 9L15 8" stroke="currentColor" stroke-width="1" fill="none"/>
</svg>'''

ICON_TWITTER = '''<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
  <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
</svg>'''

ICON_DISCORD = '''<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
  <path d="M20.317 4.37a19.791 19.791 0 00-4.885-1.515.074.074 0 00-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 00-5.487 0 12.64 12.64 0 00-.617-1.25.077.077 0 00-.079-.037A19.736 19.736 0 003.677 4.37a.07.07 0 00-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 00.031.057 19.9 19.9 0 005.993 3.03.078.078 0 00.084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 00-.041-.106 13.107 13.107 0 01-1.872-.892.077.077 0 01-.008-.128 10.2 10.2 0 00.372-.292.074.074 0 01.077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 01.078.01c.12.098.246.198.373.292a.077.077 0 01-.006.127 12.299 12.299 0 01-1.873.892.077.077 0 00-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 00.084.028 19.839 19.839 0 006.002-3.03.077.077 0 00.032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 00-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.095 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.095 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/>
</svg>'''

ICON_DOWNLOAD = '''<svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M7 1V10M7 10L3 6M7 10L11 6" stroke="currentColor" stroke-width="1"/>
  <line x1="1" y1="13" x2="13" y2="13" stroke="currentColor" stroke-width="1"/>
</svg>'''


# ---------------------------------------------------------------------------
# Image loading utility
# ---------------------------------------------------------------------------

def _get_static_dir():
    """Get path to the static directory."""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")


def load_image_base64(filename: str) -> str:
    """Load an image from static/ and return as base64 data URI."""
    filepath = os.path.join(_get_static_dir(), filename)
    if not os.path.exists(filepath):
        # Return a 1px transparent placeholder
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    
    with open(filepath, "rb") as f:
        data = f.read()
    
    ext = filename.rsplit(".", 1)[-1].lower()
    mime = {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "webp": "image/webp",
        "svg": "image/svg+xml",
        "gif": "image/gif",
    }.get(ext, "image/png")
    
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"


def get_all_images() -> dict:
    """Load all image assets and return as dict of base64 data URIs.
    
    Uses compressed JPEG versions for much smaller HTML output.
    """
    images = {
        "keeper_hero": load_image_base64("keeper_hero.jpg"),
        "keeper_gallery": load_image_base64("keeper_gallery.jpg"),
        "cityscape": load_image_base64("cityscape.jpg"),
        "kai_crystal": load_image_base64("kai_crystal.jpg"),
        "keeper_eye": load_image_base64("keeper_eye.jpg"),
        "world_temple": load_image_base64("world_temple.jpg"),
        "keeper_side": load_image_base64("keeper_side.jpg"),
    }
    return images
