import logging
import smtplib
from datetime import datetime

from config.settings import SMTP_HOST, SMTP_PASSWORD, SMTP_PORT, SMTP_USER

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self):
        self.notifications = []

    def send_email(self, to, subject, body):
        if not SMTP_USER or not SMTP_PASSWORD:
            logger.info("Email skipped (SMTP not configured): %s -> %s", subject, to)
            return True
        try:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(SMTP_USER, to, message)
            server.quit()
            return True
        except Exception as e:
            logger.error("Erro ao enviar email: %s", e)
            return False

    def notify_task_assigned(self, user, task):
        subject = f"Nova task atribuída: {task.title}"
        body = (
            f"Olá {user.name},\n\nA task '{task.title}' foi atribuída a você.\n\n"
            f"Prioridade: {task.priority}\nStatus: {task.status}"
        )
        self.send_email(user.email, subject, body)
        self.notifications.append({
            'type': 'task_assigned',
            'user_id': user.id,
            'task_id': task.id,
            'timestamp': datetime.utcnow(),
        })
