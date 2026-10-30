# theme.py – centralized design tokens and stylesheets for HooverTron
from PyQt5 import QtCore, QtGui

# ---------------------------------------------------------------------------
# Design tokens
# ---------------------------------------------------------------------------

LIGHT = {
    # Surfaces
    "bg":            "#F4F6FA",
    "surface":       "#FFFFFF",
    "surface_alt":   "#F7F9FC",
    "surface_sunken":"#EEF1F6",
    "border":        "#E1E5EC",
    "border_emphasis": "#CBD2DC",
    "divider":       "#ECEEF2",

    # Text
    "text":          "#1B2330",
    "text_muted":    "#5A6473",
    "text_subtle":   "#8A93A2",
    "text_inverse":  "#FFFFFF",

    # Brand / states
    "primary":       "#2563EB",
    "primary_hover": "#1D4ED8",
    "primary_press": "#1E40AF",
    "primary_soft":  "#E0EAFF",

    "success":       "#16A34A",
    "success_soft":  "#DCFCE7",
    "warning":       "#D97706",
    "warning_soft":  "#FEF3C7",
    "danger":        "#DC2626",
    "danger_hover":  "#B91C1C",
    "danger_soft":   "#FEE2E2",

    # Graph
    "graph_bg":      "#FFFFFF",
    "graph_grid":    "#E6EAF0",
    "graph_axis":    "#A8B1BF",
    "graph_label":   "#2A3340",
    "graph_primary": "#2563EB",
    "graph_average": "#7280A0",
    "graph_region":  (37, 99, 235, 40),
}

DARK = {
    "bg":            "#0E1218",
    "surface":       "#161C25",
    "surface_alt":   "#1B232E",
    "surface_sunken":"#10151C",
    "border":        "#2A323F",
    "border_emphasis": "#3A4452",
    "divider":       "#222B36",

    "text":          "#E6EAF2",
    "text_muted":    "#A6B0BF",
    "text_subtle":   "#6E7889",
    "text_inverse":  "#0E1218",

    "primary":       "#60A5FA",
    "primary_hover": "#3B82F6",
    "primary_press": "#2563EB",
    "primary_soft":  "#1E2A44",

    "success":       "#34D399",
    "success_soft":  "#0F2A20",
    "warning":       "#FBBF24",
    "warning_soft":  "#2A1E08",
    "danger":        "#F87171",
    "danger_hover":  "#EF4444",
    "danger_soft":   "#2A1414",

    "graph_bg":      "#161C25",
    "graph_grid":    "#2A323F",
    "graph_axis":    "#525B6B",
    "graph_label":   "#D0D7E2",
    "graph_primary": "#60A5FA",
    "graph_average": "#94A3B8",
    "graph_region":  (96, 165, 250, 50),
}

# Spacing / radius scale – kept small for a native Windows feel
RADIUS_SM = 2
RADIUS_MD = 3
RADIUS_LG = 4

FONT_FAMILY = "'Segoe UI', 'Calibri', 'Arial', sans-serif"
FONT_FAMILY_DISPLAY = "'Segoe UI', 'Calibri', 'Arial', sans-serif"
FONT_FAMILY_MONO = "'Consolas', 'Cascadia Mono', 'Menlo', monospace"

_active_palette = LIGHT
_active_mode = "light"


def palette():
    return _active_palette


def mode():
    return _active_mode


def set_mode(new_mode):
    global _active_palette, _active_mode
    _active_mode = "dark" if new_mode == "dark" else "light"
    _active_palette = DARK if _active_mode == "dark" else LIGHT
    return _active_palette


# ---------------------------------------------------------------------------
# Cached chevron SVG written to disk so QSS `image: url(...)` can pick it up
# ---------------------------------------------------------------------------

import os
import tempfile

_chevron_paths = {}


def _chevron_svg(color_hex):
    return (
        "<?xml version='1.0' encoding='UTF-8'?>"
        "<svg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'>"
        f"<path d='M1 1 L5 5 L9 1' stroke='{color_hex}' stroke-width='1.6' "
        "stroke-linecap='round' stroke-linejoin='round' fill='none'/></svg>"
    )


def chevron_url(color_hex):
    """Write a small chevron SVG to a temp file and return a forward-slash path."""
    key = color_hex.lstrip("#").lower()
    if key in _chevron_paths and os.path.exists(_chevron_paths[key]):
        return _chevron_paths[key].replace("\\", "/")
    tmp_dir = os.path.join(tempfile.gettempdir(), "hoovertron_ui")
    os.makedirs(tmp_dir, exist_ok=True)
    path = os.path.join(tmp_dir, f"chevron_{key}.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(_chevron_svg(color_hex))
    _chevron_paths[key] = path
    return path.replace("\\", "/")


_icon_cache = {}


def _icon_path(name, svg_text):
    key = name
    if key in _icon_cache and os.path.exists(_icon_cache[key]):
        return _icon_cache[key].replace("\\", "/")
    tmp_dir = os.path.join(tempfile.gettempdir(), "hoovertron_ui")
    os.makedirs(tmp_dir, exist_ok=True)
    path = os.path.join(tmp_dir, f"{name}.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg_text)
    _icon_cache[key] = path
    return path.replace("\\", "/")


def caret_left_url(color_hex):
    svg = (
        "<?xml version='1.0' encoding='UTF-8'?>"
        "<svg xmlns='http://www.w3.org/2000/svg' width='8' height='12' viewBox='0 0 8 12'>"
        f"<path d='M6 1 L1 6 L6 11' stroke='{color_hex}' stroke-width='1.7' "
        "stroke-linecap='round' stroke-linejoin='round' fill='none'/></svg>"
    )
    return _icon_path(f"caret_left_{color_hex.lstrip('#').lower()}", svg)


def caret_right_url(color_hex):
    svg = (
        "<?xml version='1.0' encoding='UTF-8'?>"
        "<svg xmlns='http://www.w3.org/2000/svg' width='8' height='12' viewBox='0 0 8 12'>"
        f"<path d='M2 1 L7 6 L2 11' stroke='{color_hex}' stroke-width='1.7' "
        "stroke-linecap='round' stroke-linejoin='round' fill='none'/></svg>"
    )
    return _icon_path(f"caret_right_{color_hex.lstrip('#').lower()}", svg)


def fit_view_url(color_hex):
    """Four corners pointing outward – fits/auto-scale icon."""
    svg = (
        "<?xml version='1.0' encoding='UTF-8'?>"
        "<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'>"
        f"<g stroke='{color_hex}' stroke-width='1.6' stroke-linecap='round' "
        "stroke-linejoin='round' fill='none'>"
        "<path d='M2 6 L2 2 L6 2'/>"
        "<path d='M10 2 L14 2 L14 6'/>"
        "<path d='M14 10 L14 14 L10 14'/>"
        "<path d='M6 14 L2 14 L2 10'/>"
        "</g></svg>"
    )
    return _icon_path(f"fit_view_{color_hex.lstrip('#').lower()}", svg)


def calendar_stylesheet():
    """Stylesheet specifically for QCalendarWidget popups."""
    p = palette()
    prev_icon = caret_left_url(p["text"])
    next_icon = caret_right_url(p["text"])
    return f"""
        QCalendarWidget {{
            background-color: {p['surface']};
            color: {p['text']};
        }}
        QCalendarWidget QWidget {{
            alternate-background-color: {p['surface']};
        }}
        QCalendarWidget QWidget#qt_calendar_navigationbar {{
            background-color: {p['surface']};
            border: none;
            border-bottom: 1px solid {p['divider']};
            min-height: 36px;
        }}
        QCalendarWidget QToolButton {{
            background-color: transparent;
            color: {p['text']};
            border: 1px solid transparent;
            padding: 4px 10px;
            margin: 4px 2px;
            border-radius: 2px;
            font-size: 13px;
            font-weight: 500;
            min-width: 64px;
        }}
        QCalendarWidget QToolButton:hover {{
            background-color: {p['surface_sunken']};
            border-color: {p['border']};
        }}
        QCalendarWidget QToolButton::menu-indicator {{
            image: none;
            width: 0; height: 0;
        }}
        QCalendarWidget #qt_calendar_prevmonth {{
            qproperty-icon: url({prev_icon});
            qproperty-iconSize: 10px;
            min-width: 28px;
            max-width: 28px;
            padding: 0;
            margin: 4px 6px;
        }}
        QCalendarWidget #qt_calendar_nextmonth {{
            qproperty-icon: url({next_icon});
            qproperty-iconSize: 10px;
            min-width: 28px;
            max-width: 28px;
            padding: 0;
            margin: 4px 6px;
        }}
        QCalendarWidget QSpinBox {{
            background-color: {p['surface']};
            color: {p['text']};
            border: 1px solid {p['border']};
            padding: 2px 6px;
            min-height: 22px;
        }}
        QCalendarWidget QMenu {{
            background-color: {p['surface']};
            border: 1px solid {p['border']};
            padding: 4px;
        }}
        QCalendarWidget QMenu::item {{
            padding: 6px 18px;
            border-radius: 2px;
        }}
        QCalendarWidget QMenu::item:selected {{
            background: {p['primary_soft']};
            color: {p['primary']};
        }}
        QCalendarWidget QAbstractItemView {{
            background-color: {p['surface']};
            color: {p['text']};
            selection-background-color: {p['primary']};
            selection-color: {p['text_inverse']};
            outline: 0;
            font-size: 13px;
            gridline-color: transparent;
            padding: 4px;
        }}
        QCalendarWidget QAbstractItemView:enabled {{
            color: {p['text']};
        }}
        QCalendarWidget QAbstractItemView:disabled {{
            color: {p['text_subtle']};
        }}
        QCalendarWidget QTableView {{
            alternate-background-color: {p['surface']};
            border: none;
            selection-background-color: {p['primary']};
        }}
        QCalendarWidget QHeaderView::section {{
            background-color: {p['surface']};
            color: {p['text_muted']};
            padding: 6px 4px;
            border: none;
            font-weight: 500;
            font-size: 11px;
            text-transform: uppercase;
        }}
    """


# ---------------------------------------------------------------------------
# Stylesheet builder
# ---------------------------------------------------------------------------

def build_stylesheet(p=None):
    p = p or palette()
    return f"""
        QMainWindow, QWidget#centralwidget {{
            background-color: {p['bg']};
        }}
        QWidget {{
            font-family: {FONT_FAMILY};
            font-size: 14px;
            color: {p['text']};
        }}
        QLabel#appTitle {{
            font-family: {FONT_FAMILY_DISPLAY};
            font-size: 18px;
            font-weight: 600;
            color: {p['text']};
        }}

        /* ---- Menu bar ---- */
        QMenuBar {{
            background-color: {p['surface']};
            border-bottom: 1px solid {p['border']};
            padding: 4px 6px;
            color: {p['text']};
        }}
        QMenuBar::item {{
            background: transparent;
            padding: 6px 12px;
            border-radius: {RADIUS_SM}px;
        }}
        QMenuBar::item:selected {{
            background: {p['primary_soft']};
            color: {p['primary']};
        }}
        QMenu {{
            background-color: {p['surface']};
            border: 1px solid {p['border']};
            border-radius: {RADIUS_MD}px;
            padding: 6px;
            color: {p['text']};
        }}
        QMenu::item {{
            padding: 7px 22px 7px 22px;
            border-radius: {RADIUS_SM}px;
        }}
        QMenu::item:selected {{
            background: {p['primary_soft']};
            color: {p['primary']};
        }}
        QMenu::separator {{
            height: 1px;
            background: {p['divider']};
            margin: 6px 4px;
        }}

        QStatusBar {{
            background: {p['surface']};
            border-top: 1px solid {p['border']};
            color: {p['text_muted']};
        }}

        /* ---- Horizontal tab bar ---- */
        QTabWidget::pane {{
            background: {p['surface']};
            border: 1px solid {p['border_emphasis']};
            border-radius: {RADIUS_SM}px;
            top: -1px;
        }}
        QTabWidget::tab-bar {{
            alignment: left;
            left: 0px;
        }}
        QTabBar {{
            background: transparent;
            qproperty-drawBase: 0;
        }}
        QTabBar::tab {{
            background: {p['surface']};
            color: {p['text']};
            border: 1px solid {p['border_emphasis']};
            border-bottom: 1px solid {p['border_emphasis']};
            padding: 9px 22px;
            margin: 0 -1px 0 0;
            font-family: {FONT_FAMILY};
            font-size: 14px;
            font-weight: 400;
            min-width: 130px;
        }}
        QTabBar::tab:first {{
            border-top-left-radius: {RADIUS_SM}px;
        }}
        QTabBar::tab:last {{
            border-top-right-radius: {RADIUS_SM}px;
            margin-right: 0;
        }}
        QTabBar::tab:hover {{
            background: {p['surface_sunken']};
        }}
        QTabBar::tab:selected {{
            background: {p['surface']};
            color: {p['primary']};
            border: 1px solid {p['border_emphasis']};
            border-bottom-color: {p['surface']};
            font-weight: 500;
        }}

        /* ---- Buttons ---- */
        QPushButton {{
            background-color: {p['primary']};
            color: {p['text_inverse']};
            border: none;
            padding: 9px 18px;
            border-radius: {RADIUS_SM}px;
            font-weight: 500;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {p['primary_hover']};
        }}
        QPushButton:pressed {{
            background-color: {p['primary_press']};
        }}
        QPushButton:disabled {{
            background-color: {p['surface_sunken']};
            color: {p['text_subtle']};
        }}

        QPushButton[variant="ghost"] {{
            background: transparent;
            color: {p['text_muted']};
            border: 1px solid {p['border']};
        }}
        QPushButton[variant="ghost"]:hover {{
            background: {p['surface_sunken']};
            color: {p['text']};
        }}
        QPushButton[variant="ghost"]:disabled {{
            background: {p['surface_sunken']};
            color: {p['text_subtle']};
            border-color: {p['border']};
        }}

        QPushButton[variant="danger"] {{
            background-color: {p['danger']};
            color: {p['text_inverse']};
        }}
        QPushButton[variant="danger"]:hover {{
            background-color: {p['danger_hover']};
        }}

        QPushButton[variant="success"] {{
            background-color: {p['success']};
            color: {p['text_inverse']};
        }}

        QPushButton[variant="record"] {{
            background-color: {p['success']};
            color: {p['text_inverse']};
            padding: 10px 22px;
        }}
        QPushButton[variant="record"]:checked {{
            background-color: {p['danger']};
        }}

        QPushButton[variant="hero"] {{
            background-color: {p['primary']};
            color: {p['text_inverse']};
            font-size: 14px;
            font-weight: 500;
            padding: 9px 18px;
            border-radius: {RADIUS_SM}px;
        }}
        QPushButton[variant="hero"]:hover {{
            background-color: {p['primary_hover']};
        }}

        /* ---- Inputs ---- */
        QLineEdit, QComboBox, QDateEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox {{
            background-color: {p['surface']};
            color: {p['text']};
            border: 1px solid {p['border']};
            border-radius: {RADIUS_SM}px;
            padding: 7px 10px;
            font-size: 14px;
            min-height: 22px;
            selection-background-color: {p['primary_soft']};
            selection-color: {p['primary_press']};
        }}
        QTextEdit, QPlainTextEdit {{
            min-height: 60px;
        }}
        QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTextEdit:focus {{
            border: 1px solid {p['primary']};
        }}
        QLineEdit:read-only, QTextEdit:read-only {{
            background-color: {p['surface_sunken']};
            color: {p['text_muted']};
        }}
        QLineEdit:disabled, QTextEdit:disabled {{
            background-color: {p['surface_sunken']};
            color: {p['text_subtle']};
        }}

        QComboBox::drop-down, QDateEdit::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: center right;
            width: 22px;
            border: none;
            background: transparent;
        }}
        QComboBox::down-arrow, QDateEdit::down-arrow {{
            image: url({chevron_url(p['text_muted'])});
            width: 10px;
            height: 6px;
            margin-right: 8px;
        }}
        QComboBox::down-arrow:on, QDateEdit::down-arrow:on {{
            image: url({chevron_url(p['primary'])});
        }}
        QComboBox QAbstractItemView {{
            background: {p['surface']};
            color: {p['text']};
            border: 1px solid {p['border']};
            border-radius: {RADIUS_SM}px;
            selection-background-color: {p['primary_soft']};
            selection-color: {p['primary']};
            padding: 4px;
            outline: 0;
        }}

        /* ---- Calendar popup ---- */
        QCalendarWidget {{
            background-color: {p['surface']};
            color: {p['text']};
        }}
        QCalendarWidget QWidget {{
            alternate-background-color: {p['surface']};
        }}
        QCalendarWidget QWidget#qt_calendar_navigationbar {{
            background-color: {p['surface']};
            border-bottom: 1px solid {p['border']};
            min-height: 32px;
        }}
        QCalendarWidget QToolButton {{
            background-color: transparent;
            color: {p['text']};
            border: none;
            padding: 4px 8px;
            margin: 4px 2px;
            border-radius: {RADIUS_SM}px;
            font-size: 13px;
            font-weight: 500;
        }}
        QCalendarWidget QToolButton:hover {{
            background-color: {p['surface_sunken']};
        }}
        QCalendarWidget QToolButton::menu-indicator {{
            image: none;
        }}
        QCalendarWidget QSpinBox {{
            background-color: {p['surface']};
            color: {p['text']};
            border: 1px solid {p['border']};
            padding: 2px 6px;
            min-height: 22px;
        }}
        QCalendarWidget QMenu {{
            background-color: {p['surface']};
            border: 1px solid {p['border']};
        }}
        QCalendarWidget QAbstractItemView {{
            background-color: {p['surface']};
            color: {p['text']};
            selection-background-color: {p['primary']};
            selection-color: {p['text_inverse']};
            outline: 0;
            font-size: 13px;
            gridline-color: {p['surface']};
        }}
        QCalendarWidget QAbstractItemView:enabled {{
            color: {p['text']};
        }}
        QCalendarWidget QAbstractItemView:disabled {{
            color: {p['text_subtle']};
        }}
        QCalendarWidget QTableView {{
            alternate-background-color: {p['surface']};
            border: none;
        }}
        QCalendarWidget QHeaderView::section {{
            background-color: {p['surface']};
            color: {p['text_muted']};
            padding: 6px 4px;
            border: none;
            border-bottom: 1px solid {p['divider']};
            font-weight: 500;
            font-size: 12px;
        }}

        /* ---- Group boxes / cards ---- */
        QGroupBox {{
            font-weight: 500;
            color: {p['text']};
            background-color: {p['surface']};
            border: 1px solid {p['border']};
            border-radius: {RADIUS_MD}px;
            margin-top: 14px;
            padding: 18px 14px 14px 14px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 10px;
            left: 8px;
            background: transparent;
            color: {p['text_muted']};
            font-size: 12px;
        }}

        QFrame[card="true"] {{
            background-color: {p['surface']};
            border: 1px solid {p['border']};
            border-radius: {RADIUS_LG}px;
        }}
        QFrame[card="muted"] {{
            background-color: {p['surface_alt']};
            border: 1px solid {p['border']};
            border-radius: {RADIUS_MD}px;
        }}
        QFrame[role="divider"] {{
            background: {p['divider']};
            max-height: 1px;
            min-height: 1px;
            border: none;
        }}
        QFrame[role="vdivider"] {{
            background: {p['divider']};
            max-width: 1px;
            min-width: 1px;
            border: none;
        }}

        QLabel[role="title"] {{
            font-size: 20px;
            font-weight: 600;
            color: {p['text']};
        }}
        QLabel[role="subtitle"] {{
            font-size: 13px;
            color: {p['text_muted']};
        }}
        QLabel[role="eyebrow"] {{
            font-size: 12px;
            font-weight: 500;
            color: {p['text_subtle']};
        }}
        QLabel[role="metric"] {{
            font-size: 28px;
            font-weight: 600;
            color: {p['text']};
        }}
        QLabel[role="metric-unit"] {{
            font-size: 13px;
            color: {p['text_muted']};
        }}
        QLabel[role="metric-label"] {{
            font-size: 12px;
            font-weight: 500;
            color: {p['text_subtle']};
        }}
        QLabel[role="row-label"] {{
            font-size: 13px;
            font-weight: 400;
            color: {p['text_muted']};
        }}
        QLineEdit[role="row-value"] {{
            font-size: 13px;
            font-weight: 500;
            color: {p['text']};
        }}

        /* Tab corner buttons sit visually inside the tab bar ------------- */
        QWidget#tabCornerActions {{
            background: transparent;
        }}
        QWidget#tabCornerActions QPushButton {{
            background-color: {p['primary']};
            color: {p['text_inverse']};
            padding: 0;
            margin: 0;
            border: 1px solid {p['primary']};
            border-radius: {RADIUS_SM}px;
            font-size: 14px;
            font-weight: 500;
        }}
        QWidget#tabCornerActions QPushButton:hover {{
            background-color: {p['primary_hover']};
            border-color: {p['primary_hover']};
        }}
        QWidget#tabCornerActions QPushButton:pressed {{
            background-color: {p['primary_press']};
            border-color: {p['primary_press']};
        }}
        QWidget#tabCornerActions QPushButton[variant="ghost"] {{
            background: transparent;
            color: {p['text_muted']};
            border: 1px solid {p['border']};
        }}
        QWidget#tabCornerActions QPushButton[variant="ghost"]:hover {{
            background: {p['surface_sunken']};
            color: {p['text']};
        }}
        QWidget#tabCornerActions QPushButton[variant="ghost"]:disabled {{
            background: {p['surface_sunken']};
            color: {p['text_subtle']};
            border-color: {p['border']};
        }}

        QScrollBar:vertical {{
            background: transparent;
            width: 10px;
            margin: 4px;
        }}
        QScrollBar::handle:vertical {{
            background: {p['border_emphasis']};
            border-radius: 4px;
            min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{ background: {p['text_subtle']}; }}
        QScrollBar::add-line, QScrollBar::sub-line {{ background: none; height: 0; }}
        QScrollBar:horizontal {{
            background: transparent;
            height: 10px;
            margin: 4px;
        }}
        QScrollBar::handle:horizontal {{
            background: {p['border_emphasis']};
            border-radius: 4px;
            min-width: 30px;
        }}
        QScrollBar::handle:horizontal:hover {{ background: {p['text_subtle']}; }}

        QToolTip {{
            background-color: {p['surface_alt']};
            color: {p['text']};
            border: 1px solid {p['border']};
            padding: 6px 8px;
            border-radius: {RADIUS_SM}px;
        }}
    """


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def apply_property(widget, name, value):
    """Set a Qt dynamic property and re-polish the widget so QSS reflects it."""
    widget.setProperty(name, value)
    style = widget.style()
    style.unpolish(widget)
    style.polish(widget)
    widget.update()


def chip_style(color_key="primary", soft=True):
    p = palette()
    soft_key = f"{color_key}_soft"
    if soft and soft_key in p:
        bg = p[soft_key]
        fg = p.get(color_key, p["text"])
    else:
        bg = p.get(color_key, p["surface_sunken"])
        if color_key in ("text_subtle", "text_muted"):
            # Soft chip rendered on a neutral background
            bg = p["surface_sunken"]
            fg = p[color_key]
        else:
            fg = p["text_inverse"]
    return (
        f"background-color: {bg}; color: {fg}; "
        f"border-radius: 999px; padding: 4px 12px; "
        f"font-weight: 500; font-size: 12px;"
    )


def font(size=14, weight=QtGui.QFont.Normal, italic=False):
    f = QtGui.QFont("Segoe UI")
    f.setPixelSize(size)
    f.setWeight(weight)
    f.setItalic(italic)
    return f
