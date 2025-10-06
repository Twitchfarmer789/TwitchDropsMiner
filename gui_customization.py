# gui_customization.py
# Starter module for GUI customization options (theme, layout, preferences)
import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field

GUI_CONFIG_FILE = 'gui_config.json'

@dataclass
class GUICustomization:
    """Stores GUI customization settings."""
    # Theme settings
    theme: str = 'default'  # 'default', 'dark', 'light'
    font_size: int = 12
    font_family: Optional[str] = None  # None means system default
    
    # Layout settings
    window_width: int = 800
    window_height: int = 600
    window_x: Optional[int] = None
    window_y: Optional[int] = None
    
    # UI preferences
    show_tooltips: bool = True
    compact_mode: bool = False
    
    # Custom colors (hex format)
    custom_bg_color: Optional[str] = None
    custom_fg_color: Optional[str] = None
    

def load_gui_config() -> GUICustomization:
    """Load GUI customization from config file."""
    if not Path(GUI_CONFIG_FILE).exists():
        return GUICustomization()
    
    try:
        with open(GUI_CONFIG_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return GUICustomization(**data)
    except Exception:
        # Fallback to defaults if config is corrupted
        return GUICustomization()


def save_gui_config(config: GUICustomization) -> None:
    """Save GUI customization to config file."""
    with open(GUI_CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config.__dict__, f, indent=2)


def apply_theme(config: GUICustomization, root) -> None:
    """
    Apply theme settings to the GUI.
    This is a placeholder - actual implementation will depend on gui.py.
    
    Args:
        config: GUICustomization instance
        root: tkinter root or main window
    """
    # TODO: Integrate with existing GUI (gui.py)
    # Example theme application (stub):
    if config.theme == 'dark':
        pass  # Apply dark theme colors
    elif config.theme == 'light':
        pass  # Apply light theme colors
    else:
        pass  # Default theme
    
    # Font customization
    if config.font_family:
        pass  # Update font family
    # Font size
    # ... etc


def set_theme(theme_name: str) -> None:
    """Convenience function to change theme."""
    config = load_gui_config()
    config.theme = theme_name
    save_gui_config(config)


def set_font(size: int, family: Optional[str] = None) -> None:
    """Convenience function to change font settings."""
    config = load_gui_config()
    config.font_size = size
    if family is not None:
        config.font_family = family
    save_gui_config(config)


def save_window_geometry(width: int, height: int, x: Optional[int] = None, y: Optional[int] = None) -> None:
    """Save window position and size."""
    config = load_gui_config()
    config.window_width = width
    config.window_height = height
    config.window_x = x
    config.window_y = y
    save_gui_config(config)
