import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from app.core.config import settings
from app.core.logging import get_logger
from typing import Optional
import traceback

logger = get_logger(__name__)


class EmailService:

    @staticmethod
    def _get_password_reset_template() -> str:
        return """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Recuperação de Senha</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                }
                .container {
                    max-width: 600px;
                    margin: 40px auto;
                    background: #ffffff;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }
                .header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 40px 30px;
                    text-align: center;
                }
                .header h1 {
                    margin: 0;
                    font-size: 28px;
                    font-weight: 600;
                }
                .content {
                    padding: 40px 30px;
                }
                .content p {
                    margin: 0 0 20px 0;
                    font-size: 16px;
                    color: #555;
                }
                .button-container {
                    text-align: center;
                    margin: 30px 0;
                }
                .button {
                    display: inline-block;
                    padding: 14px 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white !important;
                    text-decoration: none;
                    border-radius: 6px;
                    font-weight: 600;
                    font-size: 16px;
                    transition: transform 0.2s;
                }
                .button:hover {
                    transform: translateY(-2px);
                }
                .token-box {
                    background: #f8f9fa;
                    border: 2px dashed #dee2e6;
                    border-radius: 6px;
                    padding: 15px;
                    margin: 20px 0;
                    text-align: center;
                    font-family: 'Courier New', monospace;
                    font-size: 14px;
                    color: #495057;
                    word-break: break-all;
                }
                .warning {
                    background: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 15px;
                    margin: 20px 0;
                    border-radius: 4px;
                }
                .warning p {
                    margin: 0;
                    color: #856404;
                    font-size: 14px;
                }
                .footer {
                    background: #f8f9fa;
                    padding: 20px 30px;
                    text-align: center;
                    font-size: 14px;
                    color: #6c757d;
                }
                .footer p {
                    margin: 5px 0;
                }
                .divider {
                    height: 1px;
                    background: #e9ecef;
                    margin: 30px 0;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 Recuperação de Senha</h1>
                </div>
                <div class="content">
                    <p>Olá, <strong>{{ user_name }}</strong>!</p>
                    <p>Recebemos uma solicitação para redefinir a senha da sua conta.</p>
                    <p>Clique no botão abaixo para criar uma nova senha:</p>

                    <div class="button-container">
                        <a href="{{ reset_link }}" class="button">Redefinir Senha</a>
                    </div>

                    <div class="divider"></div>

                    <p style="font-size: 14px; color: #6c757d;">
                        Se o botão não funcionar, copie e cole o link abaixo no seu navegador:
                    </p>
                    <div class="token-box">
                        {{ reset_link }}
                    </div>

                    <div class="warning">
                        <p><strong>⚠️ Importante:</strong></p>
                        <p>Este link expira em <strong>{{ expiration_time }}</strong>.</p>
                        <p>Se você não solicitou esta recuperação, ignore este e-mail.</p>
                    </div>

                    <div class="divider"></div>

                    <p style="font-size: 14px; color: #6c757d;">
                        Por questões de segurança, nunca compartilhe este link com outras pessoas.
                    </p>
                </div>
                <div class="footer">
                    <p><strong>{{ app_name }}</strong></p>
                    <p>Este é um e-mail automático, por favor não responda.</p>
                </div>
            </div>
        </body>
        </html>
        """

    @staticmethod
    def _get_password_changed_template() -> str:
        return """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Senha Alterada</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                }
                .container {
                    max-width: 600px;
                    margin: 40px auto;
                    background: #ffffff;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }
                .header {
                    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                    color: white;
                    padding: 40px 30px;
                    text-align: center;
                }
                .header h1 {
                    margin: 0;
                    font-size: 28px;
                    font-weight: 600;
                }
                .content {
                    padding: 40px 30px;
                }
                .content p {
                    margin: 0 0 20px 0;
                    font-size: 16px;
                    color: #555;
                }
                .success-icon {
                    text-align: center;
                    font-size: 60px;
                    margin: 20px 0;
                }
                .warning {
                    background: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 15px;
                    margin: 20px 0;
                    border-radius: 4px;
                }
                .warning p {
                    margin: 0;
                    color: #856404;
                    font-size: 14px;
                }
                .footer {
                    background: #f8f9fa;
                    padding: 20px 30px;
                    text-align: center;
                    font-size: 14px;
                    color: #6c757d;
                }
                .footer p {
                    margin: 5px 0;
                }
                .divider {
                    height: 1px;
                    background: #e9ecef;
                    margin: 30px 0;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✅ Senha Alterada</h1>
                </div>
                <div class="content">
                    <div class="success-icon">🎉</div>
                    <p>Olá, <strong>{{ user_name }}</strong>!</p>
                    <p>Sua senha foi alterada com sucesso em <strong>{{ change_date }}</strong>.</p>
                    <p>Você já pode fazer login com sua nova senha.</p>

                    <div class="warning">
                        <p><strong>⚠️ Você não fez esta alteração?</strong></p>
                        <p>Se você não solicitou esta mudança, entre em contato conosco imediatamente.</p>
                    </div>

                    <div class="divider"></div>

                    <p style="font-size: 14px; color: #6c757d;">
                        Recomendamos que você use uma senha forte e única para proteger sua conta.
                    </p>
                </div>
                <div class="footer">
                    <p><strong>{{ app_name }}</strong></p>
                    <p>Este é um e-mail automático, por favor não responda.</p>
                </div>
            </div>
        </body>
        </html>
        """

    @staticmethod
    async def send_email(
            to_email: str,
            subject: str,
            html_content: str,
            text_content: Optional[str] = None
    ) -> bool:
        try:
            message = MIMEMultipart("alternative")
            message["From"] = f"{settings.smtp_from_name} <{settings.smtp_from_email}>"
            message["To"] = to_email
            message["Subject"] = subject

            if text_content:
                part1 = MIMEText(text_content, "plain")
                message.attach(part1)

            part2 = MIMEText(html_content, "html")
            message.attach(part2)

            if settings.smtp_ssl:
                smtp = aiosmtplib.SMTP(
                    hostname=settings.smtp_host,
                    port=settings.smtp_port,
                    use_tls=True
                )
            else:
                smtp = aiosmtplib.SMTP(
                    hostname=settings.smtp_host,
                    port=settings.smtp_port,
                    start_tls=settings.smtp_tls
                )

            await smtp.connect()

            if settings.smtp_username and settings.smtp_password:
                await smtp.login(settings.smtp_username, settings.smtp_password)

            await smtp.send_message(message)
            await smtp.quit()

            logger.info("email_sent", to_email=to_email, subject=subject)
            return True

        except Exception as e:
            logger.error("email_send_error", to_email=to_email, error=str(e), traceback=traceback.format_exc())
            return False

    @staticmethod
    async def send_password_reset_email(
            to_email: str,
            user_name: str,
            reset_token: str,
            expiration_hours: int = 1
    ) -> bool:
        try:
            reset_link = f"{settings.frontend_url}/reset-password?token={reset_token}"

            template = Template(EmailService._get_password_reset_template())
            html_content = template.render(
                user_name=user_name,
                reset_link=reset_link,
                expiration_time=f"{expiration_hours} hora(s)",
                app_name=settings.smtp_from_name
            )

            text_content = f"""
            Olá, {user_name}!

            Recebemos uma solicitação para redefinir a senha da sua conta.

            Acesse o link abaixo para criar uma nova senha:
            {reset_link}

            Este link expira em {expiration_hours} hora(s).

            Se você não solicitou esta recuperação, ignore este e-mail.

            {settings.smtp_from_name}
            """

            return await EmailService.send_email(
                to_email=to_email,
                subject="Recuperação de Senha",
                html_content=html_content,
                text_content=text_content
            )

        except Exception as e:
            logger.error("password_reset_email_error", to_email=to_email, error=str(e))
            return False

    @staticmethod
    async def send_password_changed_email(
            to_email: str,
            user_name: str,
            change_date: str
    ) -> bool:
        try:
            template = Template(EmailService._get_password_changed_template())
            html_content = template.render(
                user_name=user_name,
                change_date=change_date,
                app_name=settings.smtp_from_name
            )

            text_content = f"""
            Olá, {user_name}!

            Sua senha foi alterada com sucesso em {change_date}.

            Se você não fez esta alteração, entre em contato conosco imediatamente.

            {settings.smtp_from_name}
            """

            return await EmailService.send_email(
                to_email=to_email,
                subject="Senha Alterada com Sucesso",
                html_content=html_content,
                text_content=text_content
            )

        except Exception as e:
            logger.error("password_changed_email_error", to_email=to_email, error=str(e))
            return False

