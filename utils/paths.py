import yaml
from pathlib import Path

def get_config():
    """Obtiene la configuración completa"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def resolve_paths(config):
    """Convierte rutas relativas a rutas absolutas desde la raíz del proyecto"""
    project_root = Path(__file__).parent.parent
    
    def resolve_dict(d, resolved=None):
        if resolved is None:
            resolved = {}
        
        for key, value in d.items():
            if isinstance(value, dict):
                resolved[key] = resolve_dict(value)
            elif isinstance(value, str):
                if value == ".":
                    resolved[key] = str(project_root)
                else:
                    resolved[key] = str(project_root / value)
            else:
                resolved[key] = value
        return resolved
    
    return resolve_dict(config['rutas'])

# Crear variables globales para acceso directo
_config = get_config()
PATHS = resolve_paths(_config)
PARAMS = _config['parametros']

# Funciones de conveniencia para acceso más fácil
def get_data_path(subfolder, filename=None):
    """Obtiene ruta de la carpeta Data o archivo específico"""
    base_path = PATHS['data'][subfolder]
    if filename:
        return str(Path(base_path) / filename)
    return base_path

def get_file_path(category, filename):
    """Obtiene ruta de archivo específico por categoría"""
    return PATHS['archivos'][category][filename]