import os
import pandas as pd
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


class Exporter:
    """
    Responsável por exportar os resultados da folha:
    - Excel final
    - PDF final com resumo
    """

    def __init__(self, config):
        self.config = config

    # ----------------------------------------------------------
    # Gera pasta de saída no formato data/output/AAAA_MM/
    # ----------------------------------------------------------
    def _get_output_dir(self):
        output_base = self.config.dirs["output"]

        # mês atual no padrão AAAA_MM
        folder = datetime.now().strftime("%Y_%m")
        full_path = os.path.join(output_base, folder)

        os.makedirs(full_path, exist_ok=True)
        return full_path

    # ----------------------------------------------------------
    # Exporta o Excel final
    # ----------------------------------------------------------
    def export_excel(self, df, path):
        df.to_excel(path, index=False)
        print(f"📁 Excel gerado em: {path}")

    # ----------------------------------------------------------
    # Exporta o PDF final
    # ----------------------------------------------------------
    def export_pdf(self, resumo, df, path):
        styles = getSampleStyleSheet()
        doc = SimpleDocTemplate(path, pagesize=A4)
        story = []

        # Título
        story.append(Paragraph("<b>Relatório de Folha de Pagamento</b>", styles["Title"]))
        story.append(Spacer(1, 20))

        # Resumo
        story.append(Paragraph("<b>Resumo Geral</b>", styles["Heading2"]))
        story.append(Spacer(1, 10))

        texto_resumo = (
            f"Total de colaboradores: {resumo['total_colaboradores']}<br/>"
            f"Total salário base: R$ {resumo['total_salario_base']:.2f}<br/>"
            f"Total horas extras: R$ {resumo['Total_HExtra']:.2f}<br/>"
            f"Total descontos: R$ {resumo['total_descontos']:.2f}<br/>"
            f"Total salário pago: R$ {resumo['total_salario_pago']:.2f}"
        )

        story.append(Paragraph(texto_resumo, styles["Normal"]))
        story.append(Spacer(1, 20))

        # Título da Tabela
        story.append(Paragraph("<b>Tabela Consolidada</b>", styles["Heading2"]))
        story.append(Spacer(1, 10))

        # Monta dados da tabela
        table_data = [df.columns.tolist()] + df.astype(str).values.tolist()

        # === Ajuste automático de largura ===
        page_width = A4[0] - 40  # margem
        num_cols = len(df.columns)
        col_width = page_width / num_cols

        # Cria tabela ajustada
        table = Table(
            table_data,
            colWidths=[col_width] * num_cols,
            repeatRows=1,
            splitByRow=True
        )

        # Estilos
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 5),
        ]))

        story.append(table)
        story.append(Spacer(1, 20))

        # Rodapé
        story.append(Paragraph("Gerado automaticamente pelo sistema de RH.", styles["Normal"]))

        # Gera PDF
        doc.build(story)
        print(f"📄 PDF gerado em: {path}")

    # ----------------------------------------------------------
    # Função principal: gera EXCEL + PDF
    # ----------------------------------------------------------
    def export_all(self, df, resumo):
        output_dir = self._get_output_dir()

        excel_path = os.path.join(output_dir, "relatorio_final.xlsx")
        pdf_path = os.path.join(output_dir, "relatorio_final.pdf")

        self.export_excel(df, excel_path)
        self.export_pdf(resumo, df, pdf_path)

        return excel_path, pdf_path
