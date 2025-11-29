import json
import os

class Config:
    def __init__(self, config_path="config.json"):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Arquivo de configuração não encontrado: {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            self._config = json.load(f)

        self._validate()

    # ----------------------------------------------------------
    # Métodos de acesso
    # ----------------------------------------------------------

    @property
    def valor_hora_padrao(self):
        return float(self._config.get("valor_hora_padrao", 0))

    @property
    def percentual_hora_extra(self):
        return float(self._config.get("percentual_hora_extra", 0))

    @property
    def desconto_falta_por_dia(self):
        return float(self._config.get("desconto_falta_por_dia", 0))

    @property
    def usar_valor_hora_da_planilha(self):
        return bool(self._config.get("usar_valor_hora_da_planilha", True))

    @property
    def formato_data(self):
        return self._config.get("formato_data", "YYYY-MM-DD")

    @property
    def dirs(self):
        return self._config.get("diretorios", {})

    @property
    def email(self):
        return self._config.get("email", {})

    @property
    def log(self):
        return self._config.get("log", {})

    # ----------------------------------------------------------
    # Validação básica
    # ----------------------------------------------------------

    def _validate(self):
        required_keys = [
            "valor_hora_padrao",
            "percentual_hora_extra",
            "diretorios"
        ]

        for key in required_keys:
            if key not in self._config:
                raise ValueError(f"Configuração obrigatória ausente em config.json: '{key}'")

