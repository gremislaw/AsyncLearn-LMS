import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

class EmailService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.smtp_tls = settings.SMTP_TLS

    async def send_email(self, to: str, subject: str, body: str, html: bool = False):
        message = MIMEMultipart("alternative")
        message["From"] = settings.EMAILS_FROM_EMAIL
        message["To"] = to
        message["Subject"] = subject

        if html:
            message.attach(MIMEText(body, "html"))
        else:
            message.attach(MIMEText(body, "plain"))

        try:
            async with aiosmtplib.SMTP(
                hostname=self.smtp_host,
                port=self.smtp_port,
                use_tls=self.smtp_tls
            ) as smtp:
                if self.smtp_user and self.smtp_password:
                    await smtp.login(self.smtp_user, self.smtp_password)

                await smtp.send_message(message)
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

    async def send_welcome_email(self, to: str, username: str):
        subject = "Добро пожаловать в AsyncLearn LMS!"
        body = f"""
        Уважаемый(ая) {username},

        Спасибо за регистрацию в нашей платформе онлайн-обучения AsyncLearn LMS!

        Мы рады приветствовать вас в нашем сообществе и надеемся, что вы найдете много интересных курсов для изучения.

        Если у вас возникнут вопросы, не стесняйтесь обращаться в нашу поддержку.

        С уважением,
        Команда AsyncLearn LMS
        """
        return await self.send_email(to, subject, body)

    async def send_purchase_confirmation(self, to: str, course_name: str, amount: int):
        subject = "Подтверждение оплаты курса"
        body = f"""
        Уважаемый(ая) пользователь,

        Мы подтверждаем успешную оплату курса "{course_name}" на сумму {amount} рублей.

        Теперь у вас есть доступ ко всем материалам курса в течение 30 дней.

        Желаем успешного обучения!

        С уважением,
        Команда AsyncLearn LMS
        """
        return await self.send_email(to, subject, body)

    async def send_access_expiry_notification(self, to: str, course_name: str, expiry_date: str):
        subject = "Внимание: скоро истечет доступ к курсу"
        body = f"""
        Уважаемый(ая) пользователь,

        Напоминаем, что ваш доступ к курсу "{course_name}" истекает {expiry_date}.

        Если вы хотите продолжить обучение, пожалуйста, продлите доступ в личном кабинете.

        С уважением,
        Команда AsyncLearn LMS
        """
        return await self.send_email(to, subject, body)
