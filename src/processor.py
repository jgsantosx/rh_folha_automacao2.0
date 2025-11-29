import pandas as pd

class Processor:
    """
    Processa a folha de pagamento com base no DataFrame carregado pelo Loader.
    Calcula salário base, extras, descontos e salário final.
    """

    def __init__(self, config):
        self.config = config

    # ----------------------------------------------------------
    # Função principal
    # ----------------------------------------------------------
    def process(self, df):
        df = df.copy()

        # Define o valor hora (da planilha ou do config)
        df["Valor_HF"] = df.apply(
            lambda row: row["Valor_Hora"] if self.config.usar_valor_hora_da_planilha 
            else self.config.valor_hora_padrao,
            axis=1
        )

        # ------------------------------------------------------
        # Cálculo do salário base
        # ------------------------------------------------------
        df["Salario_Base"] = df["Horas_Trab"] * df["Valor_HF"]

        # ------------------------------------------------------
        # Cálculo de hora extra
        # ------------------------------------------------------
        df["Valor_HExtra"] = df["Valor_HF"] * (1 + self.config.percentual_hora_extra)
        df["Total_HExtra"] = df["Horas_Extras"] * df["Valor_HExtra"]

        # ------------------------------------------------------
        # Cálculo de descontos por falta
        # ------------------------------------------------------
        # Cada falta consome 8 horas de trabalho (padrão RH)
        df["Desconto_Falt"] = (
            df["Faltas"] * 8 * df["Valor_HF"] * self.config.desconto_falta_por_dia
        )

        # ------------------------------------------------------
        # Salário final do colaborador
        # ------------------------------------------------------
        df["Salario_Final"] = (
            df["Salario_Base"] +
            df["Total_HExtra"] -
            df["Desconto_Falt"]
        )

        # Arredondamento para evitar problemas com casas decimais
        df = df.round(2)

        # Gera um resumo geral para exportação
        resumo = self._gerar_resumo(df)

        return df, resumo

    # ----------------------------------------------------------
    # Gera um resumo geral do mês
    # ----------------------------------------------------------
    def _gerar_resumo(self, df):
        resumo = {
            "total_colaboradores": len(df),
            "total_salario_base": float(df["Salario_Base"].sum()),
            "Total_HExtra": float(df["Total_HExtra"].sum()),
            "total_descontos": float(df["Desconto_Falt"].sum()),
            "total_salario_pago": float(df["Salario_Final"].sum())
        }

        return resumo
