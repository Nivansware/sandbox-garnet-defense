"""
Presentation Theme Tokens
Menerapkan doktrin Premium SaaS Aesthetics & Color Palette sesuai GYM-Absence-member.md:
- Primary colour: #c00707 (Wine Red)
- Secondary colour: #df9e12 (Amber Gold)
- Dark mode BG: #292929
"""

class GymTheme:
    # Core Colors
    BG_MAIN = "#292929"         # Dark mode main background
    BG_SURFACE = "#1f1f1f"      # Deeper container surface
    BG_CARD = "#343434"         # Bento card surface
    BG_INPUT = "#222222"        # Input fields

    # Brand Colors
    PRIMARY = "#c00707"         # Primary Wine Red
    PRIMARY_HOVER = "#990505"   # Primary darker state
    SECONDARY = "#df9e12"       # Secondary Amber Gold
    SECONDARY_HOVER = "#b8820c" # Secondary darker state

    # Semantic Status Colors
    STATUS_ACTIVE_BG = "#2a3b2a"
    STATUS_ACTIVE_TEXT = "#4ade80" # Fresh neon green
    STATUS_INACTIVE_BG = "#3d2525"
    STATUS_INACTIVE_TEXT = "#f87171" # Soft red

    # Neutral Accents & Borders
    BORDER_COLOR = "#444444"
    BORDER_FOCUSED = "#df9e12"
    TEXT_PRIMARY = "#f9f9f9"
    TEXT_MUTED = "#a3a3a3"
    TEXT_DARK = "#121212"

    # Typography
    FONT_FAMILY = "Segoe UI"
    FONT_TITLE = ("Segoe UI", 20, "bold")
    FONT_SUBTITLE = ("Segoe UI", 13, "bold")
    FONT_BODY = ("Segoe UI", 12)
    FONT_BODY_BOLD = ("Segoe UI", 12, "bold")
    FONT_HERO_NUM = ("Segoe UI", 28, "bold")
    FONT_BADGE = ("Segoe UI", 11, "bold")
