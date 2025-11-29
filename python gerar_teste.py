import pandas as pd
import os

# Cria pasta input se não existir
input_dir = "data/input"
os.makedirs(input_dir, exist_ok=True)

# Dados de teste
data = {
    "Nome": ["Alice", "Bruno", "Carla"],
    "CPF": ["12345678900", "98765432100", "45678912300"],
    "Cargo": ["Analista", "Gerente", "Assistente"],
    "Depart": ["RH", "Financeiro", "Marketing"],
    "Data_Adm": ["2020-01-15", "2018-05-22", "2022-09-01"],
    "Horas_Trab": [160, 180, 150],
    "Horas_Ext": [10, 5, 8],
    "Faltas": [2, 0, 1],
    "Atestados": [0, 1, 0],
    "Valor_Hora": [25, 40, 20],
    "Observacoes": ["", "", ""]
}

# Cria DataFrame e salva como Excel
df = pd.DataFrame(data)
file_path = os.path.join(input_dir, "planilha_exemplo.xlsx")
df.to_excel(file_path, index=False)

print(f"Arquivo gerado em: {file_path}")
