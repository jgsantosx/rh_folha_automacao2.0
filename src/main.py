import os
from datetime import datetime
from src.config import Config
from src.loader import Loader
from src.processor import Processor
from src.exporter import Exporter
from src.email_sender import EmailSender

def main():
    print("\n=== Sistema de Automação de Folha - RH ===\n")

    # ---------------------------------------------------
    # 1) Carregar Configurações
    # ---------------------------------------------------
    cfg = Config()
    print("✔ Configurações carregadas.")

    # ---------------------------------------------------
    # 2) Criar pasta de saída (ex: data/output/AAAA_MM)
    # ---------------------------------------------------
    output_base = cfg.dirs["output"]
    folder_name = datetime.now().strftime("%Y_%m")
    output_dir = os.path.join(output_base, folder_name)
    os.makedirs(output_dir, exist_ok=True)
    print(f"✔ Pasta de saída criada/em uso: {output_dir}")

    # ---------------------------------------------------
    # 3) Encontrar planilha mais recente na pasta input
    # ---------------------------------------------------
    loader = Loader(cfg)
    try:
        df, arquivo_input = loader.load()
        print(f"✔ Planilha carregada: {arquivo_input}")
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return
    except ValueError as e:
        print(f"❌ Erro ao validar planilha: {e}")
        return

    # ---------------------------------------------------
    # 4) Processar folha
    # ---------------------------------------------------
    processor = Processor(cfg)
    df_final, resumo = processor.process(df)
    print("✔ Folha processada.")

    # ---------------------------------------------------
    # 5) Exportar Excel e PDF
    # ---------------------------------------------------
    exporter = Exporter(cfg)
    excel_path, pdf_path = exporter.export_all(df_final, resumo)
    print(f"✔ Relatórios gerados:\n - {excel_path}\n - {pdf_path}")

    # ---------------------------------------------------
    # 6) Enviar por e-mail (opcional)
    # ---------------------------------------------------
    if cfg.email.get("habilitar_envio", False):
        email = EmailSender(cfg)
        email.send(
            subject="Relatório Mensal da Folha",
            body="Segue em anexo o relatório mensal de folha de pagamento.",
            attachments=[excel_path, pdf_path]
        )
    else:
        print("📨 Envio de e-mail desativado.")

    print("\n=== Processo finalizado com sucesso! ===\n")


if __name__ == "__main__":
    main()
