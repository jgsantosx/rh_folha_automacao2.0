import smtplib
import os
from email.message import EmailMessage
from email.utils import formatdate
from email.mime.base import MIMEBase
from email import encoders


class EmailSender:
    """
    Responsável por enviar e-mails com anexos (Excel e PDF).
    Utiliza as configurações definidas em config.json.
    """

    def __init__(self, config):
        self.config = config
        self.email_cfg = config.email

    # ----------------------------------------------------------
    # Prepara e envia o e-mail
    # ----------------------------------------------------------
    def send(self, subject, body, attachments=None):
        if not self.email_cfg.get("habilitar_envio", False):
            print("⚠️ Envio de e-mails desativado no config.json")
            return False

        server = self.email_cfg.get("servidor_smtp")
        port = self.email_cfg.get("porta", 587)
        user = self.email_cfg.get("usuario")
        password = self.email_cfg.get("senha")
        destinatarios = self.email_cfg.get("destinatarios", [])

        if not all([server, user, password, destinatarios]):
            raise ValueError(
                "Configurações de e-mail incompletas em config.json"
            )

        # Cria mensagem
        msg = EmailMessage()
        msg["From"] = user
        msg["To"] = ", ".join(destinatarios)
        msg["Date"] = formatdate(localtime=True)
        msg["Subject"] = subject
        msg.set_content(body)

        # ------------------------------------------------------
        # Anexos
        # ------------------------------------------------------
        if attachments:
            for file_path in attachments:
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        file_data = f.read()
                    file_name = os.path.basename(file_path)

                    msg.add_attachment(
                        file_data,
                        maintype="application",
                        subtype="octet-stream",
                        filename=file_name
                    )
                else:
                    print(f"⚠️ Arquivo não encontrado para anexar: {file_path}")

        # ------------------------------------------------------
        # Envio SMTP
        # ------------------------------------------------------
        try:
            with smtplib.SMTP(server, port) as smtp:
                smtp.starttls()
                smtp.login(user, password)
                smtp.send_message(msg)

            print("📧 E-mail enviado com sucesso!")
            return True

        except Exception as e:
            print(f"❌ Erro ao enviar e-mail: {e}")
            return False
