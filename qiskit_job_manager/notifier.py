from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

from qcutils import settings

class Notifier:
    def __init__(self):
        self.from_addr = settings.notifier_from_addr
        self.password = settings.notifier_password
        self.to_addr = settings.notifier_to_addr
        self.smtp_host = settings.notifier_smtp_host
        self.smtp_port = settings.notifier_smtp_port

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))
    
    def send_email(self, msg_str = None, job_status = None, job_id = None):
        if not msg_str:
            msg_str = "Automatically send by qcutils"
        msg = MIMEText(msg_str, 'plain', 'utf-8') # TODO: add job result
        msg['From'] = self._format_addr(f'qcutils <{self.from_addr}>')
        msg['To'] = self._format_addr(f'<{self.to_addr}>')
        msg['Subject'] = Header(f'(Send by qcutils) IBM Quantum Job Status: {job_status} -- Job ID {job_id}', 'utf-8').encode()

        import smtplib
        server = smtplib.SMTP(self.smtp_host, self.smtp_port)
        server.login(self.from_addr, self.password)
        server.sendmail(self.from_addr, [self.to_addr], msg.as_string())
        server.quit()
