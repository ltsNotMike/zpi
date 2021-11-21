import smtplib
from typing import List, Tuple

from services.loggers import StdoutLogger
from services.notifications import ISmtpConnection, ISmtpConnectionFactory, EmailBroadcastService


DEBUGGING_SERVER_CMD = 'python -m smtpd -n -c DebuggingServer localhost:1000'


class DebuggingSmtpConnection(ISmtpConnection):

    def __init__(self, host: str, port: int):
        server = smtplib.SMTP(host, port)
        self._server = server

    def __enter__(self) -> ISmtpConnection:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._server.close()

    def send_email(self, sender: str, recipients: List[str], message: str):
        self._server.sendmail(sender, recipients, message)


class DebuggingSmtpConnectionFactory(ISmtpConnectionFactory):

    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port

    def create(self, credentials: Tuple[str, str]) -> ISmtpConnection:
        return DebuggingSmtpConnection(self._host, self._port)


if __name__ == '__main__':
    service = EmailBroadcastService(
        credentials=('', ''),
        recipients=[''],
        templates={EmailBroadcastService.ERROR_TEMPLATE_NAME: 'template.str'},
        connection_factory=DebuggingSmtpConnectionFactory(host='localhost', port=1000),
        logger=StdoutLogger())
    service.error('Info', body='This is a message body.')
