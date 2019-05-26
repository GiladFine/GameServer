import json
import requests

class Interface(object):

	def __init__(slef, ip, format):
		self.ip = ip;
		self.format = format
	def send_card(ip, card):
		  card_name = card.get_card_name()
		  self.send_picture(ip, card_name + self.format)
		  
class UserInterface(Interface):

    def __init__(self,ip_android, ip_esp):
        Interface.__init__(ip, '.jpg')
		
	def send_picture(ip, file):	
		
class EspInterface(Interface):

    def __init__(self):
        Interface.__init__(ip, '.json')
	
	def send_picture(esp_url, json_file):
	commands_info = json.load(open(json_file))
	if esp_url[:7] != 'http://':
		esp_url = 'http://' + esp_url
	for command_info in commands_info:
		res = requests.post(url=esp_url+command_info['command'], data=command_info['data'])
		print command_info['command'], res
		sleep(0.8)
	print "sent picture. please wait for screen to change"
		
