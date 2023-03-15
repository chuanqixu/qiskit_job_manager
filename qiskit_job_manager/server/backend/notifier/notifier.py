from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

from backend.configure import settings



class Notifier:
    def __init__(self, from_addr = None, password = None, smtp_host = None, smtp_port = None):
        self.from_addr = settings.NOTIFIER_FROM_ADDR
        self.password = settings.NOTIFIER_PASSWORD
        self.smtp_host = settings.NOTIFIER_SMTP_HOST
        self.smtp_port = settings.NOTIFIER_SMTP_PORT
        if from_addr:
            self.from_addr = from_addr
        if password:
            self.password = password
        if smtp_host:
            self.smtp_host = smtp_host
        if smtp_port:
            self.smtp_port = smtp_port

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))
    
    def send_email(self, to_addr, subject = None, msg_str = None):
        subject = '(Send by qiskit_job_manager) ' + subject
        if not msg_str:
            msg_str = "Automatically send by qiskit_job_manager"
        msg = MIMEText(msg_str, 'plain', 'utf-8') # TODO: add job result
        msg['From'] = self._format_addr(f'qiskit_job_manager <{self.from_addr}>')
        msg['To'] = self._format_addr(f'<{to_addr}>')
        msg['Subject'] = Header(subject, 'utf-8').encode()

        try:
            server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
            server.login(self.from_addr, self.password)
            server.sendmail(self.from_addr, [to_addr], msg.as_string())
            server.quit()
            return True
        except:
            raise Exception("WARNING: Email sending fails!")

if __name__ == "__main__":
    pass
    # notifier = Notifier()
    # notifier.send_email()
