import Card
import Interface
import random
import socket
import threading


HOST = '127.0.0.1'
ESP_PORT = 5501
APP_PORT = 5502

def start_socket(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, APP_PORT))
    s.listen(number_of_players)
    return s

def bootstrap(number_of_players):
    esp_interface = Interface.EspInterface('C:\\Users\\idoas\\Documents\\Projects\\E-card\\card_data\\JSON')
    app_to_esp = dict()
    connection_to_client = dict()
    rand_card_to_esp = dict()
    esp_socket = start_socket(ESP_PORT)
    app_socket = start_socket(APP_PORT)
    inputs = [esp_socket, app_socket]
    outputs = []

    while inputs:
        readable, writable, exceptional = select.select(
            inputs, outputs, inputs)
        for s in readable:
            if s is esp_socket or s is app_socket:
                connection, client_address = s.accept()
                connection_to_client[connection] = client_address[0]
                connection.setblocking(0)
                inputs.append(connection)
            else:
                data = s.recv(1024)
                if data == 'E-Card!':
                    random_card = Card.Card(random.choice(Card.VALUES),
                                            random.choice(Card.SHAPES[:-1]))
                    while random_card in rand_card_to_esp.keys():
                        random_card = Card.Card(random.choice(Card.VALUES),
                                                random.choice(Card.SHAPES[:-1]))
                    thread = threading.Thread(target=Interface.EspInterface.send_card, args="(esp_interface, connection_to_client[s], random_card,)")
                    thread.start()
                    rand_card_to_esp[random_card.get_card_name()] = connection_to_client[s]
                    inputs.remove(s)
                elif data in rand_card_to_esp.keys():
                    app_to_esp[connection_to_client[s]] = rand_card_to_esp[data]
                    s.send("Ok")
                    inputs.remove(s)
                    s.close()
                    rand_card_to_esp[data].close()
                    if len(app_to_esp) == number_of_players:
                        break
                else:
                    s.send("Bad")
        if len(app_to_esp) == number_of_players:
            break
    return app_to_esp
