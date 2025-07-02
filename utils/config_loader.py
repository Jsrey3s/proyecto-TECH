import yaml
import re

class Config:
    def __init__(self, path="config.yaml", encoding="utf-8"):
        with open(path, "r", encoding=encoding) as file:
            self._config = yaml.safe_load(file)
        self._expand_variables()

    def _expand_variables(self):
        """
        Reemplaza referencias como ${rutas.base}/archivo.csv con el valor correspondiente.
        """
        pattern = re.compile(r"\$\{([^\}]+)\}")

        def resolve(value):
            if isinstance(value, str):
                matches = pattern.findall(value)
                for match in matches:
                    keys = match.split(".")
                    ref = self._config
                    for key in keys:
                        ref = ref.get(key, "")
                    value = value.replace(f"${{{match}}}", str(ref))
            return value

        def recursive_expand(d):
            for key, val in d.items():
                if isinstance(val, dict):
                    recursive_expand(val)
                else:
                    d[key] = resolve(val)

        recursive_expand(self._config)

    def get_ruta(self, nombre):
        return self._config["rutas"][nombre]

    def get_parametro(self, nombre):
        return self._config["parametros"][nombre]
