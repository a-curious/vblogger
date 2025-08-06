"""
Configuration Loader
Utility to load video project configurations.
"""

import importlib
import os
from typing import Dict, Any


def load_config(config_name: str) -> Dict[str, Any]:
    """
    Load a video configuration by name.
    
    Args:
        config_name: Name of the configuration file (without .py extension)
                     Examples: 'table_rocks_config', 'wuhan_trip_config'
    
    Returns:
        Dictionary containing all configuration parameters
    """
    try:
        # Import the configuration module
        config_module = importlib.import_module(f"config.{config_name}")
        
        # Get all uppercase variables from the module
        config = {}
        for attr_name in dir(config_module):
            if attr_name.isupper() and not attr_name.startswith('_'):
                config[attr_name] = getattr(config_module, attr_name)
        
        return config
    
    except ImportError as e:
        raise ValueError(f"Configuration '{config_name}' not found: {e}")


def list_available_configs() -> list:
    """
    List all available configuration files in the config directory.
    
    Returns:
        List of configuration names (without .py extension)
    """
    config_dir = os.path.dirname(os.path.abspath(__file__))
    configs = []
    
    for file in os.listdir(config_dir):
        if file.endswith('_config.py') and file != 'video_config_template.py':
            configs.append(file[:-3])  # Remove .py extension
    
    sorted_configs = sorted(configs)
    return sorted_configs


def create_config_from_template(template_name: str, new_config_name: str, **kwargs) -> str:
    """
    Create a new configuration file from template.
    
    Args:
        template_name: Name of the template file
        new_config_name: Name for the new configuration
        **kwargs: Parameters to override in the new config
    
    Returns:
        Path to the created configuration file
    """
    config_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(config_dir, f"{template_name}.py")
    new_config_path = os.path.join(config_dir, f"{new_config_name}.py")
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template '{template_name}' not found")
    
    # Read template
    with open(template_path, 'r') as f:
        content = f.read()
    
    # Replace parameters
    for key, value in kwargs.items():
        if isinstance(value, str):
            content = content.replace(f"{key.upper()} = ", f"{key.upper()} = \"{value}\"")
        else:
            content = content.replace(f"{key.upper()} = ", f"{key.upper()} = {value}")
    
    # Write new config
    with open(new_config_path, 'w') as f:
        f.write(content)
    
    return new_config_path


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate a configuration dictionary.
    
    Args:
        config: Configuration dictionary to validate
    
    Returns:
        True if valid, raises ValueError if invalid
    """
    required_fields = [
        'INPUT_FOLDER', 'OUTPUT_FILE', 'MUSIC_FILE',
        'TITLE', 'SUBTITLE', 'FILL_COLOR'
    ]
    
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required configuration field: {field}")
    
    # Check if input folder exists
    if not os.path.exists(config['INPUT_FOLDER']):
        raise ValueError(f"Input folder does not exist: {config['INPUT_FOLDER']}")
    
    # Check if music file exists
    if not os.path.exists(config['MUSIC_FILE']):
        raise ValueError(f"Music file does not exist: {config['MUSIC_FILE']}")
    
    return True 