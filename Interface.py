import json
import requests


class Interface(object):
    def __init__(self, format):
        self.format = format

    def send_card(self, ip, card):
          card_name = card.get_card_name()
          print "\n\n\n******", card_name, "*********\n\n\n"
          self._send_picture(ip, card_name + self.format)
          print "\n\n\n******", "END", "*********\n\n\n"

    def _send_picture(self, target_ip, json_file):
       raise NotImplementedError()

class UserInterface(Interface):
    def __init__(self,ip_android, ip_esp):
        super(UserInterface, self).__init__(ip, '.jpg')

    def _send_picture(self, ip, file):
        pass

class EspInterface(Interface):

    def __init__(self, folder):
        super(EspInterface, self).__init__('.json')
        self.folder = folder

    def _send_picture(self, esp_url, json_file):
        commands_info = json.load(open(self.folder + json_file))
        if esp_url[:7] != 'http://':
            esp_url = 'http://' + esp_url
        for command_info in commands_info:
            res = requests.post(url=esp_url+command_info['command'], data=command_info['data'])
