from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

from backend.configure import settings

class Notifier:
    def __init__(self):
        self.from_addr = settings.NOTIFIER_FROM_ADDR
        self.password = settings.NOTIFIER_PASSWORD
        self.smtp_host = settings.NOTIFIER_SMTP_HOST
        self.smtp_port = settings.NOTIFIER_SMTP_PORT

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))
    
    def send_email(self, to_addr, msg_str = None, job_status = None, job_id = None):
        if not msg_str:
            msg_str = "Automatically send by qiskit_job_manager"
        msg = MIMEText(msg_str, 'plain', 'utf-8') # TODO: add job result
        msg['From'] = self._format_addr(f'qiskit_job_manager <{self.from_addr}>')
        msg['To'] = self._format_addr(f'<{to_addr}>')
        msg['Subject'] = Header(f'(Send by qiskit_job_manager) IBM Quantum Job Status: {job_status} -- Job ID {job_id}', 'utf-8').encode()

        import smtplib
        server = smtplib.SMTP(self.smtp_host, self.smtp_port)
        server.login(self.from_addr, self.password)
        server.sendmail(self.from_addr, [to_addr], msg.as_string())
        server.quit()
