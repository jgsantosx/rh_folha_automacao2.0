import os
import pandas as pd

class Loader:
    """
    Responsável por carregar e validar planilhas de ponto do RH.
    """

    REQUIRED_COLUMNS = [
        "Nome", "CPF", "Cargo", "Departamento", "Data_Adm",
        "Horas_Trab", "Horas_Extras", "Faltas",
        "Atestados", "Valor_Hora"
    ]

    def __init__(self, config):
        self.config = config

    # ----------------------------------------------------------
    # Localiza o arquivo mais recente em data/input/
    # ----------------------------------------------------------
    def _find_latest_file(self):
        input_dir = self.config.dirs["input"]

        files = [
            f for f in os.listdir(input_dir)
            if f.lower().endswith((".xlsx", ".xls"))
        ]

        if not files:
            raise FileNotFoundError(
                f"Nenhum arquivo Excel encontrado em {input_dir}"
            )

        # Seleciona o mais recente
        files = sorted(
            files,
            key=lambda f: os.path.getmtime(os.path.join(input_dir, f)),
            reverse=True
        )

        return os.path.join(input_dir, files[0])

    # ----------------------------------------------------------
    # Carrega planilha
    # ----------------------------------------------------------
    def load(self):
        file_path = self._find_latest_file()
        print(f"📄 Carregando planilha: {file_path}")

        # Lê o Excel
        df = pd.read_excel(file_path)

        # Normaliza nomes das colunas
        df.columns = [col.strip() for col in df.columns]

        self._validate_columns(df)
        df = self._convert_types(df)

        return df, file_path

    # ----------------------------------------------------------
    # Verifica se todas as colunas obrigatórias existem
    # ----------------------------------------------------------
    def _validate_columns(self, df):
        for col in self.REQUIRED_COLUMNS:
            if col not in df.columns:
                raise ValueError(
                    f"Coluna obrigatória ausente na planilha: '{col}'. "
                    f"Colunas encontradas: {list(df.columns)}"
                )

    # ----------------------------------------------------------
    # Converte e padroniza tipos dos campos
    # ----------------------------------------------------------
    def _convert_types(self, df):
        numeric_cols = [
            "Horas_Trab", "Horas_Extras",
            "Faltas", "Atestados", "Valor_Hora"
        ]

        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # Normaliza datas
        df["Data_Adm"] = pd.to_datetime(
            df["Data_Adm"], errors="coerce"
        )

        # CPF como string
        df["CPF"] = df["CPF"].astype(str)

        # Observações como texto
        
        #df["Observacoes"] = df["Observacoes"].astype(str)

        return df
