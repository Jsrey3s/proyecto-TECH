import yaml
from pathlib import Path

def get_config():
    """Obtiene la configuración completa"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

# Crear variables globales para acceso directo
_config = get_config()
PATHS = _config['rutas']
PARAMS = _config['parametros']