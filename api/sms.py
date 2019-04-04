import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient


class SMSRobot:
    def __init__(self):
        self.compte_id = "ACefa3332426e584f6e3aeb468af5a5fcd"
        self.kento = "4461364fbc482e7a1f312875156d9003"
        self.mon_numero = "+33644642246"
        proxy_client = TwilioHttpClient()
        proxy_client.session.proxies = {'https': os.environ['https_proxy']}
        self.mon_client = Client(self.compte_id, self.kento, http_client=proxy_client)
    def send_message(self, destinataire, message):
        message = self.mon_client.messages.create(from_=self.mon_numero, body=message, to=destinataire)
        return message