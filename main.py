from PresidentGame import *
from game_bootstrap import bootstrap

def main():
    app_to_esp_ips_map = bootstrap(4)
    players = [
                Player("Gilad",
                       [],
                       app_to_esp_ips_map.keys()[0],
                       app_to_esp_ips_map[app_to_esp_ips_map.keys()[0]]),
                Player("Asher", [],
                        app_to_esp_ips_map.keys()[1],
                        app_to_esp_ips_map[app_to_esp_ips_map.keys()[1]]),
                Player("Meged", [],
                        app_to_esp_ips_map.keys()[2],
                        app_to_esp_ips_map[app_to_esp_ips_map.keys()[2]]),
                Player("Ofir", [],
                        app_to_esp_ips_map.keys()[3],  
                        app_to_esp_ips_map[app_to_esp_ips_map.keys()[3]])
                ]

    president = PresidentGame(players)

    print("STUFF")



if __name__ == "__main__":
    main()
