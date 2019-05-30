from WarGame import *
from game_bootstrap import bootstrap

def main():
    #app_to_esp_ips_map = bootstrap(4)
    players = [
                Player("Gilad",
                       [],
                       "192.168.43.1",#"172.16.2.86",
                       "192.168.43.166"#"172.16.2.15",
                       ),
                Player("Asher",
                        [],
                        "192.168.43.122",#"172.16.2.109",
                        "192.168.43.172"#"172.16.2.90",
                        )
                ]

    president = WarGame(players)

    print("STUFF")



if __name__ == "__main__":
    main()
